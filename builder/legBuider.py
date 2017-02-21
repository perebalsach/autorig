import pymel.core as pm
import autorig.builder.rigHelper as rigHelper

class legGen(object):

	def __init__(self, base_name='default_name', side='L'):

		self.name = base_name
		self.side = side

		self._build(base_name=self.name, side=self.side)

	def _build(self, base_name=None, side=None):

		limbRigHelpers = []
		limb_pos_list = []
		legParts = ['hip', 'knee', 'ankle', 'footBack', 'footRoll', 'footEnd']
		helperSize = 0.05

		# creates leg RigHelpers
		limbRigHelpers.append(rigHelper.RigHelperClass(name=side + '_leg_0' ,size=helperSize+0.02, pos=(0.1, 1.0, 0)))
		limbRigHelpers.append(rigHelper.RigHelperClass(name=side + '_leg_1' ,size=helperSize, pos=(0.1, 0.5, 0.02)))
		limbRigHelpers.append(rigHelper.RigHelperClass(name=side + '_leg_2' ,size=helperSize, pos=(0.1, 0.15, -0.04)))
		limbRigHelpers.append(rigHelper.RigHelperClass(name=side + '_leg_3' ,size=helperSize, pos=(0.1, 0, -0.1)))
		limbRigHelpers.append(rigHelper.RigHelperClass(name=side + '_leg_4' ,size=helperSize, pos=(0.1, 0, 0.075)))
		limbRigHelpers.append(rigHelper.RigHelperClass(name=side + '_leg_5' ,size=helperSize, pos=(0.1, 0, 0.2)))

		# saves all the manipulatorHelper positions to create the curve later
		for helper in range(len(limbRigHelpers)):
			limb_pos_list.append(limbRigHelpers[helper].getPos())

		limbRigHelpers.reverse()
		limb_pos_list.reverse()

		# create the curve and sets the color
		link_crv = pm.curve(name=side + '_' + base_name + '_crv', d=1, p=limb_pos_list)
		pm.setAttr(link_crv + '.overrideEnabled', 1)
		pm.setAttr(link_crv + '.overrideColor', 18)

		# create cluster and parent it under the rigHelper
		for cv in range(len(link_crv.cv)):
			cls = pm.cluster(link_crv.cv[cv], name='limb_cls_'+ base_name )
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
