CalVal Time Series at Harvest and Catalina
==========================================

Title: calval-timeseries

Options
-------

optional arguments:
  -h, --help            show this help message and exit
  --harv HARV           Create Harvest Time Series. Argument is location of
                        file with satellite data.
  --cata CATA           Create Catalina Time Series. Argument is location of
                        file with satellite data.
  -i LIDARINDEX, --lidarindex LIDARINDEX
                        Type of lidar data to use for time series. l_6m_quad2h
                        is a 4 hour quadratic regression on the 6 minute data.
                        l_mean is an average of 2200 seconds of data around
                        the overflight. l_lin1100 is a linear regression of
                        2200 seconds of data around the overflight. l_quad2h
                        is a quadratic regression of 4 hours of data around
                        the overflight. l_6m_quad2h is the default value.
  -l, --load            Loads and averages LiDAR data. This is for when new
                        overflight data is available.


Related Files
-------------
Input satellite data file for Harvest:
   - Column 1: Can either be seconds since J2000 or a string containing the date
   - Column 2: Satellite Measurement
   - Column 3: GPS Benchmark
   - Column 4: Backscatter Measurement
   - Column 5: Significant Wave Height Measurement

Input satellite data file for Catalina:
   - Column 1: Can either be seconds since J2000 or a string containing the date
   - Column 2: Satellite Measurement
   - Column 3: Vertical Land Motion correction

Author
------
Adam Dodge

University of Colorado Boulder

Colorado Center for Astrodynamics Research

Jet Propulsion Laboratory

Purpose
-------

This program is written to allow for the creation of Calibration/Validation time series at both the Harvest Oil Platform
and Catalina Island CalVal locations. At harvest, it creates time series for the LiDAR, Bubbler, and Radar datasets,
as well as their corrected datasets and the average between the radar and bubbler. At Catalina, it creates time series
for the LiDAR and LA acoustic datasets, as well as a linear interpolation between the two to get a measurement in the
middle of the san pedro channel. 

