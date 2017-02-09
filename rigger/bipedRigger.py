import pymel.core as pm
import rigger.limbClass as limb
import rigger.handClass as hand
import rigger.spineClass as spine
import rigger.footClass as foot
import rigger.shoulderClass as shoulder
import rigger.organize as rigOrganizer
import rigger.headClass as head
import rigger.createRigStructure as rigStruct

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
