import numpy as np


# This function computes the Vasicek discount factors

def get_df_Vasicek(x, ttm):
    kappa = x[0]
    theta = x[1]
    sg = x[2]
    r0 = x[3]

    B = (1 - np.exp(-kappa * np.array(ttm))) / kappa
    logA = (B - ttm) * (theta - sg * sg / (2 * kappa ** 2)) - sg * sg * B ** 2 / (4 * kappa)
    A = np.exp(logA)

    df = A * np.exp(-B * r0)

    if ttm[0] == 0:
        df[0] = 1

    return df
