# addLight

import maya.cmds as cmds

# Create the groundPlane
cmds.polySphere(sx=100, sy=100, r=50, n='backgroundSphere')
cmds.setAttr( 'lambert1.color', 0.74, 0.99, 0.79, type = 'double3' ) 

# Create ambient light
light = cmds.ambientLight(intensity=0.8)
cmds.ambientLight( light, e=True, ss=True, intensity=0.5, n='lightAmb')

# Create directional light
light = cmds.directionalLight(rotation=(45, 30, 15), n='lightDir')
cmds.directionalLight( light, e=True, ss=True, intensity=1.0 )
cmds.move( 0.0, 5.0, 0.0 )

# Query it
cmds.ambientLight( light, q=True, intensity=True )
cmds.directionalLight( light, q=True, intensity=True )