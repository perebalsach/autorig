import pymel.core as pm
import autorig.utils.utils as rigUtils

reload(rigUtils)


class Foot(object):
	def __init__(self, footJnt, side):

		self.footJnt = footJnt
		self.side = side

		self._buid()

	def createFootJointChain(self, jnt):

		self.footJnt = pm.duplicate(jnt, returnRootsOnly=True, rc=True, name=self.side + '_foot_jnt_FK')[0]
		pm.parent(self.footJnt, w=True)

		footJntList = pm.listRelatives(self.footJnt, ad=True, c=True)

		for jntFK, jnt in zip([self.side + '_ball_jnt_FK', self.side + '_toe_jnt_FK'],
							  (footJntList[1], footJntList[0])):
			pm.rename(jnt, jntFK)

		return footJntList

	def createFootCtrl(self):
		"""
		Create foot nurbs curve and place in the feel of the character.
		The control will have the size from the heel helper to the end foot helper
		"""

		footCtrl = rigUtils.createRigControl('foot')
		pm.rename(footCtrl, self.side + footCtrl)
		footCtrl = self.side + footCtrl

		# mirror ctrl if we are doing the right side
		if self.side == 'R':
			pm.scale(footCtrl, (-1, 1, 1))
			pm.makeIdentity(footCtrl, a=True, s=True)

		# place the foot ctrl in the 3rd rig helper (heel)
		pm.delete(pm.pointConstraint(self.side + '_leg_3_rigHelper', footCtrl))
		pm.makeIdentity(footCtrl, a=True, t=True)

		endFootHelper = pm.PyNode(self.side + '_leg_5_rigHelper')
		endFootCtrl = pm.PyNode(self.side + '_foot_ctrl')

		# gets the heel helper world position and the bounding box of the foot controller
		endFootHelperPos = endFootHelper.getTranslation('world')
		bbox = pm.exactWorldBoundingBox(footCtrl)

		# gets the correct scale to feet the helpers
		scaleFactor = (endFootHelperPos[2] - bbox[5]) + 1
		pm.scale(footCtrl, scaleFactor, scaleFactor, scaleFactor)

		pm.makeIdentity(footCtrl, a=True, s=True)

		# parent the control to the new created foot chain
		rigUtils.setControlColor(footCtrl)
		pm.parent(self.footJnt, self.side + '_foot_ctrl')

		return footCtrl

	def addChannelBoxFootAttrs(self, ctrl):

		pm.addAttr(ctrl, at='float', longName='_________', min=0, max=1, dv=0, k=True)
		pm.addAttr(ctrl, at='float', longName='FK_IK', min=0, max=1, dv=0, k=True)
		pm.addAttr(ctrl, at='float', longName='__________', min=0, max=1, dv=0, k=True)
		pm.addAttr(ctrl, at='float', longName='heel_roll', dv=0, k=True)
		pm.addAttr(ctrl, at='float', longName='ball_roll', dv=0, k=True)
		pm.addAttr(ctrl, at='float', longName='toe_roll', dv=0, k=True)
		pm.addAttr(ctrl, at='float', longName='toe_bend', dv=0, k=True)

		pm.setAttr(ctrl + '._________', lock=True)
		pm.setAttr(ctrl + '.__________', lock=True)

	def createFootGroupSetup(self):

		# get all the rigHelpers foot positions
		self.footPositions = {'ankle': (0, 0, 0), 'heel': (0, 0, 0), 'ball': (0, 0, 0), 'toe': (0, 0, 0)}

		ankleHelper = pm.PyNode(self.side + '_leg_2_rigHelper')
		heelHelper = pm.PyNode(self.side + '_leg_3_rigHelper')
		ballHelper = pm.PyNode(self.side + '_leg_4_rigHelper')
		toeHelper = pm.PyNode(self.side + '_leg_5_rigHelper')

		self.footPositions['ankle'] = ankleHelper.getTranslation('world')
		self.footPositions['heel'] = heelHelper.getTranslation('world')
		self.footPositions['ball'] = ballHelper.getTranslation('world')
		self.footPositions['toe'] = toeHelper.getTranslation('world')

		# setup up groups
		pm.select(self.side + '_foot_jnt_FK')
		heelRollGrp = pm.group(name=self.side + '_heelRoll_grp')

		pm.select(self.side + '_foot_jnt_FK')
		toeRollGrp = pm.group(name=self.side + '_toeRoll_grp')

		pm.select(self.side + '_foot_jnt_FK')
		ballRollGrp = pm.group(name=self.side + '_ballRoll_grp')

		# setup pivots for the groups
		# set the pivot for the foot_ctrl to the ankle
		pm.xform(self.side + '_foot_ctrl', piv=self.footPositions['ankle'])

		# set the pivot for the foot_grp to the toe
		pm.xform(toeRollGrp, piv=self.footPositions['toe'])

		# set the pivot for the foot_grp to the ball
		pm.xform(ballRollGrp, piv=self.footPositions['ball'])

		# set the pivot for the foot_grp to the heel
		pm.xform(heelRollGrp, piv=self.footPositions['heel'])


	def createFootConnections(self, ctrl):

		pm.connectAttr(ctrl + '.heel_roll', self.side + '_heelRoll_grp.rotateX', f=True)
		pm.connectAttr(ctrl + '.toe_roll', self.side + '_toeRoll_grp.rotateX', f=True)
		pm.connectAttr(ctrl + '.ball_roll', self.side + '_ballRoll_grp.rotateX', f=True)

		footMdNode = pm.createNode('multiplyDivide', name=self.side + '_foot_md')
		pm.connectAttr(ctrl + '.ball_roll', footMdNode + '.input1X')
		# pm.connectAttr(footMdNode + '.outputX', self.side + '_ball_jnt_FK.rotateZ' )
		pm.setAttr(footMdNode + ".input2X", -1)

		# add new items in the plus minus avarage input3D
		plusMinusNode = pm.createNode('plusMinusAverage', name=self.side + '_foot_pma')

		pm.connectAttr(footMdNode + '.output.outputX', self.side + '_foot_pma.input3D[0].input3Dx')
		pm.connectAttr(ctrl + '.toe_bend', self.side + '_foot_pma.input3D[1].input3Dx')
		pm.connectAttr(self.side + '_foot_pma.output3D.output3Dx', self.side + '_ball_jnt_FK.rotateZ', f=True)

	def setupFootBehavior(self):
		"""
		Main proc for creating the IK / FK switch
		"""

		# create locators for the blending arm and groups.
		# and then position into the right place
		footPositions = {'ankle': (0, 0, 0), 'heel': (0, 0, 0), 'ball': (0, 0, 0), 'toe': (0, 0, 0)}

		# convert rigHelpers to PyNodes
		ankleHelper = pm.PyNode(self.side + '_leg_2_rigHelper')
		heelHelper  = pm.PyNode(self.side + '_leg_3_rigHelper')
		ballHelper  = pm.PyNode(self.side + '_leg_4_rigHelper')
		toeHelper   = pm.PyNode(self.side + '_leg_5_rigHelper')

		# get rigHelpers positions
		footPositions['ankle'] = ankleHelper.getTranslation('world')
		footPositions['heel']  = heelHelper.getTranslation('world')
		footPositions['ball']  = ballHelper.getTranslation('world')
		footPositions['toe']   = toeHelper.getTranslation('world')

		# create locators for the blending and groups them
		orientFKLoc = pm.spaceLocator(name=self.side + '_footFKOrient_loc')
		orientIKLoc = pm.spaceLocator(name=self.side + '_footIKOrient_loc')

		orientFKGrp = pm.group(name=self.side + '_footFKOrient_grp', em=True)
		orientIKGrp = pm.group(name=self.side + '_footIKOrient_grp', em=True)

		locFKShape = pm.listRelatives(orientFKLoc, s=1)[0]
		locIKShape = pm.listRelatives(orientIKLoc, s=1)[0]

		# setup a smaller locator and moves to the ankle joint
		for loc in [locFKShape, locIKShape]:
			for scale in ['.localScaleX', '.localScaleY', '.localScaleZ']:
				pm.setAttr(loc + scale, 0.0005
				)

			pm.move(loc, (footPositions['ankle'][0], footPositions['ankle'][1], footPositions['ankle'][2]))

		# parent each locator to the corresponding group
		for loc, grp in zip([orientFKLoc, orientIKLoc], [orientFKGrp, orientIKGrp]):
			pm.parent(loc, grp)

		# parent each locator group (IK and FK) to the right place
		pm.parent(orientIKGrp, self.side + '_leg_ik_ctrl')
		pm.parent(orientFKGrp, self.side + '_leg1_FK_ctrl')

		pm.parent(self.side + '_leg_limb_ikh', self.side + '_leg_ik_ctrl')

		footPointConst = pm.pointConstraint(orientIKLoc, orientFKLoc, self.side + '_foot_grp')
		footOrientConst = pm.orientConstraint(orientIKLoc, orientFKLoc, self.side + '_foot_grp')

		# connect orientConstraint weights to footCtrl to be able to switch the weights from the FK/IK attribute
		pm.connectAttr(self.side + '_foot_ctrl.FK_IK', footOrientConst + '.' + self.side + '_footFKOrient_locW1')
		footReverseNode = pm.createNode('reverse', name=self.side + '_footRev')

		pm.connectAttr(self.side + '_foot_ctrl.FK_IK', footReverseNode + '.input.inputX')
		pm.connectAttr(footReverseNode + '.output.outputX', footOrientConst + '.' + self.side + '_footIKOrient_locW0')

		pm.connectAttr(self.side + '_foot_ctrl.FK_IK', footPointConst + '.' + self.side + '_footFKOrient_locW1')
		footPointReverseNode = pm.createNode('reverse', name=self.side + '_footPointConsRev')
		pm.connectAttr(self.side + '_foot_ctrl.FK_IK', footPointReverseNode + '.input.inputX')
		pm.connectAttr(footPointReverseNode + '.output.outputX',
					   footPointConst + '.' + self.side + '_footIKOrient_locW0')

		# create groups setup for the foot
		footIkGrp = pm.group(name=self.side + '_footlRollIk_grp', em=True)
		heelIkGrp = pm.group(name=self.side + '_heelRollIk_grp', em=True)
		toeIkGrp = pm.group(name=self.side + '_toeRollIk_grp', em=True)
		ballIkGrp = pm.group(name=self.side + '_ballRollIk_grp', em=True)

		pm.move(heelIkGrp, (footPositions['heel'][0], footPositions['heel'][1], footPositions['heel'][2]))
		pm.move(toeIkGrp, (footPositions['toe'][0], footPositions['toe'][1], footPositions['toe'][2]))
		pm.move(ballIkGrp, (footPositions['ball'][0], footPositions['ball'][1], footPositions['ball'][2]))
		pm.move(footIkGrp, (footPositions['ankle'][0], footPositions['ankle'][1], footPositions['ankle'][2]))

		pm.parent(ballIkGrp, toeIkGrp)
		pm.parent(toeIkGrp, heelIkGrp)
		pm.parent(heelIkGrp, footIkGrp)

		pm.parent(self.side + '_leg_limb_ikh', ballIkGrp)
		pm.parent(footIkGrp, self.side + '_foot_ctrl')

		for rot in ['.rx', '.ry', '.rz']:
			pm.connectAttr(self.side + '_heelRoll_grp.rotate' + rot, heelIkGrp + '.rotate' + rot)

		for rot in ['.rx', '.ry', '.rz']:
			pm.connectAttr(self.side + '_toeRoll_grp.rotate' + rot, toeIkGrp + '.rotate' + rot)

		for rot in ['.rx', '.ry', '.rz']:
			pm.connectAttr(self.side + '_ballRoll_grp.rotate' + rot, ballIkGrp + '.rotate' + rot)

		for rot in ['.rx', '.ry', '.rz']:
			pm.connectAttr(self.side + '_foot_ctrl.rotate' + rot, footIkGrp + '.rotate' + rot)

		pm.parent(self.side + '_foot_grp', 'main_ctrl')
		pm.parent(self.side + '_foot0_jnt', self.side + '_foot_grp')


	def setFootGroupPivot(self):

		footGrp = pm.group(name=self.side + '_foot_grp', em=True)
		pm.parent(self.side + '_foot_ctrl', footGrp)
		anklePos = self.footPositions['ankle']
		pm.xform(footGrp, piv=(anklePos[0], anklePos[1], anklePos[2]))

	def connectFKIKBlendAttrs(self):
		"""
		Connects FK and IK channelBox attributes to the blend node for the FK/IK swith in the channelBox
		"""

		for legPart in [self.side + '_leg0_jnt_BC.blender',
						self.side + '_leg1_jnt_BC.blender',
						self.side + '_leg2_jnt_BC.blender']:
			pm.connectAttr(self.side + '_foot_ctrl' + '.FK_IK', legPart)

	def setupVisibility(self):
		for ctrl in ['_leg0_FK_ctrl', '_leg_poleVector_ctrl', '_leg_ik_ctrl']:
			pm.setAttr(self.side + ctrl + '.visibility', lock=False)

		legRevNode = pm.createNode('reverse', n=self.side + '_leg_inv')
		pm.connectAttr(self.side + '_foot_ctrl.FK_IK', self.side + '_leg0_FK_ctrl.visibility')

		pm.connectAttr(self.side + '_foot_ctrl.FK_IK', legRevNode + '.input.inputX')
		pm.connectAttr(legRevNode + '.output.outputX', self.side + '_leg_poleVector_ctrl.visibility')

		pm.connectAttr(self.side + '_foot_ctrl.FK_IK', legRevNode + '.input.inputY')
		pm.connectAttr(legRevNode + '.output.outputY', self.side + '_leg_ik_ctrl.visibility')


	def _buid(self):

		self.createFootJointChain(self.footJnt)

		footCtrl = self.createFootCtrl()

		rigUtils.hideAttributes(footCtrl, trans=True, scale=True, rot=False, vis=True, radius=False)

		self.addChannelBoxFootAttrs(footCtrl)
		self.createFootGroupSetup()

		self.createFootConnections(footCtrl)

		self.setFootGroupPivot()

		self.connectFKIKBlendAttrs()

		self.setupFootBehavior()
		self.setupVisibility()
