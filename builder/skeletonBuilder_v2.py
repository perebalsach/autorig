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

	armHelpersList      = []
	shoulderHelpersList = []
	legHelpersList      = []
	spineHelpersList    = []
	footHelperList      = []
	neckHelperList      = []
	headHelperList      = []

	# spine helper list generation
	for i in range(len(pm.ls('M_spine*_rigHelper'))-2):
		spineHelpersList.append('M_spine%s_rigHelper' %str(i))

	# head helper list generation
	for i in reversed(range(len(pm.ls('M_spine*_rigHelper')))):
		if i > 3:
			headHelperList.append('M_spine%s_rigHelper' %str(i))
	headHelperList.reverse()

	# neck helper list generation
	for i in range(len(pm.ls('M_spine*_rigHelper'))):
		if i > 2 and i < 5:
			neckHelperList.append('M_spine%s_rigHelper' %str(i))

	armHelpersList      = pm.ls(side + '_arm1_rigHelper', side + '_arm2_rigHelper', side + '_arm3_rigHelper')
	shoulderHelpersList = (side + '_arm0_rigHelper', side + '_arm1_rigHelper')
	legHelpersList      = pm.ls(side + '_leg*rigHelper')

	handHelperListLeft  = (side + '_arm3_rigHelper', side + '_arm4_rigHelper')
	handHelperListRight = ('R' + '_arm3_rigHelper', side + '_arm4_rigHelper')
	footHelperList      = pm.ls(side + '_leg_2_rigHelper', side + '_leg_4_rigHelper', side + '_leg_5_rigHelper')

	armJnts   = generateJoints(side=side, baseName='arm', helperList=armHelpersList, discardLast=0)
	legJnts   = generateJoints(side=side, baseName='leg', helperList=legHelpersList, discardLast=3)
	handJnts  = generateJoints(side=side, baseName='hand', helperList=handHelperListLeft, discardLast=0)
	footJnts  = generateJoints(side=side, baseName='foot', helperList=footHelperList, discardLast=0)

	spineJnts = generateJoints(side='M', baseName='spine', helperList=spineHelpersList, discardLast=0)
	neckJnts  = generateJoints(side='M', baseName='neck', helperList=neckHelperList, discardLast=0)
	headJnts  = generateJoints(side='M', baseName='head', helperList=headHelperList, discardLast=0)

	# orient joints
	for jnt in spineJnts:
		pm.select(jnt)
		pm.joint(e=True, oj='yxz', secondaryAxisOrient='zup', ch=True, zso=True)

	for jnt in armJnts:
		pm.select(jnt)
		pm.joint(e=True, oj='yxz', secondaryAxisOrient='zup', ch=True, zso=True)

	for jnt in legJnts:
		pm.select(jnt)
		pm.joint(e=True, oj='yxz', secondaryAxisOrient='zup', ch=True, zso=True)

	for jnt in handJnts:
		pm.select(jnt)
		pm.joint(e=True, oj='yxz', secondaryAxisOrient='zup', ch=True, zso=True)

	for jnt in footJnts:
		pm.select(jnt)
		pm.joint(e=True, oj='yxz', secondaryAxisOrient='zup', ch=True, zso=True)

	for jnt in neckJnts:
		pm.select(jnt)
		pm.joint(e=True, oj='yxz', secondaryAxisOrient='zup', ch=True, zso=True)

	for jnt in headJnts:
		pm.select(jnt)
		pm.joint(e=True, oj='yxz', secondaryAxisOrient='zup', ch=True, zso=True)


	#  mirror joints
	for jnt in [armJnts[0], legJnts[0], footJnts[0], handJnts[0]]:
		pm.select(jnt)
		pm.mirrorJoint(mirrorYZ=True, mirrorBehavior=True, searchReplace=("L_", "R_"))
