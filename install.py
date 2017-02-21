import pymel.core as pm
import maya.cmds as cmds
import os
import sys

# add menu in the userSetup.py to load the menu every time maya runs
# get maya install documents path
userLocalScriptPath= cmds.internalVar(usd=True)


def add_menu():
	# Name of the global variable for the Maya window
	MainMayaWindow = pm.language.melGlobals['gMainWindow']
	# Build a menu and parent underthe Maya Window
	customMenu = pm.menu('Hero Autorig', parent=MainMayaWindow)
	# Build a menu item and parent under the 'customMenu'
	pm.menuItem(label="Add Biped character", command="printLine()", parent=customMenu)


usd = cmds.internalVar(usd=True)

try:
	userSetupFile = open(usd + 'userSetup.py')
	print ('\nuserSetup file found. Added Hero Autorig')

except IOError as e:
	print ('userSetup does not exists, creating one for you')

