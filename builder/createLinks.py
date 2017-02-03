import pymel.core as pm

class Create(object):

	def __init__(self, source='', target='', name=''):
		"""
		Create a visual link between the source and the target rigHelpers to further connect the rig joints

		:param source: PyNode object
		:param target: PyNode object
		:param name: str - Name of the curve link
		:return: None
		"""
		self.source = source
		self.target= target
		self.link_name = name

		print ('Source: %s ' % self.source)
		print ('Target: %s ' % self.target)

		self._link(sourceObj=self.source, targetObj=self.target, base_name=name)

	def _link(self, sourceObj=None, targetObj=None, base_name=''):

		sourcePos = sourceObj.getTranslation('world')
		targetPos = targetObj.getTranslation('world')

		link_crv = pm.curve(name= base_name + '_linkCrv', d=1, p=(targetPos, sourcePos))
		pm.setAttr(link_crv + '.overrideEnabled', 1)
		pm.setAttr(link_crv + '.overrideColor', 18)

		# add custom attribute to write the connection
		pm.addAttr(link_crv, ln='linked_source', dt='string')
		pm.addAttr(link_crv, ln='linked_target', dt='string')
		pm.setAttr(link_crv + '.linked_source', self.source)
		pm.setAttr(link_crv + '.linked_target', self.target)

		pm.select(deselect=True)

	def getLinks(self):
		return self.source, self.target

	def getPositions(self):
		return self.source.getTranslation('world'), self.target.getTranslation('world')

"""
Create(pm.PyNode('L_arm0_rigHelper'),pm.PyNode('M_spine3_rigHelper'), 'dsds')
Create(pm.PyNode('L_leg_0_rigHelper'),pm.PyNode('M_spine5_rigHelper'), 'ssss')
"""