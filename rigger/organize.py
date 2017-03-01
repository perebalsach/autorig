import pymel.core as pm
import autorig.utils.utils as rigUtils

reload(rigUtils)

def organizeRig():
	pm.select(deselect=True)
	chestCtrl = 'M_spine2_jnt'
	
	chestGrp = pm.group(name='chest_grp', p='main_ctrl')
	
	for side in ['L', 'R']:
		pm.parent(side + '_shoulder_grp', chestGrp)
		pm.parent(side + '_hand_grp', chestGrp)
		pm.parent(chestGrp, chestCtrl)
		
		pm.parent(side + '_leg_grp', 'COG_ctrl')