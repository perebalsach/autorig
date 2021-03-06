import pymel.core as pm
import maya.mel as mel
from maya import OpenMaya
import autorig.utils.utils as rigUtils

reload(rigUtils)


class Limb(object):
	def __init__(self, startJoint=None, midJoint=None, endJoint=None, ikFk=True, side=None, limbPart=None):

		self.startJoint = startJoint
		self.midJoint = midJoint
		self.endJoint = endJoint
		self.ikFkSwitch = ikFk
		self.side = side
		self.limbPart = limbPart

		self._build(self.side)

	def duplicateLimbChain(self, jnt=None, FK=None, IK=None):
		"""
		based on the first joint for the limb
		duplicate and renames the joints with the proper name
		and deletes the last joint (hand)

		:param: jnt - string - First joint of the chain to duplicate
		:param: FK - bool
		:param: IK - bool
		"""
		chainJntList = []
		fkChain = pm.duplicate(jnt, rc=True)[0]
		fkChainList = pm.listRelatives(fkChain, c=True, ad=True)
		fkChainList.append(fkChain)

		if IK:
			for jnt in fkChainList:
				newName = jnt.replace('_jnt1', '_IK_jnt')
				chainJntList.append(pm.rename(jnt, newName))

			chainJntList.reverse()
			"""
			# delete the first joint, so the children too
			for jnt in chainJntList[3::]:
				pm.delete(jnt)
				break
			"""

		if FK:
			for jnt in fkChainList:
				newName = jnt.replace('_jnt1', '_FK_ctrl')
				chainJntList.append(pm.rename(jnt, newName))

			chainJntList.reverse()
			"""
			# delete the first joint, so the children too
			for jnt in chainJntList[3::]:
				pm.delete(jnt)
				break
			"""

	def placeCtrl(self, jnt=None, type=None):
		"""
		snaps the control to the given joint with the same orientation
		:return string - ctrl name
		"""

		# create different control based on the type IK/FK
		if type == 'fk':
			ctrlCrv = rigUtils.createRigControl('sphere')
			ctrlCrv = pm.rename(ctrlCrv, self.side + '_' + self.limbPart + '_' + ctrlCrv)
			rigUtils.setControlColor(ctrlCrv)

			pm.delete(pm.orientConstraint(jnt, ctrlCrv))

			pm.scale(0.12, 0.12, 0.12)
			pm.makeIdentity(a=True, s=True)

			pm.parent(ctrlCrv, jnt)

			# resets the transforms for the controller
			for trans in ['.tx', '.ty', '.tz', '.rx', '.ry', '.rz']:
				pm.setAttr(ctrlCrv + trans, 0)

			# unparent the control and parent the shape from the control to the joint, so we are adding a shape node to
			# the joint interact with the animator
			pm.parent(world=True)
			ctrlCrvShape = pm.listRelatives(ctrlCrv)
			pm.select(ctrlCrvShape)
			pm.select(jnt, add=True)
			pm.parent(r=True, s=True)
			pm.delete(ctrlCrv)

		elif type == 'ik':
			ctrlCrv = rigUtils.createRigControl('cross')

			pm.delete(pm.orientConstraint(jnt, ctrlCrv))
			pm.scale(ctrlCrv, (0.08, 0.08, 0.08))

			pm.makeIdentity(s=True, t=True, r=True, a=True)

			ctrlCrv = pm.rename(ctrlCrv, self.side + '_' + self.limbPart + '_ik_ctrl')
			pm.delete(pm.pointConstraint(self.endJoint, ctrlCrv))
			pm.makeIdentity(a=True, t=True)

			if self.limbPart == 'arm':
				pm.rotate(ctrlCrv, (0,0,90))
				pm.makeIdentity(a=True, r=True)

		return ctrlCrv

	def createIkFkBlendConnections(self, jnt):
		"""
		create blendColor node and connects the rotations to the blendColor inputs
		then connects the blendColor outputs to the rotations for the other joint chain
		"""

		bcNode = pm.createNode('blendColors', name=jnt + '_BC')
		jntFK = jnt.replace('_jnt', '_FK_ctrl')
		jntIK = jnt.replace('_jnt', '_IK_jnt')

		# blend connections between bind chain and IK/FK chains
		for rot, color in zip(['.rotateX', '.rotateY', '.rotateZ'], ['.color1R', '.color1G', '.color1B']):
			pm.connectAttr(jntFK + rot, bcNode + color)

		for rot, color in zip(['.rotateX', '.rotateY', '.rotateZ'], ['.color2R', '.color2G', '.color2B']):
			pm.connectAttr(jntIK + rot, bcNode + color)
		# blend output connections
		for output, rot in zip(['.outputR', '.outputG', '.outputB'], ['.rotateX', '.rotateY', '.rotateZ']):
			pm.connectAttr(bcNode + output, jnt + rot)

	def addChannelBoxBlendAttr(self, ctrl):
		"""
		add ik / fk channelBox attributes and locks and hides scales and visibility
		:param ctrl: string - control name
		"""

		pm.select(ctrl)

		# hide scales and visibility from channel box
		for attr in ['.sx', '.sy', '.sz']:
			pm.setAttr(ctrl + attr, lock=True, keyable=False, channelBox=False)
		pm.setAttr(ctrl + '.visibility', lock=True, keyable=False, channelBox=False)

		# add ik / fk blend attribute
		pm.addAttr(at='float', longName='IK_FK_Blend', min=0, max=1, dv=0, k=True)

	def connectAttrsFKCtrlToJoints(self, jnt, ctrl):
		"""
		Connects rotation attributes from the control cruve to the joint
		:param jnt: string - Joint
		:param ctrl: string - Nurbs curve
		"""

		for attr in ['.rx', '.ry', '.rz']:
			pm.connectAttr(ctrl + attr, jnt + attr)

	def getLimbLength (self, startHelper, endHelper):
		limbLength = []
		
		if self.limbPart == 'arm':
			armStartHelper = pm.PyNode(startHelper)
			armEndHelper = pm.PyNode(endHelper)
		
			armStartHelperPos = armStartHelper.getTranslation('world')
			armEndHelperPos = armEndHelper.getTranslation('world')
			
			limbLength = armEndHelperPos[0] - armStartHelperPos[0]
			
		elif self.limbPart == 'leg':
			legStartHelper = pm.PyNode(startHelper)
			legEndHelper = pm.PyNode(endHelper)
			
			legStartHelperPos = legStartHelper.getTranslation('world')
			legEndHelperPos = legEndHelper.getTranslation('world')
			
			limbLength = legEndHelperPos[1] - legStartHelperPos[1]
			
		return limbLength
	
	def placePoleVectorCtrl(self, jntList):
		"""
		place pole vector controller in the middle joint and offsets the position
		:param jntList: string list- list of 3 limb joints
		"""
		armlimbLenght = self.getLimbLength(self.side + '_arm1_rigHelper', self.side + '_arm3_rigHelper')
		leglimbLenght = self.getLimbLength(self.side + '_leg_0_rigHelper', self.side + '_leg_2_rigHelper')
		
		start = pm.xform(jntList[0], q=1, ws=1, t=1)
		mid = pm.xform(jntList[1], q=1, ws=1, t=1)
		end = pm.xform(jntList[2], q=1, ws=1, t=1)

		startV = OpenMaya.MVector(start[0], start[1], start[2])
		midV = OpenMaya.MVector(mid[0], mid[1], mid[2])
		endV = OpenMaya.MVector(end[0], end[1], end[2])

		startEnd = endV - startV
		startMid = midV - startV

		dotP = startMid * startEnd

		proj = float(dotP) / float(startEnd.length())
		startEndN = startEnd.normal()
		projV = startEndN * proj

		arrowV = startMid - projV
		arrowV *= 8.0
		finalV = arrowV + midV

		# create poleVector controller
		self.poleVectCtrl = rigUtils.createRigControl('poleVector')
		self.poleVectCtrl = pm.rename(self.poleVectCtrl, self.side + '_' + self.limbPart + '_' + self.poleVectCtrl)

		pm.select(self.poleVectCtrl)

		pm.xform(ws=1, t=(finalV.x, finalV.y, finalV.z))
		pm.makeIdentity(self.poleVectCtrl, a=True, t=True)

		rigUtils.setControlColor(self.poleVectCtrl)


	def buildIkCtrlSetup(self, side):
		"""
		Builds IK control for the limb. Create a controller and it places the controller to the right place
		and create the pole vector and the constrains plus connections
		:param side: string - 'L' or 'R'
		"""

		ikCtrl = self.placeCtrl(self.endJoint, type='ik')

		if not self.limbPart == 'leg':
			pm.delete(pm.orientConstraint(self.endJoint, ikCtrl, mo=True))

		# create ik handle and pole vector for the IK limb
		ikh = pm.ikHandle(name=side + '_' + self.limbPart + '_limb_ikh', sj=self.startJoint.replace('_jnt', '_IK_jnt'),
						  ee=self.endJoint.replace('_jnt', '_IK_jnt'), sol='ikRPsolver')[0]

		rigUtils.setControlColor(ikCtrl)

		self.placePoleVectorCtrl((self.startJoint, self.midJoint, self.endJoint))
		pm.poleVectorConstraint(self.poleVectCtrl, ikh)

		# End limb control constraint
		# pm.parentConstraint(ikCtrl, ikh)
		if self.limbPart == 'arm':
			pm.parent(self.side + '_arm_limb_ikh', self.side + '_arm_ik_ctrl')
		else:
			pm.parent(self.side + '_leg_limb_ikh', self.side + '_leg_ik_ctrl')

		rigUtils.hideAttributes(ikCtrl, trans=False, scale=True, rot=False, vis=True, radius=False)
		rigUtils.hideAttributes(self.poleVectCtrl, trans=False, scale=True, rot=True, vis=True, radius=False)


	def organizeLimbGrps(self, limbPart):
		"""
		Organize limb groups
		"""
		limbmGrp = pm.group(name=self.side + '_' + self.limbPart + '_grp', em=True)
		pm.parent(self.side + '_' + self.limbPart + '_limb_ikh', self.side + '_' + self.limbPart + '_ik_ctrl')

		# create arm groups
		if limbPart == 'arm':
			pm.parent(self.side + '_' + self.limbPart + '_poleVector_ctrl', limbmGrp)

			pm.parent(self.side + '_' + self.limbPart + '_ik_ctrl', limbmGrp)
			pm.parent(self.side + '_' + self.limbPart + '0_IK_jnt', limbmGrp)
			pm.parent(self.side + '_' + self.limbPart + '0_FK_ctrl', limbmGrp)
			pm.parent(self.side + '_' + self.limbPart + '0_jnt', limbmGrp)

			pm.parent(self.side + '_arm_grp', 'main_ctrl')

		# create legs groups
		elif limbPart == 'leg':
			pm.parent(self.side + '_hip_jnt', limbmGrp)
			pm.parent(self.side + '_leg_ik_ctrl', limbmGrp)
			pm.parent(self.side + '_leg_limb_ikh', limbmGrp)
			pm.parent(self.side + '_leg_poleVector_ctrl', limbmGrp)

			pm.parent(self.poleVectCtrl, limbmGrp)
			pm.parent(self.startJoint.replace('_jnt', '_FK_ctrl'), limbmGrp)
			pm.parent(self.startJoint.replace('_jnt', '_IK_jnt'), limbmGrp)

			pm.parent(self.side + '_' + limbPart + '_ik_ctrl', limbmGrp)
			pm.parent(self.side + '_' + limbPart + '0_jnt', limbmGrp)
			pm.parent(limbmGrp, 'main_ctrl')
			pm.parent(self.side + '_arm_poleVector_ctrl', 'main_ctrl')
			pm.parent(self.side + '_arm_ik_ctrl', 'main_ctrl')
			
			pm.parent(self.side + '_leg_poleVector_ctrl', 'main_ctrl')
			pm.parent(self.side + '_leg_ik_ctrl', 'main_ctrl')

	def _build(self, side):
		"""
		main building block for rigging the limb
		"""

		# Duplicate and rename new joint chains (IK and FK)
		self.duplicateLimbChain(jnt=self.startJoint, FK=True)
		self.duplicateLimbChain(jnt=self.startJoint, IK=True)

		# FK Build controls for the limb
		for jnt in [self.startJoint, self.midJoint]:
			self.placeCtrl(jnt.replace('_jnt', '_FK_ctrl'), type='fk')

		# Create IK handle and control for switching IK/FK in the correct place
		self.buildIkCtrlSetup(side=self.side)

		# # IK/FK Blend Setup
		for jnt in [self.startJoint, self.midJoint, self.endJoint]:
			self.createIkFkBlendConnections(jnt)

		# hide rotations and scale and visibility from the channel box
		for ctrl in [self.startJoint.replace('_jnt', '_FK_ctrl'),
					 self.midJoint.replace('_jnt', '_FK_ctrl'), self.endJoint.replace('_jnt', '_FK_ctrl')]:
			rigUtils.hideAttributes(ctrl, trans=True, scale=True, rot=False, vis=True, radius=True)

		self.organizeLimbGrps(limbPart=self.limbPart)
