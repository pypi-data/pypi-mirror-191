# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 09:09:20 2022

@author: pawan
"""
import numpy as np

"""
Calculate 3D Geary autocorrelation indices
"""
def calgearyindices(G, propertyValue, propertyName):
    n = 30
    step = 0.5 # step size [Å]
    lagL = np.array([i for i in range(0,n)]).astype(float)*step
    lagU = lagL+step
    nA = len(G)
    
    avgpropertyValue = sum(propertyValue)/nA
    tempp = sum(np.square(propertyValue-avgpropertyValue))
    
    GATS = {}
    for kkk in range(len(lagL)):
        temp = 0.0
        index = 0
        for i in range(nA):
            for j in range(nA):  
                if G[i,j] >= lagL[kkk] and G[i,j] < lagU[kkk]:
                    temp= temp + np.square(propertyValue[i]-propertyValue[j])
                    index = index + 1
                else:
                    temp = temp + 0.0           
        if tempp == 0 or index == 0:
            GATS['GATS'+propertyName+str(kkk+1)] = 0
        else:
            GATS['GATS'+propertyName+str(kkk+1)] = (temp/index/2)/(tempp/(nA-1))
    return GATS

"""
Get 3D Geary autocorrelation indices for all atomic weights/properties
"""
def getgearyindices(*args):
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
    
    GATS = {}
    for i in range(len(propertyNames)):
        GATS.update(calgearyindices(args[0], args[i+1], propertyNames[i]))
    return GATS