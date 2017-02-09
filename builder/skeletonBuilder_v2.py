import pymel.core as pm


def generateJoints(side, baseName, helperList, discardLast):
	"""
	# based on the rigHelpers it creaes the joints in each rigHelper
	:param side: stirng - L or R
	:param baseName: string - Name of rig part (arm, leg, spine, ... )
	:param helperList: list - rigHelpers listr
	:param discardLast: int - discard last n joints from the helperList
	:return: list - joints generated
	"""

	jntList = []

	for i in range(len(helperList) - discardLast):
		helperNode = pm.PyNode(helperList[i])
		helperPos = helperNode.getTranslation('world')
		jntList.append(
			pm.joint(name=side + '_' + baseName + str(i) + '_jnt', p=(helperPos[0], helperPos[1], helperPos[2])))

	pm.select(deselect=True)

	return jntList


def build():
	side = 'L'

	armHelpersList = []
	shoulderHelpersList = []
	legHelpersList = []
	spineHelpersList = []

	armHelpersList = pm.ls(side + '_arm1_rigHelper', side + '_arm2_rigHelper', side + '_arm3_rigHelper')
	shoulderHelpersList = (side + '_arm0_rigHelper', side + '_arm1_rigHelper')
	legHelpersList = pm.ls(side + '_leg*rigHelper')
	spineHelpersList = pm.ls('*_spine*rigHelper')
	handHelperList = (side + '_arm3_rigHelper', side + '_arm4_rigHelper')

	armJnts = generateJoints(side=side, baseName='arm', helperList=armHelpersList, discardLast=0)
	shoulderJnts = generateJoints(side=side, baseName='shoulder', helperList=shoulderHelpersList, discardLast=0)
	legJnts = generateJoints(side=side, baseName='leg', helperList=legHelpersList, discardLast=3)
	spineJnts = generateJoints(side='M', baseName='spine', helperList=spineHelpersList, discardLast=1)
	handJnts = generateJoints(side=side, baseName='hand', helperList=handHelperList, discardLast=0)

	pm.select(armJnts[0])
	pm.mirrorJoint(mirrorYZ=True, mirrorBehavior=True, searchReplace=("L_", "R_"))

	pm.select(legJnts[0])
	pm.mirrorJoint(mirrorYZ=True, mirrorBehavior=True, searchReplace=("L_", "R_"))

	pm.select(handJnts[0])
	pm.mirrorJoint(mirrorYZ=True, mirrorBehavior=True, searchReplace=("L_", "R_"))
