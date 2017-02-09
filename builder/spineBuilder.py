import builder.rigHelper as rigHelper
import pymel.core as pm


def build_spine(num_sections=5, base_name='spine', side=''):

	if num_sections < 2:
		print 'Need more sections to create a limb'
		return False

	spacing = 0
	limbRigHelpers = []
	limb_pos_list = []

	# create all the manipulatorHelpers and stores the objects and the positions
	for i in range(num_sections):
		# creates the RigHelper
		limbRigHelpers.append(rigHelper.RigHelperClass(name=side + '_' + base_name + str(i), size=0.1,
														   pos=(0, spacing + (0.14 * num_sections), 0)))

		# saves all the manipulatorHelper positions to create the curve later
		limb_pos_list.append(limbRigHelpers[i].getPos())
		spacing += 0.25

	limbRigHelpers.reverse()
	limb_pos_list.reverse()

	# create the curve and sets the color
	link_crv = pm.curve(name=side + '_' + base_name + '_crv', d=1, p=limb_pos_list)
	pm.setAttr(link_crv + '.overrideEnabled', 1)
	pm.setAttr(link_crv + '.overrideColor', 18)

	# create cluster and parent it under the rigHelper
	for cv in range(len(link_crv.cv)):
		cls = pm.cluster(link_crv.cv[cv], name='limb_cls_')
		limbRigHelpers[cv].setChild(cls[1])
		pm.setAttr(cls[1] + '.visibility', 0)

	# create hidracity for the arm
	for i in range(len(limbRigHelpers)):
		if not (i + 1) >= (len(limbRigHelpers)):
			pm.parent(limbRigHelpers[i].name(),
					  limbRigHelpers[i + 1].name())

	# create group and parent all the elements
	limb_grp = pm.group(name=side + '_' + base_name + '_helper_grp', em=True)
	pm.parent(limbRigHelpers[(len(limbRigHelpers) - 1)].name(), limb_grp)
	pm.parent(link_crv, limb_grp)

	pm.select(deselect=True)

	return True
