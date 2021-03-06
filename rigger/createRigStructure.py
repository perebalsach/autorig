import pymel.core as pm
import autorig.utils.utils as rigUtils


def createRigStructure():

	pm.promptDialog (m='Enter character name:', title='Autorig')
	characterName = pm.promptDialog(query=True, text=True)

	# create group structre for the rig
	mainGrp = pm.group(name=characterName, em=True)
	pm.group(name='mesh_grp', em=True, p=mainGrp)
	rigGrp = pm.group(name='rig_grp', em=True, p=mainGrp)

	# create main ctrl for the rig
	mainCtrlGrp = rigUtils.createRigControl('cross')
	mainCtrlGrp = pm.rename(mainCtrlGrp, 'main_ctrl')
	rigUtils.setControlColor(mainCtrlGrp)
	"""
	pm.group(name='m_head_grp', em=True, p=mainCtrlGrp)
	pm.group(name='m_spine_grp', em=True, p=mainCtrlGrp)
	pm.group(name='l_leg_grp', em=True, p=mainCtrlGrp)
	pm.group(name='l_leg_grp', em=True, p=mainCtrlGrp)
	pm.group(name='l_arm_grp', em=True, p=mainCtrlGrp)
	pm.group(name='r_arm_grp', em=True, p=mainCtrlGrp)
	pm.group(name='l_foot_grp', em=True, p=mainCtrlGrp)
	pm.group(name='r_foot_grp', em=True, p=mainCtrlGrp)
	"""
	pm.parent(mainCtrlGrp, rigGrp)
