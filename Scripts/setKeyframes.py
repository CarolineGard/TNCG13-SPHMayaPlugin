# setKeyFrames 

import maya.cmds as cmds
import maya.mel as mel


cmds.select( 'nParticleShape1.pt[0:7]', 'nParticleShape1.pt[11]' )
cmds.setParticleAttr( vv=(50, 50, 50), at='velocity' )
cmds.setParticleAttr( 'nParticleShape1', at='velocity' )

cmds.getParticleAttr( 'nParticleShape1.pt[1]', at='position' )
cmds.setParticleAttr( 'nParticleShape1.pt[1]', at='position' value=-1.0909090190666146, 2.5863125324249268, -1.363636330923503)

def setNextKeyParticle( pName, pStartKey, pEndKey, pTargetAttribute, pValue ):
    
    # stepLenght
    h = .01
    endKey2 = pStartKey + h
    
    # clear selection list and select all particles
    cmds.select( clear=True )
    
    cmds.cutKey( pName, time=( pStartKey, endTime ), attribute=pTargetAttribute )

    # create animation, set startkeyframe, startvalue=0 at first key frame. Make linear keyframes
    cmds.setKeyframe( pName, time=pStartKey, attribute=pTargetAttribute, value=0 )
    cmds.setKeyframe( pName, time=pEndKey, attribute=pTargetAttribute, value=pValue ) 
    cmds.selectKey( pName, time=( pStartKey, pEndKey ), attribute=pTargetAttribute, keyframe=True )
    cmds.keyTangent( inTangentType='linear', outTangentType='linear' )


# Moce the whole cube of particles
cmds.select( 'nParticleShape1' )


startTime = cmds.playbackOptions( query=True, minTime=True )
endTime = cmds.playbackOptions( query=True, maxTime=True )
 
#setKeyframeParticle( 'nParticle1.pt[1]', startTime, endTime, 'translateX', 50 )       
setKeyframeParticle( 'nParticle1', startTime, endTime, 'rotateY', 360 )








# ---- BRA ATT HA -----

# mel.eval( 'select -r nParticleShape1.pt[0:1330]' )
# selectionList = cmds.ls( selection=True )


'''
#if len( selectionList ) >=1:
    for objectName in nParticle1:
             
        objectTypeResult = cmds.objectType( nParticle1 )
        print '%s type: %s' % ( nParticle1, objectTypeResult )
  '''      

#else: 
 #   print 'Please select at least one object'
 
 
 '''
# Working
# clear selection list and select all particles
cmds.select( clear=True )
    
cmds.cutKey( 'nParticle1', time=( startTime, endTime ), attribute='rotateY' )

# create animation, set startkeyframe, startvalue=0 at first key frame. Make linear keyframes
cmds.setKeyframe( 'nParticle1', time=startTime, attribute='rotateY', value=0 )
cmds.setKeyframe( 'nParticle1', time=endTime, attribute='rotateY', value=360 ) 
cmds.selectKey( 'nParticle1', time=( startTime, endTime ), attribute='rotateY', keyframe=True )
cmds.keyTangent( inTangentType='linear', outTangentType='linear' )