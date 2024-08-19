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

Ensure the following packages are installed to your python environement

```
argparse
os
re
warnings
shapefile
cartopy
matplotlib
shapely
numpy
pandas
termcolor
```

Clone this repository into a the path of your Python environment. For Anaconda virutal environments, this could be

```
cd /opt/anaconda3/myEnv/lib/Python3.7/site-packages
git clone https://github.com/jeanlucshaw/shp2dex.git shp2dex
```

For this utility to be available at the command line, add a
file called `shp2dex` on your shell path, for example
at `/usr/local/bin/` containing the following lines,

```
#!/path/to/bash
/path/to/python /path/to/shp2dex/shp2dex.py "$@"
```

## Note
More background information can be found at the following links:

   * [About the Egg code and CIS data products](https://www.canada.ca/en/environment-climate-change/services/weather-manuals-documentation/manice-manual-of-ice/chapter-5.htm)

   * [About the SIGRID-3 shapefile format used by the CIS](https://www.jcomm.info/index.php?option=com_oe&task=viewDocumentRecord&docID=4439)

   * [CIS sea ice glossary](https://www.canada.ca/en/environment-climate-change/services/ice-forecasts-observations/latest-conditions/glossary.html)

## Getting Started

Have a look at

* example_python.py
* example_julien.py

which demonstrate use of this module as part of a Python script, and at

* example_shell.sh

which demonstrates how to use the module via its command line interface.




