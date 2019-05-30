import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as pltdt
import datetime as dt
from . import reg


########################## Create LiDAR time series ##########################################################
def raw_lidar(ssh, benchmark, lid, time, plotfile):
    # Perform calculations, indices
    data = (np.add(np.subtract(ssh, benchmark), lid) - 6.85) * 1000 - 25
    indnan = np.argwhere(np.invert(np.isnan(data)))
    data = data[indnan]
    time = time[indnan]

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
    xnum = [(x[0] - base).total_seconds() for x in time]
    xnum = np.array(xnum) / (3600 * 24 * 365)

    yfit, b0, b1, r2 = reg.linreg_ts(xnum[not_ind], data[not_ind])
    ax.plot_date(pltdt.date2num(time[not_ind]), yfit, 'b--',
                 label='Linear Fit, R$^2$=' + str(round(r2, 6)) + ", b$_1$=" + str(round(b1, 3)) + " mm/yr")

    # Set axes parameters
    ax.set_title('Raw LiDAR Jason 3 SSH Bias Time Series')
    ax.set_xlabel('Time')
    ax.set_ylabel('SSH Bias [mm]')
    ax.set_ylim(-200, 300)
    ax.xaxis.set_tick_params(rotation=30, labelsize=10)
    ax.legend()
    ax.grid()
    fig.savefig(plotfile, dpi=500, bbox_inches='tight')
    plt.close()
    print("Raw LiDAR Time series saved to:", plotfile)


def corr_lidar(ssh, benchmark, lid, amp, wind, time, plotfile):
    # 'c2-.0054*c3+.0000087*c4' - Wind then amplitude
    # Perform calculations, indices
    data = (np.add(np.subtract(np.add(np.subtract(ssh, benchmark), lid), .0054 * wind),
                   .0000087 * amp) - 6.85) * 1000 - 25 - 88.25
    indnan = np.argwhere(np.invert(np.isnan(data)))
    data = data[indnan]
    time = time[indnan]

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
    xnum = [(x[0] - base).total_seconds() for x in time]
    xnum = np.array(xnum) / (3600 * 24 * 365)

    yfit, b0, b1, r2 = reg.linreg_ts(xnum[not_ind], data[not_ind])
    ax.plot_date(pltdt.date2num(time[not_ind]), yfit, 'b--',
                 label='Linear Fit, R$^2$=' + str(round(r2, 6)) + ", b$_1$=" + str(round(b1, 3)) + " mm/yr")

    # Set axes parameters
    ax.set_title("Corrected LiDAR Jason 3 SSH Bias Time Series")
    ax.set_xlabel('Time')
    ax.set_ylabel('SSH Bias [mm]')
    ax.set_ylim(-200, 300)
    ax.xaxis.set_tick_params(rotation=30, labelsize=10)
    ax.legend()
    ax.grid()
    fig.savefig(plotfile, dpi=500, bbox_inches='tight')
    plt.close()
    print("Raw Bubbler Time series saved to:", plotfile)
    print("Corrected LiDAR Time series saved to:", plotfile)


########################## Create Bubbler time series ########################################################
def raw_bubbler(ssh, benchmark, bub, time, plotfile):
    # Perform calculations, indices
    data = (np.subtract(np.subtract(ssh, benchmark), bub - 20.15)) * 1000 - 50
    indnan = np.argwhere(np.invert(np.isnan(data)))
    data = data[indnan]
    time = time[indnan]

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
    xnum = [(x[0] - base).total_seconds() for x in time]
    xnum = np.array(xnum) / (3600 * 24 * 365)

    yfit, b0, b1, r2 = reg.linreg_ts(xnum[not_ind], data[not_ind])
    ax.plot_date(pltdt.date2num(time[not_ind]), yfit, 'b--',
                 label='Linear Fit, R$^2$=' + str(round(r2, 6)) + ", b$_1$=" + str(round(b1, 3)) + " mm/yr")

    # Set axes parameters
    ax.set_title('Raw Bubbler Jason 3 SSH Bias Time Series')
    ax.set_xlabel('Time')
    ax.set_ylabel('SSH Bias [mm]')
    ax.set_ylim(-200, 300)
    ax.xaxis.set_tick_params(rotation=30, labelsize=10)
    ax.legend()
    ax.grid()
    fig.savefig(plotfile, dpi=500, bbox_inches='tight')
    plt.close()
    print("Raw Bubbler Time series saved to:", plotfile)


def corr_bubbler(ssh, benchmark, bub, time, swh, plotfile):
    # Perform calculations, indices
    # for i in range(len(swh)):
    #    if swh[i]<=0.5:
    #        swh[i]=0

    bub = np.add(bub, 0.031 * swh)
    data = (np.subtract(np.subtract(ssh, benchmark), bub - 20.15)) * 1000
    indnan = np.argwhere(np.invert(np.isnan(data)))
    data = data[indnan]
    time = time[indnan]

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
    xnum = [(x[0] - base).total_seconds() for x in time]
    xnum = np.array(xnum) / (3600 * 24 * 365)

    yfit, b0, b1, r2 = reg.linreg_ts(xnum[not_ind], data[not_ind])
    ax.plot_date(pltdt.date2num(time[not_ind]), yfit, 'b--',
                 label='Linear Fit, R$^2$=' + str(round(r2, 6)) + ", b$_1$=" + str(round(b1, 3)) + " mm/yr")

    # Set axes parameters
    ax.set_title('Corrected Bubbler Jason 3 SSH Bias Time Series')
    ax.set_xlabel('Time')
    ax.set_ylabel('SSH Bias [mm]')
    ax.set_ylim(-200, 300)
    ax.xaxis.set_tick_params(rotation=30, labelsize=10)
    ax.legend()
    ax.grid()
    fig.savefig(plotfile, dpi=500, bbox_inches='tight')
    plt.close()
    print("Corrected Bubbler Time series saved to:", plotfile)


########################## Create Radar time series ##########################################################
def raw_radar(ssh, benchmark, rad, time, plotfile):
    # Perform calculations, indices
    data = (np.subtract(np.subtract(ssh, benchmark), rad)) * 1000 + 20150
    indnan = np.argwhere(np.invert(np.isnan(data)))
    data = data[indnan]
    time = time[indnan]

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
    xnum = [(x[0] - base).total_seconds() for x in time]
    xnum = np.array(xnum) / (3600 * 24 * 365)

    yfit, b0, b1, r2 = reg.linreg_ts(xnum[not_ind], data[not_ind])
    ax.plot_date(pltdt.date2num(time[not_ind]), yfit, 'b--',
                 label='Linear Fit, R$^2$=' + str(round(r2, 6)) + ", b$_1$=" + str(round(b1, 3)) + " mm/yr")

    # Set axes parameters
    ax.set_title('Raw Radar Jason 3 SSH Bias Time Series')
    ax.set_xlabel('Time')
    ax.set_ylabel('SSH Bias [mm]')
    ax.set_ylim(-200, 300)
    ax.xaxis.set_tick_params(rotation=30, labelsize=10)
    ax.legend()
    ax.grid()
    fig.savefig(plotfile, dpi=500, bbox_inches='tight')
    plt.close()
    print("Raw Radar Time series saved to:", plotfile)


def corr_radar(ssh, benchmark, rad, swh, wind, time, plotfile):
    # '(1000*c2 + 0.5*c3 - 50*c4 + 9*c5 - 0.3*c6)/1000' - SWH, wind, SWH^2, wind*SWH
    # Perform calculations, indices
    swh2 = np.multiply(swh, swh)
    swhWind = np.multiply(swh, wind)
    data = (np.subtract(np.subtract(ssh, benchmark), rad)) * 1000 + 20150
    data = (np.subtract(np.add(np.subtract(np.add(1000 * data, 0.5 * swh), 50 * wind), 9 * swh2), 0.3 * swhWind)) / 1000
    indnan = np.argwhere(np.invert(np.isnan(data)))
    data = data[indnan]
    time = time[indnan]

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
    xnum = [(x[0] - base).total_seconds() for x in time]
    xnum = np.array(xnum) / (3600 * 24 * 365)

    yfit, b0, b1, r2 = reg.linreg_ts(xnum[not_ind], data[not_ind])
    ax.plot_date(pltdt.date2num(time[not_ind]), yfit, 'b--',
                 label='Linear Fit, R$^2$=' + str(round(r2, 6)) + ", b$_1$=" + str(round(b1, 3)) + " mm/yr")

    # Set axes parameters
    ax.set_title('Corrected Radar Jason 3 SSH Bias Time Series')
    ax.set_xlabel('Time')
    ax.set_ylabel('SSH Bias [mm]')
    ax.set_ylim(-200, 300)
    ax.xaxis.set_tick_params(rotation=30, labelsize=10)
    ax.legend()
    ax.grid()
    fig.savefig(plotfile, dpi=500, bbox_inches='tight')
    plt.close()
    print("Corrected Radar Time series saved to:", plotfile)


########################## Create Average time series ##########################################################
def avg_raw(ssh, benchmark, rad, bub, time, plotfile):
    # Perform calculations, indices
    dataRad = np.subtract(np.subtract(ssh, benchmark), rad) * 1000 + 20150 - 50
    dataBub = np.subtract(np.subtract(ssh, benchmark), bub - 20.15) * 1000
    data = np.stack([dataRad, dataBub]).mean(axis=0)
    indnan = np.argwhere(np.invert(np.isnan(data)))
    data = data[indnan]
    time = time[indnan]

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
    xnum = [(x[0] - base).total_seconds() for x in time]
    xnum = np.array(xnum) / (3600 * 24 * 365)

    yfit, b0, b1, r2 = reg.linreg_ts(xnum[not_ind], data[not_ind])
    ax.plot_date(pltdt.date2num(time[not_ind]), yfit, 'b--',
                 label='Linear Fit, R$^2$=' + str(round(r2, 6)) + ", b$_1$=" + str(round(b1, 3)) + " mm/yr")

    # Set axes parameters
    ax.set_title('Average Raw Bubbler & Radar Jason 3 SSH Bias Time Series')
    ax.set_xlabel('Time')
    ax.set_ylabel('SSH Bias [mm]')
    ax.set_ylim(-200, 300)
    ax.xaxis.set_tick_params(rotation=30, labelsize=10)
    ax.legend()
    ax.grid()
    fig.savefig(plotfile, dpi=500, bbox_inches='tight')
    plt.close()
    print("Average Raw Bubbler & Radar Time series saved to:", plotfile)


def avg_corr(ssh, benchmark, rad, bub, swh, wind, time, plotfile):
    # Perform calculations, indices
    swh2 = np.multiply(swh, swh)
    swhWind = np.multiply(swh, wind)
    dataRad = (np.subtract(np.subtract(ssh, benchmark), rad)) * 1000 + 20150
    dataRad = (np.subtract(np.add(np.subtract(np.add(1000 * dataRad, 0.5 * swh), 50 * wind), 9 * swh2),
                           0.3 * swhWind)) / 1000
    for i in range(len(swh)):
        if swh[i] < 0.5:
            swh[i] = 0
    bub = np.add(bub, 0.031 * swh)
    dataBub = (np.subtract(np.subtract(ssh, benchmark), bub - 20.15)) * 1000
    data = np.stack([dataRad, dataBub]).mean(axis=0)
    indnan = np.argwhere(np.invert(np.isnan(data)))
    data = data[indnan]
    time = time[indnan]

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
    xnum = [(x[0] - base).total_seconds() for x in time]
    xnum = np.array(xnum) / (3600 * 24 * 365)

    yfit, b0, b1, r2 = reg.linreg_ts(xnum[not_ind], data[not_ind])
    ax.plot_date(pltdt.date2num(time[not_ind]), yfit, 'b--',
                 label='Linear Fit, R$^2$=' + str(round(r2, 6)) + ", b$_1$=" + str(round(b1, 3)) + " mm/yr")

    # Set axes parameters
    ax.set_title('Average Corrected Bubbler & Radar Jason 3 SSH Bias Time Series')
    ax.set_xlabel('Time')
    ax.set_ylabel('SSH Bias [mm]')
    ax.set_ylim(-200, 300)
    ax.xaxis.set_tick_params(rotation=30, labelsize=10)
    ax.legend()
    ax.grid()
    fig.savefig(plotfile, dpi=500, bbox_inches='tight')
    plt.close()
    print("Average Corrected Bubbler & Radar Time series saved to:", plotfile)