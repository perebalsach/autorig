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
		shoulder = pm.ls('L_shoulderRoot_jnt')

		# get shoulder rigHelpers positions
		shoulderRootHelper = pm.PyNode(self.side + '_arm0_rigHelper')
		shoulderEndHelper  = pm.PyNode(self.side + '_arm1_rigHelper')

		self.shoulderRootPos = shoulderRootHelper.getTranslation('world')
		self.shoulderEndPos  = shoulderEndHelper.getTranslation('world')

		if not shoulder:
			jointList = []
			jointList.append(pm.joint(name=self.side + '_shoulderRoot_jnt',
									  p=(self.shoulderRootPos[0], self.shoulderRootPos[1], self.shoulderRootPos[2])))
			jointList.append(pm.joint(name=self.side + '_shoulderEnd_jnt',
									  p=(self.shoulderEndPos[0], self.shoulderEndPos[1], self.shoulderEndPos[2])))

			# orient joints
			for i in range(len(jointList)):
				pm.select(jointList[i])
				pm.joint(e=True, oj='yxz', secondaryAxisOrient='zup', ch=True, zso=True)

			pm.select(deselect=True)

		else:
			pm.select('L_shoulderRoot_jnt')
			pm.mirrorJoint( mirrorYZ=True, mirrorBehavior=True, searchReplace=("L_", "R_"))

			pm.select(deselect=True)


	def createShoulderCtrl(self):
		"""
		create shoulder ctrl and place the ctrl in the shoulder position with the desired color
		"""
		shoulderCtrlExists = pm.ls('L_shoulder_ctrl')

		shoulderCtrl = rigUtils.createRigControl('pin')
		shoulderCtrl = pm.rename(shoulderCtrl, self.side + '_shoulder_ctrl')

		if shoulderCtrlExists:
			tmpGrp = pm.group(n='tmp_grp', p='L_shoulder_ctrl')
			pm.scale(tmpGrp, (-1, 1, 1))
			pm.parent('L_shoulder_ctrl', w=True)
			pm.delete(tmpGrp)

		else:
			pm.move(shoulderCtrl, (self.shoulderRootPos[0], self.shoulderRootPos[1], self.shoulderRootPos[2]))
			pm.rotate(shoulderCtrl, (-90, -90, 0))
			pm.makeIdentity(a=True, s=True, t=True, r=True)
			rigUtils.setControlColor(shoulderCtrl)


	def shoulderSetup(self):
		"""
		create parents to be able to move the shoulder as it should move
		"""

		pm.parent(self.side + '_shoulderRoot_jnt', self.side + '_shoulder_ctrl')
		pm.select(deselect=True)

		shoulderGrp = pm.group(n=self.side + '_shoulder_grp')
		pm.parent(self.side + '_shoulder_ctrl', shoulderGrp)

		shoulderRightGrp = pm.duplicate(shoulderGrp)
		shoulderRightGrp = pm.rename(shoulderRightGrp, 'R_shoulder_grp')
		pm.scale(shoulderRightGrp, (-1,1,1))

		# rename contents of the shoulder group
		grpList = pm.listRelatives(shoulderRightGrp, ad=True)
		for itm in grpList:
			pm.rename(itm, (itm.replace('L_', 'R_')))

		rigUtils.setControlColor('R_shoulder_ctrl')

		pm.parent(shoulderGrp, 'main_ctrl')
		pm.parent(shoulderRightGrp, 'main_ctrl')
		pm.parent(self.side + '_arm_grp', self.side + '_shoulder_ctrl')
		
		pm.parent('R_arm_grp', 'R_shoulder_ctrl')

	def build(self):
		"""
		main shoulder rig setup
		"""
		self.createShoulderJoints()
		self.createShoulderCtrl()
		self.shoulderSetup()
