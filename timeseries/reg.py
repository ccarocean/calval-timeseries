import numpy as np


########################## Regression ######################################################################
def linreg(x, y):
    p = np.polyfit(x, y, 1)
    b_0, b_1 = p[1][0], p[0][0]
    pred = b_0 + b_1*x
    SSR = np.sum(np.square(pred-np.mean(y)))
    SSTO = np.sum(np.square(y-np.mean(y)))
    r2 = SSR/SSTO
    return(pred, b_0, b_1, r2)


def quadreg(x, y, t):
    if len(x)>0:
        xnum = np.array([(z-t).total_seconds() for z in x])
        p = np.polyfit(xnum, y, 2)
        b_0, b_1, b_2 = p[2], p[1], p[0]
        return b_0
    else:
        return 0