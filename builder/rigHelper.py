import pymel.core as pm


class RigHelperClass(object):

	""" class for building manipulator prior joint creation """

	def __init__(self, name='_', size=1, pos=(0, 0, 0)):

		"""
		:param name: str, name of the manipulator
		:param size: int, size of the manipulator
		:param pos: list(float), position for the manipulator
		"""


		# create cube and the locator
		self.obj = pm.polyCube(name=name + '_rigHelper', h=size, w=size, d=size)[0]

		# set the overrides color for the cube
		# based on the side
		if 'L' in name:
			self.obj.setAttr('overrideColor', 6)
		elif 'R' in name:
			self.obj.setAttr('overrideColor', 13)
		elif 'M' in name:
			self.obj.setAttr('overrideColor', 17)

		self.obj.setAttr('overrideEnabled', 1)
		self.obj.setAttr('overrideShading', 0)
		self.obj.setAttr('displayHandle', 1)

		# sets the position
		self.obj.setTranslation(pos)

	def getPos(self):
		return self.obj.getTranslation()

	def setPos(self, pos=None):
		return self.obj.setTranslation(pos)

	def setName(self, new_name=''):
		self.obj.rename(new_name)
		return self.obj

	def name(self):
		return self.obj.name()

	def setParent(self, target):
		return pm.parent(self.obj, target)

	def setChild(self, target):
		return pm.parent(target, self.obj)

	def setSize(self, size=None):
		return self.obj.scale(size)
