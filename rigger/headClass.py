import pymel.core as pm
import autorig.utils.utils as rigUtils

reload(rigUtils)


class Head(object):
	def __init__(self):
		self._build()

	def createHeadJoints(self):
		jointList = []

		# check number of spine joints to locate the helper head helpers
		self.spineHelpersList = pm.ls('M_spine*rigHelper', type='transform')


		# get head rigHelpers positions
		self.headRoot = pm.PyNode(self.spineHelpersList[(len(self.spineHelpersList)-2)])
		self.headEnd = pm.PyNode(self.spineHelpersList[(len(self.spineHelpersList)-1)])

		self.headRootPos = self.headRoot.getTranslation('world')
		self.headEndPos  = self.headEnd.getTranslation('world')

		jointList.append(pm.joint(name='M_headRoot_jnt', p=(self.headRootPos[0], self.headRootPos[1], self.headRootPos[2])))
		jointList.append(pm.joint(name='M_headEnd_jnt', p=(self.headEndPos[0], self.headEndPos[1], self.headEndPos[2])))

		# orient Joints
		for i in range(len(jointList)):
			pm.select(jointList[i])
			pm.joint(e=True, oj='yxz', secondaryAxisOrient='zup', ch=True, zso=True)


	def createNeckCtrl(self):

		headCtrl = rigUtils.createRigControl('circle')
		headCtrl = pm.rename(headCtrl[0], 'M_head_ctrl')
		rigUtils.setControlColor(headCtrl)

		pm.move(headCtrl, (self.headRootPos[0], self.headRootPos[1], self.headRootPos[2]))
		pm.rotate(headCtrl, (0, 0, 90))
		pm.scale(headCtrl, (1.5, 1.5, 1.5))
		pm.makeIdentity(a=True, r=True, t=True, s=True)


	def headSetup(self):
		pm.parent('M_headRoot_jnt', 'M_head_ctrl')
		pm.pointConstraint('M_head_ctrl', self.headRoot )


	def spaceSwitchHeadSetup(self):

		mainFollowLoc = pm.spaceLocator(name='M_headFollowMain_loc')
		headFollowLoc = pm.spaceLocator(name='M_headFollowHead_loc')

		# reduce local scale
		for loc in [mainFollowLoc, headFollowLoc]:
			pm.setAttr(loc + 'Shape.localScaleX', 0.015 )
			pm.setAttr(loc + 'Shape.localScaleY', 0.015)
			pm.setAttr(loc + 'Shape.localScaleZ', 0.015)

		mainFollowGrp = pm.group(name='M_headFollowMain_grp', em=True)
		headFollowGrp = pm.group(name='M_headFollowHead_grp', em=True)

		pm.parent(mainFollowLoc, mainFollowGrp)
		pm.parent(mainFollowGrp, 'main_ctrl')

		pm.parent(headFollowLoc, headFollowGrp)
		# pm.parent(headFollowGrp, 'M_head_ctrl')

		pm.move(mainFollowGrp, (self.headRootPos[0], self.headRootPos[1], self.headRootPos[2]))
		pm.move(headFollowGrp, (self.headRootPos[0], self.headRootPos[1], self.headRootPos[2]))

		neckCtrlNum = (len(pm.ls('M_spine*_jnt'))-1)
		pm.select('M_spine%s_jnt' %neckCtrlNum)
		neckCtrl = pm.ls(sl=True)[0]
		neckCtrl = pm.PyNode(neckCtrl)
		neckPos = neckCtrl.getTranslation('world')

		headFollowHeadGrp = pm.group(n='M_followHead_grp')
		pm.parent(headFollowGrp ,headFollowHeadGrp)

		pm.xform(headFollowGrp, piv=neckPos, ws=True)

		followOrientConst = pm.orientConstraint('M_headFollowMain_loc', 'M_headFollowHead_loc', headFollowHeadGrp, mo=True)
		print ('NeckCtrl: %s' %neckCtrl)
		pm.parent('M_head_ctrl', neckCtrl)

		rigUtils.hideAttributes(ctrl='M_head_ctrl', trans=True, scale=True, rot=False, vis=True, radius=False)

		# add channel box attributes to switch space
		pm.addAttr('M_head_ctrl', ln="follow", at="enum", en="main:head:" )
		pm.setAttr('M_head_ctrl.follow', e=True, keyable=True)

		# create connections from the follow attrs to the orientConstraint
		headFollowInvNode = pm.createNode('reverse', name='headFollow_inv')

		pm.connectAttr('M_head_ctrl.follow', 'M_followHead_grp_orientConstraint1.M_headFollowHead_locW1', f=True)
		pm.connectAttr('M_head_ctrl.follow', headFollowInvNode + '.inputX', f=True)
		pm.connectAttr(headFollowInvNode + '.outputX', 'M_followHead_grp_orientConstraint1.M_headFollowMain_locW0',  f=True)


	def _build(self):
		self.createHeadJoints()
		self.createNeckCtrl()
		self.headSetup()
		# self.spaceSwitchHeadSetup()
