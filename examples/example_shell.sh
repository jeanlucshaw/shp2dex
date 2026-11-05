#!/bin/bash

# This example shows how shp2dex can be used to rasterize
# CIS shapefile from a UNIX shell and output a dex file
# named like the shapefile, next to the shapefile

shp2dex -g grid.csv data/shapefile.shp
