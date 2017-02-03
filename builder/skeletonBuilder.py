# Auto generates skeleton for the biped based on the rigHelpers in the scene
import pymel.core as pm
import autorig.utils.utils as rigUtils


armHelpersList = pm.ls('*arm*_rigHelper')
legHelpersList = pm.ls('*leg*_rigHelper')
spineHelpersList = pm.ls('*spine*_rigHelper')


def build_skeleton(side=None, joint_list=None):

	pm.select(deselect=True)

	armJointNames = ['_scapula_jnt', '_shoulder_jnt', '_elbow_jnt', '_hand_jnt', '_hand_end_jnt']
	legJointNames = ['_hip_jnt', '_knee_jnt', '_ankle_jnt', '_foot_back_jnt', '_foot_jnt', '_foot_end_jnt']

	armMatches = filter(lambda s: 'arm' in str(s), joint_list)
	legMatches = filter(lambda s: 'leg' in str(s), joint_list)
	spineMatches = filter(lambda s: 'spine' in str(s), joint_list)

	if len(armMatches) > 1:
		# create joints
		for i in range(len(joint_list)):
			pm.joint(name=side + armJointNames[i] ,p=(pm.PyNode(joint_list[i]).getTranslation('world')))

		# orient joints
		for i in range(len(joint_list)):
			pm.select(side + armJointNames[i])
			pm.joint(e=True, oj='yxz', secondaryAxisOrient='zup', ch=True, zso=True)

		# mirror joints
		pm.select(side + armJointNames[0])
		pm.mirrorJoint( mirrorYZ=True, mirrorBehavior=True, searchReplace=("L_", "R_"))

	elif len(legMatches) > 1:
		# create joints
		for i in range(len(joint_list)):
			print joint_list[i]
			if not joint_list[i] == side + '_leg_3_rigHelper':
				pm.joint(name=side + legJointNames[i] ,p=(pm.PyNode(joint_list[i]).getTranslation('world')))

		# orient joints
		for i in range(len(joint_list)):
			if not legJointNames[i] == '_foot_back_jnt':
				pm.select(side + legJointNames[i])
				pm.joint(e=True, oj='yxz', secondaryAxisOrient='zup', ch=True, zso=True)

		# mirror joints
		pm.select(side + legJointNames[0])
		pm.mirrorJoint( mirrorYZ=True, mirrorBehavior=True, searchReplace=("L_", "R_"))

	elif len(spineMatches) > 1:
		# spine names
		spineNameList = ['COG_jnt', 'spine01_jnt', 'spine02_jnt', 'spine03_jnt', 'spine04_jnt', 'spine05_jnt',
						 'spine06_jnt', 'spine07_jnt','spine08_jnt', 'spine09_jnt','spine10_jnt']

		spineTopNameList = ['head_end_jnt', 'head_jnt', 'neck_jnt', 'chest_jnt']

		# create joints, we discard the last one, so the head is not created
		for i in range(int(len(joint_list)-1)):
			pm.joint(name=spineNameList[i] ,p=(pm.PyNode(joint_list[i]).getTranslation('world')))

		# orient joints

		for i in range(int(len(joint_list)-1)):
			pm.select(spineNameList[i])
			pm.joint(e=True, oj='yxz', secondaryAxisOrient='zup', ch=True, zso=True)

		# rename the last 4 joints to match the rigging naming convention
		pm.select('COG_jnt')
		spineJointList = pm.listRelatives(ad=True, c=True)

		for i in range(4):
			pm.rename(spineJointList[i], spineTopNameList[i])



jntLst = filter(lambda k: 'L' in k, armHelpersList)
build_skeleton(side='L', joint_list=jntLst)

jntLst = filter(lambda k: 'L' in k, legHelpersList)
build_skeleton(side='L', joint_list=jntLst)

jntLst = filter(lambda k: 'M' in k, spineHelpersList)
jntLst.reverse()
build_skeleton(side='', joint_list=jntLst)
