# Create a transparent box

import maya.cmds as cmds

# Run mel file for creating particles
# Solve: Read mel file from python or create particle fill 

# Delete Cube created in mel file
cmds.select( 'cubeFill' )
cmds.delete()

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
cmds.rigidBody(passive=True, solver='rigidSolver1', name='passiveRigidBody')

# Create transparent material for transparent box
cmds.select( 'transpCube' )
cmds.setAttr( 'lambert1.transparency', 0.922581, 0.922581, 0.922581, type = 'double3' )
cmds.setAttr( 'lambert1.refractions', 1 )
cmds.setAttr( 'lambert1.refractiveIndex', 1.52 )
cmds.setAttr( 'lambert1.color', 0.417, 0.775769, 1, type = 'double3' )
