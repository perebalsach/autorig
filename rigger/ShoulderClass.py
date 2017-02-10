import pymel.core as pm
import autorig.utils.utils as rigUtils

reload(rigUtils)


class Shoulder(object):
	def __init__(self, side):
		self.side = side
		self.build()

	def createShoulderJoints(self):
		"""
		create shoulder joints based on the shoulder rigHelpers positions
		"""

		jointList = []

		# get shoulder rigHelpers positions
		shoulderRootHelper = pm.PyNode(self.side + '_arm0_rigHelper')
		shoulderEndHelper = pm.PyNode(self.side + '_arm1_rigHelper')

		self.shoulderRootPos = shoulderRootHelper.getTranslation('world')
		self.shoulderEndPos = shoulderEndHelper.getTranslation('world')

		jointList.append(pm.joint(name=self.side + '_shoulderRoot_jnt',
								  p=(self.shoulderRootPos[0], self.shoulderRootPos[1], self.shoulderRootPos[2])))
		jointList.append(pm.joint(name=self.side + '_shoulderEnd_jnt',
								  p=(self.shoulderEndPos[0], self.shoulderEndPos[1], self.shoulderEndPos[2])))

		# orient joints
		for i in range(len(jointList)):
			pm.select(jointList[i])
			pm.joint(e=True, oj='yxz', secondaryAxisOrient='zup', ch=True, zso=True)


	def createShoulderCtrl(self):
		"""
		create shoulder ctrl and place the ctrl in the shoulder position with the desired color
		"""

		shoulderCtrl = rigUtils.createRigControl('pin')
		shoulderCtrl = pm.rename(shoulderCtrl, self.side + '_shoulder_ctrl')
		pm.move(shoulderCtrl, (self.shoulderRootPos[0], self.shoulderRootPos[1], self.shoulderRootPos[2]))
		pm.rotate(shoulderCtrl, (-90, -90, 0))
		pm.makeIdentity(a=True, s=True, t=True, r=True)
		rigUtils.setControlColor(shoulderCtrl)


	def shoulderSetup(self):
		"""
		create parents to be able to move the shoulder as it should move
		"""

		pm.parent(self.side + '_shoulderRoot_jnt', self.side + '_shoulder_ctrl')
		pm.parent(self.side + '_arm_grp', self.side + '_shoulder_ctrl')

		pm.parent(self.side + '_shoulder_ctrl', 'main_ctrl')


	def build(self):
		"""
		main shoulder rig setup
		"""

		self.createShoulderJoints()
		self.createShoulderCtrl()
		self.shoulderSetup()
