import datetime as dt
import numpy as np
import sys
from . import reg


########################## Load Data #######################################################################
def load_cata(f_lid, f_sat):
    # Load LiDAR Data
    time = []
    lid = []
    amp = []
    acoust = []
    i = 0
    with open(f_lid, 'r') as lidarfile:
        for line in lidarfile:
            data = [x.strip() for x in line.split(',')]
            if i== 0:
                indTime = data.index("time")
                indLid = data.index("lid_6m_quad")
                indAmp = data.index("l_amp")
                indAcoust = data.index("acoust")
            else:
                time.append(dt.datetime.strptime(data[indTime], "%Y-%m-%d %H:%M:%S.%f"))
                lid.append(float(data[indLid]))
                amp.append(float(data[indAmp]))
                acoust.append(float(data[indAcoust]))
            i = i + 1

    # Load Satellite Data
    tJ2000 = dt.datetime(2000, 1, 1)
    time2 = []
    ssh = []
    corr = []
    with open(f_sat, 'r') as satfile:
        for line in satfile:
            data = [x.strip() for x in line.split()]
            time2.append(tJ2000 + dt.timedelta(seconds=float(data[0])))
            ssh.append(float(data[1]))
            corr.append(float(data[2]))

    # Ensure dates are the same
    try:
        assert (len(time) == len(time2))
    except:
        print("Different Overflight Times. Something is wrong.")
        sys.exit(0)

    # Convert to numpy arrays
    time = np.asarray(time)
    lid = np.asarray(lid)
    amp = np.asarray(amp)
    ssh = np.asarray(ssh)
    acoust = np.asarray(acoust)

    # Return Data
    print("Data loaded successfully.")
    return time, lid, amp, ssh, acoust, corr


########################## Load Data #######################################################################
def load_harv(f_lid, f_sat, f_wind):
    # Load LiDAR Data
    time = []
    lid = []
    bub = []
    rad = []
    amp = []
    i = 0
    with open(f_lid, 'r') as lidarfile:
        for line in lidarfile:
            data = [x.strip() for x in line.split(',')]
            if i == 0:
                indTime = data.index("time")
                indLid = data.index("l_quad2h")
                indAmp = data.index("l_amp")
                indBub = data.index("bub")
                indRad = data.index("rad")
            else:
                time.append(dt.datetime.strptime(data[indTime], "%Y-%m-%d %H:%M:%S.%f"))
                lid.append(float(data[indLid]))
                amp.append(float(data[indAmp]))
                bub.append(float(data[indBub]))
                rad.append(float(data[indRad]))
            i = i + 1

    # Load Satellite Data
    time2 = []
    ssh = []
    benchmark = []
    backscatter = []
    swh = []
    with open(f_sat, 'r') as satfile:
        for line in satfile:
            data = [x.strip() for x in line.split()]
            time2.append(dt.datetime.strptime(data[0] + " " + data[1], "%d-%b-%Y %H:%M:%S.%f"))
            ssh.append(float(data[2]))
            benchmark.append(float(data[3]))
            backscatter.append(float(data[4]))
            swh.append(float(data[5]))

            # Ensure dates are the same
    try:
        assert (time == time2)
    except:
        print("Different Overflight Times. Something is wrong.")
        sys.exit(0)

    # Load Wind Data
    # YY  MM DD hh mm WDIR WSPD GDR GST GTIME
    # yr  mo dy hr mn degT m/s degT m/s hhmm
    wspd = []
    time3 = []
    with open(f_wind, 'r') as windfile:
        for line in windfile:
            data = [x.strip() for x in line.split()]
            time3.append(dt.datetime(int(data[0]), int(data[1]), int(data[2]), int(data[3]), int(data[4])))
            wspd.append(float(data[6]))

    wind = []
    for t in time:
        t1 = t - dt.timedelta(hours=2)
        t2 = t + dt.timedelta(hours=2)
        try:
            time_, wind_ = zip(*((i, j) for i, j in zip(time3, wspd) if i >= t1 and i <= t2))
        except ValueError:
            time_, wind_ = [], []
        wind.append(reg.quadreg(time_, wind_, t))

    # Convert to numpy arrays
    time = np.asarray(time)
    lid = np.asarray(lid)
    amp = np.asarray(amp)
    bub = np.asarray(bub)
    rad = np.asarray(rad)
    ssh = np.asarray(ssh)
    benchmark = np.asarray(benchmark)
    backscatter = np.asarray(backscatter)
    swh = np.asarray(swh)
    wind = np.asarray(wind)

    # Return Data
    print("Data loaded successfully.")
    return time, lid, amp, rad, bub, ssh, benchmark, backscatter, swh, wind