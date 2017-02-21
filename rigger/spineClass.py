import pymel.core as pm
import autorig.utils.utils as rigUtils


class Spine(object):

	def __init__(self, startJoint):

		self.starJoint = startJoint

		self._build()

	def getSpinePositions(self, startJoint):
		"""
		Gets all the spine position
		:param startJoint: string - joint name
		:return: dic - joint name : position
		"""

		jntList = []

		jntList = pm.listRelatives(startJoint, c=True, ad=True)
		jntList.append(startJoint)
		jntList.reverse()

		return jntList, len(jntList)


	def createFKControl(self, jnt):
		"""
		Create controls for the spine replacing the shape in the joints for a nurbs curve (control)
		:param jnt: string - first joint for the spine chain
		"""

		ctrlCrv = pm.circle(name=jnt.replace('_jnt', '_ctrl'), nr=(0,1,0), r=2.0)[0]
		rigUtils.setControlColor(ctrlCrv)

		pm.scale(0.12,0.12,0.12)
		pm.makeIdentity(a=True, s=True)

		pm.parent(ctrlCrv, jnt)

		# resets the transforms for the controller
		for trans in ['.tx', '.ty', '.tz', '.rx', '.ry', '.rz']:
			pm.setAttr(ctrlCrv + trans, 0)

		# unparent the control and parent the shape from the control to the joint, so we are adding a shape node to
		# the joint interact with the animator
		pm.parent(world=True)
		ctrlCrvShape = pm.listRelatives(ctrlCrv)
		pm.select(ctrlCrvShape)
		pm.select(jnt, add=True)
		pm.parent(r=True, s=True)
		pm.delete(ctrlCrv)

		pm.delete(ch = True)
		return  ctrlCrv


	def duplicateSpineChain(self, jnt):
		"""
		Duplicate spine chain and renames the chain
		:param jnt: string - first spine joint
		:return: list - all joints for the spine chain
		"""

		jntList = []
		duplicateSpine = pm.duplicate(jnt, rc=True)[0]
		duplicateSpine = pm.rename(duplicateSpine, 'COG_jnt_FK')

		spineJoints = pm.listRelatives(duplicateSpine, ad=True, c=True)

		for jnt in spineJoints:
			jntList.append(pm.rename(jnt, jnt.replace('_jnt1', '_ctrl')))

		jntList.reverse()

		return jntList


	def createCOGCtrl(self):
		"""
		create and place COG control in the COG joint
		"""

		cogCtrl = rigUtils.createRigControl('COG')
		pm.delete(pm.pointConstraint(self.starJoint, cogCtrl))
		pm.makeIdentity(cogCtrl, a=True, t=True)
		rigUtils.setControlColor(cogCtrl)
		cogCtrl = pm.rename(cogCtrl, 'COG_ctrl')

		pm.parent(self.starJoint, cogCtrl)


	def constraintFKtoBindJnts(self, jnt):
		"""
		Generate an orient constraint of each joint in the spine chain.
		:param jnt: string - start joint for the spine
		"""

		spineFKJoints = []
		jnt = pm.PyNode(jnt)

		spineJnts = pm.listRelatives(jnt, ad=True, c=True, s=False)
		bindSpineJnts = pm.listRelatives(self.starJoint, ad=True, c=True)

		for ctrl in spineJnts:
			if not ctrl.endswith('Shape'):
				spineFKJoints.append(ctrl)

		for jnt, bindJnt in zip(spineFKJoints, bindSpineJnts):
			pm.orientConstraint(jnt, bindJnt, mo=True)


	def organizeSpine(self):
		"""
		create groups and parents to have a spine module
		"""

		spineGrp = pm.group(name='spine_grp' , em=True)
		pm.parent('COG_ctrl', spineGrp)

		pm.parent(spineGrp, 'main_ctrl')


	def setChannelBoxAttrs(self, ctrl):
		rigUtils.hideAttributes(ctrl, trans=False, scale=True, rot=False, vis=True, radius=False)


	def _build(self):

		spineJntChainList = pm.ls('M_spine*_jnt')

		for i in range(len(spineJntChainList)-1):
			print(spineJntChainList[i])
			if i != 0:
				self.createFKControl(spineJntChainList[i])
				rigUtils.hideAttributes(spineJntChainList[i], trans=True, scale=True, rot=False, vis=True, radius=True)

		self.createCOGCtrl()
		rigUtils.hideAttributes('COG_ctrl', trans=False, scale=True, rot=False, vis=True, radius=False)

		self.organizeSpine()
