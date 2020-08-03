# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 16:40:23 2020

@author: Diego
"""
import numpy as np

# X0 = 0
# T=5
# NStep=50
# v0 = 0.2**2/250
# mu = 0.0
# alpha = 0.1
# beta = 0.85
# omega = 5.7800*10**(-6)
# asymm = 0

def get_secondmoment(X0, mu, v0, omega, alpha, beta, asymm, T, NStep):
    dt = 1
    horizon = np.arange(1, NStep + 1)

    phi = alpha + beta
    omega0 = omega + alpha * asymm * asymm
    v1 = omega + alpha * (X0 - mu * dt - asymm) ** 2 + beta * v0

    if asymm == 0:
        if phi < 1:
            moments2 = ((horizon - (1 - phi ** horizon) / (1 - phi)) * omega0 / (1 - phi) +
                        (1 - phi ** horizon) / (1 - phi) * v1) ** 0.5

        if phi == 1:
            # lambda_one = 1-alpha
            # K = 3
            # G = (K-1)*(1-lambda_oone)**2+1
            # H = 1 - lambda_one + lambda_one/K

            moments2 = ((horizon - 1) * horizon * omega0 / 2 + horizon * v1) ** 0.5

    # moments2 = np.reshape(moments2, (NStep, 1))
    print(moments2)
    return moments2

def get_fourthmoment(X0, mu, v0, omega, alpha, beta, asymm, T, NStep):
    # dt = 1
    # horizon= np.arange(1, NStep+1)

    phi = alpha + beta
    omega0 = omega + alpha * asymm * asymm
    # v1 = omega + alpha*(X0-mu*dt-asymm)**2 + beta *v0
    K = 3
    moments2 = get_secondmoment(X0, mu, v0, omega, alpha, beta, asymm, T, NStep)
    gammak = moments2
    P = np.zeros((NStep, NStep))
    Q = np.zeros((NStep, NStep))

    if asymm == 0:
        if phi < 1:
            # [asymm phi]
            for ll in range(1, NStep):
                for kk in range(1, NStep):
                    if ll == kk:
                        P[ll, kk] = K * (omega0 ** 2 + alpha ** 2 * P[kk - 1, kk - 1] + (beta * beta / K) * P[
                            kk - 1, kk - 1] + 2 * omega0 * alpha * gammak[kk - 1] + 2 * omega0 * beta * gammak[kk - 1])

                    if ll > kk:
                        P[kk, ll] = omega0 * moments2[kk] + alpha * P[kk, ll - 1] + beta * Q[kk, ll - 1]
                        Q[kk, ll] = omega0 * moments2[ll] + alpha * P[ll, kk - 1] + beta * Q[ll, kk - 1]

        if phi == 1:
            # lambda_one = 1-alpha
            # K = 3
            # G = (K-1)*(1-lambda_one)**2+1
            # H = 1 - lambda_one + lambda_one/K
            # moments[:,4] = (K/horizon)*(1+((G**horizon-1)/(horizon*(G-1))-1) * (6*H/(G-1)+1))
            P = 0
            Q = 0

    return P, Q

def get_mom_GARCH11(X0, mu, v0, omega, alpha, beta, asymm, T, NStep):
    # dt = T/NStep
    # dt = 1
    horizon = np.arange(1, NStep + 1)

    # phi = alpha + beta
    # omega0 = omega + alpha * asymm * asymm
    # v1 = omega + alpha*(X0-mu*dt-asymm)**2 + beta *v0
    moments = np.zeros((NStep, 4))
    moments[:, 0] = X0 + mu * np.reshape(horizon, NStep)
    moments[:, 1] = get_secondmoment(X0, mu, v0, omega, alpha, beta, asymm, T, NStep)
    moments[:, 2] = moments[:, 1]
    moments[:, 3] = moments[:, 1]
    # P, Q = get_fourthmoment(X0, mu, v0, omega, alpha, beta, asymm, T, NStep)
    a = np.array((X0, v0 ** 0.5, 0, 3))
    a = np.reshape(a, (4, 1))
    moments = np.concatenate((a.T, moments), axis=0)

    return moments


