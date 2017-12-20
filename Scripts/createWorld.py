# createWorld.py

import maya.cmds as cmds
import random


# ****************************
# ---------- SETUP ----------
# ****************************

# ----- Create Light -----

# Create ambient light

light = cmds.ambientLight(intensity=1.0)
cmds.ambientLight( light, e=True, ss=True, intensity=0.2, n='lightAmb')
cmds.move( 0, 8, 0 )

# Create directional light
light = cmds.directionalLight(rotation=(45, 30, 15), n='lightDir')
cmds.directionalLight( light, e=True, ss=True, intensity=0.0 )

# Query it
cmds.ambientLight( light, q=True, intensity=True )
cmds.directionalLight( light, q=True, intensity=True )


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

count=0
for i in range( 0, 8 ):
    for j in range( 0, 8 ):
        for k in range( 0, 8 ):
            count=count+1
            result = cmds.polySphere( r=0.15, sx=1, sy=1, name='particle#' )
            cmds.select('particle' + str(count))
            cmds.move(-i*0.35+0.75, 3+j*0.35, k*0.35-0.75,'particle' + str(count))

            cmds.sets( name='redMaterialGroup', renderable=True, empty=True )
            cmds.shadingNode( 'lambertian', name='redShader', asShader=True )
            cmds.setAttr( 'redShader.color', 0.0, 0.5333, 0.8, type='double3' )
            cmds.surfaceShaderList( 'redShader', add='redMaterialGroup' )
            cmds.sets( 'particle' + str(count), e=True, forceElement='redMaterialGroup' )


# ****************************
# -------- ANIMATION ---------
# ****************************
