## About

Convert Canadian ice service (CIS) ESRI shapefiles to ascii format (dex).

CIS daily ice analysis charts (dailys) and regional analysis charts (weeklys) are
collected every day on mixing and processed to provide information such as,

   * Ice thickness maps.
   * First occurence maps.
   * Total gulf, Newfoundland shelf and Scotian Shelf ice volumes.
   * Comparisons to climatology.

These analyses are performed by a combination of Perl/awk routines and are
facilitated by first transforming the shapefiles to gridded ascii plain text
in a format called dex, containing geographical coordinates and egg code data.
Time information is carried by the file name (YYYYMMDD) and the columns in
the file are ordered as follows,

   1. Longitude (west)
   2. Latitude
   3. Total ice concentration
   4. Partial ice concentration (thickest ice)
   5. Stage of developpment (thickest ice)
   6. Form of ice (thickest ice)
   7. Partial ice concentration (second thickest ice)
   8. Stage of developpment (second thickest ice)
   9. Form of ice (second thickest ice)
   10. Partial ice concentration (third thickest ice)
   11. Stage of developpment (third thickest ice)
   12. Form of ice (third thickest ice)

This module performs the conversion and is meant to be called from command
line. Command line interface description can be shown by entering,

```
$ shp2dex -h
```

## Installation

Create a virtual environment containing this package's dependencies. In conda, either

```
conda create -n shp2dex Python=3.12 pandas=2.2.2 cartopy=0.23.0 termcolor=2.4.0 xarray=2024.7.0
```

should install all the appropriate dependencies. Alternatively, you can use the provided
`yml` file to build the environment, i.e.,

```
conda env create -f requirement.yml
```

the output of `pip freeze > requirements.txt` is also included for pip users. Once the
environment is set up, navigate to the `site-packages` folder and clone this repository.

```
cd /path/to/anaconda/envs/shp2dex/lib/python3.12/site-packages
git clone https://github.com/jeanlucshaw/shp2dex.git shp2dex
```

For this utility to be available at the command line, add a
file called `shp2dex` on your shell path, for example
at `/usr/local/bin/` containing the following lines,

```
#!/path/to/bash
/path/to/python /path/to/shp2dex/shp2dex.py "$@"
```

To test the installation, run `shp2dex -h` from the command line or run the included
examples of command-line and scripted use cases.

## Note
More background information can be found at the following links:

   * [About the Egg code and CIS data products](https://www.canada.ca/en/environment-climate-change/services/weather-manuals-documentation/manice-manual-of-ice/chapter-5.htm)

   * [About the SIGRID-3 shapefile format used by the CIS](http://dx.doi.org/10.25607/OBP-1498.2)

   * [CIS sea ice glossary](https://www.canada.ca/en/environment-climate-change/services/ice-forecasts-observations/latest-conditions/glossary.html)

## Getting Started

Have a look at

* example_python.py
* example_julien.py

which demonstrate use of this module as part of a Python script, and at

* example_shell.sh

which demonstrates how to use the module via its command line interface.

## NetCDF integration

Although advantageous for software designed to ingest it, the .dex format can be cumbersome to integrate to new software because
it mixes string characters and numbers in some data columns, and has different numbers of columns accros its rows. To facilitate
the use of existing .dex file data bases, the `dex2nc` module included in this package reads the .dex format into `xarray` dataset objects.
Conversion to netCDF, a common format for the storage of raster data can then be performed via user scripts:

```
from shp2dex.dex2nc import dex2ds

ds = dex2ds('my_file_YYYYMMDD.dex')
ds.to_netcdf('my_file_YYYYMMDD.nc')
```

or using the module as a command line application

```
$ python /path/to/dex2nc.py /path/to/my_file_YYYYMMDD.dex
$ python /path/to/dex2nc.py /path/to/*.dex
```



