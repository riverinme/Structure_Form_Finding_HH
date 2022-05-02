# -*- coding: utf-8 -*-

import time
from TwoD_Form_Finding import TwoDShapeFinding

start = time.perf_counter()

# truss
a = TwoDShapeFinding(1, 3, 1, init_fr_sap=True)
a.init_fr_sap2000("SDL",
                  "China", "GB", "Q345", 1, 0.3, 1,
                  ["compression", "China", "GB", "GB50010 C30", 2,
                   0.5, -1],
                  )

ll1 = a.force_density("w", False, tolerance=1e-9, remove=False)

end = time.perf_counter()
print("****Run time: {:.2f} ms****".format((end-start)*1000))
