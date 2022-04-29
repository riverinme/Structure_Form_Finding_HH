# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 11:30:55 2022

@author: hh414
"""

import time
from TwoD_Form_Finding import TwoDShapeFinding

start = time.perf_counter()

# 2d net under pretensioned with all 4 side constrained
m, n = 29, 29
constrain = []
for w in range(m):
    for v in range(n):
        if v == 0 or v == n-1:
            constrain.append([w, v])
        else:
            if w == 0 or w == m-1:
                constrain.append([w, v])
boundary_z = []
z_max = 1
for w in range(m):
    for v in range(n):
        if v == 0:
            boundary_z.append([w, v, z_max/(m-1)*w])
        elif v == n-1:
            boundary_z.append([w, v, z_max-z_max/(m-1)*w])
        elif w == 0 and 0 < v < n-1:
            boundary_z.append([w, v, z_max/(n-1)*v])
        elif w == m-1 and 0 < v < n-1:
            boundary_z.append([w, v, z_max-z_max/(n-1)*v])
loading = []
unit = 1
for w in range(m):
    for v in range(n):
        if 0 < v < n-1 and 0 < w < m-1:
            loading.append([w, v, unit])
aaa = TwoDShapeFinding(m, n, 2)
aaa.set_fix(*constrain)
aaa.set_fix([20, 20], [10, 10])
aaa.set_init_F(*loading)
aaa.set_init_z(*boundary_z)
aaa.set_init_z([20, 20, 10], [10, 10, 10])
aaa.set_connectivities()
aaa.set_force_density(10000)
aaa.force_density("g", True,
                  "China", "JTG", "JTGD62 fpk1470", 7, 0.06)

end = time.perf_counter()
print("Run time: {:.2f} ms".format((end-start)*1000))
