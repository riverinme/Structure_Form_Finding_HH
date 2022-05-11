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

a.init_fr_sap2000("Pre_loading2",
                  "China", "JTG", "JTGD62 fpk1860", 7, 0.4, 6000,
                  ["000_inner_upper", "China", "JTG", "JTGD62 fpk1860", 7,
                   0.4, 8000],
                  ["000_mid_upper", "China", "JTG", "JTGD62 fpk1860", 7,
                   0.2, 500],
                  ["000_mid_lower", "China", "JTG", "JTGD62 fpk1860", 7,
                   0.2, 250],
                  ["000_ratius_upper", "China", "JTG", "JTGD62 fpk1860", 7,
                   0.12, 2000],
                  ["000_radius_upper2nd", "China", "JTG", "JTGD62 fpk1860", 7,
                   0.12, 1000],
                  ["000_radius_lower", "China", "JTG", "JTGD62 fpk1860", 7,
                   0.12, 1500],
                  ["000_radius_lower2nd", "China", "JTG", "JTGD62 fpk1860", 7,
                   0.12, 750],
                  ["000_inner_rods", "China", "GB", "Q345", 1,
                   0.3, -10],
                  ["000_mid_rod_compression", "China", "GB", "Q345", 1,
                   0.3, -10],
                  ["000_mid_rod_tension", "China", "GB", "Q345", 1,
                   0.3, 500],
                  ["000_radius_rods", "China", "GB", "Q345", 1,
                   0.3, -10],
                  )

ll1 = a.force_density("w", False, tolerance=1e-9, remove=False)

end = time.perf_counter()
print("****Run time: {:.2f} ms****".format((end-start)*1000))


# after form found ,use "dead" and "SDL" replace "Preloading" in case "Pre"
# the result shall be still reasonable.
