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
    
    # 1331
    for i in range(1,8):
        
        pos = [ cmds.getAttr( 'particle'+str(i)+'.translateX' ),
               cmds.getAttr( 'particle'+str(i)+'.translateY' ),
               cmds.getAttr( 'particle'+str(i)+'.translateZ' ) ]
        
        # Calculate distance 
        deltadist = [ pos[0] - pParticle[0],
                    pos[1] - pParticle[1],
                    pos[2] - pParticle[2] ]
        
        distance = math.sqrt( math.pow(deltadist[0], 2) + math.pow(deltadist[1], 2) + math.pow(deltadist[2], 2) )
    
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


# Compute Density
def calculateDensity( pPosition, pList, pH, pMass ):
    
    density = [0, 0, 0]
 
    for i in range( 0, len( pList ) ):
        
        neighPos = [ cmds.getAttr( pList[i]+'.translateX' ), 
                     cmds.getAttr( pList[i]+'.translateY' ), 
                     cmds.getAttr( pList[i]+'.translateZ' ) ]
        
        deltaPos = [ pPosition[0] - neighPos[0], 
                     pPosition[1] - neighPos[1], 
                     pPosition[2] - neighPos[2] ]
        
        # distance = math.sqrt( math.pow(dx, 2) + math.pow(dy, 2) + math.pow(dz, 2) )
        
        density[0] += pMass * weightFunction( deltaPos[0], pH )
        density[1] += pMass * weightFunction( deltaPos[1], pH )
        density[2] += pMass * weightFunction( deltaPos[2], pH )
    
    return density


# Compute pressures from density
# TODO: Fix contants!!!!!!!!!!!!!!!!
def calculatePressure(  pDensity ):
    
    # Gas stiffeness constant, TODO: set a proper value
    k = 1
    # rest density, TODO: set a proper values
    p0 = 0
        
    pressure = [ k * (pDensity[0] - p0),
                 k * (pDensity[1] - p0),
                 k * (pDensity[2] - p0) ]
    
    return pressure

# Compute Pressure Force from pressure interaction between neighbouring particles
def calculatePressureForce( pPosition, pDensity, pList, pMass ):
    
    pressureF = [0, 0, 0]
    pH = 1

    for i in range( 0, len( pList ) ):
        
        nPos = [ cmds.getAttr( pList[i]+'.translateX' ), 
                 cmds.getAttr( pList[i]+'.translateY' ), 
                 cmds.getAttr( pList[i]+'.translateZ' ) ]
        
        deltaPos = [ pPosition[0] - nPos[0], 
                     pPosition[1] - nPos[1], 
                     pPosition[2] - nPos[2] ]
        
        # TODO: hur ska detta berÃ¤knas??

        # nDensity = calculateDensity( nPos, pList, 1, pMass )
        # TODO: send correct pList
        nPressure = calculatePressure( calculateDensity( nPos, pList, pH, pMass ) ) 
        particlePressure = calculatePressure( pDensity )

        pressureF = [ (-1) * pMass * ( ( particlePressure[0] - nPressure[0] ) / ( 2 * nPressure[0] ) ) * weightFunction( deltaPos[0], pH ),
                      (-1) * pMass * ( ( particlePressure[1] - nPressure[1] ) / ( 2 * nPressure[1] ) ) * weightFunction( deltaPos[1], pH ),
                      (-1) * pMass * ( ( particlePressure[2] - nPressure[2] ) / ( 2 * nPressure[2] ) ) * weightFunction( deltaPos[2], pH ) ]

    return pressureF
    

def calculateViscosity( pList ):
    viscosity = [0, 0, 0]
    
    
    for i in range( 0, len( pList ) ):
        print 'hej'
    
    return viscosity
    


def calculateNewPosition( pParticlePos, pVelocityList, pDt ):
    newPosition = [0, 0, 0]
    
    newPosition = [ pDt*pVelocityList[0] + pParticlePos[0],
                    pDt*pVelocityList[1] + pParticlePos[1],
                    pDt*pVelocityList[2] + pParticlePos[2] ]
    
    return newPosition
 
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
    pos = [ cmds.getAttr( 'particle'+str(i)+'.translateX' ),
            cmds.getAttr( 'particle'+str(i)+'.translateY' ),
            cmds.getAttr( 'particle'+str(i)+'.translateZ' ) ]
    
    setNextKeyParticle( 'particle'+str(i), time, 'translateX', pos[0] )
    setNextKeyParticle( 'particle'+str(i), time, 'translateY', pos[1] )
    setNextKeyParticle( 'particle'+str(i), time, 'translateZ', pos[2] )

# Start velocity
# vel [col][row]
velocityList = [ [0, 0, 0] ] * 9

for j in range (1, 10):
    time += dt
    for i in range (1, 9):
        
        particlePos = [ cmds.getAttr( 'particle'+str(i)+'.translateX' ),
                        cmds.getAttr( 'particle'+str(i)+'.translateY' ),
                        cmds.getAttr( 'particle'+str(i)+'.translateZ' ) ]
        
        # Calculate forces
        
        listNeighbours = findNeighbours( particlePos, h )
        #print listNeighbours
        
        # 1. Compute Density
        density = calculateDensity( particlePos, listNeighbours, h, mass )
        print 'density: ' + str(density)
        
        # 2. + 3. Compute pressure force from pressure interaction between neighbouring particles
        pressure = calculatePressureForce( particlePos, density, listNeighbours, mass )
        print 'pressure: ' + str(pressure)
        
        # 4. Compute viscosity force between neighbouring particles WAIT
        
        # 5. Sum the pressure force, viscosity force and external force, ex gravity
        gravityForce = [ 0, -0.00982, 0 ]
        
        totalForce = [ pressure[0] + gravityForce[0],
                       pressure[1] + gravityForce[1],
                       pressure[2] + gravityForce[0] ]
        
        print 'totalForce: ' + str(totalForce)
        
        # 6. Compute the acceleration   
        acceleration = [ totalForce[0] / density[0],
                         totalForce[1] / density[1],
                         totalForce[2] / density[2] ]
                         
        print 'acceleration: ' + str(acceleration[1])
        # TODO QUESTION: Required to use past velocity?? 

        velocityList[i] = [ acceleration[0] * dt, 
                            acceleration[1] * dt,
                            acceleration[2] * dt ]


        # 7. new position
        newParticlePosition = calculateNewPosition( particlePos, velocityList[i], dt )
        print newParticlePosition

        # cmds.select( 'particle'+str(i) )
        # setNextKeyParticle( 'particle'+str(i), time, 'translateY', posY+(velocity) )
        
        
# error: division or modulus by zero ????        
'''
        # Set keyframes
        cmds.select( 'particle'+str(i) )
        setNextKeyParticle( 'particle'+str(i), time, 'translateX', newParticlePosition[0] )
        setNextKeyParticle( 'particle'+str(i), time, 'translateY', newParticlePosition[1] )
        setNextKeyParticle( 'particle'+str(i), time, 'translateZ', newParticlePosition[2] )
        

'''










