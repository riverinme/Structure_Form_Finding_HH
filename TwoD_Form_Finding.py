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
    def __init__(self, m, n, size, init_fr_sap=False):
        self.n = n
        self.m = m
        self.s = size
        self.sap = init_fr_sap

        self.init_z = []  # init Z coords in global sys
        self.init_F = []  # init point load in gravity dir
        self.fix = []  # store point constrain
        self.__links = []  # store sub lists of points next to a point
        self.frame_names = []  # store frame names/ID/labels
        self.frame_end_pts = []  # store frame end points
        # store frame force density
        self.frame_force_density = {}
        self.__linked_frames = []  # store sub lists of frames next to a point
        # store sub lists of force densities of frames next to a point
        self.__linked_force_densities = []
        if init_fr_sap:
            try:
                mySapObject = comtypes.client.GetActiveObject(
                    "CSI.SAP2000.API.SapObject")
                print("Attached to the running SAP instance...")
            except (OSError, comtypes.COMError):
                print("No running instance of the program found.")
                sys.exit(-1)
            self.SapModel = mySapObject.SapModel
            # Unlock the model first
            self.SapModel.SetModelIsLocked(False)

            # store sap point labels
            self.point_names = []
            # store point x coords and y coords
            self.init_x = []
            self.init_y = []
            # store frame [E, A]
            self.frame_prpt = {}
            # store pre_loading case
            self.pre_loading = ""
        else:
            # store point x sequences and y sequences
            self.init_x = [j*self.s for i in range(self.n)
                           for j in range(self.m)]
            self.init_y = [i*self.s for i in range(self.n)
                           for j in range(self.m)]

    def init_fr_sap2000(self, pre_loading, Country, code, mat_type, sap_mat_ID,
                        sec_dia, init_rou,
                        *args, group="ALL"):

        # init frames and points
        self.SapModel.SelectObj.Group(group)
        ret = self.SapModel.SelectObj.GetSelected()
        self.SapModel.SelectObj.ClearSelection()
        self.frame_names.clear()
        for i in range(ret[0]):
            if ret[1][i] == 2:
                self.frame_names.append(ret[2][i])
            elif ret[1][i] == 1:
                self.point_names.append(ret[2][i])
        # use point sequences instead of point labels
        point_seq = [k for k, i in enumerate(self.point_names)]

        # init boundary conditions fr sap
        self.fix.clear()
        for i in self.point_names:
            ret = self.SapModel.PointObj.GetRestraint(i)
            if ret[0][:3] == (True, True, True):
                self.fix.append(True)
            else:
                self.fix.append(False)

        # init frame_end_pts:
        self.frame_end_pts.clear()
        for i in self.frame_names:
            ret = self.SapModel.FrameObj.GetPoints(i)
            seq0 = point_seq[self.point_names.index(ret[0])]
            seq1 = point_seq[self.point_names.index(ret[1])]
            self.frame_end_pts.append([seq0, seq1])

        # init self.__links
        self.__links.clear()
        self.__linked_frames.clear()
        for i, k in zip(self.point_names, point_seq):
            ret = self.SapModel.PointObj.GetConnectivity(i)
            link_a = []
            frames_to_a = []
            for j in range(ret[0]):
                if ret[1][j] == 2:
                    frames_to_a.append(ret[2][j])
                    fr_index = self.frame_names.index(ret[2][j])
                    if self.frame_end_pts[fr_index][0] == k:
                        link_a.append(self.frame_end_pts[fr_index][1])
                    else:
                        link_a.append(self.frame_end_pts[fr_index][0])
            self.__links.append(link_a)
            self.__linked_frames.append(frames_to_a)

        # init_X, Y, Z
        self.init_x.clear()
        self.init_y.clear()
        self.init_z.clear()
        for i in self.point_names:
            ret = self.SapModel.PointObj.GetCoordCartesian(i)
            self.init_x.append(ret[0])
            self.init_y.append(ret[1])
            self.init_z.append(ret[2])

        # sap_mat_ID = 7 tendon or 2 concrete or 1 steel
        # define default material and tendon section
        print("--defining material and tendon section")
        self.SapModel.PropMaterial.AddMaterial("mat_default", sap_mat_ID,
                                               Country,
                                               code, mat_type,
                                               "mat_default")
        self.SapModel.PropFrame.SetCircle(
            "sec_default", "mat_default", sec_dia)

        # assign default frame sections.
        print("--assigning frame sections...")
        for i in self.frame_names:
            self.SapModel.FrameObj.SetSection(i, "sec_default")

        # obtain default mat and frame prpt
        if sap_mat_ID == 7:
            Young, thermal = self.SapModel.PropMaterial.GetMPUniaxial(
                "mat_default")[:-1]
        elif sap_mat_ID == 2 or sap_mat_ID == 1:
            ret = self.SapModel.PropMaterial.GetMPIsotropic("mat_default")[:-2]
            Young = ret[0]
            thermal = ret[2]
        sec_area = self.SapModel.PropFrame.GetSectProps("sec_default")[0]

        # assign default frame force density
        self.frame_force_density.clear()
        self.frame_prpt.clear()
        for a in self.frame_names:
            self.frame_force_density[a] = init_rou
            self.frame_prpt[a] = [Young, sec_area, thermal]

        # get preloading, gravity is positive.
        self.init_F.clear()
        self.pre_loading = pre_loading
        for pt in self.point_names:
            try:
                ret = self.SapModel.PointObj.GetLoadForce(pt)
                for i in range(ret[0]):
                    if ret[2][i] == self.pre_loading:
                        self.init_F.append(-ret[7][i])
            except Exception:
                self.init_F.append(0)

        # define addtional material and tendon sections
        for gp in args:
            gp1, Cty1, cd1, mt1, sm1, sd1, ir1 = gp
            print("----processing special group {}".format(gp1))
            self.SapModel.SelectObj.Group(gp1)
            ret = self.SapModel.SelectObj.GetSelected()
            self.SapModel.SelectObj.ClearSelection()
            frames_gp = []
            for i in range(ret[0]):
                if ret[1][i] == 2:
                    frames_gp.append(ret[2][i])
            self.SapModel.PropMaterial.AddMaterial("mat_{}".format(gp1),
                                                   sm1,
                                                   Cty1,
                                                   cd1, mt1,
                                                   "mat_{}".format(gp1))
            self.SapModel.PropFrame.SetCircle(
                "sec__{}".format(gp1), "mat_{}".format(gp1), sd1)
            if sm1 == 7:
                Y, th = self.SapModel.PropMaterial.GetMPUniaxial(
                    "mat_{}".format(gp1))[:-1]
            elif sm1 == 2 or sm1 == 1:
                ret = self.SapModel.PropMaterial.GetMPIsotropic("mat_{}".
                                                                format(gp1))[
                                                                    :-2]
                Y = ret[0]
                th = ret[2]
            sa = self.SapModel.PropFrame.GetSectProps("sec__{}".
                                                      format(gp1))[0]
            for a in frames_gp:
                self.frame_force_density[a] = ir1
                self.frame_prpt[a] = [Y, sa, th]
                self.SapModel.FrameObj.SetSection(a, "sec__{}".format(gp1))

        # init force_desities for running
        for a, b in enumerate(self.__linked_frames):
            fd_of_a = []
            for c in b:
                fd_of_a.append(self.frame_force_density[c])
            self.__linked_force_densities.append(fd_of_a)

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

    def set_force_density(self, init_rou, *args):
        if not self.frame_names:
            print("Frames are not initialized...")
            return -1
        self.frame_force_density.clear()
        for a in self.frame_names:
            self.frame_force_density[a] = init_rou
        for nm, rou in args:
            self.frame_force_density[nm] = rou
        for a, b in enumerate(self.__linked_frames):
            fd_of_a = []
            for c in b:
                fd_of_a.append(self.frame_force_density[c])
            self.__linked_force_densities.append(fd_of_a)

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

    def force_density(self, ret_type, to_sap, *args,
                      tolerance=1e-9, remove=True):

        # initialize data
        # conbined x, y, z coords to a 1d list
        xyz = self.init_x+self.init_y+self.init_z
        n = len(xyz)
        iter_xyz = list(enumerate(xyz))

        # storing convergence numbers
        convergence = [1 for i in range(n)]

        # main
        print("Analysing...")
        count = 1
        while sum(convergence)/n > tolerance:
            if count % 100 == 0:
                print("--step {}, convergence = {}".format(count,
                                                           sum(convergence)/n))
            for w, c in iter_xyz:
                a = w // (n//3)
                b = w % (n//3)
                cc = xyz[w]
                if not self.fix[b]:
                    if a == 2:
                        xyz[w] = (-self.init_F[b] +
                                  sum([xyz[a*n//3+k] * r
                                       for k, r in
                                       zip(self.__links[b],
                                           self.__linked_force_densities[b])])
                                  ) / sum(self.__linked_force_densities[b])
                    else:
                        xyz[w] = (sum([xyz[a*n//3+k] * r
                                       for k, r in
                                       zip(self.__links[b],
                                           self.__linked_force_densities[b])])
                                  ) / sum(self.__linked_force_densities[b])
                conv_w = abs(xyz[w]-cc)
                if conv_w < tolerance and remove:
                    iter_xyz.remove((w, c))
                convergence[w] = conv_w
                count += 1
        print("--step {}, convergence = {}".format(count, sum(convergence)/n))

        # collecting new coordinats
        X = xyz[:n//3]
        Y = xyz[n//3: 2*n//3]
        Z = xyz[2*n//3:]

        # to get lenghts of frame elements after form finding
        lengths = []
        for ID, frame in zip(self.frame_names, self.frame_end_pts):
            xi, xj = X[frame[0]], X[frame[1]]
            yi, yj = Y[frame[0]], Y[frame[1]]
            zi, zj = Z[frame[0]], Z[frame[1]]
            lengths.append(((xj-xi)**2+(yj-yi)**2+(zj-zi)**2)**0.5)

        # to generate the graphic result if not init fr sap
        if not self.sap:
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
                    # ax.set_xlabel("X")
                    # ax.set_ylabel("Z")
                    # ax.set_title("Shape of Rope under Gravity Loading")
                    ax.axis("equal")
                    for j in range(1, self.m-1):
                        ax.arrow(X[0][j], Z[0][j],
                                 0, -self.init_F[j],
                                 linewidth=0.1,
                                 length_includes_head=False,
                                 head_width=self.init_F[j]/4,
                                 head_length=self.init_F[j]/2,
                                 fc="b", ec="b")
                    ax.scatter(X[0][0:self.m:self.m-1],
                               Z[0][0:self.m:self.m-1],
                               marker="^", c="black")
                    plt.axis("off")
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
        if to_sap or self.sap:
            if not self.sap:  # if not mod from an existing sap...
                # sap_mat_ID = 7 tendon or 2 concrete or 1 steel
                Country, code, mat_type, sap_mat_ID, sec_dia = args
                try:
                    mySapObject = comtypes.client.GetActiveObject(
                        "CSI.SAP2000.API.SapObject")
                    print("Attached to the running SAP instance...")
                except (OSError, comtypes.COMError):
                    print("No running instance of the program found.")
                    sys.exit(-1)
                SapModel = mySapObject.SapModel
                print("Start baking to SAP2000...")

                # start a new model
                SapModel.InitializeNewModel(6)
                SapModel.File.NewBlank()

                # define material and tendon section
                print("--defining material and tendon section")
                SapModel.PropMaterial.AddMaterial("tendon", sap_mat_ID,
                                                  Country,
                                                  code, mat_type, "tendon")
                SapModel.PropFrame.SetCircle("T", "tendon", sec_dia)

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

                # bake frames
                print("--baking frames")
                for nm, ij in zip(self.frame_names, self.frame_end_pts):
                    SapModel.FrameObj.AddByPoint(str(ij[0]), str(ij[1]),
                                                 str(nm),
                                                 "T", str(nm))

                # bake constrains
                print("--baking constrains")
                for a, b in enumerate(self.fix):
                    if b:
                        SapModel.PointObj.setRestraint(str(a), [1, 1, 1,
                                                                0, 0, 0])

                # baking pre_loading
                print("--baking pre-loading")
                SapModel.LoadPatterns.Add("Pre_loading", 8)
                for a, b in enumerate(self.init_F):
                    SapModel.PointObj.SetLoadForce(str(a), "Pre_loading",
                                                   [0, 0, -b, 0, 0, 0])

                # obtain prpts
                if sap_mat_ID == 7:
                    Young, thermal = SapModel.PropMaterial.GetMPUniaxial(
                        "tendon")[:-1]
                elif sap_mat_ID == 2 or sap_mat_ID == 1:
                    ret = SapModel.PropMaterial.GetMPIsotropic("tendon")[:-2]
                    Young = ret[0]
                    thermal = ret[2]
                sec_area = SapModel.PropFrame.GetSectProps("T")[0]

                # define pre-cooling temp of each frame
                # T = ρL/(EAα) , so the stiffness K = EA/L=ρ/(Tα)
                print("--baking pre-temp")
                pre_temp = [-self.frame_force_density[z]*i/(Young *
                                                            sec_area*thermal)
                            for i, z in zip(lengths, self.frame_names)]

            else:
                SapModel = self.SapModel

                # define pre-cooling temp of each frame
                # T = ρL/(EAα) , so the stiffness K = EA/L=ρ/(Tα)
                print("--baking pre-temp")
                pre_temp = []
                for i, z in zip(lengths, self.frame_names):
                    d = self.frame_force_density[z]
                    Young, sec_area, thermal = self.frame_prpt[z]
                    pre_temp.append(-d*i/(Young*sec_area*thermal))

                # Move original points to new pos.
                print("--moving pre points to new positions")
                for i, pt in enumerate(self.point_names):
                    SapModel.EditPoint.ChangeCoordinates_1(
                        pt, X[i], Y[i], Z[i])

            # baking pre_temp
            SapModel.LoadPatterns.Add("Pre_temp", 10)
            for nm, tp in zip(self.frame_names, pre_temp):
                SapModel.FrameObj.DeleteLoadTemperature(str(nm), "Pre_temp")
                SapModel.FrameObj.SetLoadTemperature(str(nm), "Pre_temp",
                                                     1, tp)

            # set turn on the "pre" case
            print("--setting pre NL case")
            SapModel.LoadCases.StaticNonlinear.SetCase("pre")
            SapModel.LoadCases.StaticNonlinear.SetGeometricNonlinearity("pre",
                                                                        2)

            # calibrate pre loading pattern name
            if self.sap:
                prel = self.pre_loading
            else:
                prel = "Pre_loading"

            # turn on the pre stress NL case
            SapModel.LoadCases.StaticNonlinear.SetLoads("pre",
                                                        2,
                                                        ["Load", "Load"],
                                                        ["Pre_temp",
                                                         prel],
                                                        [1, 1])
            ret = SapModel.LoadCases.GetNameList_1()[1]
            for case in ret:
                SapModel.Analyze.SetRunCaseFlag(case, False)
            SapModel.Analyze.SetRunCaseFlag("pre", True)
            SapModel.View.RefreshView()
            print("Baking done.")

        return lengths  # for iterative form finding


def mass_assign(SapModel, dead_case_substitute, group="ALL"):
    # 1, manualy mesh frames into segments like 5 or 10 segs.
    # 2, run the default "DEAD" case to get mass data
    # **note, mass source shall be defined to include all load patterns needed
    SapModel.SetModelIsLocked(False)
    ret = SapModel.LoadCases.GetNameList_1()[1]
    for case in ret:
        SapModel.Analyze.SetRunCaseFlag(case, False)
    SapModel.Analyze.SetRunCaseFlag("DEAD", True)
    SapModel.Analyze.RunAnalysis()
    # 3, get mass of each node
    SapModel.SelectObj.Group(group)
    ret = SapModel.SelectObj.GetSelected()
    SapModel.SelectObj.ClearSelection()
    points = []
    masses = []
    for i in range(ret[0]):
        if ret[1][i] == 1:
            points.append(ret[2][i])
    masses = []
    for i in points:
        ret = SapModel.Results.AssembledJointMass_1("MSSSRC1", i, 0)
        masses.append(ret[3][0])
    # 4, creat another case using masses fr step 3 to simulate dead
    SapModel.SetModelIsLocked(False)
    # 8 means "other" pattern
    SapModel.LoadPatterns.Add(dead_case_substitute, 8)
    for pt, ms in zip(points, masses):
        SapModel.PointObj.DeleteLoadForce(pt, dead_case_substitute)
        SapModel.PointObj.SetLoadForce(pt,  dead_case_substitute,
                                       [0, 0, -ms*9.80665019960652, 0, 0, 0])
    SapModel.Analyze.SetRunCaseFlag(dead_case_substitute, True)
    # SapModel.Analyze.RunAnalysis()
    return dead_case_substitute


if __name__ == "__main__":

    start = time.perf_counter()

    # example_ init from SAP2000
    # aaa = TwoDShapeFinding(1, 3, 1, init_fr_sap=True)
    # aaa.init_fr_sap2000()
    # aaa.set_force_density(1, ["3", 1])
    # aaa.set_init_F(["2", 3], ["3", 5], ["4", 2])
    # ll1 = aaa.force_density(1e-9, "g", False,
    #                         "China", "JTG", "JTGD62 fpk1470", 7, 0.06)

    end = time.perf_counter()
    print("Run time: {:.2f} ms".format((end-start)*1000))
