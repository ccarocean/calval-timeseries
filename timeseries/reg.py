import numpy as np


########################## Regression ######################################################################
def linreg_ts(x, y):
    p = np.polyfit(x, y, 1)
    b_0, b_1 = p[1][0], p[0][0]
    pred = b_0 + b_1*x
    SSR = np.sum(np.square(pred-np.mean(y)))
    SSTO = np.sum(np.square(y-np.mean(y)))
    r2 = SSR/SSTO
    return(pred, b_0, b_1, r2)


def quadreg_ts(x, y, t):
    if len(x)>0:
        xnum = np.array([(z-t).total_seconds() for z in x])
        p = np.polyfit(xnum, y, 2)
        b_0, b_1, b_2 = p[2], p[1], p[0]
        return b_0
    else:
        return 0


def quadreg_lid(x, y, t, day):
    """ Function for performing quadratic regression on LiDAR data. """
    if len(x) > 0:
        try:
            xnum = (x - (t - day).total_seconds()) / 3600
        except TypeError:
            xnum = (x - t).total_seconds() / 3600
        p = np.polyfit(xnum, y, 2)
        b_0, b_1, b_2 = p[2], p[1], p[0]
        return b_0
    else:
        return float('nan')


def linreg_lid(x, y, t, day):
    """ Function for performing linear regression on LiDAR data. """
    if len(x) > 0:
        try:
            xnum = (x - (t - day).total_seconds()) / 3600
        except TypeError:
            xnum = (x - t).total_seconds() / 3600
        p = np.polyfit(xnum, y, 1)
        b_0, b_1 = p[1], p[0]
        return b_0
    else:
        return float('nan')
