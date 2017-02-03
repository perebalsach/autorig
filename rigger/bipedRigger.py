import pymel.core as pm
import pb_autorig.rigger.limbClass as limb
import pb_autorig.rigger.HandClass as hand
import pb_autorig.rigger.SpineClass as spine
import pb_autorig.rigger.FootClass as foot
import pb_autorig.rigger.ShoulderClass as shoulder
import pb_autorig.rigger.Organize as rigOrganizer
import pb_autorig.rigger.HeadClass as head
import pb_autorig.rigger.createRigStructure as rigStruct

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
		limb.Limb(startJoint=side + '_shoulder_jnt', midJoint=side + '_elbow_jnt', endJoint=side + '_hand_jnt',
				  ikFk=True, side=side, limbPart='arm')

		limb.Limb(startJoint=side + '_hip_jnt', midJoint=side + '_knee_jnt', endJoint=side + '_ankle_jnt', ikFk=True,
				  side=side, limbPart='leg')

		hand.Hand(handJoint=side + '_hand_jnt', side=side)
		foot.Foot(footJnt=side + '_ankle_jnt', side=side)

	spine.Spine(startJoint='COG_jnt')


	for side in ['L', 'R']:
		shoulder.Shoulder(side=side)

	head.Head()
	rigOrganizer.organizeRig()

rigBiped()
