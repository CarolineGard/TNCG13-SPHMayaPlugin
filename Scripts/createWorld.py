# createWorld.py

import maya.cmds as cmds
import random

#random.seed( 1234 )


# ****************************
# ---------- SETUP ----------
# ****************************

# ----- Create Particles -----


'''
particleList = cmds.ls( 'particle*' )
if len( particleList ) > 0:
    cmds.delete( particleList )
'''


result = cmds.polySphere( r=0.2, sx=1, sy=1, name='sphere#' )

p = result[0]

particleGroup = cmds.group( empty=True, name='particle_grp#' )

print particleGroup

for i in range( 0, 5 ):
    for j in range( 0, 5):
        for k in range( 0, 5 ):
            particleList = cmds.instance( p, name='particle#' )
            
            cmds.parent( particleList, particleGroup )
            
            cmds.move( i*0.5, j*0.5, k*0.5, particleList )
            
            # TODO: set collider
            # TODO: set material for particles

# Delete null sphere
cmds.select('sphere1')
cmds.delete()

#cmds.hide( transformName )
cmds.move ( 0 , 5 , 0, particleGroup )
cmds.xform( particleGroup, centerPivots=True )

# ----- Keyframes setup -----


#Set the playback options
cmds.playbackOptions(playbackSpeed = 0, maxPlaybackSpeed = 1)
cmds.playbackOptions(min = 1, max = 300)
cmds.currentTime(1)


# ----- Create Transparent Box -----

# Create the groundPlane
cmds.polyCube(w=5, h=2, d=5, sx=1, sy=1, sz=1, ax=(0, 1, 0), name='transpCube')
cmds.move(0, 1, 0)

# Delete top of cube
cmds.select( 'transpCube.f[1]' )
cmds.delete()

# Create a new rigid body solver
cmds.rigidSolver(create=True, name='rigidSolver1') 

# Set transpCube to passive rigid body (do the same for particle system)
cmds.select('transpCube')
cmds.rigidBody(passive=True, solver='rigidSolver1', pc=True, name='passiveRigidBody')
cmds.selectType(nr=True)

# Create transparent material for transparent box
cmds.select( 'transpCube' )
cmds.setAttr( 'lambert1.transparency', 0.922581, 0.922581, 0.922581, type = 'double3' )
cmds.setAttr( 'lambert1.refractions', 1 )
cmds.setAttr( 'lambert1.refractiveIndex', 1.52 )
cmds.setAttr( 'lambert1.color', 0.417, 0.775769, 1, type = 'double3' )

# Make Transparent box collider object
cmds.select( 'transpCube' )
mel.eval( 'makePassiveCollider' )



# ****************************
# -------- ANIMATION ---------
# ****************************
