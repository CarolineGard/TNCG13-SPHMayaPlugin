# createWorld.py

import maya.cmds as cmds
import random

#random.seed( 1234 )


# ****************************
# ---------- SETUP ----------
# ****************************

# ----- Create Transparent Box -----

# Create the groundPlane
cmds.polyCube(w=5, h=2, d=5, sx=1, sy=1, sz=1, ax=(0, 1, 0), name='transpCube')
cmds.polyNormal( nm=0 ) #change normals

# Delete top of cube
cmds.select( 'transpCube.f[1]' )
cmds.delete()

# Create transparent material for transparent box
cmds.select( 'transpCube' )
cmds.setAttr( 'lambert1.transparency', 0.922581, 0.922581, 0.922581, type = 'double3' )
cmds.setAttr( 'lambert1.refractions', 1 )
cmds.setAttr( 'lambert1.refractiveIndex', 1.52 )
cmds.setAttr( 'lambert1.color', 0.417, 0.775769, 1, type = 'double3' )

cmds.select('transpCube')
cmds.rigidBody(passive=True, solver='rigidSolver', name='passiveRigidBody')



# ----- Create Particles -----

'''
particleList = cmds.ls( 'particle*' )
if len( particleList ) > 0:
    cmds.delete( particleList )
'''

count=0
for i in range( 0, 2 ):
    for j in range( 0, 2):
        for k in range( 0, 2 ):
            count=count+1

            result = cmds.polySphere( r=0.2, sx=1, sy=1, name='sphere#' )
            
            cmds.rigidSolver(create=True, name='rigidSolver')
            # Set the ball to active rigid body
            cmds.select('sphere' + str(count))
            cmds.rigidBody(active=True, solver='rigidSolver', name='activeRigidBody#')
            # Add a gravity field, and connect it to ball
            cmds.gravity(pos=(0, 0, 0), m=9.8, dx=0, dy=-1, dz=0, name='gravityField')
            cmds.connectDynamic('activeRigidBody' + str(count), f='gravityField')
            cmds.rigidSolver('rigidSolver', e=True, bounciness=False)
            cmds.move(-i*0.5,5+j*0.5,k*0.5,'sphere' + str(count))
            cmds.rigidSolver('rigidSolver', e=True, bounciness=True)
            cmds.rigidSolver('passiveRigidBody', 'activeRigidBody' + str(count), 'rigidSolver1', e=True, interpenetrate=True)



#cmds.xform( particleGroup, centerPivots=True )

# ----- Keyframes setup -----


#Set the playback options
cmds.playbackOptions(playbackSpeed = 0, maxPlaybackSpeed = 1)
cmds.playbackOptions(min = 1, max = 100)
cmds.currentTime(1)



# ****************************
# -------- ANIMATION ---------
# ****************************
