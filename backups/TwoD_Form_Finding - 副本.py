# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 10:16:02 2022

@author: hh414
"""

# x coordinates: 0, 1, 2, ..., j, ..., m-1
# y coordinates: 0, 1, 2, ..., i, ..., n-1

# coordinates 2d
# (n-1, 0), (n-1, 1), ... , (n-1, j), ... ,(n-1, m-1)
#
# (i, 0),   (i, 1),   ... , (i, j),   ... ,(i, m-1)
#
# (1, 0),   (1, 1),   ... , (1, j),   ... ,(1, m-1)
# (0, 0),   (0, 1),   ... , (0, j),   ... ,(0, m-1)

# coordinates 1d
# 0, 1, ..., j, ..., m-1


from matplotlib import cbook
from matplotlib import cm
from matplotlib.colors import LightSource
import matplotlib.pyplot as plt
import numpy as np


class TwoDShapeFinding():
    def __init__(self, m, n, fix=[], init_z=[], init_F=[], links=[]):
        self.n = n
        self.m = m

        self.init_x = [j for i in range(self.n) for j in range(self.m)]
        self.init_y = [i for i in range(self.n) for j in range(self.m)]
        self.init_z = init_z
        self.init_F = init_F
        self.fix = fix
        self.__links = links

    '''
    def grid_x(self):
        return [j for i in range(self.n) for j in range(self.m)]

    def grid_y(self):
        return [i for i in range(self.n) for j in range(self.m)]
    '''

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

    def force_density(self, rou, tolerance=1e-4, ret_type="t"):

        # conbined x, y, z coords to a 1d list
        xyz = self.init_x+self.init_y+self.init_z
        n = 3*self.m*self.n  # get the lenght of the 1d list to process
        convergence = [1 for i in range(n)]  # storing convergence numbers

        # main
        while sum(convergence)/n > tolerance:
            for w in range(n):
                a = w // (self.m*self.n)
                b = w % (self.m*self.n)
                cc = xyz[w]
                if not self.fix[b]:
                    if a == 2:
                        xyz[w] = (-self.init_F[b]/rou +
                                  sum([xyz[a*self.m*self.n+k]
                                       for k in self.__links[b]]))\
                            / len(self.__links[b])
                    else:
                        xyz[w] = sum([xyz[a*self.m*self.n+k]
                                      for k in self.__links[b]])\
                            / len(self.__links[b])
                convergence[w] = abs(xyz[w]-cc)

        # to generate the graphic result
        if ret_type == "g":
            X = np.array(xyz[:self.m*self.n]).reshape(self.n, self.m)
            Y = np.array(xyz[self.m*self.n: 2*self.m*self.n]
                         ).reshape(self.n, self.m)
            Z = np.array(xyz[2*self.m*self.n:]).reshape(self.n, self.m)
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
                             0, -self.init_F[j]/rou,
                             linewidth=0.1,
                             length_includes_head=False,
                             head_width=0.25/rou, head_length=1/rou,
                             fc="b", ec="b")
                ax.scatter(X[0][0:m:m-1], Z[0][0:m:m-1], marker="^", c="black")
                plt.show()

        # to get the text result
        else:
            ret = [[[]for j in range(self.m)] for i in range(self.n)]
            for i in range(self.n):
                for j in range(self.m):
                    for k in (0, 1, 2):
                        ret[i][j].append(xyz[k*self.m*self.n+i*self.m+j])
            return np.array(ret[::-1])


if __name__ == "__main__":

    # examples
    # 1d rope
    m = 12
    ccc = TwoDShapeFinding(m, 1)
    ccc.set_fix([0, 0], [m-1, 0])
    ccc.set_init_F(*[[k, 0, 1] for k in range(1, m-1)])
    ccc.set_init_F([1, 0, 5], [10, 0, 5])
    ccc.set_init_z()
    ccc.set_connectivities()
    print(ccc.force_density(5, ret_type="g"))

    # 2d net under center load
    ccc = TwoDShapeFinding(5, 5)
    ccc.set_fix([0, 0], [4, 0], [0, 4], [4, 4])
    ccc.set_init_F([2, 2, 1])
    ccc.set_init_z()
    ccc.set_connectivities()
    ccc.force_density(1, ret_type="g")

    # 2d net under end disps
    # ccc = TwoDShapeFinding(29, 29)
    # ccc.set_fix([0, 0], [28, 0], [0, 28], [28, 28])
    # ccc.set_init_F()
    # ccc.set_init_z([0, 0, 1], [28, 28, 1])
    # ccc.set_connectivities()
    # ccc.force_density(0.001, ret_type="g")

    # 2d net under gravity and all 4 side constrained
    # m, n = 29, 29
    # aaa = TwoDShapeFinding(m, n)
    # constrain = []
    # for w in range(m):
    #     for v in range(n):
    #         if v == 0 or v == n-1:
    #             constrain.append([w, v])
    #         else:
    #             if w == 0 or w == m-1:
    #                 constrain.append([w, v])
    # aaa.set_fix(*constrain)
    # loading = []
    # unit = 1
    # for w in range(m):
    #     for v in range(n):
    #         if 0 < v < n-1 and 0 < w < m-1:
    #             loading.append([w, v, unit])
    # aaa.set_init_F(*loading)
    # aaa.set_init_z()
    # aaa.set_connectivities()
    # aaa.force_density(100, ret_type="g")

    # 2d net under pretensioned with all 4 side constrained
    m, n = 29, 29
    aaa = TwoDShapeFinding(m, n)
    constrain = []
    for w in range(m):
        for v in range(n):
            if v == 0 or v == n-1:
                constrain.append([w, v])
            else:
                if w == 0 or w == m-1:
                    constrain.append([w, v])
    aaa.set_fix(*constrain)
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
    aaa.set_init_F([20, 20, 0.5], [10, 10, -0.5])
    aaa.set_init_z(*boundary_z)
    aaa.set_connectivities()
    aaa.force_density(1, ret_type="g")
