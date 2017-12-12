# SPHSimulation.py

import maya.cmds as cmds
import maya.mel as mel    

# Run mel file for creating particles
# Solve: Read mel file from python or create particle fill 
 
 
# ----- SETUP -----


#Set the playback options
cmds.playbackOptions(playbackSpeed = 0, maxPlaybackSpeed = 1)
cmds.playbackOptions(min = 1, max = 300)
cmds.currentTime(1)

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

# Remove maya-initialised values for nParticle
cmds.select( 'nParticle1' )
cmds.setAttr( 'nParticleShape1.ignoreSolverGravity', 1)
cmds.setAttr( 'nParticleShape1.particleRenderType', 4)     #sets particle to being spheres
cmds.setAttr( 'nParticleShape1.bounce', 0)
cmds.setAttr( 'nParticleShape1.friction', 0)
cmds.setAttr( 'nParticleShape1.selfCollide', True)

# Color the particles
cmds.setAttr( 'nParticleShape1.color[0].color_Color', 0.3, 0.657, 0.657, type = 'double3' )
cmds.setAttr( 'nParticleShape1.color[1].color_Color', 0.3, 0.657, 0.657, type = 'double3' )



# ---- FORCES -----



# create gravity and attatch to particles
cmds.gravity( 'nParticle1', n= 'gravity' ) 
cmds.setAttr( 'gravity.attenuation', 1)
cmds.connectDynamic( 'nParticle1', f ='gravity')

'''
cmds.rigidBody( n='myRigidBody', active=True, iv=(10, 0, 0), b=0.5, sf=0.4 )
cmds.connectDynamic( 'nParticle1', f ='myRigidBody')
'''



































