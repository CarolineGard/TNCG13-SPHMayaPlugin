# calculateForces.py

import maya.cmds as cmds
import maya.mel as mel
import math

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
        if distance <= pSmoothLength: 
            neighbourList.append( 'nParticle1.pt[' + str(i) + ']' )
    
    return neighbourList
    
# Calculate smoothing Lenght
smoothL = .1

# Per every time step h
for i in range(1330):
    
    # Get neighbor list for the current particle
    nList = findNeighbours( 'nParticle1.pt[' + str(i) + ']', smoothL )
    
    # Calculate Forces   
   
   
   
   
     
    
    
'''
for i in range(1330):
    cmds.select( 'nParticle1.pt[' + str(i) + ']' )
''' 
    
    
    
    
    
    
    
    
    
    
    