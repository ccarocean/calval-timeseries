#!/usr/bin/env python3
############################################################################################################
# Author: Adam Dodge
# Date Created: 1/1/2019
# Date Modified: 5/23/2019
############################################################################################################
import os
import sys
import argparse
from . import loading, cata_ts, harv_ts, overflight


def main():
    """ Main function for calling time series analysis functions """

    # Parse Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--harv', type=str, default=None,
                        help='Create Harvest Time Series. Argument is location of file with satellite data.')
    parser.add_argument('--cata', type=str, default=None,
                        help='Create Catalina Time Series. Argument is location of file with satellite data.')
    parser.add_argument('-i', '--lidarindex', type=str, default='l_6m_quad2h',
                        help='Type of lidar data to use for time series. l_6m_quad2h is a 4 hour quadratic regression'
                             ' on the 6 minute data. l_mean is an average of 2200 seconds of data around the '
                             'overflight. l_lin1100 is a linear regression of 2200 seconds of data around the '
                             'overflight. l_quad2h is a quadratic regression of 4 hours of data around the overflight. '
                             'l_6m_quad2h is the default value. ')
    parser.add_argument('-l', '--load', action="store_true", default=None,
                        help="Loads and averages LiDAR data. This is for when new overflight data is available. ")

    args = parser.parse_args()
    if args.harv is None and args.cata is None:
        print("--harv or --cata is required for use.")
        sys.exit(0)

    if args.lidarindex not in ['l_6m_quad2h', 'l_mean', 'l_lin1100', 'l_quad2h']:
        print('Not a valid lidar index. ')
        sys.exit(0)

    datafile = os.getenv('LIDARDATAFILE', os.path.join('/', 'srv', 'data', 'harvest'))

    f_lid_harv = os.path.join('/', 'srv', 'data', 'harvest', 'harv', 'lidardata_overflights.csv')
    f_wind = os.path.join('/', 'srv', 'data', 'harvest', 'harv', 'co-ops', 'wind.txt')
    f_lid_cata = os.path.join('/', 'srv', 'data', 'harvest', 'cata', 'lidardata_overflights.csv')
    dir_ts = os.path.join('/', 'srv', 'data', 'harvest', 'timeseries')

    if args.harv is not None:
        if args.load is not None:
            rawdir = os.path.join(datafile, 'harv', 'uls')
            ov_outfile = os.path.join(datafile, 'harv', 'lidardata_overflights.csv')
            outdir = os.path.join(datafile, 'harv', 'six_minute')

            # LiDAR, Radar, and Bubbler data
            print('Reading Overflight Data from:', args.harv)
            # Call overflight averaging function
            ovdata = overflight.ovavg(args.harv, 'harv', outdir, rawdir)
            ovdata.to_csv(ov_outfile, na_rep='NaN')
            print('Writing Overflight Data to:', ov_outfile)
            print('-------------------------------------')
        # Create harvest time series
        plotfile_raw_lid = os.path.join(dir_ts, 'harv', 'TS_RawLiDAR.png')
        plotfile_corr_lid = os.path.join(dir_ts, 'harv', 'TS_CorrLiDAR.png')
        plotfile_raw_bub = os.path.join(dir_ts, 'harv', 'TS_RawBubbler.png')
        plotfile_corr_bub = os.path.join(dir_ts, 'harv', 'TS_CorrBubbler.png')
        plotfile_raw_rad = os.path.join(dir_ts, 'harv', 'TS_RawRadar.png')
        plotfile_corr_rad = os.path.join(dir_ts, 'harv', 'TS_CorrRadar.png')
        plotfile_avg_raw = os.path.join(dir_ts, 'harv', 'TS_RawAverage.png')
        plotfile_avg_corr = os.path.join(dir_ts, 'harv', 'TS_CorrAverage.png')
        time, lid, rpw, rad, bub, ssh, benchmark, backscatter, swh, wind = \
            loading.load_harv(f_lid_harv, args.harv, f_wind, args.lidarindex)
        harv_ts.raw_lidar(ssh, benchmark, lid, time, plotfile_raw_lid)
        harv_ts.corr_lidar(ssh, benchmark, lid, rpw, wind, time, plotfile_corr_lid)
        harv_ts.raw_bubbler(ssh, benchmark, bub, time, plotfile_raw_bub)
        harv_ts.corr_bubbler(ssh, benchmark, bub, time, swh, plotfile_corr_bub)
        harv_ts.raw_radar(ssh, benchmark, rad, time, plotfile_raw_rad)
        harv_ts.corr_radar(ssh, benchmark, rad, swh, wind, time, plotfile_corr_rad)
        harv_ts.avg_raw(ssh, benchmark, rad, bub, time, plotfile_avg_raw)
        harv_ts.avg_corr(ssh, benchmark, rad, bub, swh, wind, time, plotfile_avg_corr)

    if args.cata is not None:
        if args.load is not None:
            rawdir = os.path.join(datafile, 'cata', 'uls')
            ov_outfile = os.path.join(datafile, 'cata', 'lidardata_overflights.csv')
            outdir = os.path.join(datafile, 'cata', 'six_minute')

            # LiDAR, Radar, and Bubbler data
            print('Reading Overflight Data from:', args.cata)
            # Call overflight averaging function
            ovdata = overflight.ovavg(args.cata, 'cata', outdir, rawdir)
            ovdata.to_csv(ov_outfile, na_rep='NaN')
            print('Writing Overflight Data to:', ov_outfile)
            print('-------------------------------------')
        # Create Catalina Time Series
        plotfile_lid = os.path.join(dir_ts, 'cata', 'TS_RawLiDAR_Catalina.png')
        plotfile_acoust = os.path.join(dir_ts, 'cata', 'TS_RawAcoust_LA.png')
        plotfile_avg = os.path.join(dir_ts, 'cata', 'TS_RawAvg_Catalina.png')
        bs_max = 15
        time, lid, rpw, ssh, acoust, corr, swh, backscatter = loading.load_cata(f_lid_cata, args.cata, args.lidarindex)
        cata_ts.raw_lidar(ssh, lid, corr, backscatter, time, plotfile_lid, bs_max)
        cata_ts.raw_acoust(ssh, corr, acoust, backscatter, time, plotfile_acoust, bs_max)
        cata_ts.raw_avg(ssh, corr, lid, acoust, backscatter, time, plotfile_avg, bs_max)
