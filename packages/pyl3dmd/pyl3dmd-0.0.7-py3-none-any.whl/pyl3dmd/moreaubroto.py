# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 09:08:18 2022

@author: pawan
"""
import numpy as np
"""
Calculate Moreau-Broto autocorrelation descriptors
"""
def calmoreaubrotodescriptors(G, propertyValue, propertyName):
    n = 30
    step = 0.5 # step size [Å]
    lagL = np.array([i for i in range(0,n)]).astype(float)*step
    lagU = lagL+step
    nA = len(G)

    ATS = {}
    for kkk in range(len(lagL)):
        temp = 0.0
        for i in range(nA):
            for j in range(nA):  
                if G[i,j] >= lagL[kkk] and G[i,j] < lagU[kkk]:
                    temp = temp + propertyValue[i]*propertyValue[j]
                else:
                    temp= temp + 0.0     
        ATS['ATS'+propertyName+str(kkk+1)] = np.log(temp/2+1)
    return ATS

"""
Get Moreau-Broto autocorrelation for all atomic weights/properties
"""
def getmoreaubrotodescriptors(*args):
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
    
    ATS = {}
    for i in range(len(propertyNames)):
        ATS.update(calmoreaubrotodescriptors(args[0], args[i+1], propertyNames[i]))
    return ATS