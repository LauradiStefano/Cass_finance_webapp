# -*- coding: utf-8 -*-
"""
Created on Tue May 28 09:36:56 2019

@author: Diego
"""
import numpy as np


def Power(x, y):
    out = x ** y

    return out


def get_heston_moment(x0, v0, mu, alpha, beta, eta, rho, timestep):
    r = mu

    central = 1

    # powers of parameters
    x02 = x0 ** 2
    x03 = x0 ** 3
    v02 = v0 ** 2
    r2 = r ** 2  # mu
    r3 = r ** 3
    sg2 = eta ** 2  # etaT
    sg3 = eta ** 3
    sg4 = eta ** 4
    k2 = alpha ** 2  # alpka
    k3 = alpha ** 3
    k4 = alpha ** 4
    k5 = alpha ** 5
    k6 = alpha ** 6
    k7 = alpha ** 7
    th2 = beta ** 2  # beta
    th3 = beta ** 3

    rho2 = rho ** 2  # rho
    rho3 = rho ** 3

    # First moment
    m1_list = []
    m2_list = []
    m3_list = []
    m4_list = []
    for j in range(0, len(timestep)):
        tau = timestep[j]
        tau2 = timestep[j] ** 2
        tau3 = timestep[j] ** 3
        m1 = x0 + (r - beta / 2) * tau + (beta - v0) * (1 - np.exp(-alpha * tau)) / (2 * alpha)
        m1_list.append(m1)

        # Second moment
        m2 = (sg2 * (beta - 2 * v0) + 2 * alpha * (beta - v0) ** 2 + 4 * np.exp(alpha * tau) *
              (sg2 * beta - alpha * (rho * eta * (4 * beta - 2 * v0) + (beta - v0) * (-(sg2 * tau) + beta - v0)) + k2
               * (beta - v0) * (2 - 2 * r * tau - 2 * rho * eta * tau + tau * beta - 2 * x0)) + np.exp(2 * alpha * tau)
              * (2 * alpha * (sg2 * tau * beta + rho * eta * (8 * beta - 4 * v0) + (beta - v0) ** 2) + sg2 *
                 (- 5 * beta + 2 * v0) + 2 * k3 * (4 * (r * tau) ** 2 + (tau * beta) ** 2 - 4 * r * tau *
                                                   (tau * beta - 2 * x0) - 4 * tau * beta * (-1 + x0) + 4 * x0 ** 2) - 4
                 * k2 * (tau * th2 + 2 * v0 * (-1 + r * tau + x0) - beta *
                         (- 2 + 2 * r * tau - 2 * rho * eta * tau + tau * v0 + 2 * x0)))) / (
                         8. * np.exp(2 * alpha * tau)
                         * k3)
        m2_list.append(m2)
        # Third moment
        m3 = (-(sg4 * (beta - 3 * v0)) - 2 * k2 * (beta - v0) ** 3 - 3 * alpha * sg2 * (th2 - 3 * beta * v0 + 2 * v02) +
              3 * np.exp(alpha * tau) * (2 * sg4 * (-beta + v0) + alpha * sg2 * (-3 * th2 + 4 * rho * eta *
                                                                                 (2 * beta - 3 * v0) - 2 * sg2 * tau *
                                                                                 (
                                                                                             beta - 2 * v0) + beta * v0 + 2 * v02) -
                                         2 * k3 * (beta - v0) ** 2 *
                                         (4 - 2 * r * tau - 4 * rho * eta * tau + tau * beta - 2 * x0) + k2 *
                                         (4 * rho * sg3 * tau * (beta - 2 * v0) + 2 * (beta - v0) ** 3 + 8 * rho * eta *
                                          (2 * th2 - 3 * beta * v0 + v02) + sg2 *
                                          (-5 * tau * th2 - 4 * v0 * (- 2 + r * tau + tau * v0 + x0) + 2 * beta *
                                           (-2 + r * tau + 5 * tau * v0 + x0)))) + np.exp(3 * alpha * tau) *
              (2 * sg4 * (11 * beta - 3 * v0) - 3 * alpha * sg2 * (2 * sg2 * tau * beta + 5 * th2 + 4 * rho * eta *
                                                                   (10 * beta - 3 * v0) - 7 * beta * v0 + 2 * v02) + 6 *
               k4 * (4 * r2 * tau2 * (beta - v0) - 4 * r * tau * (tau * th2 + beta * (2 + 2 * rho * eta * tau - tau * v0
                                                                                      - 2 * x0) + 2 * v0 * (
                                                                              -1 + x0)) + 4
                     * rho * eta * tau * beta * (2 + tau * beta - 2 * x0) + (beta - v0) *
                     (tau2 * th2 - 4 * tau * beta * (- 2 + x0) + 4 * (-2 + x0) * x0)) + 2 * k5 *
               (8 * r3 * tau3 - tau3 * th3 - 12 * r2 * tau2 * (tau * beta - 2 * x0) + 6 * tau2 * th2 *
                (-2 + x0) - 12 * tau * beta * (-2 + x0) * x0 + 8 * x03 + 6 * r * tau * (tau2 * th2 - 4 * tau * beta *
                                                                                        (-1 + x0) + 4 * x02)) + k2 *
               (36 * rho * sg3 * tau * beta + 2 * (beta - v0) ** 3 + 24 * rho * eta * (2 * th2 - 3 * beta * v0 + v02) +
                3 * sg2 * (7 * tau * th2 + 2 * beta * (10 + 24 * rho2 - 5 * r * tau - 2 * tau * v0 - 5 * x0) + 4 * v0 *
                           (-2 - 4 * rho2 + r * tau + x0))) - 6 * k3 * (8 * rho2 * sg2 * tau * beta +
                                                                        (sg2 * tau * beta + (beta - v0) ** 2) *
                                                                        (
                                                                                    4 - 2 * r * tau + tau * beta - 2 * x0) + 4 * rho *
                                                                        eta * (3 * tau * th2 + 2 * v0 *
                                                                               (- 1 + r * tau + x0) - 2 * beta *
                                                                               (
                                                                                           -2 + 2 * r * tau + tau * v0 + 2 * x0)))) -
              3 * np.exp(2 * alpha * tau) * (sg4 * (5 * beta + v0) + alpha * sg2 * (-32 * rho * eta * beta - 9 * th2 +
                                                                                    sg2 * tau * (
                                                                                                6 * beta - 2 * v0) + 11 *
                                                                                    beta * v0 - 2 * v02) + 2 * k2 *
                                             (sg4 * tau2 * (beta - v0) + (beta - v0) ** 3 + 8 * rho * sg3 * tau *
                                              (-2 * beta + v0) + 8 * rho * eta * (2 * th2 - 3 * beta * v0 + v02) + sg2 *
                                              (tau * th2 - 2 * v0 * (4 * rho2 + tau * v0) + beta *
                                               (8 + 24 * rho2 - 4 * r * tau + 3 * tau * v0 - 4 * x0))) + 2 * k4 *
                                             (beta - v0) * (
                                                         4 * r2 * tau2 + 4 * rho2 * sg2 * tau2 + 8 * tau * beta + tau2
                                                         * th2 - 4 * rho * eta * tau * (2 + tau * beta - 2 * x0) -
                                                         8 * x0 - 4 * tau * beta * x0 + 4 * x02 + 4 * r * tau *
                                                         (- 2 + 2 * rho * eta * tau - tau * beta + 2 * x0)) + 4 * k3
                                             * (4 * rho2 * sg2 * tau * (2 * beta - v0) + (beta - v0) *
                                                (sg2 * tau - beta + v0) * (4 - 2 * r * tau + tau * beta - 2 * x0) + 2 *
                                                rho * eta * (-2 * tau * th2 + v0 * (2 - 2 * r * tau + sg2 * tau2 + tau *
                                                                                    v0 - 2 * x0) + beta *
                                                             (- 4 + 4 * r * tau - sg2 * tau2 + 4 * x0))))) / \
             (16. * np.exp(3 * alpha * tau) * k5)

        m3_list.append(m3)

        # Fourth moment
        m4 = (3 * alpha * Power(sg2 * (beta - 2 * v0) + np.exp(2 * alpha * tau) *
                                (8 * k3 * tau * beta - 8 * k2 * (beta + rho * eta * tau * beta - v0) + sg2 *
                                 (-5 * beta + 2 * v0) + 2 * alpha * eta *
                                 (8 * rho * beta + eta * tau * beta - 4 * rho * v0)) + 4 * np.exp(alpha * tau) *
                                (sg2 * beta - 2 * k2 * (-1 + rho * eta * tau) * (beta - v0) + alpha * eta *
                                 (-4 * rho * beta + eta * tau * beta + 2 * rho * v0 - eta * tau * v0)), 2) + sg2 *
              (3 * sg4 * (beta - 4 * v0) + 24 * np.exp(alpha * tau) * sg2 *
               (-2 * k2 * (-1 + rho * eta * tau) * (beta - 3 * v0) + sg2 * (beta - 2 * v0) + alpha * eta *
                (eta * tau * (beta - 3 * v0) + rho * (-4 * beta + 10 * v0))) + 3 * np.exp(4 * alpha * tau) *
               (64 * k5 * (1 + 4 * rho2) * tau * beta + 4 * alpha * sg3 * (5 * eta * tau * beta + 8 * rho *
                                                                           (22 * beta - 5 * v0)) +
                32 * k3 * eta * (3 * eta * tau * beta + 12 * rho2 * eta * tau * beta + 4 * rho *
                                 (10 * beta - 3 * v0) + 8 * rho3 * (4 * beta - v0)) + sg4 *
                (-93 * beta + 20 * v0) - 32 * k2 * sg2 * ((11 + 50 * rho2 + 5 * rho * eta * tau) * beta - 3 *
                                                          (v0 + 4 * rho2 * v0)) - 32 * k4 *
                ((5 + 24 * rho2 + 12 * rho * eta * tau + 8 * rho3 * eta * tau) * beta - 2 * (v0 + 4 * rho2 * v0))) +
               12 * np.exp(2 * alpha * tau) * (sg4 * (7 * beta - 4 * v0) + 8 * k4 *
                                               (1 - 4 * rho * eta * tau + 2 * rho2 * sg2 * tau2) * (beta - 2 * v0) + 2 *
                                               alpha * sg3 * (-24 * rho * beta + 5 * eta * tau * beta + 20 * rho *
                                                              v0 - 6 * eta * tau * v0) + 4 * k2 * sg2 *
                                               ((6 + 20 * rho2 - 14 * rho * eta * tau + sg2 * tau2) *
                                                beta - 2 * (3 + 12 * rho2 - 10 * rho * eta * tau + sg2 * tau2) * v0) + 8
                                               * k3 * eta * (4 * rho2 * eta * tau * (2 * beta - 3 * v0) + 3 * eta *
                                                             tau * (beta - 2 * v0) - 2 * rho *
                                                             ((4 + sg2 * tau2) * beta - 2 * (3 + sg2 * tau2) * v0)))
               - 8 * np.exp(3 * alpha * tau) * (16 * k6 * rho2 * tau2 * (-3 + rho * eta * tau) * (beta - v0) - 3 * sg4 *
                                                (7 * beta + 2 * v0) - 6 * k2 * sg2 *
                                                ((15 + 80 * rho2 - 35 * rho * eta * tau + 2 * sg2 * tau2) * beta +
                                                 (3 + 7 * rho * eta * tau - sg2 * tau2) * v0) - 24 * k5 * tau *
                                                ((2 - 4 * rho * eta * tau - 4 * rho3 * eta * tau + rho2 *
                                                  (8 + sg2 * tau2)) * beta +
                                                 (-2 + 4 * rho * eta * tau + 2 * rho3 * eta * tau - rho2 *
                                                  (4 + sg2 * tau2)) * v0) + 12 * k4 *
                                                ((-4 + 24 * rho3 * eta * tau - 3 * sg2 * tau2 + rho * eta * tau *
                                                  (32 + sg2 * tau2) - 2 * rho2 * (12 + 7 * sg2 * tau2)) * beta +
                                                 (-8 * rho3 * eta * tau + 3 * sg2 * tau2 + 8 * rho2 * (1 + sg2 * tau2) -
                                                  rho * eta * tau * (16 + sg2 * tau2)) * v0) + 3 * alpha * sg3 *
                                                (eta * tau * (-9 * beta + v0) + 10 * rho * (6 * beta + v0)) +
                                                2 * k3 * eta * (48 * rho3 * (4 * beta - v0) + 24 * rho2 * eta * tau *
                                                                (-10 * beta + 3 * v0) + 6 * rho *
                                                                ((32 + 7 * sg2 * tau2) * beta - 4 * sg2 * tau2 * v0) +
                                                                eta * tau * ((-54 - sg2 * tau2) * beta +
                                                                             (18 + sg2 * tau2) * v0)))) + 8 * alpha *
              eta * (-(sg3 * (beta - 3 * v0)) - 6 * np.exp(alpha * tau) * eta *
                     (-2 * k2 * (-1 + rho * eta * tau) * (beta - 2 * v0) + sg2 * (beta - v0) + alpha * eta *
                      (eta * tau * (beta - 2 * v0) + rho * (-4 * beta + 6 * v0))) + 2 * np.exp(3 * alpha * tau) *
                     (24 * k4 * rho * tau * beta + sg3 * (11 * beta - 3 * v0) - 3 * alpha * sg2 *
                      (20 * rho * beta + eta * tau * beta - 6 * rho * v0) - 12 * k3 *
                      (4 * rho * beta + eta * tau * beta + 2 * rho2 * eta * tau * beta - 2 * rho * v0) + 6 * k2 *
                      eta * ((5 + 12 * rho2 + 3 * rho * eta * tau) * beta - 2 * (v0 + 2 * rho2 * v0))) - 3 *
                     np.exp(2 * alpha * tau) * (8 * k4 * rho * tau * (-2 + rho * eta * tau) * (beta - v0) + sg3 *
                                                (5 * beta + v0) + 2 * k2 * eta *
                                                ((8 + 24 * rho2 - 16 * rho * eta * tau + sg2 * tau2) * beta -
                                                 (8 * rho2 - 8 * rho * eta * tau + sg2 * tau2) * v0) - 2 * alpha *
                                                sg2 * (16 * rho * beta + eta * tau * (-3 * beta + v0)) + 8 * k3 *
                                                (2 * eta * tau * (beta - v0) + 2 * rho2 * eta * tau *
                                                 (2 * beta - v0) + rho * ((-4 - sg2 * tau2) * beta +
                                                                          (2 + sg2 * tau2) * v0)))) *
              (-beta + v0 + np.exp(alpha * tau) * (beta - v0 + alpha * (2 * r * tau - tau * beta + 2 * x0))) + 12 * k2 *
              (sg2 * (beta - 2 * v0) + np.exp(2 * alpha * tau) * (8 * k3 * tau * beta - 8 * k2 *
                                                                  (beta + rho * eta * tau * beta - v0) + sg2 *
                                                                  (-5 * beta + 2 * v0) + 2 * alpha * eta *
                                                                  (8 * rho * beta + eta * tau * beta - 4 * rho * v0)) +
               4 * np.exp(alpha * tau) * (sg2 * beta - 2 * k2 * (-1 + rho * eta * tau) * (beta - v0) + alpha * eta *
                                          (-4 * rho * beta + eta * tau * beta + 2 * rho * v0 - eta * tau * v0))) *
              (-beta + v0 + np.exp(alpha * tau) * (beta - v0 + alpha * (2 * r * tau - tau * beta + 2 * x0))) ** 2 + 4 *
              k3 * (-beta + v0 + np.exp(alpha * tau) * (beta - v0 + alpha *
                                                        (2 * r * tau - tau * beta + 2 * x0))) ** 4) / (
                     64. * np.exp(4 * alpha * tau) * k7)
        m4_list.append(m4)

    if central == 0:
        moments = [m1, m2, m3, m4]

    else:  # central == 1
        m1 = np.array(m1_list)
        m2 = np.array(m2_list)
        m3 = np.array(m3_list)
        m4 = np.array(m4_list)

        sd = (m2 - m1 ** 2) ** 0.5
        sk = (m3 - 3 * m1 * sd ** 2 - m1 ** 3) / sd ** 3
        kur = (m4 - 4 * m1 * m3 + 6 * m1 ** 2 * sd ** 2 + 3 * m1 ** 4) / sd ** 4
        moments = np.array([m1, sd, sk, kur]).T

    return moments
