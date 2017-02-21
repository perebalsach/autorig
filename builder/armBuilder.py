import pymel.core as pm
import autorig.builder.rigHelper as rigHelper


class LimbGen(object):

	def __init__(self, spacing=0, num_sections=5, side='L', base_name='limb'):

		self.spacingDistance = spacing
		self.sections = num_sections
		self.sideName = side
		self.baseName = base_name

		self._build(spacing=self.spacingDistance, num_sections=self.sections, base_name=self.baseName, side=self.sideName)

	def _build(self, spacing=None, num_sections=None, base_name='None', side='None'):

		if num_sections < 2:
			print 'Need more sections to create a limb'
			return False

		limbRigHelpers = []
		arm_pos_list = []

		# create all the manipulatorHelpers and stores the objects and the positions
		for i in range(num_sections):
			# creates the RigHelper
			limbRigHelpers.append(rigHelper.RigHelperClass(name=side + '_' + base_name + str(i),
													size=0.08,
													pos=(spacing, 0, 0)))
			# saves all the manipulatorHelper positions to create the curve later
			arm_pos_list.append(limbRigHelpers[i].getPos())
			spacing += 0.20

		limbRigHelpers.reverse()
		arm_pos_list.reverse()

		# create the curve and sets the color
		link_crv = pm.curve(name=side + '_' + base_name + '_crv', d=1, p=arm_pos_list)
		pm.setAttr(link_crv + '.overrideEnabled', 1)


		pm.setAttr(link_crv + '.overrideColor', 18)

		# create cluster and parent it under the rigHelper
		for cv in range(len(link_crv.cv)):
			cls = pm.cluster(link_crv.cv[cv], name='limb_cls_' )
			limbRigHelpers[cv].setChild(cls[1])
			pm.setAttr(cls[1] + '.visibility', 0)

		# create hidracity for the arm
		for i in range(len(limbRigHelpers)):
			if not (i + 1) >= (len(limbRigHelpers)):
				pm.parent(limbRigHelpers[i].name(),
						  limbRigHelpers[i + 1].name())

		# create group and parent all the elements
		limb_grp = pm.group(name= side + '_' + base_name + '_helper_grp', em=True)
		pm.parent(limbRigHelpers[(len(limbRigHelpers)-1)].name(), limb_grp)
		pm.parent(link_crv, limb_grp)

		pm.select(deselect=True)

		return True
