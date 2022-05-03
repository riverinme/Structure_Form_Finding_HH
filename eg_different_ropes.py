# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 10:57:17 2022

@author: hh414
"""

import time
import numpy as np
from TwoD_Form_Finding import TwoDShapeFinding

start = time.perf_counter()

# examples
# ****eg1 1d rope with point loads, coords and force densities pre-assigned
m = 5
# m * n points with n=1, 2 is the element length
ccc = TwoDShapeFinding(m, 1, 2)
ccc.set_fix([0, 0], [m-1, 0])  # to fix and both ends
# add unit load downwards at all mid points
ccc.set_init_F(*[[k, 0, 1] for k in range(1, m-1)])
ccc.set_init_z([0, 0, -1])  # set point(0, 0) initial z -1
ccc.set_connectivities()  # make connections to nodes
# set general frame load density, followed by special load densities
ccc.set_force_density(1, [1, 10])
# run. "g" means to give a graph for out put
# False means not to export to sap2000
ll1 = ccc.force_density("g", False)

# # ****eg2 random loading
# for i in range(9):
#     m = 10
#     ccc = TwoDShapeFinding(m, 1, 1)
#     ccc.set_fix([0, 0], [m-1, 0])
#     ccc.set_init_F(*[[k, 0, np.random.rand()] for k in range(1, m-1)])
#     ccc.set_init_z()
#     ccc.set_connectivities()
#     ccc.set_force_density(50)
#     ll1 = ccc.force_density("g", False)

# ****eg2 random loading arch
for i in range(9):
    m = 10
    ccc = TwoDShapeFinding(m, 1, 1)
    ccc.set_fix([0, 0], [m-1, 0])
    ccc.set_init_F(*[[k, 0, np.random.rand()] for k in range(1, m-1)])
    ccc.set_init_z()
    ccc.set_connectivities()
    ccc.set_force_density(-1)
    ll1 = ccc.force_density("g", False)

# # ****eg3 random joint forces
# for i in range(5):
#     m = 10
#     ccc = TwoDShapeFinding(m, 1, 1)
#     ccc.set_fix([0, 0], [m-1, 0])
#     ccc.set_init_F(*[[k, 0, np.random.rand()] for k in range(1, m-1)])
#     ccc.set_init_z()
#     ccc.set_connectivities()
#     ccc.set_force_density(1)
#     ll1 = ccc.force_density("g", False)

# # ****eg4 random frame force densities
# for i in range(5):
#     m = 10
#     ccc = TwoDShapeFinding(m, 1, 1)
#     ccc.set_fix([0, 0], [m-1, 0])
#     ccc.set_init_F(*[[k, 0, 1] for k in range(1, m-1)])
#     ccc.set_init_z()
#     ccc.set_connectivities()
#     ccc.set_force_density(1, *[[i, np.random.rand()*10] for i in range(m-1)])
#     ll1 = ccc.force_density("g", False)

# # ****eg5 arch
# m = 10
# for i in [-1, -10, -100]:
#     ccc = TwoDShapeFinding(m, 1, 1)
#     ccc.set_fix([0, 0], [m-1, 0])
#     ccc.set_init_F(*[[k, 0, 1] for k in range(1, m-1)])
#     ccc.set_init_z()
#     ccc.set_connectivities()
#     ccc.set_force_density(i)
#     ll1 = ccc.force_density("g", False)

end = time.perf_counter()
print("Run time: {:.2f} ms".format((end-start)*1000))
