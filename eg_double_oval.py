# -*- coding: utf-8 -*-

import time
from TwoD_Form_Finding import TwoDShapeFinding

start = time.perf_counter()

# double oval
a = TwoDShapeFinding(1, 3, 1, init_fr_sap=True)
a.init_fr_sap2000("Pre_loading",
                  "China", "JTG", "JTGD62 fpk1470", 7, 0.3, 1000,
                  ["inner_up", "China", "JTG", "JTGD62 fpk1470", 7,
                   0.3, 1000],
                  ["mid_upper", "China", "JTG", "JTGD62 fpk1470", 7,
                   0.2, 500],
                  ["mid_down", "China", "JTG", "JTGD62 fpk1470", 7,
                   0.2, 500],
                  ["radius_upper", "China", "JTG", "JTGD62 fpk1470", 7,
                   0.12, 200],
                  ["radius_down", "China", "JTG", "JTGD62 fpk1470", 7,
                   0.12, 200],
                  ["radius_web", "China", "GB", "Q345", 1,
                   0.3, -5]
                  )

ll1 = a.force_density("w", False, tolerance=1e-9, remove=False)

end = time.perf_counter()
print("****Run time: {:.2f} ms****".format((end-start)*1000))
