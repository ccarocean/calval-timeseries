import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as pltdt
import datetime as dt
from . import reg
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()



########################## Create LiDAR time series ##########################################################
def raw_lidar(ssh, lid, corr, backscatter, time, plotfile, bs_max):
    # Perform calculations, indices
    data = np.add(np.subtract(ssh, corr), lid * 1000)
    indnan = np.argwhere(np.invert(np.isnan(data)))
    data = data[indnan]
    data = data - np.mean(data)
    time = time[indnan]
    backscatter = backscatter[indnan]

    # Remove high backscatter
    ind_lowbs = np.where(backscatter < bs_max)
    data = data[ind_lowbs]
    time = time[ind_lowbs]

    # Find Outliers
    out_ind = np.argwhere((data > 3 * np.std(data) + np.mean(data)) | (data < -3 * np.std(data) + np.mean(data)))[:, 0]
    not_ind = np.argwhere((data < 3 * np.std(data) + np.mean(data)) & (data > -3 * np.std(data) + np.mean(data)))[:, 0]

    # Plot Time Series
    fig, ax = plt.subplots()
    ax.plot_date(pltdt.date2num(time)[not_ind], data[not_ind], 'g-v',
                 label='Included Data (' + str(len(not_ind)) + '), Variance=' + str(
                     round(np.std(data[not_ind]), 3)) + "mm")
    ax.plot_date(pltdt.date2num(time)[out_ind], data[out_ind], 'rv',
                 label='3$\sigma$ Outliers (' + str(len(out_ind)) + ')')

    # Fit data
    base = dt.datetime(2016, 1, 1)
    xnum = [(x - base).total_seconds() for x in time]
    xnum = np.array(xnum) / (3600 * 24 * 365)

    yfit, b0, b1, r2 = reg.linreg_ts(xnum[not_ind], data[not_ind])
    ax.plot_date(pltdt.date2num(time[not_ind]), yfit, 'b--',
                 label='Linear Fit, R$^2$=' + str(round(r2, 6)) + ", b$_1$=" + str(round(b1, 3)) + " mm/yr")

    # Set axes parameters
    ax.set_title('Raw LiDAR Jason 3 SSH Bias Time Series at Catalina')
    ax.set_xlabel('Time')
    ax.set_ylabel('SSH Bias [mm]')
    ax.set_ylim(-200, 300)
    ax.xaxis.set_tick_params(rotation=30, labelsize=10)
    ax.legend()
    ax.grid()
    fig.savefig(plotfile, dpi=500, bbox_inches='tight')
    plt.close()
    print("Raw LiDAR Time series saved to:", plotfile)


########################## Create Acoustic time series ##########################################################
def raw_acoust(ssh, corr, acoust, backscatter, time, plotfile, bs_max):
    # Perform calculations, indices
    data = np.subtract(np.subtract(ssh, corr), acoust * 1000)
    indnan = np.argwhere(np.invert(np.isnan(data)))
    data = data[indnan]
    data = data - np.mean(data)
    time = time[indnan]
    backscatter = backscatter[indnan]

    # Remove high backscatter
    ind_lowbs = np.where(backscatter < bs_max)
    data = data[ind_lowbs]
    time = time[ind_lowbs]

    # Find Outliers
    out_ind = np.argwhere((data > 3 * np.std(data) + np.mean(data)) | (data < -3 * np.std(data) + np.mean(data)))[:, 0]
    not_ind = np.argwhere((data < 3 * np.std(data) + np.mean(data)) & (data > -3 * np.std(data) + np.mean(data)))[:, 0]

    # Plot Time Series
    fig, ax = plt.subplots()
    ax.plot_date(pltdt.date2num(time)[not_ind], data[not_ind], 'g-v',
                 label='Included Data (' + str(len(not_ind)) + '), Variance=' + str(
                     round(np.std(data[not_ind]), 3)) + "mm")
    ax.plot_date(pltdt.date2num(time)[out_ind], data[out_ind], 'rv',
                 label='3$\sigma$ Outliers (' + str(len(out_ind)) + ')')

    # Fit data
    base = dt.datetime(2016, 1, 1)
    xnum = [(x - base).total_seconds() for x in time]
    xnum = np.array(xnum) / (3600 * 24 * 365)

    yfit, b0, b1, r2 = reg.linreg_ts(xnum[not_ind], data[not_ind])
    ax.plot_date(pltdt.date2num(time[not_ind]), yfit, 'b--',
                 label='Linear Fit, R$^2$=' + str(round(r2, 6)) + ", b$_1$=" + str(round(b1, 3)) + " mm/yr")

    # Set axes parameters
    ax.set_title('Raw Acoustic Jason 3 SSH Bias Time Series at LA Tide Gauge')
    ax.set_xlabel('Time')
    ax.set_ylabel('SSH Bias [mm]')
    ax.set_ylim(-200, 300)
    ax.xaxis.set_tick_params(rotation=30, labelsize=10)
    ax.legend()
    ax.grid()
    fig.savefig(plotfile, dpi=500, bbox_inches='tight')
    plt.close()
    print('Raw Acoustic Time series saved to:', plotfile)


########################## Create Average time series ##########################################################
def raw_avg(ssh, corr, lid, acoust, backscatter, time, plotfile, bs_max):
    # Perform calculations, indices
    avg = np.subtract(lid * 1000, acoust * 1000) / 2
    data = np.add(np.subtract(ssh, corr), avg)
    indnan = np.argwhere(np.invert(np.isnan(data)))
    data = data[indnan]
    data = data - np.mean(data)
    time = time[indnan]
    backscatter = backscatter[indnan]

    # Remove high backscatter
    ind_lowbs = np.where(backscatter < bs_max)
    data = data[ind_lowbs]
    time = time[ind_lowbs]

    # Find Outliers
    out_ind = np.argwhere((data > 3 * np.std(data) + np.mean(data)) | (data < -3 * np.std(data) + np.mean(data)))[:, 0]
    not_ind = np.argwhere((data < 3 * np.std(data) + np.mean(data)) & (data > -3 * np.std(data) + np.mean(data)))[:, 0]

    # Plot Time Series
    fig, ax = plt.subplots()
    ax.plot_date(pltdt.date2num(time)[not_ind], data[not_ind], 'g-v',
                 label='Included Data (' + str(len(not_ind)) + '), Variance=' + str(
                     round(np.std(data[not_ind]), 3)) + "mm")
    ax.plot_date(pltdt.date2num(time)[out_ind], data[out_ind], 'rv',
                 label='3$\sigma$ Outliers (' + str(len(out_ind)) + ')')

    # Fit data
    base = dt.datetime(2016, 1, 1)
    xnum = [(x - base).total_seconds() for x in time]
    xnum = np.array(xnum) / (3600 * 24 * 365)

    yfit, b0, b1, r2 = reg.linreg_ts(xnum[not_ind], data[not_ind])
    ax.plot_date(pltdt.date2num(time[not_ind]), yfit, 'b--',
                 label='Linear Fit, R$^2$=' + str(round(r2, 6)) + ", b$_1$=" + str(round(b1, 3)) + " mm/yr")

    # Set axes parameters
    ax.set_title('Raw Average LiDAR/Acoustic Jason 3 SSH Bias Time Series in San Pedro Channel')
    ax.set_xlabel('Time')
    ax.set_ylabel('SSH Bias [mm]')
    ax.set_ylim(-200, 300)
    ax.xaxis.set_tick_params(rotation=30, labelsize=10)
    ax.legend()
    ax.grid()
    fig.savefig(plotfile, dpi=500, bbox_inches='tight')
    plt.close()
    print('Raw Average LiDAR/Acoustic Time series saved to:', plotfile)


