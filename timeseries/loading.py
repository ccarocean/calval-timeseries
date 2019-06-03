import datetime as dt
import numpy as np
import sys
from . import reg
import os
import lzma
import gzip
import pandas as pd
import dateutil.parser as parser


########################## Load Data #######################################################################
def load_cata(f_lid, f_sat, ind_lid):
    # Load LiDAR Data
    time = []
    lid = []
    rpw = []
    acoust = []
    i = 0
    with open(f_lid, 'r') as lidarfile:
        for line in lidarfile:
            data = [x.strip() for x in line.split(',')]
            if i== 0:
                indTime = data.index("time")
                indLid = data.index(ind_lid)
                indRpw = data.index("l_rpw")
                indAcoust = data.index("acoust")
            else:
                time.append(dt.datetime.strptime(data[indTime], "%Y-%m-%d %H:%M:%S.%f"))
                lid.append(float(data[indLid]))
                rpw.append(float(data[indRpw]))
                acoust.append(float(data[indAcoust]))
            i = i + 1

    # Load Satellite Data
    tJ2000 = dt.datetime(2000, 1, 1, 12)
    time2 = []
    ssh = []
    corr = []
    swh = []
    backscatter = []
    with open(f_sat, 'r') as satfile:
        for line in satfile:
            data = [x.strip() for x in line.split()]
            try:
                time2.append(tJ2000 + dt.timedelta(seconds=float(data[0])))
                ssh.append(float(data[1]))
                corr.append(float(data[2]))
                swh.append(float(data[3]))
                backscatter.append(float(data[4]))
            except ValueError:
                time2.append(parser.parse(data[0] + " " + data[1]))
                ssh.append(float(data[2]))
                corr.append(float(data[3]))
                swh.append(float(data[4]))
                backscatter.append(float(data[5]))

    # Ensure dates are the same
    try:
        assert time == time2
    except:
        print("Different Overflight Times. Something is wrong.")
        sys.exit(0)

    # Convert to numpy arrays
    time = np.asarray(time)
    lid = np.asarray(lid)
    rpw = np.asarray(rpw)
    ssh = np.asarray(ssh)
    acoust = np.asarray(acoust)
    swh = np.array(swh)
    backscatter = np.array(backscatter)

    # Return Data
    print("Data loaded successfully.")
    return time, lid, rpw, ssh, acoust, corr, swh, backscatter


########################## Load Data #######################################################################
def load_harv(f_lid, f_sat, f_wind, ind_lid):
    # Load LiDAR Data
    time = []
    lid = []
    bub = []
    rad = []
    rpw = []
    i = 0
    with open(f_lid, 'r') as lidarfile:
        for line in lidarfile:
            data = [x.strip() for x in line.split(',')]
            if i == 0:
                indTime = data.index("time")
                indLid = data.index(ind_lid)
                indRpw = data.index("l_rpw")
                indBub = data.index("bub")
                indRad = data.index("rad")
            else:
                time.append(dt.datetime.strptime(data[indTime], "%Y-%m-%d %H:%M:%S.%f"))
                lid.append(float(data[indLid]))
                rpw.append(float(data[indRpw]))
                bub.append(float(data[indBub]))
                rad.append(float(data[indRad]))
            i = i + 1

    # Load Satellite Data
    tJ2000 = dt.datetime(2000, 1, 1, 12)
    time2 = []
    ssh = []
    benchmark = []
    backscatter = []
    swh = []
    with open(f_sat, 'r') as satfile:
        for line in satfile:
            data = [x.strip() for x in line.split()]
            try:
                time2.append(tJ2000 + dt.timedelta(seconds=float(data[0])))
                ssh.append(float(data[1]))
                benchmark.append(float(data[2]))
                backscatter.append(float(data[3]))
                swh.append(float(data[4]))
            except ValueError:
                time2.append(parser.parse(data[0] + " " + data[1]))
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
        wind.append(reg.quadreg_ts(time_, wind_, t))

    # Convert to numpy arrays
    time = np.asarray(time)
    lid = np.asarray(lid)
    rpw = np.asarray(rpw)
    bub = np.asarray(bub)
    rad = np.asarray(rad)
    ssh = np.asarray(ssh)
    benchmark = np.asarray(benchmark)
    backscatter = np.asarray(backscatter)
    swh = np.asarray(swh)
    wind = np.asarray(wind)

    # Return Data
    print("Data loaded successfully.")
    return time, lid, rpw, rad, bub, ssh, benchmark, backscatter, swh, wind

########## Load Raw Data #######################################################################################
def load_raw(d, rawdir):
    """ Function to determine filetype and load raw LiDAR data. """
    fgzbin = d.strftime(rawdir + '/uls_%Y%m%d.bin.gz')
    fxzbin = d.strftime(rawdir + '/uls_%Y%m%d.bin.xz')
    dtype = np.dtype([(str('time'), np.uint32), (str('range'), np.uint32), (str('rpw'), np.uint32)])
    if os.path.isfile(fgzbin):
        return load_gzbin(fgzbin, dtype)
    elif os.path.isfile(fxzbin):
        return load_xzbin(fxzbin, dtype)
    else:
        return None


def load_gzbin(f, dtype):
    """ Function to load binary data file from LIDAR sensor using gz compression. """
    if os.path.isfile(f):  # Ensures file exists
        with gzip.open(f, 'rb') as nf:  # Open file
            try:
                file_content = nf.read()  # Read file
            except EOFError:
                print('File is still being transfered from LiDAR Station.')
                sys.exit(0)
        filesize = len(file_content)
        data = np.frombuffer(file_content, dtype, count=filesize // 12)  # returns data from file
        data = {'time': data['time'].astype(float) / 10000, 'range': data['range'].astype(float) / 1000,
                'rpw': data['rpw']}  # data organization
        data = pd.DataFrame.from_dict(data)  # creates dataframe
        data.set_index('time', inplace=True, drop=True)  # sets index as time
        print('LiDAR Data loaded from:', f[-19:])
        return data
    else:
        return None


def load_xzbin(f, dtype):
    """ Function to load binary data file from LIDAR sensor using xz compression. """
    if os.path.isfile(f):  # Ensures file exists
        with lzma.open(f, 'rb') as nf:  # Open file
            try:
                file_content = nf.read()  # Read file
            except EOFError:
                print('File is still being transfered from LiDAR Station.')
                sys.exit(0)
        filesize = len(file_content)
        data = np.frombuffer(file_content, dtype, count=filesize // 12)  # returns data from file
        data = {'time': data['time'].astype(float) / 10000, 'range': data['range'].astype(float) / 1000,
                'rpw': data['rpw']}  # data organization
        data = pd.DataFrame.from_dict(data)  # creates dataframe
        data.set_index('time', inplace=True, drop=True)  # sets index as time
        print('LiDAR Data loaded from:', f[-19:])
        return data
    else:
        return None


############### Load Six Minute Data ############################################################################
def load_output(d, loc, outdir):
    """ Function to load output data. """
    names_cata_saved = ['time', 'A1', 'A1_t1', 'A1_t2', 'B1', 'E1', 'F1', 'L1_1', 'L1_2', 'P6', 'U1',
                        'W1', 'l', 'l_Hs', 'l_rpw', 'l_max', 'l_mean', 'l_median', 'l_min', 'l_n', 'l_skew', 'l_std']
    names_harv_saved = ['time', 'D1', 'F1', 'L1_1', 'L1_2', 'N1_1', 'N1_1_ssh', 'N1_2', 'P6', 'U1', 'W1',
                        'Y1_1', 'Y1_1_ssh', 'Y1_2', 'l', 'l_Hs', 'l_rpw', 'l_max', 'l_mean', 'l_median', 'l_min',
                        'l_n', 'l_skew', 'l_ssh', 'l_std']
    f = os.path.join(outdir, loc + '_' + d.strftime('%Y%m') + '.csv')
    if loc == 'harv':
        try:
            filedata = pd.read_csv(f, header=0, usecols=range(0, 25), names=names_harv_saved, parse_dates=True,
                                   index_col=0, na_values='   -   ')
            return filedata
        except IOError:
            data = pd.DataFrame(columns=names_harv_saved)
            data.set_index('time', inplace=True, drop=True)
            return data
    else:
        try:
            filedata = pd.read_csv(f, header=0, usecols=range(0, 22), names=names_cata_saved, parse_dates=True,
                                   index_col=0, na_values='   -   ')
            return filedata
        except IOError:
            data = pd.DataFrame(columns=names_cata_saved)
            data.set_index('time', inplace=True, drop=True)
            return data