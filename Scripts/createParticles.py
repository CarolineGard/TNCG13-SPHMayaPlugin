# particles.py

import maya.cmds as cmds
import random

#random.seed( 1234 )

'''
particleList = cmds.ls( 'particle*' )
if len( particleList ) > 0:
    cmds.delete( particleList )
'''

result = cmds.polySphere( r=0.3, sx=1, sy=1, name='particle#' )

#print 'result: ' + str( result )

transformName = result[0]

instanceGroupName = cmds.group( empty=True, name=transformName + '_instance_grp#' )

for i in range( 0, 10 ):
    for j in range( 0, 10 ):
        for k in range( 0, 10 ):
            instanceResult = cmds.instance( transformName, name=transformName + '_instance#' )
            
            cmds.parent( instanceResult, instanceGroupName )
            
            #print 'instanceResult: ' + str( instanceResult )
            
            x = random.uniform(-10, 10 )
            y = random.uniform( 10, 10 )
            z = random.uniform( -10, 10 )
            
            cmds.move( i, j, k, instanceResult )




#cmds.hide( transformName )
cmds.move ( -5 , -5 , 20, instanceGroupName )
cmds.xform( instanceGroupName, centerPivots=True )


