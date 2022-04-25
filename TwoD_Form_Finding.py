# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 10:16:02 2022

@author: hh414
"""

# x sequence: 0, 1, 2, ..., j, ..., m-1
# y sequence: 0, 1, 2, ..., i, ..., n-1

# sequence 2d
# 1, given following x and y sequence
# (n-1, 0), (n-1, 1), ... , (n-1, j), ... ,(n-1, m-1)
#
# (i, 0),   (i, 1),   ... , (i, j),   ... ,(i, m-1)
#
# (1, 0),   (1, 1),   ... , (1, j),   ... ,(1, m-1)
# (0, 0),   (0, 1),   ... , (0, j),   ... ,(0, m-1)

# 2 to get a combined seqence like, also are point numbers
# (from left bottom to upper right)
# (n-1)*m, (n-1)*m+1, ... , (n-1)*m+j, ... ,n*m-1]
#
# i*m,     i*m+1,     ... , i*m+j      ... ,(i+1)m-1,
#
# m,       m+1,       ... , m+j,       ... ,2m-1,
# [0,      1,         ... , j,         ... ,m-1,


# sequence 1d
# 0, 1, ..., j, ..., m-1


# from matplotlib import cbook
from matplotlib import cm
from matplotlib.colors import LightSource
import matplotlib.pyplot as plt
import numpy as np
import comtypes.client
import sys
import time


class TwoDShapeFinding():
    def __init__(self, m, n, size,
                 fix=[],
                 init_z=[],
                 init_F=[], links=[],
                 frame_names=[],
                 frame_end_pts=[],
                 frame_force_density={}):
        self.n = n
        self.m = m
        self.s = size

        # store point x sequences and y sequences
        self.init_x = [j*self.s for i in range(self.n) for j in range(self.m)]
        self.init_y = [i*self.s for i in range(self.n) for j in range(self.m)]
        self.init_z = init_z  # init Z coords in global sys
        self.init_F = init_F  # init point load in gravity dir
        self.fix = fix  # store point constrain
        self.__links = links  # store sub lists of points next to a point
        self.frame_names = frame_names  # store frame names/ID/labels
        self.frame_end_pts = frame_end_pts  # store frame end points
        # store frame force density
        self.frame_force_density = frame_force_density
        self.__linked_frames = []  # store sub lists of frames next to a point
        # store sub lists of force densities of frames next to a point
        self.__linked_force_densities = []

    def __points_around_x(self, x, y):
        if self.n > 1:
            if 0 < x < self.m-1 and 0 < y < self.n-1:
                return [x-1, x+1, x, x]  # LRDU
            elif 0 < x < self.m-1 and y == 0:
                return [x-1, x+1, x]  # LRU
            elif 0 < x < self.m-1 and y == self.n-1:
                return [x-1, x+1, x]  # LRD
            elif x == 0 and 0 < y < self.n-1:
                return [x+1, x, x]  # RDU
            elif x == self.m-1 and 0 < y < self.n-1:
                return [x-1, x, x]  # LDU
            elif x == 0 and y == 0:
                return [x+1, x]  # RU
            elif x == 0 and y == self.n-1:
                return [x+1, x]  # RD
            elif x == self.m-1 and y == 0:
                return [x-1, x]  # LU
            elif x == self.m-1 and y == self.n-1:
                return [x-1, x]  # LD
            else:
                return [0, 0]
        elif self.n == 1:
            if 0 < x < self.m-1:
                return [x-1, x+1]  # LR
            elif x == 0:
                return [x+1]  # RDU
            elif x == self.m-1:
                return [x-1]  # LDU
            else:
                return [0]

    def __points_around_y(self, x, y):
        if 0 < x < self.m-1 and 0 < y < self.n-1:
            return [y, y, y-1, y+1]  # LRDU
        elif 0 < x < self.m-1 and y == 0:
            return [y, y, y+1]  # LRU
        elif 0 < x < self.m-1 and y == self.n-1:
            return [y, y, y-1]  # LRD
        elif x == 0 and 0 < y < self.n-1:
            return [y, y-1, y+1]  # RDU
        elif x == self.m-1 and 0 < y < self.n-1:
            return [y, y-1, y+1]  # LDU
        elif x == 0 and y == 0:
            return [y, y+1]  # RU
        elif x == 0 and y == self.n-1:
            return [y, y-1]  # RD
        elif x == self.m-1 and y == 0:
            return [y, y+1]  # LU
        elif x == self.m-1 and y == self.n-1:
            return [y, y-1]  # LD
        else:
            return [0, 0]

    def set_connectivities(self):
        if not self.__links:
            self.__links = [[] for a in range(self.n*self.m)]
        for a in range(self.n*self.m):
            x_links = self.__points_around_x(a % self.m, a // self.m)
            y_links = self.__points_around_y(a % self.m, a // self.m)
            link_a = []
            for xl, yl in zip(x_links, y_links):
                link_a.append(yl*self.m+xl)
            self.__links[a] = link_a
        # generate frame IDs and end points
        first_name = 0
        for a, b in enumerate(self.__links):
            for c in b:
                if a < c:
                    self.frame_names.append(first_name)
                    self.frame_end_pts.append([a, c])
                    first_name += 1
        # to get frame_names to a point
        for a, b in enumerate(self.__links):
            frames_to_a = []
            for c in b:
                if a < c:
                    frames_to_a.append(
                        self.frame_names[self.frame_end_pts.index([a, c])])
                else:
                    frames_to_a.append(
                        self.frame_names[self.frame_end_pts.index([c, a])])
            self.__linked_frames.append(frames_to_a)
        # print(self.__links)
        # print(self.__linked_frames)

    def set_force_density(self, init_rou, *args):
        if not self.frame_names:
            print("Frames are not initialized...")
            return -1
        for a in self.frame_names:
            self.frame_force_density[a] = init_rou
        for nm, rou in args:
            self.frame_force_density[nm] = rou
        for a, b in enumerate(self.__linked_frames):
            fd_of_a = []
            for c in b:
                fd_of_a.append(self.frame_force_density[c])
            self.__linked_force_densities.append(fd_of_a)
        # print(self.__linked_force_densities)

    def set_fix(self, *args):
        if not self.fix:
            self.fix = [False for a in range(self.n*self.m)]
        for pt in args:
            self.fix[pt[1]*self.m+pt[0]] = True

    def set_init_z(self, *args):
        if not self.init_z:
            self.init_z = [0 for a in range(self.n*self.m)]
        if args:
            for pt in args:
                self.init_z[pt[1]*self.m+pt[0]] = pt[2]

    def set_init_F(self, *args):
        if not self.init_F:
            self.init_F = [0 for a in range(self.n*self.m)]
        if args:
            for pt in args:
                self.init_F[pt[1]*self.m+pt[0]] = pt[2]

    def force_density(self, ret_type="t",
                      SAP2000=False, tolerance=1e-4, *args):

        # initialize data
        # conbined x, y, z coords to a 1d list
        xyz = self.init_x+self.init_y+self.init_z
        n = 3*self.m*self.n  # get the lenght of the 1d list to process
        convergence = [1 for i in range(n)]  # storing convergence numbers
        iter_xyz = list(enumerate(xyz))

        # main
        while sum(convergence)/n > tolerance:
            for w, c in iter_xyz:
                a = w // (self.m*self.n)
                b = w % (self.m*self.n)
                cc = xyz[w]
                if not self.fix[b]:
                    if a == 2:
                        xyz[w] = (-self.init_F[b] +
                                  sum([xyz[a*self.m*self.n+k] * r
                                       for k, r in
                                       zip(self.__links[b],
                                           self.__linked_force_densities[b])])
                                  ) / sum(self.__linked_force_densities[b])
                    else:
                        xyz[w] = (sum([xyz[a*self.m*self.n+k] * r
                                       for k, r in
                                       zip(self.__links[b],
                                           self.__linked_force_densities[b])])
                                  ) / sum(self.__linked_force_densities[b])
                conv_w = abs(xyz[w]-cc)
                if conv_w < tolerance:
                    iter_xyz.remove((w, c))
                convergence[w] = abs(xyz[w]-cc)

        # collecting new coordinats
        X = xyz[:self.m*self.n]
        Y = xyz[self.m*self.n: 2*self.m*self.n]
        Z = xyz[2*self.m*self.n:]

        # to get lenghts of frame elements
        lengths = []
        for ID, frame in zip(self.frame_names, self.frame_end_pts):
            xi, xj = X[frame[0]], X[frame[1]]
            yi, yj = Y[frame[0]], Y[frame[1]]
            zi, zj = Z[frame[0]], Z[frame[1]]
            lengths.append(((xj-xi)**2+(yj-yi)**2+(zj-zi)**2)**0.5)

        # to generate the graphic result
        if ret_type == "g":
            X = np.array(X).reshape(self.n, self.m)
            Y = np.array(Y).reshape(self.n, self.m)
            Z = np.array(Z).reshape(self.n, self.m)
            if self.n > 1:
                fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))
                ls = LightSource(270, 45)
                rgb = ls.shade(Z, cmap=cm.gist_earth,
                               vert_exag=0.1, blend_mode='soft')
                ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
                                facecolors=rgb,
                                linewidth=0,
                                antialiased=False, shade=False)
                plt.show()
            elif self.n == 1:
                fig, ax = plt.subplots()
                ax.plot(X[0], Z[0], linestyle="dashed", linewidth=1, c="r")
                ax.set_xlabel("X")
                ax.set_ylabel("Z")
                ax.set_title("Shape of Rope under Gravity Loading")
                ax.axis("equal")
                for j in range(1, self.m-1):
                    ax.arrow(X[0][j], Z[0][j],
                             0, -self.init_F[j],
                             linewidth=0.1,
                             length_includes_head=False,
                             head_width=0.25, head_length=1,
                             fc="b", ec="b")
                ax.scatter(X[0][0:self.m:self.m-1], Z[0][0:self.m:self.m-1],
                           marker="^", c="black")
                plt.show()

        # or just to get the text result
        elif ret_type == "t":
            ret = [[[]for j in range(self.m)] for i in range(self.n)]
            for i in range(self.n):
                for j in range(self.m):
                    for k in (0, 1, 2):
                        ret[i][j].append(xyz[k*self.m*self.n+i*self.m+j])
            print("Following is the deformed joint coordinates:")
            print(np.array(ret[::-1]))

        # to bake the model to SAP2000
        if SAP2000:
            try:
                mySapObject = comtypes.client.GetActiveObject(
                    "CSI.SAP2000.API.SapObject")
                print("Attached to the running SAP instance...")
            except (OSError, comtypes.COMError):
                print("No running instance of the program found.")
                sys.exit(-1)
            SapModel = mySapObject.SapModel
            print("Start baking to SAP2000...")
            # bake points
            print("--baking points")
            for i in range(self.n):
                for j in range(self.m):
                    SapModel.PointObj.AddCartesian(xyz[i*self.m+j],
                                                   xyz[self.m*self.n +
                                                       i*self.m+j],
                                                   xyz[2*self.m*self.n +
                                                       i*self.m+j],
                                                   str(i*self.m+j),
                                                   str(i*self.m+j))
            # define material and tendon section
            print("--defining material and tendon section")
            Country, code, mat_type, sec_dia = args
            SapModel.PropMaterial.AddMaterial("tendon", 7, Country,
                                              code, mat_type, "tendon")
            SapModel.PropFrame.SetCircle("T", "tendon", sec_dia)
            # bake frames
            print("--baking frames")
            for nm, ij in zip(self.frame_names, self.frame_end_pts):
                SapModel.FrameObj.AddByPoint(str(ij[0]), str(ij[1]), str(nm),
                                             "T", str(nm))
            # bake constrains
            print("--baking constrains")
            for a, b in enumerate(self.fix):
                if b:
                    SapModel.PointObj.setRestraint(str(a), [1, 1, 1, 0, 0, 0])
            # define pre-cooling temp of each frame
            # T = ρL/(EAα) , so the stiffness K = EA/L=ρ/(Tα)
            print("--baking pre-temp and pre-loading")
            Young, thermal = SapModel.PropMaterial.GetMPUniaxial("tendon")[:-1]
            sec_area = SapModel.PropFrame.GetSectProps("T")[0]
            pre_temp = [-self.frame_force_density[z]*i/(Young*sec_area*thermal)
                        for i, z in zip(lengths, self.frame_names)]
            # baking pre_temp
            SapModel.LoadPatterns.Add("Pre_temp", 10)
            for nm, tp in zip(self.frame_names, pre_temp):
                SapModel.FrameObj.SetLoadTemperature(str(nm), "Pre_temp",
                                                     1, tp)
            # baking pre_loading
            SapModel.LoadPatterns.Add("Pre_loading", 8)
            for a, b in enumerate(self.init_F):
                SapModel.PointObj.SetLoadForce(str(a), "Pre_loading",
                                               [0, 0, -b, 0, 0, 0])
            # set turn on the "pre" case
            print("--setting pre NL case")
            SapModel.LoadCases.StaticNonlinear.SetCase("pre")
            SapModel.LoadCases.StaticNonlinear.SetGeometricNonlinearity("pre",
                                                                        2)
            SapModel.LoadCases.StaticNonlinear.SetLoads("pre",
                                                        2,
                                                        ["Load", "Load"],
                                                        ["Pre_temp",
                                                         "Pre_loading"],
                                                        [1, 1])
            ret = SapModel.LoadCases.GetNameList_1()[1]
            for case in ret:
                SapModel.Analyze.SetRunCaseFlag(case, False)
            SapModel.Analyze.SetRunCaseFlag("pre", True)

            print("Baking done.")

        return lengths  # for iterative form finding


if __name__ == "__main__":

    start = time.perf_counter()

    # examples
    # 1d rope
    # m = 100
    # ccc = TwoDShapeFinding(m, 1, 2)
    # ccc.set_fix([0, 0], [m-1, 0])
    # ccc.set_init_F(*[[k, 0, 1] for k in range(1, m-1)])
    # ccc.set_init_z()
    # ccc.set_connectivities()
    # ccc.set_force_density(10)
    # ll1 = ccc.force_density("g", False,  1e-4,
    #                         "China", "JTG", "JTGD62 fpk1470", 0.06)
    # print(ccc.fix)
    # print(ccc.frame_names)
    # print(ccc.frame_end_pts)
    # print(ccc.frame_force_density)
    # print(ccc.init_F)
    # print(ccc.init_x)
    # print(ccc.init_y)
    # print(ccc.init_z)
    # print(ll1)

    # m = 4
    # ccc = TwoDShapeFinding(m, 1, 1)
    # ccc.set_fix([0, 0], [m-1, 0])
    # ccc.set_init_F(*[[k, 0, 1] for k in range(1, m-1)])
    # # ccc.set_init_F()
    # ccc.set_init_z()
    # ccc.set_connectivities()
    # ccc.set_force_density(1)
    # ll1 = ccc.force_density("g", True, 1e-9,
    #                         "China", "JTG", "JTGD62 fpk1470", 0.06)
    # print(ccc.fix)
    # print(ccc.frame_names)
    # print(ccc.frame_end_pts)
    # print(ccc.frame_force_density)
    # print(ccc.init_F)
    # print(ccc.init_x)
    # print(ccc.init_y)
    # print(ccc.init_z)
    # print(ll1)

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
    unit = 0
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
    aaa.set_force_density(10000, [333, -10])
    aaa.force_density("g", True, 1e-8,
                      "China", "JTG", "JTGD62 fpk1470", 0.06)

    end = time.perf_counter()
    print("Run time: {} ms".format((end-start)*1000))
