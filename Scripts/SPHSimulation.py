# calculateForcesSpheres.py

import maya.cmds as cmds
import maya.mel as mel
import math

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
# ------ FOR ANIMATION -------
# ****************************


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
def findNeighbours( pParticle, pSmoothLength, pNr ):
    
    neighbourList = []

    for i in range( 1, pNr ):
        
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
def wfPoly6( pParticle, pH, pNr ):
    
    a = 315/( 64*3.14*math.pow( pH, pNr ) )
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
def calculateDensity( pPosition, pList, pH, pMass, pNr ):
    
    density = [0.1, 0.1, 0.1]
 
    for i in range( 0, len( pList ) ):
        
        nPos = [ cmds.getAttr( pList[i]+'.translateX' ), 
                 cmds.getAttr( pList[i]+'.translateY' ), 
                 cmds.getAttr( pList[i]+'.translateZ' ) ]
        
        deltaPos = [ pPosition[0] - nPos[0], 
                     pPosition[1] - nPos[1], 
                     pPosition[2] - nPos[2] ]
        
        density[0] += pMass * wfPoly6( deltaPos[0], pH, pNr )
        density[1] += pMass * wfPoly6( deltaPos[1], pH, pNr )
        density[2] += pMass * wfPoly6( deltaPos[2], pH, pNr ) 

    return density


# Compute pressures from density
def calculatePressure(  pDensity ):
    
    k = 1
    p0 = 0
        
    pressure = [ k * (pDensity[0] - p0),
                 k * (pDensity[1] - p0),
                 k * (pDensity[2] - p0) ]
    
    return pressure

# Compute Pressure Force from pressure interaction between neighbouring particles
def calculatePressureForce( pPosition, pDensity, pDensityList, pList, pMass, pNr ):
    
    pressureF = [0, 0, 0]
    pH = 1

    for i in range( 0, len( pList ) ):
        
        nPos = [ cmds.getAttr( pList[i]+'.translateX' ), 
                 cmds.getAttr( pList[i]+'.translateY' ), 
                 cmds.getAttr( pList[i]+'.translateZ' ) ]
        
        deltaPos = [ pPosition[0] - nPos[0], 
                     pPosition[1] - nPos[1], 
                     pPosition[2] - nPos[2] ]
        

        nDensity = calculateDensity( nPos, pList, 1, pMass, pNr )

        nPressure = calculatePressure( pDensityList[i] )  
        particlePressure = calculatePressure( pDensity )
        
        gradient = wfGradientSpiky( deltaPos, pH )
        
        pressureF[0] += (-1) * pMass * ( ( particlePressure[0] + nPressure[0] ) / ( 2 * nPressure[0] ) ) * gradient[0]
        pressureF[1] += (-1) * pMass * ( ( particlePressure[1] + nPressure[1] ) / ( 2 * nPressure[1] ) ) * gradient[1]
        pressureF[2] += (-1) * pMass * ( ( particlePressure[2] + nPressure[2] ) / ( 2 * nPressure[2] ) ) * gradient[2]

    return pressureF
    
# Compute Viscosity
def calculateViscosity( pPosition, pID, pList, pVelocity, pDensity, pH ):
    
    viscosity = [0, 0, 0]
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
       
        smoothVisc = wfLaplacianviscosity( deltaPos, pH )

        viscosity[0] += mass * ( ( nVel[0] - pVel[0] ) / pDensity[0] )
        viscosity[1] += mass * ( ( nVel[1] - pVel[1] ) / pDensity[1] )
        viscosity[2] += mass * ( ( nVel[2] - pVel[2] ) / pDensity[2] )
                       
    return ( uConstant * viscosity )


def calculateNewPosition( pParticlePos, pVelocityList, pDt ):
      
    newPosition = [ pDt * pVelocityList[0] + pParticlePos[0],
                    pDt * pVelocityList[1] + pParticlePos[1],
                    pDt * pVelocityList[2] + pParticlePos[2] ]
    
    #Boundary conditions
    Xmin = -2.5
    Xmax = 2.5
    Ymin = -0.5
    Zmin = -2.5
    Zmax = 2.5
    
    # X
    if ( newPosition[0] < Xmin or newPosition[0] > Xmax ):
        
        pVelocityList[0] = 0.0
        
        if ( newPosition[0] < Xmin ):
            newPosition[0] = Xmin
            
        if ( newPosition[0] > Xmax ):
            newPosition[0] = Xmax       
    # Y
    if ( newPosition[1] < Ymin ):
        
        pVelocityList[1] = 0.0
        newPosition[1] = -0.5
        
    # Z
    if ( newPosition[2] < Zmin or newPosition[2] > Zmax ):
        pVelocityList[2] = 0.0
        
        if ( newPosition[2] < Zmin ):
            newPosition[2] = Zmin
            
        if ( newPosition[2] > Zmax ):
            newPosition[2] = Zmax
    
    
    posAndVel = [ newPosition[0], newPosition[1], newPosition[2], pVelocityList[0], pVelocityList[1], pVelocityList[2] ]
    return posAndVel
    


# ******************************************************#

# ---------------------- MAIN --------------------------

# ******************************************************#


h = 1
mass = 5
G = 9.82
nr = 1001
time = startTime

dt = 1 # 24 f/s

# Playback options
cmds.playbackOptions( playbackSpeed=0, maxPlaybackSpeed=1 )
cmds.playbackOptions( min=1, max=300 )
startTime = cmds.playbackOptions( query=True, minTime=True )
endTime = cmds.playbackOptions( query=True, maxTime=True )


# Set first Keyframe for all partices
for i in range ( 1, nr ):
    pos = [ cmds.getAttr( 'particle'+str(i)+'.translateX' ),
            cmds.getAttr( 'particle'+str(i)+'.translateY' ),
            cmds.getAttr( 'particle'+str(i)+'.translateZ' ) ]
    
    setNextKeyParticle( 'particle'+str(i), time, 'translateX', pos[0] )
    setNextKeyParticle( 'particle'+str(i), time, 'translateY', pos[1] )
    setNextKeyParticle( 'particle'+str(i), time, 'translateZ', pos[2] )


# vel [col][row]
velocityList = [ [0.0, 0.0, 0.0] ] * 13
densityList = [ [0.1, 0.1, 0.1] ] * 13

for j in range ( 1, 300 ):
    print 'frame: ' + str(j)
    time += dt
    for i in range ( 1, nr ):
        
        particlePos = [ cmds.getAttr( 'particle'+str(i)+'.translateX' ),
                        cmds.getAttr( 'particle'+str(i)+'.translateY' ),
                        cmds.getAttr( 'particle'+str(i)+'.translateZ' ) ]
        
        # --------- CALCULATE FORCES ----------
        
        listNeighbours = findNeighbours( particlePos, h, nr )
        
        # 1. Compute Density
        density = calculateDensity( particlePos, listNeighbours, h, mass, nr )
        densityList[i] = density 
        
        # 2. + 3. Compute pressure force from pressure interaction between neighbouring particles
        pressure = calculatePressureForce( particlePos, density, densityList, listNeighbours, mass, nr )

                
        # 4. Compute viscosity force between neighbouring particles 
        viscosity = calculateViscosity( particlePos, i, listNeighbours, velocityList, density, h )
        
        # 5. Sum the pressure force, viscosity force and external force: gravity
        gravityForce = -9.82 * mass * time
        
        totalForce = [ pressure[0] + viscosity[0],
                       pressure[1] + viscosity[1] + gravityForce,
                       pressure[2] + viscosity[2]  ]
        
        # 6. Compute the acceleration   

        acceleration = [ totalForce[0] / density[0],
                         totalForce[1] / density[1],
                         totalForce[2] / density[2] ]
        
        # velocity
        velocityList[i] = [ acceleration[0] * (time/576), 
                            acceleration[1] * (time/576),
                            acceleration[2] * (time/576)]
                    
        
        '''
        velocityList[i] = [ velocityList[i][0] + acceleration[0] * (time/576), 
                            velocityList[i][1] + acceleration[1] * (time/576),
                            velocityList[i][2] + acceleration[2] * (time/576) ]
        '''
        
        # 7. new position
        
        positionAndVelocity = calculateNewPosition( particlePos, velocityList[i], dt )
        newParticlePosition = [ positionAndVelocity[0], positionAndVelocity[1], positionAndVelocity[2] ]
        
        velocityList[i][0] = positionAndVelocity[3]
        velocityList[i][1] = positionAndVelocity[4]
        velocityList[i][2] = positionAndVelocity[5]
             

        # Set keyframes
        cmds.select( 'particle'+str(i) )
        setNextKeyParticle( 'particle'+str(i), time, 'translateX', newParticlePosition[0] )
        setNextKeyParticle( 'particle'+str(i), time, 'translateY', newParticlePosition[1] )
        setNextKeyParticle( 'particle'+str(i), time, 'translateZ', newParticlePosition[2] )
