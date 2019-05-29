#!/usr/bin/env python3
############################################################################################################
# Author: Adam Dodge
# Date Created: 8/30/2017
# Date Modified: 5/23/2019
############################################################################################################
import os
import sys
import argparse
from . import loading, cata_ts, harv_ts


def main():
    """ Main function for calling time series analysis functions """

    # Parse Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-h', '--harv', type=str, default=None,
                        help='Create Harvest Time Series. Argument is location of file with satellite data.')
    parser.add_argument('-c', '--cata', type=str, default=None,
                        help='Create Catalina Time Series. Argument is location of file with satellite data.')

    args = parser.parse_args()
    if args.harv is None and args.cata is None:
        print("-h or -c is required for use.")
        sys.exit(0)

    f_lid_harv = os.path.join('/', 'srv', 'data', 'harvest', 'harv', 'lidardata_overflights.csv')
    f_wind = os.path.join('/', 'srv', 'data', 'harvest', 'harv', 'co-ops', 'wind.txt')
    f_lid_cata = os.path.join('/', 'srv', 'data', 'harvest', 'cata', 'lidardata_overflights.csv')
    dir_ts = os.path.join('/', 'srv', 'data', 'harvest', 'timeseries')

    if args.harv is not None:
        # Create harvest time series
        plotfile_rawLid = os.path.join(dir_ts, 'TS_RawLiDAR.png')
        plotfile_corrLid = os.path.join(dir_ts, 'TS_CorrLiDAR.png')
        plotfile_rawBub = os.path.join(dir_ts, 'TS_RawBubbler.png')
        plotfile_corrBub = os.path.join(dir_ts, 'TS_CorrBubbler.png')
        plotfile_rawRad = os.path.join(dir_ts, 'TS_RawRadar.png')
        plotfile_corrRad = os.path.join(dir_ts, 'TS_CorrRadar.png')
        plotfile_avgRaw = os.path.join(dir_ts, 'TS_RawAverage.png')
        plotfile_avgCorr = os.path.join(dir_ts, 'TS_CorrAverage.png')
        time, lid, amp, rad, bub, ssh, benchmark, backscatter, swh, wind = loading.load_harv(f_lid_harv, args.harv, f_wind)
        harv_ts.raw_lidar(ssh, benchmark, lid, time, plotfile_rawLid)
        harv_ts.corr_lidar(ssh, benchmark, lid, amp, wind, time, plotfile_corrLid)
        harv_ts.raw_bubbler(ssh, benchmark, bub, time, plotfile_rawBub)
        harv_ts.corr_bubbler(ssh, benchmark, bub, time, swh, plotfile_corrBub)
        harv_ts.raw_radar(ssh, benchmark, rad, time, plotfile_rawRad)
        harv_ts.corr_radar(ssh, benchmark, rad, swh, wind, time, plotfile_corrRad)
        harv_ts.avg_raw(ssh, benchmark, rad, bub, time, plotfile_avgRaw)
        harv_ts.avg_corr(ssh, benchmark, rad, bub, swh, wind, time, plotfile_avgCorr)

    if args.cata is not None:
        # Create Catalina Time Series
        plotfile_lid = os.path.join(dir_ts, 'TS_RawLiDAR_Catalina.png')
        plotfile_acoust = os.path.join(dir_ts, 'TS_RawAcoust_LA.png')
        plotfile_avg = os.path.join(dir_ts, 'TS_RawAvg_Catalina.png')
        time, lid, amp, ssh, acoust, corr = loading.load_cata(f_lid_cata, args.cata)

        cata_ts.raw_lidar(ssh, lid, corr, time, plotfile_lid)
        cata_ts.raw_acoust(ssh, corr, acoust, time, plotfile_acoust)
        cata_ts.raw_avg(ssh, corr, lid, acoust, time, plotfile_avg)