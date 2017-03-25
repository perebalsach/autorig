from utils.pyside_dynamic import loadUi
from PySide import QtCore, QtGui

import builder.bipedBuilder as bipBuild


class Autorigger(QtGui.QDialog):
	def __init__(self):
		super(Autorigger, self).__init__()
		self.ui = loadUi('/Users/perebalsach/Documents/projects/maya/autorig/ui/autorigUi.ui', self)

	@QtCore.Slot()
	def loadBipedSlot(self):
		numSpineJoints = self.ui.sbNumSpineJoints.value()
		characterName = self.ui.lineEditCharName.text()
		bipBuild.build(spine_sections=int(numSpineJoints))

	@QtCore.Slot()
	def rigSlot(self):
		pass



try:
	ui.deleteLater()
except:
	pass

ui = Autorigger()

try:
	ui.show()
except:
	ui.deleteLater()


