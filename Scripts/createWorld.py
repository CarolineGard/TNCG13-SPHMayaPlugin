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


# ----- Create Particles -----

'''
particleList = cmds.ls( 'particle*' )
if len( particleList ) > 0:
    cmds.delete( particleList )
'''

count=0
for i in range( 0, 2 ):
    for j in range( 0, 2):
        for k in range( 0, 3 ):
            count=count+1
            result = cmds.polySphere( r=0.2, sx=1, sy=1, name='particle#' )
            cmds.select('particle' + str(count))
            cmds.move(-i*0.5,5+j*0.5,k*0.5,'particle' + str(count))


#cmds.xform( particleGroup, centerPivots=True )

# ----- Keyframes setup -----


#Set the playback options
cmds.playbackOptions(playbackSpeed = 0, maxPlaybackSpeed = 1)
cmds.playbackOptions(min = 1, max = 100)
cmds.currentTime(1)



# ****************************
# -------- ANIMATION ---------
# ****************************
