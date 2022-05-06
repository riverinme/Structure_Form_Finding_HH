# -*- coding: utf-8 -*-

import time
from TwoD_Form_Finding import TwoDShapeFinding

start = time.perf_counter()

# example_ init from SAP2000-igloo
aaa = TwoDShapeFinding(1, 3, 1, init_fr_sap=True)
aaa.init_fr_sap2000("Pre_loading",  # preloading case
                    "China", "GB", "GB50010 C30", 2,  # default material
                    0.1,  # default sec dia
                    -0.1,  # force density
                    ["G2",  # special group name 1
                     "China", "GB", "GB50010 C50", 2,  # material for sp1
                     0.2,  # sec dia and end for sp1
                     -0.1]  # force density for sp1
                    )
# output format and to_sap is not working when import fr sap alreaday
ll1 = aaa.force_density("t", False, remove=False)

end = time.perf_counter()
print("****Run time: {:.2f} ms****".format((end-start)*1000))
