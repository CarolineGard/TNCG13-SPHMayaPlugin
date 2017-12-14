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
def findNeighbours( pParticleX, pParticleY, pParticleZ , pSmoothLength ):
    
    neighbourList = []
    
    # 1331
    for i in range(1,8):
        
        posX = cmds.getAttr( 'particle'+str(i)+'.translateX' )
        posY = cmds.getAttr( 'particle'+str(i)+'.translateY' )
        posZ = cmds.getAttr( 'particle'+str(i)+'.translateZ' )
        
        # Calculate distance 
        dx = posX - pParticleX
        dy = posY - pParticleY
        dz = posZ - pParticleZ
        
        distance = math.sqrt( math.pow(dx, 2) + math.pow(dy, 2) + math.pow(dz, 2) )
    
        # if distance <= psmoothLength, put in array
        if distance <= pSmoothLength and distance > 0: 
            neighbourList.append( 'particle'+str(i) )
    
    return neighbourList

#nPosition = new position of one particle 
#H = 0.1
def weightFunction( pParticle, pH ): 
    
    q = ( pParticle )/pH
    
    w = ( 1.0/( 3.14*pH*pH*pH ))*( 1.0-1.5*q*q + 0.75*q*q*q )

    return w



def calculateDensity( pParticleX, pParticleY, pParticleZ, pList, pH, pMass ):
    
    densityX = densityY = densityZ = 0
 
    for i in range( 0, len( pList ) ):
        
        neighbourPositionX = cmds.getAttr( pList[i]+'.translateX' )
        neighbourPositionY = cmds.getAttr( pList[i]+'.translateY' )
        neighbourPositionZ = cmds.getAttr( pList[i]+'.translateZ' )
        
        dx = abs( pParticleX - neighbourPositionX )
        dy = abs( pParticleY - neighbourPositionY )
        dz = abs( pParticleZ - neighbourPositionZ )
        
        # distance = math.sqrt( math.pow(dx, 2) + math.pow(dy, 2) + math.pow(dz, 2) )
        
        densityX += pMass * weightFunction( dx, pH )
        densityY += pMass * weightFunction( dy, pH )
        densityZ += pMass * weightFunction( dz, pH )
    
    return [ densityX, densityY, densityZ ]
 
'''
 
def calculatePressure( pList ):
    pressure = 0
    
    return pressure
    

def calculateViscosity( pList ):
    viscosity = 0
    
    return viscosity
    
'''

def calculateNewPosition( pPositionX, pPositionY, pPositionZ, pDensity, pMass, pDt ):
     
   
    
    #density and velocity = 0 at the moment
    
    nPosition = [ 0, 0, 0 ]
    velocityX = pDensity[0] / pMass 
    velocityY = pDensity[1] / pMass
    velocityZ = pDensity[2] / pMass
    

    #kanske multiplicerat med pDt
    #Ska velocity vara float eller vector??????????????????????????????????????

    nPosition[0] = ( velocityX * pDt ) + pPositionX
    nPosition[1] = ( velocityY * pDt ) + pPositionY
    nPosition[2] = ( velocityZ * pDt ) + pPositionZ
    
    
    #Boundary conditions
    Xmin = -2.5
    Xmax = 2.5
    Ymin = -1
    Zmin = -2.5
    Zmax = 2.5
       
    if ( nPosition[0] < Xmin or nPosition[0] > Xmax ):
        print 'X'
        velocityX = (-1) * velocityX
        nPosition[0] = pPositionX
        
    if ( nPosition[1] < Ymin ):
        print 'Y'
        velocityY = (-1) * velocityY
        nPosition[1] = pPositionY
        
    if ( nPosition[2] < Zmin or nPosition[2] > Zmax ):
        print 'Z'
        velocityZ = (-1) * velocityZ
        nPosition[2] = pPositionZ  
    
    return nPosition

def calculateBoundaries( pPositionX, pPositionY, pPositionZ, pvelocity ):
    
    
    return





# ******************************************************#
# ------ MAIN ------
# ******************************************************#


# Playback options
cmds.playbackOptions( playbackSpeed=0, maxPlaybackSpeed=1 )
cmds.playbackOptions( min=1, max=120 )
startTime = cmds.playbackOptions( query=True, minTime=True )
endTime = cmds.playbackOptions( query=True, maxTime=True )

  
# Calculate smoothing Lenght
h = 1
mass = 0.1
G = 9.82

# stepLenght
dt = 10

time = startTime
# cmds.select('particle100')


# Set first Keyframe for all partices

for i in range (1,8):
    # Current position for each particle 
    posX = cmds.getAttr( 'particle'+str(i)+'.translateX' )
    posY = cmds.getAttr( 'particle'+str(i)+'.translateY' )
    posZ = cmds.getAttr( 'particle'+str(i)+'.translateZ' )
    
    setNextKeyParticle( 'particle'+str(i), time, 'translateX', posX )
    setNextKeyParticle( 'particle'+str(i), time, 'translateY', posY )
    setNextKeyParticle( 'particle'+str(i), time, 'translateZ', posZ )


for j in range (1, 10):
    time += dt
    for i in range (1, 9):
        
        posX = cmds.getAttr( 'particle'+str(i)+'.translateX' )
        posY = cmds.getAttr( 'particle'+str(i)+'.translateY' )
        posZ = cmds.getAttr( 'particle'+str(i)+'.translateZ' )
        
        # Calculate forces
        
        listNeighbours = findNeighbours( posX, posY, posZ, h )
        #print listNeighbours
        
        # 1. Compute Density
        density = calculateDensity( posX, posY, posY, listNeighbours, h, mass )
        #print 'density: ' + str(density)
        
        # 2. compute pressure from density
        
        # 3. Compute pressure force from pressure interaction between neighbouring particles
        
        # 4. Compute viscosity force between neighbouring particles
        
        # 5. Sum the pressure force, viscosity force and external force, ex gravity
        
        # 6. Compute the acceleration
        
        # 7. new position
        
        
        
        newPosition = calculateNewPosition( posX, posY, posZ, density, mass, dt )
        # print newPosition
        
        # v = -(G/100)*time
        # Caulculate Gravity
        gravityF = -mass*9.82
        velocity = gravityF*time/10
        print velocity
        
        cmds.select( 'particle'+str(i) )
        setNextKeyParticle( 'particle'+str(i), time, 'translateY', posY+(velocity) )
        
        '''
        # Set keyframes
        cmds.select( 'particle'+str(i) )
        setNextKeyParticle( 'particle'+str(i), time, 'translateX', newPosition[0] )
        setNextKeyParticle( 'particle'+str(i), time, 'translateY', newPosition[1] )
        setNextKeyParticle( 'particle'+str(i), time, 'translateZ', newPosition[2] )
        '''














