"""
In this example, the initial grid was not formatted as expected
by shp2dex, i.e., it had an index column and column names

"id","x","y"
1,-71.2633744816721,51.8870744481099
2,-71.1651234450164,51.8870744481099
3,-71.0668724083606,51.8870744481099
4,-70.9686213717049,51.8870744481099
5,-70.8703703350491,51.8870744481099
6,-70.7721192983933,51.8870744481099
7,-70.6738682617376,51.8870744481099
8,-70.5756172250818,51.8870744481099
9,-70.4773661884261,51.8870744481099

for shp2dex, it needs to have only longitude and latitude separated
by a comma. To format it, run

$ awk -F, '(NR > 1){print $2","$3}' Grid_Julien.txt > Grid_Julien_formatted.txt 

or equivalent. The result is

-71.2633744816721,51.8870744481099
-71.1651234450164,51.8870744481099
-71.0668724083606,51.8870744481099
-70.9686213717049,51.8870744481099
-70.8703703350491,51.8870744481099
-70.7721192983933,51.8870744481099
-70.6738682617376,51.8870744481099
-70.5756172250818,51.8870744481099
-70.4773661884261,51.8870744481099
-70.3791151517703,51.8870744481099

and with this grid, the following script produces a rasterized
egg code file with the grid information, total concentration,
first ice class concentration, stage of developpment, and
form of ice.

"""
import shp2dex

# Rasterize
df = shp2dex._shp2dex('data/shapefile.shp', 'Grid_Julien_formatted.txt')

# View
df.head()

# Write to CSV
columns = ['lon', 'lat', 'E_CT', 'E_CA', 'E_SA', 'E_FA']
df.loc[:, columns].to_csv('julien_raster.csv', index=False)
