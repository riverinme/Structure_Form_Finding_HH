# -*- coding: utf-8 -*-

import time
from TwoD_Form_Finding import TwoDShapeFinding

start = time.perf_counter()

# example_ get_started_1d_rope
ccc = TwoDShapeFinding(5, 1, 2)  # 生成一个找形实例。5x1的网格，其实就是1维索。网格间距2(m)
ccc.set_fix([0, 0], [4, 0])  # 两端铰接
# 中间3个节点(1, 0), (2, 0), (3, 0)分别施加1(kN)重力方向的集中力
ccc.set_init_F([1, 0, 1], [2, 0, 1], [3, 0, 1])
ccc.set_init_z([0, 0, -1])  # 支座(0, 0) 的初始位置在Z=-1(m)的位置
ccc.set_connectivities()  # 生成节点之间的单元
ccc.set_force_density(1, [1, 10])  # 默认的力密度为1kN/m，同时1号单元的力密度改为10kN/m
ll1 = ccc.force_density("g", False)  # 进行分析，同时返回找形后的图片结果，“False”表示不输出到SAP2000

# example_ get_started_web
ccc = TwoDShapeFinding(5, 5, 1)  # 生成一个找形实例。5x5的网格。网格间距1(m)
ccc.set_fix([0, 0], [0, 4], [4, 0], [4, 4])  # 4端铰接
# 自由收缩，不加任何力
ccc.set_init_F()
ccc.set_init_z([0, 0, 1], [4, 4, 1])  # 对角角点标高为1m
ccc.set_connectivities()  # 生成节点之间的单元
ccc.set_force_density(1)  # 默认的力密度为1kN/m
ll1 = ccc.force_density("g", False, remove=False)  # 进行分析，同时返回找形后的图片结果

# example_ get_started_web
ccc = TwoDShapeFinding(5, 5, 1)  # 生成一个找形实例。5x5的网格。网格间距1(m)
ccc.set_fix([0, 0], [0, 4], [4, 0], [4, 4])  # 4端铰接
# 中间施加1kN的向下的力
ccc.set_init_F([2, 2, 1])
ccc.set_init_z([0, 0, 1], [4, 4, 1])  # 对角角点标高为1m
ccc.set_connectivities()  # 生成节点之间的单元
ccc.set_force_density(1)  # 默认的力密度为1kN/m
ll1 = ccc.force_density("g", False, remove=False)  # 进行分析，同时返回找形后的图片结果

end = time.perf_counter()
print("****Run time: {:.2f} ms****".format((end-start)*1000))
