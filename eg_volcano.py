# -*- coding: utf-8 -*-

import time
from TwoD_Form_Finding import TwoDShapeFinding

start = time.perf_counter()

# a volcano shape
aaa = TwoDShapeFinding(1, 3, 1, init_fr_sap=True)
aaa.init_fr_sap2000("Pre_loading",  # preloading case
                    "China", "GB", "Q345", 1,  # default material
                    0.1,  # default sec dia
                    -10,  # force density
                    ["T",  # special group name 1
                     "China", "JTG", "JTGD62 fpk1470", 7,  # material for sp1,
                     0.05,  # sec dia and end for sp1
                     1]  # force density for sp1
                    )
# output format and to_sap is not working when import fr sap alreaday
ll1 = aaa.force_density("w", False)

end = time.perf_counter()
print("****Run time: {:.2f} ms****".format((end-start)*1000))
