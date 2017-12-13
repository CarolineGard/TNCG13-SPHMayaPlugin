# calculateForcesSpheres.py

import maya.cmds as cmds
import maya.mel as mel
import math

# ------ FUNCTIONS ------


# Set Keyframes
def setNextKeyParticle( pName, pKeyStart, pTargetAttribute, pValue ):
    
    # keyNext = pKeyStart + pDt
    keyNext = pKeyStart
    
    # clear selection list and select all particles
    cmds.select( clear=True )


    # create animation, set startkeyframe, startvalue=0 at first key frame. Make linear keyframes
    cmds.setKeyframe( pName, time=keyNext, attribute=pTargetAttribute, value=pValue )
    
    # cmds.setKeyframe( pName, time=pEndKey, attribute=pTargetAttribute, value=pValue ) 
    cmds.selectKey( pName, time=( pKeyStart, keyNext ), attribute=pTargetAttribute, keyframe=True )
    cmds.keyTangent( inTangentType='linear', outTangentType='linear' )
   



# Function returnig array of neighbouring particles with smoothing length
def findNeighbours( pParticle, pSmoothLength ):
    neighbourList = []
    p1_pos = cmds.getParticleAttr( pParticle, at='position' )
    
    # 1331
    for i in range(20):
        
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

'''
#nPosition = new position of one particle 
#H = 0.1
def weightFunction( pPosition, pH ): 
    
    q = ( pPosition )/pH
    
    return ( 1.0/( 3.14*pH*pH*pH ))*( 1.0-1.5*q*q + 0.75*q*q*q )



def calculateDensity( pPosition, pList, pH, pMass ):
    
    density = 0 
 
    for i in range( 0, len( pList ) ):
        neighbourPosition = cmds.getParticleAttr( pList[i], at = 'position' )
        difference = [pPosition[j]-neighbourPosition[j] for j in xrange(min(len(pPosition), len(neighbourPosition)))]
        distance = math.sqrt( pow(difference[0],2) + pow(difference[1],2) + pow(difference[2],2) )
        density += pMass[0] * weightFunction( distance, pH )
    
    return density
    
    
def calculatePressure( pList ):
    pressure = 0
    
    return pressure

def calculateViscosity( pList ):
    viscosity = 0
    
    return viscosity
    
    
    
def calculateNewPosition( pPosition, pDensity, pMass, pDt ):
    
    newPosition = [ 0, 0, 0 ]
    velocity = pDensity / pMass[0] #kanske multiplicerat med pDt
    #Ska velocity vara float eller vector??????????????????????????????????????

    newPosition[0] = ( velocity * pDt ) + pPosition[0]
    newPosition[1] = ( velocity * pDt ) + pPosition[1]
    newPosition[2] = ( velocity * pDt ) + pPosition[2]
    
    return newPosition
'''

# ******************************************************#
# ------ MAIN ------
# ******************************************************#


# Playback options
cmds.playbackOptions( playbackSpeed=0, maxPlaybackSpeed=1 )
cmds.playbackOptions( min=1, max=120 )
startTime = cmds.playbackOptions( query=True, minTime=True )
endTime = cmds.playbackOptions( query=True, maxTime=True )

  
# Calculate smoothing Lenght
h = .3
mass = 0.1
G = 9.82

# stepLenght
dt = 10

time = startTime
# cmds.select('particle100')


# Set first Keyframe for all partices

for i in range (1, 126):
    # Current position for each particle 
    pos = cmds.getAttr( 'particle'+str(i)+'.translateY' )
    
    setNextKeyParticle( 'particle'+str(i), time, 'translateY', pos)


for j in range (1, 10):
    time += dt
    for i in range (1, 126):
        # Calculate forces
        v = -(G/100)*time
        
        # Set keyframes
        cmds.select( 'particle'+str(i) )
        setNextKeyParticle( 'particle'+str(i), time, 'translateY', v )















