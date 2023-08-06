# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 09:10:33 2022

@author: pawan
"""
import numpy as np

"""
Calculate Moran autocorrelation descriptors
"""
def calmorandescriptors(G, propertyValue, propertyName):    
    n = 30
    step = 0.5 # step size [Å]
    lagL = np.array([i for i in range(0,n)]).astype(float)*step
    lagU = lagL+step
    nA = len(G)
    
    avgpropertyValue = sum(propertyValue)/nA
    tempp = sum(np.square(propertyValue-avgpropertyValue))
    
    MATS = {}
    for kkk in range(len(lagL)):
        temp = 0.0
        index = 0
        for i in range(nA):
            for j in range(nA):  
                if G[i,j] >= lagL[kkk] and G[i,j] < lagU[kkk]:
                    temp = temp + (propertyValue[i]-avgpropertyValue)*(propertyValue[j]-avgpropertyValue)
                    index = index + 1
                else:
                    temp = temp + 0.0  
        if tempp == 0 or index == 0:
            MATS['MATS'+propertyName+str(kkk+1)] = 0
        else:
            MATS['MATS'+propertyName+str(kkk+1)] = (temp/index)/(tempp/nA)
    return MATS

"""
Get 3D Moran autocorrelation descriptors for all atomic weights/properties
"""
def getmorandescriptors(*args):
    """ INPUTS
    0 ; Geometric or 3D distnace matrix (G)
    1 : atomic charge (c)
    2 : atomic mass (m)
    3 : van der Waals vloume (V)
    4 : Sanderson electronegativity (En)
    5 : atomic polarizability in 10e-24 cm3 (P)
    6 : ionization potential in eV (IP)
    7 : electron affinity in eV (EA)
    """
     
    propertyNames = ['c','m','V','En','P','IP','EA']
    
    MATS = {}
    for i in range(len(propertyNames)):
        MATS.update(calmorandescriptors(args[0], args[i+1], propertyNames[i]))
    return MATS