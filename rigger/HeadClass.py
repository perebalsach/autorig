import pymel.core as pm
import autorig.utils.utils as rigUtils

reload(rigUtils)


class Head(object):
	def __init__(self):
		self._build()

	def createHeadJoints(self):
		jointList = []

		# get head rigHelpers positions
		headRoot = pm.PyNode('M_spine1_rigHelper')
		headEnd = pm.PyNode('M_spine0_rigHelper')

		self.headRootPos = headRoot.getTranslation('world')
		self.headEndPos = headEnd.getTranslation('world')

		jointList.append(pm.joint(name='M_headRoot_jnt', p=(self.headRootPos[0], self.headRootPos[1], self.headRootPos[2])))
		jointList.append(pm.joint(name='M_headEnd_jnt', p=(self.headEndPos[0], self.headEndPos[1], self.headEndPos[2])))

		# orient Joints
		for i in range(len(jointList)):
			pm.select(jointList[i])
			pm.joint(e=True, oj='yxz', secondaryAxisOrient='zup', ch=True, zso=True)

	def createneckCtrl(self):
		headCtrl = rigUtils.createRigControl('circle')
		headCtrl = pm.rename(headCtrl[0], 'M_head_ctrl')
		rigUtils.setControlColor(headCtrl)

		pm.move(headCtrl, (self.headRootPos[0], self.headRootPos[1], self.headRootPos[2]))
		pm.rotate(headCtrl, (0, 0, 90))
		pm.scale(headCtrl, (1.5, 1.5, 1.5))
		pm.makeIdentity(a=True, r=True, t=True, s=True)

	def headSetup(self):
		pm.parent('M_headRoot_jnt', 'M_head_ctrl')

	def spaceSwitchHeadSetup(self):
		mainFollowLoc = pm.spaceLocator(name='M_headFollowMain_loc')
		headFollowLoc = pm.spaceLocator(name='M_headFollowHead_loc')

		# reduce local scale
		for loc in [mainFollowLoc, headFollowLoc]:
			pm.setAttr(loc + 'Shape.localScaleX', 0.0015)
			pm.setAttr(loc + 'Shape.localScaleY', 0.0015)
			pm.setAttr(loc + 'Shape.localScaleZ', 0.0015)

		mainFollowGrp = pm.group(name='M_headFollowMain_grp', em=True)
		headFollowGrp = pm.group(name='M_headFollowHead_grp', em=True)

		pm.parent(mainFollowLoc, mainFollowGrp)
		pm.parent(headFollowLoc, headFollowGrp)

		pm.move(mainFollowGrp, (self.headRootPos[0], self.headRootPos[1], self.headRootPos[2]))
		pm.move(headFollowGrp, (self.headRootPos[0], self.headRootPos[1], self.headRootPos[2]))

		pm.parent('M_head_ctrl', 'main_ctrl')


	def _build(self):
		self.createHeadJoints()
		self.createneckCtrl()
		self.headSetup()
		self.spaceSwitchHeadSetup()


