import pymel.core as pm
import maya.mel as mel
import autorig.utils.utils as rigUtils


class Hand(object):
	def __init__(self, handJoint, side):

		self.handJoint = handJoint
		self.side = side

		self._build(handJoint, side)

	def createHandControl(self):
		"""
		Create hand control and sets the color based on the name
		:return - string - name of the created control
		"""

		crv = mel.eval('curve -d 3 -p 0 0 0 -p 0.4 0 0.111111 -p 1.2 0 0.333333 -p 1.2 0 -1.333333 -p 0.4 0 -1.111111 '
					   '-p 0 0 -1 -k 0 -k 0 -k 0 -k 1 -k 2 -k 3 -k 3 -k 3 ;')
		pm.setAttr(crv + '.tz', 0.5)
		pm.makeIdentity(a=True, t=True)
		pm.xform(crv, piv=(0.0, 0.0, 0.0))
		pm.scale(0.4, 0.4, 0.4)
		pm.makeIdentity(a=True, s=True)

		crv = pm.rename(crv, self.side + '_hand_ctrl')

		rigUtils.setControlColor(crv)
		#self.setControlColor(crv)

		# mirror the controller for the Right side
		if self.side == 'R':
			pm.scale(crv, (-1, 1, 1))
			pm.makeIdentity(a=True, s=True)

		return crv

	def hideAttributes(self, ctrl, trans, scale, rot, vis, radius):
		"""
		Hide channelbox attributes
		:param ctrl: string - Name of the control
		:param trans: bool
		:param scale: bool
		:param rot: bool
		:param vis: bool
		"""

		if trans:
			for attr in ['.tx', '.ty', '.tz']:
				pm.setAttr(ctrl + attr, lock=True, keyable=False, cb=False)

		if rot:
			for attr in ['.rx', '.ry', '.rz']:
				pm.setAttr(ctrl + attr, lock=True, keyable=False, cb=False)

		if scale:
			for attr in ['.sx', '.sy', '.sz']:
				pm.setAttr(ctrl + attr, lock=True, keyable=False, cb=False)

		if vis:
			pm.setAttr(ctrl + '.v', lock=True, keyable=False, cb=False)

		if radius:
			pm.setAttr(ctrl + '.radi', lock=True, keyable=False, cb=False)


	def addCtrlAttribute(self, ctrl, attr, locked):
		"""
		Adds channel box attribute
		:param ctrl: string - name of the control to add the attribute
		:param attr: string - name of the attribute to add
		:param locked: bool - attribute state
		"""

		if locked:
			pm.addAttr(longName=attr, at='long', dv=False, min=0, max=1)
			pm.setAttr(ctrl + '.' + attr, edit=True, lock=locked, keyable=locked, channelBox=True)

		elif locked == False:
			pm.addAttr(longName=attr, at='long', dv=False, min=0, max=1)
			pm.setAttr(ctrl + '.' + attr, edit=True, keyable=True)

	def placeControl(self, jnt):
		"""
		Place control in the given joint position
		:param jnt: string - name of the joint to place the control
		"""

		pm.delete(pm.pointConstraint(self.handJoint, self.handCtrl))
		pm.makeIdentity(self.handCtrl, a=True, t=True)

	def connectFKIKBlendAttrs(self):
		"""
		Connects FK and IK channelBox attributes to the blend node for the FK/IK swith in the channelBox
		"""

		for armPart in [self.side + '_arm0_jnt_BC.blender',
						self.side + '_arm1_jnt_BC.blender',
						self.side + '_arm2_jnt_BC.blender']:
			pm.connectAttr(self.handCtrl + '.FK_IK', armPart)

	def createHandJoint(self, jnt):
		"""
		Create a new hand joint chain getting the hand world positions
		:param jnt: string - first hand joint (wrist)
		"""

		pm.select(deselect=True)
		handRootJnt = self.handJoint
		handRootJnt = pm.PyNode(handRootJnt)

		handEndJnt = pm.listRelatives(self.handJoint, c=True, ad=True)
		handEndJnt = pm.PyNode(handEndJnt[0])

		self.handRootPos = handRootJnt.getTranslation('world')
		handEndPos = handEndJnt.getTranslation('world')

		pm.joint(name=self.side + '_handRoot_jnt', p=(self.handRootPos[0], self.handRootPos[1], self.handRootPos[2]))
		pm.joint(name=self.side + '_handEnd_jnt', p=(handEndPos[0], handEndPos[1], handEndPos[2]))

	def organize(self):
		"""
		Create groups and parents for the hand
		"""

		handGrp = pm.group(name=self.side + '_hand_grp', em=True)

		handJntPos = pm.PyNode(self.side + '_hand0_jnt')
		handJntPos = handJntPos.getTranslation()

		pm.xform(handGrp, piv=(handJntPos[0], handJntPos[1], handJntPos[2]))
		pm.parent(self.side + '_hand_ctrl', handGrp)

	def setupHandBehavior(self):
		"""
		Main proc for creating the IK / FK arm switch
		"""
		handRootNode =  pm.PyNode(self.side + '_hand0_jnt')
		handRootPos = handRootNode.getTranslation('world')

		# create locators for the blending FK/IK arm and groups.
		# to set hand position into the right place
		orientFKLoc = pm.spaceLocator(name=self.side + '_armFKOrient_loc')
		orientIKLoc = pm.spaceLocator(name=self.side + '_armIKOrient_loc')

		orientFKGrp = pm.group(name=self.side + '_armFKOrient_grp', em=True)
		orientIKGrp = pm.group(name=self.side + '_armIKOrient_grp', em=True)

		locFKShape = pm.listRelatives(orientFKLoc, s=1)[0]
		locIKShape = pm.listRelatives(orientIKLoc, s=1)[0]

		# setup a smaller locator and move it to the wrist joint (handRoot)
		for loc in [locFKShape, locIKShape]:
			for scale in ['.localScaleX', '.localScaleY', '.localScaleZ']:
				pm.setAttr(loc + scale, 0.0005)

			pm.move(loc, (handRootPos[0], handRootPos[1], handRootPos[2]))

		# parent each locator to the corresponding group
		for loc, grp in zip([orientFKLoc, orientIKLoc], [orientFKGrp, orientIKGrp]):
			pm.parent(loc, grp)

		# parent each locator group (IK and FK) to the right place
		pm.parent(orientFKGrp, self.side + '_arm1_jnt')
		pm.parent(orientIKGrp, self.side + '_arm_ik_ctrl')

		self.handOrientConst = pm.orientConstraint(orientIKLoc, orientFKLoc, self.side + '_hand_grp')

		# pointConstraint blend arm joint and handGrp
		pm.pointConstraint(self.side + '_arm2_jnt', self.side + '_hand_grp')

		# connect orientConstraint weights to handCtrl to be able to switch the weights from the FK/IK attribute
		pm.connectAttr(self.side + '_hand_ctrl.FK_IK',
					   self.handOrientConst + '.' + self.side + '_armFKOrient_locW1')
		handReverseNode = pm.createNode('reverse', name=self.side + '_handRev')

		pm.connectAttr(self.side + '_hand_ctrl.FK_IK', handReverseNode + '.input.inputX')
		pm.connectAttr(handReverseNode + '.output.outputX',
					   self.handOrientConst + '.' + self.side + '_armIKOrient_locW0')

		# orient constraint hand module with the bind joints
		#pm.orientConstraint(self.side + '_hand_IK_jnt', self.side + '_hand0_jnt', mo=True)
		pm.parent(self.side + '_arm_limb_ikh',self.side + '_arm_ik_ctrl')

		pm.parent(self.side + '_hand_grp', 'main_ctrl')

		rigUtils.hideAttributes(ctrl=self.side + '_hand_ctrl', trans=True, scale=False, rot=False, vis=True, radius=False)

	def setupVisibility(self):
		for ctrl in ['_arm0_FK_ctrl', '_arm_poleVector_ctrl', '_arm_ik_ctrl']:
			pm.setAttr(self.side + ctrl + '.visibility', lock=False)

		armRevNode = pm.createNode('reverse', n=self.side + '_arm_inv')
		pm.connectAttr(self.side + '_hand_ctrl.FK_IK', self.side + '_arm0_FK_ctrl.visibility')

		pm.connectAttr(self.side + '_hand_ctrl.FK_IK', armRevNode + '.input.inputX')
		pm.connectAttr(armRevNode + '.output.outputX', self.side + '_arm_poleVector_ctrl.visibility')

		pm.connectAttr(self.side + '_hand_ctrl.FK_IK', armRevNode + '.input.inputY')
		pm.connectAttr(armRevNode + '.output.outputY', self.side + '_arm_ik_ctrl.visibility')

	def _build(self, handJoint, side):

		# create new hand joint chan
		#self.createHandJoint(handJoint)

		# create nurbs curve to control the hand
		self.handCtrl = self.createHandControl()

		# place the control for the hand
		self.placeControl(handJoint)

		# hide and create channelBox attributes for the hand controller
		self.hideAttributes(ctrl=self.handCtrl, trans=True, scale=True, rot=False, vis=True, radius=False)
		self.addCtrlAttribute(self.handCtrl, attr='_______', locked=True)
		self.addCtrlAttribute(self.handCtrl, attr='FK_IK', locked=False)

		# create and connect FK/IK blend nodes
		self.connectFKIKBlendAttrs()

		# parent hand joint under the hand controller
		pm.parent(side + '_hand0_jnt', self.handCtrl)

		# create groups and parents to have the hand as a separate module
		self.organize()

		self.setupHandBehavior()
		self.setupVisibility()
