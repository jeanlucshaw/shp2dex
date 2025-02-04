"""
This example shows how shp2dex can be used to load a rasterized
CIS shapefile as a pandas dataframe in python. It can then be
further processed, or printed to CSV for transfer to another
program or programming language.
"""
import shp2dex.shp2dex as shp2dex

# Rasterize
df = shp2dex._shp2dex('data/shapefile.shp', 'grid.csv')

# View
df.head()

# Write to CSV
columns = ['lon', 'lat', 'E_CT', 'E_CA', 'E_SA', 'E_FA']
df.loc[:, columns].to_csv('example_raster.csv', index=False)
