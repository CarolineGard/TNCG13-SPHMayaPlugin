# calculateForces.py

import maya.cmds as cmds
import maya.mel as mel
import math

# ------ FUNCTIONS ------

# Set Keyframes
def setNextKeyParticle( pName, pKeyStart, pTargetAttribute, pValue ):
    
    # stepLenght
    h = .1
    keyNext = pStartKey + h
    
    # clear selection list and select all particles
    cmds.select( clear=True )
    
    # cmds.cutKey( pName, time=( pStartKey, endTime ), attribute=pTargetAttribute )

    # create animation, set startkeyframe, startvalue=0 at first key frame. Make linear keyframes
    cmds.setKeyframe( pName, time=keyNext, attribute=pTargetAttribute, value=0 )
    # cmds.setKeyframe( pName, time=pEndKey, attribute=pTargetAttribute, value=pValue ) 
    cmds.selectKey( pName, time=( pStartKey, pEndKey ), attribute=pTargetAttribute, keyframe=True )
    cmds.keyTangent( inTangentType='linear', outTangentType='linear' )


# Function returnig array of neighbouring particles with smoothing length
def findNeighbours( pParticle, pSmoothLength ):
    neighbourList = []
    p1_pos = cmds.getParticleAttr( pParticle, at='position' )
    
    for i in range(1330):
        
        p2_pos = cmds.getParticleAttr( 'nParticle1.pt[' + str(i) + ']', at='position' )
        
        # Calculate distance 
        dx = p1_pos[0] - p2_pos[0]
        dy = p1_pos[1] - p2_pos[1]
        dz = p1_pos[2] - p2_pos[2]
        
        distance = math.sqrt( math.pow(dx, 2) + math.pow(dy, 2) + math.pow(dz, 2) )
    
        # if distance <= psmoothLength, put in array
        if distance <= pSmoothLength and distance > 0: 
            neighbourList.append( 'nParticle1.pt[' + str(i) + ']' )
    
    return neighbourList


def calculateVelocity( pList ):
    velocity = ( 0, 0, 0 )
    
    return velocity
    
def calculateDensity( pList ):
    density = 0 
    
    return density
    
def calculatePressure( pList ):
    pressure = 0
    
    return pressure

def calculateViscosity( pList ):
    viscosity = 0
    
    return viscosity
    
def calculateNewPosition( pVelocity, pDensity, pPressure, pViscosity, pPosition ):
    newPosition = ( 0, 0, 0 )
    
    return newPosition
    

# ******************************************************#
# ------ MAIN ------
# ******************************************************#


# Read Mel-file
# Read Python-file

# Playback options
cmds.playbackOptions( playbackSpeed=0, maxPlaybackSpeed=1 )
cmds.playbackOptions( min=1, max=120 )
startTime = cmds.playbackOptions( query=True, minTime=True )
endTime = cmds.playbackOptions( query=True, maxTime=True )


  
# Calculate smoothing Lenght
smoothL = .3


# ------ ANIMATION LOOP ------
for i in range(0, 40):
    
    # Per every time step h
    for i in range(100):    #1330
    
        # Get neighbor list for the current particle
        nList = findNeighbours( 'nParticle1.pt[' + str(i) + ']', smoothL )
        
        
        # Calculate Forces  
        
        # Calculate new position of particles 
         
        setNextKeyParticle( 'nParticle1', startTime, endTime, 'rotateY', 360 )
    

#cmds.setKeyframe(obj + '.translateX', value=xVal, time=frame)
































    