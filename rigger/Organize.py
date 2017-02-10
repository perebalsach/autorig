import pymel.core as pm
import autorig.utils.utils as rigUtils

reload(rigUtils)

def organizeRig():
	chestGrp = pm.group(name='chest_grp', p='main_ctrl')

	for side in ['L', 'R']:
		pm.parent(side + '_arm_grp', chestGrp)
		pm.parent(side + '_shoulder_ctrl', chestGrp)
		pm.parent(side + '_hand_grp', chestGrp)

	pm.parent('M_head_ctrl', chestGrp)
	pm.parent(chestGrp, 'head_end_jnt')