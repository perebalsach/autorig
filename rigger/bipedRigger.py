import pymel.core as pm
import autorig.rigger.limbClass as limb
import autorig.rigger.handClass as hand
import autorig.rigger.spineClass as spine
import autorig.rigger.footClass as foot
import autorig.rigger.shoulderClass as shoulder
import autorig.rigger.organize as rigOrganizer
import autorig.rigger.headClass as head
import autorig.rigger.createRigStructure as rigStruct

reload(rigStruct)
reload(limb)
reload(hand)
reload(spine)
reload(foot)
reload(shoulder)
reload(rigOrganizer)
reload(head)


def rigBiped():

	# generate groups to hold the rig
	rigStruct.createRigStructure()

	# limbs creation
	for side in ['L', 'R']:
		limb.Limb(startJoint=side + '_arm0_jnt', midJoint=side + '_arm1_jnt', endJoint=side + '_arm2_jnt',
				  ikFk=True, side=side, limbPart='arm')

		#limb.Limb(startJoint=side + '_hip_jnt', midJoint=side + '_knee_jnt', endJoint=side + '_ankle_jnt', ikFk=True, side=side, limbPart='leg')

		hand.Hand(handJoint=side + '_hand0_jnt', side=side)
		foot.Foot(footJnt=side + '_foot0_jnt', side=side)


	spine.Spine(startJoint='COG_jnt')


	for side in ['L', 'R']:
		shoulder.Shoulder(side=side)

	head.Head()
	rigOrganizer.organizeRig()
