#!/bin/bash

# This example shows how shp2dex can be used to rasterize
# CIS shapefile from a UNIX shell and output a dex file
# named like the shapefile, next to the shapefile

python shp2dex.py -g grid.csv data/shapefile.shp
