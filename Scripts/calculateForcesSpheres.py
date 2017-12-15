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
    for i in range(1,9):
        
        pos = [ cmds.getAttr( 'particle'+str(i)+'.translateX' ),
                cmds.getAttr( 'particle'+str(i)+'.translateY' ),
                cmds.getAttr( 'particle'+str(i)+'.translateZ' ) ]
        
        deltadist = [0, 0, 0]
        # Calculate distance 
        deltadist[0] = pos[0] - pParticle[0]
        deltadist[1] = pos[1] - pParticle[1]
        deltadist[2] = pos[2] - pParticle[2]
        
        distance = math.sqrt( math.pow(deltadist[0], 2) + math.pow(deltadist[1], 2) + math.pow(deltadist[2], 2) )
    
        # if distance <= psmoothLength, put in array
        if distance <= pSmoothLength and distance > 0: 
            neighbourList.append( 'particle'+str(i) )
    
    return neighbourList

# wfPoly6
def wfPoly6( pParticle, pH ):
    
    #if (pParticle <= pH):     
    a = 315/( 64*3.14*math.pow( pH, 9 ) )
    w = a * math.pow( ( math.pow( pH, 2 ) - math.pow( pParticle, 2 ) ), 3 )
         
    return w

# wfGradientSpiky
def wfGradientSpiky( pParticle, pH ):
    
    a = -45/(64*3.14*math.pow( pH, 6 ) )
    w = [ a * math.pow( pH - pParticle[0], 2 ),
          a * math.pow( pH - pParticle[1], 2 ),
          a * math.pow( pH - pParticle[2], 2 ) ]
                        
    return w

# wfLaplacianviscosity
def wfLaplacianviscosity( pParticle, pH ):
    
    a = 45/( 3.14*math.pow( pH, 6 ) )
    w = [ a * ( pH-pParticle[0] ),
          a * ( pH-pParticle[1] ),
          a * ( pH-pParticle[2] ) ]
             
    return w



# Compute Density
def calculateDensity( pPosition, pList, pH, pMass ):
    
    density = [0.1, 0.1, 0.1]
    
    #print 'pList: ' + str(pList)
 
    for i in range( 0, len( pList ) ):
        
        nPos = [ cmds.getAttr( pList[i]+'.translateX' ), 
                 cmds.getAttr( pList[i]+'.translateY' ), 
                 cmds.getAttr( pList[i]+'.translateZ' ) ]
        
        deltaPos = [ pPosition[0] - nPos[0], 
                     pPosition[1] - nPos[1], 
                     pPosition[2] - nPos[2] ]
        
        # distance = math.sqrt( math.pow(dx, 2) + math.pow(dy, 2) + math.pow(dz, 2) )
        
        density[0] += pMass * wfPoly6( deltaPos[0], pH )
        density[1] += pMass * wfPoly6( deltaPos[1], pH )
        density[2] += pMass * wfPoly6( deltaPos[2], pH ) 

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
        
        # TODO: hur ska detta berÃƒÂ¤knas??

        nDensity = calculateDensity( nPos, pList, 1, pMass )
        # TODO: send correct pList 
        nPressure = calculatePressure( calculateDensity( nPos, pList, pH, pMass ) ) 
        particlePressure = calculatePressure( pDensity )
        
        gradient = wfGradientSpiky( deltaPos, pH )
        
        pressureF[0] += (-1) * pMass * ( ( particlePressure[0] - nPressure[0] ) / ( 2 * nPressure[0] ) ) * gradient[0]
        pressureF[1] += (-1) * pMass * ( ( particlePressure[1] - nPressure[1] ) / ( 2 * nPressure[1] ) ) * gradient[1]
        pressureF[2] += (-1) * pMass * ( ( particlePressure[2] - nPressure[2] ) / ( 2 * nPressure[2] ) ) * gradient[2]

    return pressureF
    
# Compute Viscosity
def calculateViscosity( pPosition, pID, pList, pVelocity, pDensity, pH ):
    
    viscosity = [0, 0, 0]
    # TODO: Set proper constant value
    uConstant = 1
    
    pVel = pVelocity[ pID ]
    
    for i in range( 0, len( pList ) ):
        
        nPos = [ cmds.getAttr( pList[i]+'.translateX' ), 
                 cmds.getAttr( pList[i]+'.translateY' ), 
                 cmds.getAttr( pList[i]+'.translateZ' ) ]
        
        deltaPos = [ pPosition[0] - nPos[0], 
                     pPosition[1] - nPos[1], 
                     pPosition[2] - nPos[2] ]
        
        
        nVel = pVelocity[ i ]
        
        # TODO: add gradient^2 W ANTAGLIGEN FETT FEL
        smoothVisc = wfLaplacianviscosity( deltaPos, pH )

        viscosity[0] += mass * ( ( nVel[0] - pVel[0] ) / pDensity[0] )
        viscosity[1] += mass * ( ( nVel[1] - pVel[1] ) / pDensity[1] )
        viscosity[2] += mass * ( ( nVel[2] - pVel[2] ) / pDensity[2] )
                       
    return ( uConstant * viscosity )


def calculateNewPosition( pParticlePos, pVelocityList, pDt ):
    
    #print pParticlePos
      
    newPosition = [ pDt * pVelocityList[0] + pParticlePos[0],
                    pDt * pVelocityList[1] + pParticlePos[1],
                    pDt * pVelocityList[2] + pParticlePos[2] ]
    
    # print newPosition
    #Boundary conditions
    Xmin = -2.5
    Xmax = 2.5
    Ymin = -1
    Zmin = -2.5
    Zmax = 2.5
       
    if ( newPosition[0] < Xmin or newPosition[0] > Xmax ):
        #print 'X'
        #pVelocityList[0] = (-1) * pVelocityList[0]
        pVelocityList[0] = 0
        newPosition[0] = pParticlePos[0]
        
    if ( newPosition[1] < Ymin ):
        #print 'Y'
        #pVelocityList[1] = (-1) * pVelocityList[1]
        pVelocityList[1] = 0
        newPosition[1] = pParticlePos[1]
        
    if ( newPosition[2] < Zmin or newPosition[2] > Zmax ):
        #print 'Z'
        #pVelocityList[2] = (-1) * pVelocityList[2]
        pVelocityList[2] = 0
        newPosition[2] = pParticlePos[2]  
        
    posAndVel = [ newPosition[0], newPosition[1], newPosition[2], pVelocityList[0], pVelocityList[1], pVelocityList[2] ]
    
    return posAndVel
    
def calculateBoundaries( pPositionX, pPositionY, pPositionZ, pvelocity ):

    
    return [0, 0, 0]


# ******************************************************#
# ------ MAIN ------
# ******************************************************#


# Playback options
cmds.playbackOptions( playbackSpeed=0, maxPlaybackSpeed=1 )
cmds.playbackOptions( min=1, max=300 )
startTime = cmds.playbackOptions( query=True, minTime=True )
endTime = cmds.playbackOptions( query=True, maxTime=True )

  
# Calculate smoothing Lenght
h = 1
mass = 10
G = 9.82

# stepLenght 24 frames / sec
dt = 4

time = startTime

# cmds.select('particle100')


# Set first Keyframe for all partices
for i in range (1,9):
    pos = [ cmds.getAttr( 'particle'+str(i)+'.translateX' ),
            cmds.getAttr( 'particle'+str(i)+'.translateY' ),
            cmds.getAttr( 'particle'+str(i)+'.translateZ' ) ]
    
    setNextKeyParticle( 'particle'+str(i), time, 'translateX', pos[0] )
    setNextKeyParticle( 'particle'+str(i), time, 'translateY', pos[1] )
    setNextKeyParticle( 'particle'+str(i), time, 'translateZ', pos[2] )

# Start velocity
# vel [col][row]
velocityList = [ [0.0, 0.0, 0.0] ] * 9

for j in range (1, 100):
    time += dt
    for i in range (1, 9):
        
        particlePos = [ cmds.getAttr( 'particle'+str(i)+'.translateX' ),
                        cmds.getAttr( 'particle'+str(i)+'.translateY' ),
                        cmds.getAttr( 'particle'+str(i)+'.translateZ' ) ]
        
        # Calculate forces
        
        listNeighbours = findNeighbours( particlePos, h )
        #print 'listNeighbours: ' + str(listNeighbours)
        
        # 1. Compute Density
        density = calculateDensity( particlePos, listNeighbours, h, mass )
        #print 'density: ' + str(density)
        
        # 2. + 3. Compute pressure force from pressure interaction between neighbouring particles
        pressure = calculatePressureForce( particlePos, density, listNeighbours, mass )
        #print 'pressure: ' + str(pressure)
        
        
        
        # 4. Compute viscosity force between neighbouring particles 
        viscosity = calculateViscosity( particlePos, i, listNeighbours, velocityList, density, h )
        
        # 5. Sum the pressure force, viscosity force and external force, ex gravity
        gravityForce = -9.82*mass
 
        totalForce = [ pressure[0] + viscosity[0],
                       pressure[1] + viscosity[1] + gravityForce,
                       pressure[2] + viscosity[2]  ]
        

        #print 'totalForce: ' + str(totalForce)
        
        # 6. Compute the acceleration   
        acceleration = [ totalForce[0] / density[0],
                         totalForce[1] / density[1],
                         totalForce[2] / density[2] ]
        
        #print acceleration                 
                         
        #print 'acceleration: ' + str(acceleration[1])
        # TODO QUESTION: Required to use past velocity?? 

        velocityList[i] = [ velocityList[i][0] + acceleration[0] * (time/576), 
                            velocityList[i][1] + acceleration[1] * (time/576),
                            velocityList[i][2] + acceleration[2] * (time/576) ]
                    
        #print 'acc_ '+str(acceleration)                    
        #print 'vel: '+str(velocityList[i])
        #print velocityList[i]

        # 7. new position
        positionAndVelocity = calculateNewPosition( particlePos, velocityList[i], dt )
        newParticlePosition = [ positionAndVelocity[0], positionAndVelocity[1], positionAndVelocity[2]]
        
        velocityList[i][0] = positionAndVelocity[3]
        velocityList[i][1] = positionAndVelocity[4]
        velocityList[i][2] = positionAndVelocity[5]
        
        # print 'vel2: ' + str(velocityList[i])
        #print 'position: ' + str(newParticlePosition)
        #print newParticlePosition

        #cmds.select( 'particle'+str(i) )
        #setNextKeyParticle( 'particle'+str(i), time, 'translateY', posY+(velocity) )
        
        
        # error: division or modulus by zero ????        

        # Set keyframes
        cmds.select( 'particle'+str(i) )
        setNextKeyParticle( 'particle'+str(i), time, 'translateX', newParticlePosition[0] )
        setNextKeyParticle( 'particle'+str(i), time, 'translateY', newParticlePosition[1] )
        setNextKeyParticle( 'particle'+str(i), time, 'translateZ', newParticlePosition[2] )












