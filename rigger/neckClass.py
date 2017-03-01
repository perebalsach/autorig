import pymel.core as pm
import autorig.utils.utils as rigUtils

reload(rigUtils)

def build_head():
	headJnts = pm.ls('*_head*_jnt')
	ctrl = rigUtils.createRigControl('circle')[0]
	pm.rotate(90,0,0)
	pm.makeIdentity(ctrl, a=True, t=True, r=True)

	pm.rename(ctrl, 'head_ctrl')
	rigUtils.setControlColor(ctrl)

	pm.delete(pm.pointConstraint(headJnts[0], ctrl))
	orientConst = pm.orientConstraint(headJnts[0], ctrl, mo=False)

	pm.delete(orientConst)
	pm.makeIdentity(ctrl, a=True, t=True, r=True)

	pm.parent(headJnts[0], ctrl)

	headGrp = pm.group(n='head_grp', em=True)
	pm.parent(ctrl, headGrp)

	spineJntList = pm.ls('M_spine*_jnt')
	pm.parent(headGrp, 'neck_ctrl')
	rigUtils.hideAttributes(ctrl=ctrl, trans=True, rot=False, scale=True, vis=True, radius=False)

	pm.delete(ctrl, ch=1)


def build_neck():
	neckJnts = pm.ls('*_neck*_jnt')
	ctrl = rigUtils.createRigControl('circle')[0]
	pm.rotate(90,0,0)
	pm.makeIdentity(ctrl, a=True, t=True, r=True)

	pm.rename(ctrl, 'neck_ctrl')

	rigUtils.setControlColor(ctrl)

	pm.delete(pm.pointConstraint(neckJnts[0], ctrl))
	orientConst = pm.orientConstraint(neckJnts[0], ctrl, mo=False)

	pm.delete(orientConst)
	pm.makeIdentity(ctrl, a=True, t=True, r=True)

	pm.parent(neckJnts[0], ctrl)

	neckGrp = pm.group(n='neck_grp', em=True)
	pm.parent(ctrl, neckGrp)

	spineJntList = pm.ls('M_spine*_jnt')
	pm.parent(neckGrp, spineJntList[(len(spineJntList)-2)])

	rigUtils.hideAttributes(ctrl=ctrl, trans=True, rot=False, scale=True, vis=True, radius=False)
	pm.delete(ctrl, ch=1)
