imoprt pymel.croe as pm

spineJntList  = ['_spine0_jnt', '_spine1_jnt', '_spine2_jnt', '_neck0_jnt', '_head0_jnt', '_head1_jnt']
legJntList    = ['_leg0_jnt', '_leg1_jnt', '_leg2_jnt']
footJntList   = ['_foot_jnt_FK', '_ball_jnt_FK', '_toe_jnt_FK']
armJntList    = ['_shoulderRoot_jnt', '_arm0_jnt', '_arm1_jnt', '_arm2_jnt']
handJntList   = ['_hand0_jnt', '_hand1_jnt']


def createBindJnts(jntList, baseName, side):
    pm.select(deselect=True)
    for i in range(len(jntList)):
        jntNode = pm.PyNode(side + jntList[i])
        jntPos = jntNode.getTranslation('world')
        newJnt = pm.joint(name=side + '_' + baseName + str(i) + '_bind_jnt', p=(jntPos[0], jntPos[1], jntPos[2]), rad=2)
        pm.pointConstraint(side + jntList[i], newJnt)
        pm.orientConstraint(side + jntList[i], newJnt)


createBindJnts(jntList=spineJntList, baseName='spìnes', side='M')
for side in ['L', 'R']:
    createBindJnts(jntList=armJntList, baseName='arms', side=side)
    createBindJnts(jntList=footJntList, baseName='foots', side=side)
    createBindJnts(jntList=footJntList, baseName='legs', side=side)
    createBindJnts(jntList=handJntList, baseName='hands', side=side)
    createBindJnts(jntList=legJntList, baseName='legs', side=side)
