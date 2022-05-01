# -*- coding: utf-8 -*-
"""
Created on Sun May  1 08:53:08 2022

@author: hh414
"""

import time
from TwoD_Form_Finding import TwoDShapeFinding
from TwoD_Form_Finding import mass_assign


start = time.perf_counter()

a = TwoDShapeFinding(1, 3, 1, init_fr_sap=True)

a.init_fr_sap2000(mass_assign(a.SapModel, "Pre_loading"),
                  "China", "JTG", "JTGD62 fpk1470", 7, 0.3, 2000,
                  ["inner_up", "China", "JTG", "JTGD62 fpk1470", 7,
                   0.3, 1500],
                  ["mid_upper", "China", "JTG", "JTGD62 fpk1470", 7,
                   0.2, 750],
                  ["mid_down", "China", "JTG", "JTGD62 fpk1470", 7,
                   0.2, 1000],
                  ["radius_upper", "China", "JTG", "JTGD62 fpk1470", 7,
                   0.12, 375],
                  ["radius_down", "China", "JTG", "JTGD62 fpk1470", 7,
                   0.12, 500],
                  ["radius_web", "China", "GB", "Q345", 1,
                   0.3, -15]
                  )

ll1 = a.force_density("w", False, tolerance=1e-9, remove=False)

end = time.perf_counter()
print("****Run time: {:.2f} ms****".format((end-start)*1000))


# after form found ,use "dead" and "SDL" replace "Preloading" in case "Pre"
# the result shall be still reasonable.
