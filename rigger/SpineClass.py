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


	def setControlColor(self, ctrl):
		"""
		turn on drawing overrides for the control and sets the color based on the name of the controller.
		L = Blue, R = Red and others = Yellow
		:param ctrl: transform
		"""

		shape = pm.listRelatives(ctrl, s=1)[0]
		pm.setAttr(shape + '.ove', 1)

		if ctrl.startswith('L'):
			pm.setAttr(shape + '.ovc', 6)

		elif ctrl.startswith('R'):
			pm.setAttr(shape + '.ovc', 13)

		else:
			pm.setAttr(shape + '.ovc', 17)


	def hideAttributes(self, ctrl, trans, scale, rot, vis, radius):
		"""
		Hide channelbox attributes
		:param ctrl: string - Name of the control
		:param trans: bool
		:param scale: bool
		:param rot: bool
		:param vis: bool
		"""

		if trans:
			for attr in ['.tx', '.ty', '.tz']:
				pm.setAttr(ctrl + attr, lock=True, keyable=False, cb=False)

		if rot:
			for attr in ['.rx', '.ry', '.rz']:
				pm.setAttr(ctrl + attr, lock=True, keyable=False, cb=False)

		if scale:
			for attr in ['.sx', '.sy', '.sz']:
				pm.setAttr(ctrl + attr, lock=True, keyable=False, cb=False)

		if vis:
			pm.setAttr(ctrl + '.v', lock=True, keyable=False, cb=False)

		if radius:
			pm.setAttr(ctrl + '.radi', lock=True, keyable=False, cb=False)


	def createFKControl(self, jnt):
		"""
		Create controls for the spine replacing the shape in the joints for a nurbs curve (control)
		:param jnt: string - first joint for the spine chain
		"""

		ctrlCrv = pm.circle(name=jnt.replace('_jnt', '_ctrl'), nr=(0,1,0), r=2.0)[0]
		self.setControlColor(ctrlCrv)

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
		self.setControlColor(cogCtrl)
		cogCtrl = pm.rename(cogCtrl, 'COG_ctrl')

		pm.parentConstraint(cogCtrl, 'COG_jnt_FK', mo=True)
		pm.orientConstraint('COG_jnt_FK', self.starJoint, mo=True)
		pm.pointConstraint('COG_jnt_FK', self.starJoint, mo=True)


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
		pm.parent(self.starJoint, spineGrp)
		pm.parent('COG_ctrl', spineGrp)
		pm.parent('COG_jnt_FK', spineGrp)

		pm.parent('spine_grp', 'main_ctrl')


	def setChannelBoxAttrs(self, ctrl):
		self.hideAttributes(ctrl, trans=False, scale=True, rot=False, vis=True, radius=False)

	def _build(self):

		jntList, numJoints = self.getSpinePositions(self.starJoint)
		spineJntChainList = self.duplicateSpineChain(self.starJoint)

		for i in range(len(spineJntChainList)-1):
			self.createFKControl(spineJntChainList[i])
			self.hideAttributes(spineJntChainList[i], trans=True, scale=True, rot=False, vis=True, radius=True)

		self.createCOGCtrl()
		self.constraintFKtoBindJnts('COG_jnt_FK')

		self.setChannelBoxAttrs('COG_ctrl')

		self.organizeSpine()
