# -*- coding: utf-8 -*-
"""
Created on Thu December 10 11:41:02 2022

@author: Pawan Panwar, Quanpeng Yang, Ashlie Martini


PyL3dMD: Python LAMMPS 3D Molecular Dynamics/Descriptors
Copyright (C) 2022  Pawan Panwar, Quanpeng Yang, Ashlie Martini

This file is part of PyL3dMD.

PyL3dMD is free software: you can redistribute it and/or modify 
it under the terms of the GNU General Public License as published 
by the Free Software Foundation, either version 3 of the License, 
or (at your option) any later version.

PyL3dMD is distributed in the hope that it will be useful, but 
WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
 along with PyL3dMD. If not, see <https://www.gnu.org/licenses/>.
"""



from setuptools import setup, find_packages

VERSION = '0.0.5' 
DESCRIPTION = 'Python LAMMPS 3-Dimensional Molecular Dynamics/Descriptors'
LONG_DESCRIPTION = 'PyL3dMD stands for Python LAMMPS 3-Dimensional Molecular Dynamics/Descriptors, a python package for 3D descriptors calculation'

# setup
setup(
       # name has to be identical with the name of the folder where the package is
        name="pyl3dmd", 
        version=VERSION,
        author="Pawan Panwar, Quanpeng Yang, Ashlie Martini",
        author_email="panwarp@msoe.edu",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=["numpy","pandas","multiprocessing","math", "time"], # add any additional packages that 
        #install_requires=[], # add any additional packages that 
        
        keywords=['Python', 'LAMMPS', 'Molecular Dynamics Simulations', 'Molecular Descriptors', 'Machine Learning', 'MD Simulations', '3-Dimensional'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)