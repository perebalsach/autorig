import pymel.core as pm
import maya.mel as mel


def createRigControl(ctrlType, size=1):
	"""
	create rig control curves

	:param ctrlType: string
	:return: string - name of the control
	"""

	if ctrlType == 'COG':
		ctrlCrv =mel.eval('string $cog=`curve -d 3 -p 7.06316e-009 0 -1 -p 0.104714 0 -0.990425 -p 0.314142 0 -0.971274 '
				 '-p 0.597534 0 -0.821244 -p 0.822435 0 -0.597853 -p 0.96683 0 -0.314057 -p 1.016585 0 -2.28604e-005 '
				 '-p 0.96683 0 0.314148 -p 0.822435 0 0.597532 -p 0.597534 0 0.822435 -p 0.314142 0 0.96683 '
				 '-p 1.22886e-008 0 1.016585 -p -0.314142 0 0.96683 -p -0.597534 0 0.822435 -p -0.822435 0 0.597532 '
				 '-p -0.96683 0 0.314148 -p -1.016585 0 -2.29279e-005 -p -0.96683 0 -0.314057 -p -0.822435 0 -0.597853 '
				 '-p -0.597534 0 -0.821244 -p -0.314142 0 -0.971274 -p -0.104714 0 -0.990425 -p 7.06316e-009 0 -1 -k 0 '
				 '-k 0 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16 -k 17'
				 ' -k 18 -k 19 -k 20 -k 20 -k 20 -n helperCog`;')
		mel.eval('select -r $cog.ep[1] $cog.ep[3] $cog.ep[5] $cog.ep[7] $cog.ep[9] $cog.ep[11] $cog.ep[13] $cog.ep[15] '
				 '$cog.ep[17] $cog.ep[19];')
		mel.eval('scale -r -p 0cm 0cm 0cm 0.732056 0.732056 0.732056 ;')
		mel.eval('select -cl;')
		mel.eval('select $cog')
		mel.eval('scale 0.5 0.5 0.5')
		pm.makeIdentity(a=True, s=True)

		return ctrlCrv

	elif ctrlType == 'cube':
		ctrlCrv = mel.eval('curve -d 1 -p 0.5 0.5 0.5 -p 0.5 0.5 -0.5 -p -0.5 0.5 -0.5 -p -0.5 -0.5 -0.5 '
						   '-p 0.5 -0.5 -0.5 -p 0.5 0.5 -0.5 -p -0.5 0.5 -0.5 -p -0.5 0.5 0.5 -p 0.5 0.5 0.5 '
						   '-p 0.5 -0.5 0.5 -p 0.5 -0.5 -0.5 -p -0.5 -0.5 -0.5 -p -0.5 -0.5 0.5 -p 0.5 -0.5 0.5 '
						   '-p -0.5 -0.5 0.5 -p -0.5 0.5 0.5 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10'
						   '-k 11 -k 12 -k 13 -k 14 -k 15 -n "controller_ik" ;')
		return ctrlCrv

	elif ctrlType == 'circle':
		ctrlCrv = pm.circle(name='ctrl', nr=(1,0,0), r=0.18)[0]

		return ctrlCrv

	elif ctrlType == 'sphere':
		ctrlCrv = mel.eval('curve -d 1 -p 0 0 1 -p 0 0.5 0.866025 -p 0 0.866025 0.5 -p 0 1 0 -p 0 0.866025 -0.5 '
						   '-p 0 0.5 -0.866025 -p 0 0 -1 -p 0 -0.5 -0.866025 -p 0 -0.866025 -0.5 -p 0 -1 0 '
						   '-p 0 -0.866025 0.5 -p 0 -0.5 0.866025 -p 0 0 1 -p 0.707107 0 0.707107 -p 1 0 0 '
						   '-p 0.707107 0 -0.707107 -p 0 0 -1 -p -0.707107 0 -0.707107 -p -1 0 0 -p -0.866025 0.5 0 '
						   '-p -0.5 0.866025 0 -p 0 1 0 -p 0.5 0.866025 0 -p 0.866025 0.5 0 -p 1 0 0 '
						   '-p 0.866025 -0.5 0 -p 0.5 -0.866025 0 -p 0 -1 0 -p -0.5 -0.866025 0 -p -0.866025 -0.5 0 '
						   '-p -1 0 0 -p -0.707107 0 0.707107 -p 0 0 1 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 '
						   '-k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16 -k 17 -k 18 -k 19 -k 20 -k 21 -k 22 -k 23'
						   '-k 24 -k 25 -k 26 -k 27 -k 28 -k 29 -k 30 -k 31 -k 32 -n "ctrl" ;')
		return ctrlCrv

	elif ctrlType == 'poleVector':
		ctrlCrv = mel.eval('curve -d 1 -p 0.5 -1 0.866025 -p -0.5 -1 0.866025 -p 0 1 0 -p 0.5 -1 0.866025 -p 1 -1 0 '
						   '-p 0 1 0 -p 0.5 -1 -0.866025 -p 1 -1 0 -p 0 1 0 -p -0.5 -1 -0.866026 -p 0.5 -1 -0.866025'
						   '-p 0 1 0 -p -1 -1 -1.5885e-007 -p -0.5 -1 -0.866026 -p 0 1 0 -p -0.5 -1 0.866025 '
						   '-p -1 -1 -1.5885e-007 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 '
						   '-k 12 -k 13 -k 14 -k 15 -k 16 -n poleVector_ctrl;')
		pm.scale(ctrlCrv, (0.05, 0.05, 0.05))
		pm.rotate(ctrlCrv, (90,0,0))
		pm.makeIdentity(a=True, r=True, s=True)

		return ctrlCrv

	elif ctrlType == 'cross':
		ctrlCrv = mel.eval('curve -d 1 -p 2 0 1 -p 2 0 -1 -p 1 0 -1 -p 1 0 -2 -p -1 0 -2 -p -1 0 -1 -p -2 0 -1 -p -2 0 1 '
				 '-p -1 0 1 -p -1 0 2 -p 1 0 2 -p 1 0 1 -p 2 0 1 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 '
				 '-k 10 -k 11 -k 12 -n "controller_ik" ;')

		pm.scale(ctrlCrv, (0.5, 0.5, 0.5))
		pm.makeIdentity(a=True, s=True)

		return ctrlCrv

	elif ctrlType == 'foot':
		ctrlCrv = mel.eval('curve -d 1 -p -0.081122 0 -1.11758 -p 0.390719 0 -0.921584 -p 0.514124 0 -0.616704 '
				 '-p 0.412496 0 0.0293557 -p 0.86256 0 0.552008 -p 0.920632 0 1.161772 -p 0.775452 0 1.669908 '
				 '-p 0.38346 0 2.011088 -p -0.131936 0 2.330484 -p -0.552964 0 2.308708 -p -0.654588 0 1.691688 '
				 '-p -0.57474 0 0.63912 -p -0.364226 0 0.109206 -p -0.531184 0 -0.39893 -p -0.465852 0 -0.841736 '
				 '-p -0.081122 0 -1.11758 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 '
				 '-k 14 -k 15 -n "_foot_ctrl" ;')
		pm.scale(ctrlCrv, (0.25, 0.25, 0.25))
		pm.makeIdentity(ctrlCrv, a=True, s=True)

		# place the pivot at the back
		bbox = pm.exactWorldBoundingBox(ctrlCrv)
		bottom = [(bbox[0]/8.0), bbox[1], bbox[2]]
		pm.xform(ctrlCrv, piv=bottom, ws=True)

		# move the ctrl to 0,0,0 and freeze transfroms
		pm.move(ctrlCrv, (0.02,0,0.279))
		pm.makeIdentity(ctrlCrv, a=True, t=True)

		return ctrlCrv

	elif ctrlType == 'pin':
		ctrlCrv = mel.eval('curve -d 1 -p 0 0 0 -p -2 0 0 -p -2.292893 0 0.707107 -p -3 0 1 -p -3.707107 0 0.707107 '
						   '-p -4 0 0 -p -3.707107 0 -0.707107 -p -3 0 -1 -p -2.292893 0 -0.707107 -p -2 0 0 '
						   '-p -2.292893 0 0.707107 -p -3.707107 0 -0.707107 -p -4 0 0 -p -3.707107 0 0.707107 '
						   '-p -2.292893 0 -0.707107 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12'
						   '-k 13 -k 14 -n "pinCtrl";')
		pm.scale(ctrlCrv, (0.1,0.1,0.1))
		pm.makeIdentity(a=True, s=True)

		return ctrlCrv

	else:
		print('---> Debug: Cannot create ctrl based on the given name: %s' %ctrlType)
		print('---> Debug: accepted types: foot, cross, poleVector, pin, sphere, circle, cube')
		#pm.warning(m='cannot create ctrl based on the given name')

	pm.scale(ctrlCrv, (size, size, size))
	pm.makeIdentity(a=True, s=True)


def setControlColor(ctrl):
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


def hideAttributes(ctrl, trans, scale, rot, vis, radius):
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