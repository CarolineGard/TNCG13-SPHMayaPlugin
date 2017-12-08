# calculateForces.py

import maya.cmds as cmds
import maya.mel as mel
import math

# ------ FUNCTIONS ------

# Set Keyframes
def setNextKeyParticle( pName, pKeyStart, pTargetAttribute, pValue, pDt ):
    

    keyNext = pStartKey + pDt
    
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

#nPosition = new position of one particle 
def weightFunction( pPosition, pH ): #H = 0.1
    
    q = ( pPosition )/pH
    
    return ( 1.0/( 3.14*pH*pH*pH ))*( 1.0-1.5*q*q + 0.75*q*q*q )



def calculateDensity( pPosition, pList, pH, pMass ):
    
    density = 0 
 
    for i in range( 0, len( pList ) ):
        density += pMass * weightFunction( abs( pPosition - cmds.getParticleAttr( pList[i], at = 'position' ) ), pH )
    
    return density
    

    
def calculatePressure( pList ):
    pressure = 0
    
    return pressure

def calculateViscosity( pList ):
    viscosity = 0
    
    return viscosity
    
    
    
def calculateNewPosition( pPosition, pDensity, pMass, pDt ):
    newPosition = ( 0, 0, 0 )
    
    velocity = pDensity / pMass #kanske multiplicerat med pDt
    
    newPosition = ( velocity * pDt ) + pPosition
    
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
h = .3
mass = cmds.getParticleAttr( 'nParticle1', at = 'mass' )
# send mass[0]

# stepLenght
dt = .1


# ------ ANIMATION LOOP ------
for i in range(0, 40):
    
    # Per every time step h
    for i in range(100):    #1330
    
        # Get neighbor list for the current particle
        nList = findNeighbours( 'nParticle1.pt[' + str(i) + ']', h )
        
        
        currentPosition = cmds.getParticleAttr( 'nParticle1.pt[' + str(i) + ']', at = 'position' )
        
        # Calculate Forces  
        F = calculateDensity( currentPosition, nList, h, mass )
        
        # Calculate new position of particles 
        nextPosition = calculateNewPosition( currentPosition, F, mass, dt )
        
        
        # Set next keyFrame 
        setNextKeyParticle( 'nParticle1', startTime, endTime, 'rotateY', 360 )
  
  
# TESTING ERROR
# unsupported operand type(s) for -: 'list' and 'list' #  
nList = findNeighbours( 'nParticle1.pt[' + str(0) + ']', h )  
print nList
hej = cmds.getParticleAttr( pList[i], at = 'position' )
print hej





#cmds.setKeyframe(obj + '.translateX', value=xVal, time=frame)
































