# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 10:57:17 2022

@author: hh414
"""

import time
import numpy as np
from TwoD_Form_Finding import TwoDShapeFinding

start = time.perf_counter()


def e(rou, ret="w"):
    m = 5
    ccc = TwoDShapeFinding(m, 1, 2)
    ccc.set_fix([0, 0], [m-1, 0])
    ccc.set_init_F(*[[k, 0, 1] for k in range(1, m-1)])
    ccc.set_init_z()
    ccc.set_connectivities()
    ccc.set_force_density(rou/1000)
    ll1 = ccc.force_density(ret, False, remove=False)
    return sum([rou*j**2 for j in ll1])


r0 = 1
r1 = 1000

e0 = e(r0)
e1 = e(r1)

while r1 - r0 > 1e-8:
    r = 0.5*(r0+r1)
    ee = e(r)
    eep1 = e(r+1)
    if ee > eep1:
        r0 = r
        e0 = e(r0)
    elif ee < eep1:
        r1 = r
        e1 = e(r1)

print(r/1000, ee)

e(r, ret="g")


end = time.perf_counter()
print("Run time: {:.2f} ms".format((end-start)*1000))
