import autorig.builder.armBuilder as armBuilder
import autorig.builder.legBuider as legBuilder
import autorig.builder.spineBuilder as spineBuilder
import pymel.core as pm
import maya.cmds as cmds
import autorig.utils.utils as rigUtils

reload(armBuilder)
reload(legBuilder)
reload(spineBuilder)


def createSym(source=None, target=None):
	"""
	Create a symmetry constraint between 2 objects to be moved in realtime in the viewport

	:param source: str - first object
	:param target: str - second object
	:return: None
	"""
	symmConst = cmds.createNode('symmetryConstraint', n=source + 'SymmetryConstraint')
	cmds.connectAttr(source + '.translate', symmConst + '.targetTranslate')
	cmds.connectAttr(source + '.rotate', symmConst + '.targetRotate')
	cmds.connectAttr(source + '.scale', symmConst + '.targetScale')
	cmds.connectAttr(source + '.parentMatrix[0]', symmConst + '.targetParentMatrix')
	cmds.connectAttr(source + '.worldMatrix[0]', symmConst + '.targetWorldMatrix')
	cmds.connectAttr(source + '.rotateOrder', symmConst + '.targetRotateOrder')
	cmds.connectAttr(symmConst + '.constraintTranslate', target + '.translate')
	cmds.connectAttr(symmConst + '.constraintRotate', target + '.rotate')
	cmds.connectAttr(symmConst + '.constraintScale', target + '.scale')
	cmds.connectAttr(symmConst + '.constraintRotateOrder', target + '.rotateOrder')
	cmds.connectAttr(target + '.parentInverseMatrix[0]', symmConst + '.constraintInverseParentWorldMatrix')
	cmds.parent(symmConst, target)
	cmds.select(source)

	return None


def build_legs():
	objList = ['_leg_0_rigHelper', '_leg_1_rigHelper', '_leg_2_rigHelper', '_leg_3_rigHelper', '_leg_4_rigHelper', '_leg_5_rigHelper']

	legBuilder.legGen(base_name='leg', side='L')
	legBuilder.legGen(base_name='leg', side='R')

	# create the symmetry for each helper
	for ob in objList:
		createSym(source='L' + ob, target='R' + ob)

	# moves the leg
	pm.move('L_leg_0_rigHelper', 0.1, ws=True, x=True)


def build_arms():
	armBuilder.LimbGen(spacing=0, num_sections=5, side='L', base_name='arm')
	armBuilder.LimbGen(spacing=0, num_sections=5, side='R', base_name='arm')

	pm.rotate('R_arm0_rigHelper', (0, 180, 0))
	pm.move('L_arm0_rigHelper', (0.17, 1.6, 0))
	pm.move('R_arm0_rigHelper', (-0.17, 1.6, 0))


	# create the symmetry for each helper
	for i in range(5):
		createSym('L_arm' + str(i) + '_rigHelper', 'R_arm' + str(i) + '_rigHelper')


def build_spine(num_sections=5):
	spineBuilder.build_spine(num_sections=num_sections, base_name='spine', side='M')


def organize():
	"""
	Create group structure to hold the helpers rig
	"""

	rigHelpersGrp = pm.group(name='rigHelpers_grp', em=True)

	for side in ['L', 'R']:
		pm.parent(side + '_leg_0_rigHelper', rigHelpersGrp)
		pm.parent(side + '_arm0_rigHelper', rigHelpersGrp)

	pm.parent('M_spine0_rigHelper', rigHelpersGrp)

	crvsGrp = pm.group(n='crvs_grp', em=True)

	for side in ['L','R']:
		pm.parent(side + '_leg_helper_grp', crvsGrp)
		pm.parent(side + '_arm_helper_grp', crvsGrp)

	pm.parent('M_spine_helper_grp', crvsGrp)

	scaleCtrl = pm.circle(n='scale_ctrl', r=1, nr=(0,1,0))
	rigUtils.setControlColor(scaleCtrl[0])

	pm.parent(rigHelpersGrp, scaleCtrl[0])

	helpersGrp = pm.group(n='helpers_grp', em=True)
	pm.parent(crvsGrp, helpersGrp)
	pm.parent(scaleCtrl[0], helpersGrp)



# main
def build(spine_sections=5, char_name="character"):

	build_legs()
	build_arms()
	build_spine(spine_sections)
	organize(name=char_name)
