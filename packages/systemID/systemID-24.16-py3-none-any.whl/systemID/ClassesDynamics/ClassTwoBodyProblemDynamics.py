"""
Author: Damien GUEHO
Copyright: Copyright (C) 2023 Damien GUEHO
License: Public Domain
Version: 24
Date: April 2022
Python: 3.7.7
"""



import numpy as np
import scipy.linalg as LA


class TwoBodyProblemDynamicsCartesian:
    def __init__(self, mu):
        self.state_dimension = 6
        self.input_dimension = 3
        self.output_dimension = 6
        self.mu = mu

    def F(self, x, t, u):
        dxdt = np.zeros(6)
        r = LA.norm(x[0:3])
        dxdt[0] = x[3]
        dxdt[1] = x[4]
        dxdt[2] = x[5]
        dxdt[3] = -self.mu(t) * x[0] / (r ** 3) + u(t)[0]
        dxdt[4] = -self.mu(t) * x[1] / (r ** 3) + u(t)[1]
        dxdt[5] = -self.mu(t) * x[2] / (r ** 3) + u(t)[2]
        return dxdt

    def G(self, x, t, u):
        return x

    def Ac1(self, x, t, u):
        Ac1 = np.zeros([self.state_dimension, self.state_dimension])
        r = LA.norm(x[0:3])
        Ac1[3, 0] = self.mu(t) * (2 * x[0] ** 2 - x[1] ** 2 - x[2] ** 2) / r ** 5
        Ac1[4, 0] = 3 * self.mu(t) * x[0] * x[1] / r ** 5
        Ac1[5, 0] = 3 * self.mu(t) * x[0] * x[2] / r ** 5
        Ac1[3, 1] = 3 * self.mu(t) * x[0] * x[1] / r ** 5
        Ac1[4, 1] = self.mu(t) * (-x[0] ** 2 + 2 * x[1] ** 2 - x[2] ** 2) / r ** 5
        Ac1[5, 1] = 3 * self.mu(t) * x[1] * x[2] / r ** 5
        Ac1[3, 2] = 3 * self.mu(t) * x[0] * x[2] / r ** 5
        Ac1[4, 2] = 3 * self.mu(t) * x[1] * x[2] / r ** 5
        Ac1[5, 2] = self.mu(t) * (-x[0] ** 2 - x[1] ** 2 + 2 * x[2] ** 2) / r ** 5
        Ac1[0, 3] = 1
        Ac1[1, 4] = 1
        Ac1[2, 5] = 1
        return Ac1

    def Ac2(self, x, t, u):
        Ac2 = np.zeros([self.state_dimension, self.state_dimension, self.state_dimension])
        r = LA.norm(x[0:3])
        Ac2[3, 0, 0] = 3 * self.mu(t) * x[0] * (- 2 * x[0] ** 2 + 3 * x[1] ** 2 + 3 * x[2] ** 2) / r ** 7
        Ac2[4, 0, 0] = 3 * self.mu(t) * x[1] * (-4 * x[0] ** 2 + x[1] ** 2 + x[2] ** 2) / r ** 7
        Ac2[5, 0, 0] = 3 * self.mu(t) * x[2] * (-4 * x[0] ** 2 + x[1] ** 2 + x[2] ** 2) / r ** 7
        Ac2[3, 1, 0] = 3 * self.mu(t) * x[1] * (-4 * x[0] ** 2 + x[1] ** 2 + x[2] ** 2) / r ** 7
        Ac2[4, 1, 0] = 3 * self.mu(t) * x[0] * (x[0] ** 2 - 4 * x[1] ** 2 + x[2] ** 2) / r ** 7
        Ac2[5, 1, 0] = - 15 * self.mu(t) * x[0] * x[1] * x[2] / r ** 7
        Ac2[3, 2, 0] = 3 * self.mu(t) * x[2] * (-4 * x[0] ** 2 + x[1] ** 2 + x[2] ** 2) / r ** 7
        Ac2[4, 2, 0] = - 15 * self.mu(t) * x[0] * x[1] * x[2] / r ** 7
        Ac2[5, 2, 0] = 3 * self.mu(t) * x[0] * (x[0] ** 2 + x[1] ** 2 - 4 * x[2] ** 2) / r ** 7
        Ac2[3, 0, 1] = 3 * self.mu(t) * x[1] * (-4 * x[0] ** 2 + x[1] ** 2 + x[2] ** 2) / r ** 7
        Ac2[4, 0, 1] = 3 * self.mu(t) * x[0] * (x[0] ** 2 - 4 * x[1] ** 2 + x[2] ** 2) / r ** 7
        Ac2[5, 0, 1] = - 15 * self.mu(t) * x[0] * x[1] * x[2] / r ** 7
        Ac2[3, 1, 1] = 3 * self.mu(t) * x[0] * (x[0] ** 2 - 4 * x[1] ** 2 + x[2] ** 2) / r ** 7
        Ac2[4, 1, 1] = 3 * self.mu(t) * x[1] * (3 * x[0] ** 2 - 2 * x[1] ** 2 + 3 * x[2] ** 2) / r ** 7
        Ac2[5, 1, 1] = 3 * self.mu(t) * x[2] * (x[0] ** 2 - 4 * x[1] ** 2 + x[2] ** 2) / r ** 7
        Ac2[3, 2, 1] = - 15 * self.mu(t) * x[0] * x[1] * x[2] / r ** 7
        Ac2[4, 2, 1] = 3 * self.mu(t) * x[2] * (x[0] ** 2 - 4 * x[1] ** 2 + x[2] ** 2) / r ** 7
        Ac2[5, 2, 1] = 3 * self.mu(t) * x[1] * (x[0] ** 2 + x[1] ** 2 - 4 * x[2] ** 2) / r ** 7
        Ac2[3, 0, 2] = 3 * self.mu(t) * x[2] * (-4 * x[0] ** 2 + x[1] ** 2 + x[2] ** 2) / r ** 7
        Ac2[4, 0, 2] = - 15 * self.mu(t) * x[0] * x[1] * x[2] / r ** 7
        Ac2[5, 0, 2] = 3 * self.mu(t) * x[0] * (x[0] ** 2 + x[1] ** 2 - 4 * x[2] ** 2) / r ** 7
        Ac2[3, 1, 2] = - 15 * self.mu(t) * x[0] * x[1] * x[2] / r ** 7
        Ac2[4, 1, 2] = 3 * self.mu(t) * x[2] * (x[0] ** 2 - 4 * x[1] ** 2 + x[2] ** 2) / r ** 7
        Ac2[5, 1, 2] = 3 * self.mu(t) * x[1] * (x[0] ** 2 + x[1] ** 2 - 4 * x[2] ** 2) / r ** 7
        Ac2[3, 2, 2] = 3 * self.mu(t) * x[0] * (x[0] ** 2 + x[1] ** 2 - 4 * x[2] ** 2) / r ** 7
        Ac2[4, 2, 2] = 3 * self.mu(t) * x[1] * (x[0] ** 2 + x[1] ** 2 - 4 * x[2] ** 2) / r ** 7
        Ac2[5, 2, 2] = 3 * self.mu(t) * x[2] * (3 * x[0] ** 2 + 3 * x[1] ** 2 - 2 * x[2] ** 2) / r ** 7
        return Ac2



class TwoBodyProblemDynamicsPolar:
    def __init__(self, mu):
        self.state_dimension = 4
        self.input_dimension = 2
        self.output_dimension = 4
        self.mu = mu

    def F(self, x, t, u):
        dxdt = np.zeros(4)
        dxdt[0] = x[2]
        dxdt[1] = x[3]
        dxdt[2] = -self.mu(t) / (x[0] ** 2) + x[0] * x[3] ** 2
        dxdt[3] = -2 * x[2] * x[3] / x[0]
        return dxdt

    def G(self, x, t, u):
        return x

    def Ac1(self, x, t, u):
        Ac1 = np.zeros([self.state_dimension, self.state_dimension])
        Ac1[0, 2] = 1
        Ac1[1, 3] = 1
        Ac1[2, 0] = 2 * self.mu(t) / (x[0] ** 3) + x[3] ** 2
        Ac1[2, 3] = 2 * x[0] * x[3]
        Ac1[3, 0] = 2 * x[2] * x[3] / (x[0] ** 2)
        Ac1[3, 2] = -2 * x[3] / x[0]
        Ac1[3, 3] = -2 * x[2] / x[0]
        return Ac1

    def Ac2(self, x, t, u):
        Ac2 = np.zeros([self.state_dimension, self.state_dimension, self.state_dimension])
        Ac2[2, 0, 0] = -6 * self.mu(t) / (x[0] ** 4)
        Ac2[2, 3, 0] = 2 * x[3]
        Ac2[3, 0, 0] = -4 * x[2] * x[3] / (x[0] ** 3)
        Ac2[3, 2, 0] = 2 * x[3] / (x[0] ** 2)
        Ac2[3, 3, 0] = 2 * x[2] / (x[0] ** 2)
        Ac2[3, 0, 2] = 2 * x[3] / (x[0] ** 2)
        Ac2[3, 3, 2] = -2 / x[0]
        Ac2[2, 0, 3] = 2 * x[3]
        Ac2[2, 3, 3] = 2 * x[0]
        Ac2[3, 0, 3] = 2 * x[2] / (x[0] ** 2)
        Ac2[3, 2, 3] = -2 / x[0]
        return Ac2

    def Ac3(self, x, t, u):
        Ac3 = np.zeros([self.state_dimension, self.state_dimension, self.state_dimension, self.state_dimension])
        Ac3[2, 0, 0, 0] = 24 * self.mu(t) / (x[0] ** 5)
        Ac3[3, 0, 0, 0] = 12 * x[2] * x[3] / (x[0] ** 4)
        Ac3[3, 2, 0, 0] = -4 * x[3] / (x[0] ** 3)
        Ac3[3, 3, 0, 0] = -4 * x[2] / (x[0] ** 3)
        Ac3[3, 0, 2, 0] = -4 * x[3] / (x[0] ** 3)
        Ac3[3, 3, 2, 0] = 2 / (x[0] ** 2)
        Ac3[2, 3, 3, 0] = 2
        Ac3[3, 0, 3, 0] = -4 * x[2] / (x[0] ** 3)
        Ac3[3, 2, 3, 0] = 2 / (x[0] ** 2)
        Ac3[3, 0, 0, 2] = -4 * x[3] / (x[0] ** 3)
        Ac3[3, 3, 0, 2] = 2 / (x[0] ** 2)
        Ac3[3, 0, 3, 2] = 2 / (x[0] ** 2)
        Ac3[2, 3, 0, 3] = 2
        Ac3[3, 0, 0, 3] = -4 * x[2] / (x[0] ** 3)
        Ac3[3, 2, 0, 3] = 2 / (x[0] ** 2)
        Ac3[3, 0, 2, 3] = 2 / (x[0] ** 2)
        Ac3[2, 0, 3, 3] = 2
        return Ac3

    def Ac4(self, x, t, u):
        Ac4 = np.zeros([self.state_dimension, self.state_dimension, self.state_dimension, self.state_dimension, self.state_dimension])
        Ac4[2, 0, 0, 0, 0] = -120 * self.mu(t) / (x[0] ** 6)
        Ac4[3, 0, 0, 0, 0] = -48 * x[2] * x[3] / (x[0] ** 5)
        Ac4[3, 2, 0, 0, 0] = 12 * x[3] / (x[0] ** 4)
        Ac4[3, 3, 0, 0, 0] = 12 * x[2] / (x[0] ** 4)
        Ac4[3, 0, 2, 0, 0] = 12 * x[3] / (x[0] ** 4)
        Ac4[3, 3, 2, 0, 0] = -4 / (x[0] ** 3)
        Ac4[3, 0, 3, 0, 0] = 12 * x[2] / (x[0] ** 4)
        Ac4[3, 2, 3, 0, 0] = -4 / (x[0] ** 3)
        Ac4[3, 0, 0, 2, 0] = 12 * x[3] / (x[0] ** 4)
        Ac4[3, 3, 0, 2, 0] = -4 / (x[0] ** 3)
        Ac4[3, 0, 3, 2, 0] = -4 / (x[0] ** 3)
        Ac4[3, 0, 0, 3, 0] = 12 * x[2] / (x[0] ** 4)
        Ac4[3, 2, 0, 3, 0] = -4 / (x[0] ** 3)
        Ac4[3, 0, 2, 3, 0] = -4 / (x[0] ** 3)
        Ac4[3, 0, 0, 0, 2] = 12 * x[3] / (x[0] ** 4)
        Ac4[3, 3, 0, 0, 2] = -4 / (x[0] ** 3)
        Ac4[3, 0, 3, 0, 2] = -4 / (x[0] ** 3)
        Ac4[3, 0, 0, 3, 2] = -4 / (x[0] ** 3)
        Ac4[3, 0, 0, 0, 3] = 12 * x[2] / (x[0] ** 4)
        Ac4[3, 2, 0, 0, 3] = -4 / (x[0] ** 3)
        Ac4[3, 0, 2, 0, 3] = -4 / (x[0] ** 3)
        Ac4[3, 0, 0, 2, 3] = -4 / (x[0] ** 3)
        return Ac4
