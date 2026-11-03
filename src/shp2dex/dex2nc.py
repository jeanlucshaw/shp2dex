"""

Read gridded sea ice ASCII files (.dex) into xarray/netcdf

To use this source as a module in third party scripts, write:

    from shp2dex.dex2nc import dex2ds

which reads the .dex file given as argument into an xarray
dataset. This module can also be used as a command line
application, to convert .dex to netcdf e.g. :

    $ python dex2nc.py my_file_20200315.dex
    $ python dex2nc.py *.dex

or since conversion is slow (10-30 seconds) because of the
mix of strings and numerics in the .dex format, parallelize
the conversion on systems with sufficient ressources:

    $ for f in `ls *.dex`; do python dex2nc.py $f & done

By default, the .dex file's name (extension removed) is used
for the output netcdf file, but users can specify the output
file name for single file conversions.

Notes about converted data:

    1) egg code notation using the `.` character substitutes
       the `.` character with `0`, such as to obtain numeric
       data only for stage of developpment.

    2) egg code notation using th `+` character substitutes
       this character for `.9`, e.g., `9+` becomes `9.9`. This
       was chosen to be consistent with the 1/10 scale of sea
       ice concentration and the idea that `9+` represents
       the most concentrated sea ice possible without consolidation.

    3) .dex files replace the egg code information with strings
       for grid cells which are ice free, whitout ice information,
       containing landfast ice, or points on land. This is replaced
       by flags from 1 to 4, respectively, and 0 meaning sea ice
       is present at the grid point.

"""
import pandas as pd
import xarray as xr
import argparse as ap
import warnings
import os
import re
from datetime import datetime


def dex2ds(file_):
    """
    Read a (.dex) sea ice file into xarray

    Parameters
    ----------
    file_ : str
        name and path ot the .dex sea ice file to read.

    Returns
    -------
    dataset : xarray.Dataset
        Concentrations, stages, form, flags, and metadata.

    """

    # -------------------------------------------------------------------------
    # Helper functions: convert string data to coded integer (or numeric) types
    # -------------------------------------------------------------------------


    def _strip_plus(x):
        """ simplify concentrations: 9+ ->  9.9 (not consolidated, but no open water) """
        if isinstance(x, str):
            x = x.replace(r'9+', '9.9')
        return x


    def _strip_dots(x):
        """ simplify stage of developpment of ice: 1. 4. 7. 8. 9. -> 10, 40, 70, etc.  """
        if isinstance(x, str):
            x = x.replace(r'.', '0')
        return x


    def _num_flags(x):
        """
        metadata are encoded in column 3 (CT). use this dict to convert tu numeric
        flags destined for a dedicated column.

        Flag meanings
        --------

        0: ice
        1: ice free
        2: missing data
        3: fast-ice

        """
        conv = {'IF': 1,
                'missing': 2,
                'Fast-ice': 3,
                '1': 0,
                '2': 0,
                '3': 0,
                '4': 0,
                '5': 0,
                '6': 0,
                '7': 0,
                '8': 0,
                '9': 0,
                '9+': 0,
                '9.9': 0,
                '10': 0,
                }

        return conv[x]


    # Read dex: column format
    col_names = ['lon', 'lat', 'CT', 'CA', 'SA', 'FA', 'CB', 'SB', 'FB', 'CC', 'SC', 'FC']
    col_types = [float, float, str, str, str, str, str, str, str, float, float, float]
    types = {n_: t_ for n_, t_ in zip(col_names, col_types)}

    # Read dex: into dataframe
    df = pd.read_csv(file_,
                     sep=r'\s+',
                     parse_dates=False,
                     names=col_names,
                     index_col=col_names[:2],
                     dtype=types,
                     na_values='X',
                     engine='c')

    # Make concentrations compatible with numeric formats
    for c_ in ['CT', 'CA']: # , 'CB', 'CC']:
        df[c_]= df[c_].apply(_strip_plus)

    # Make stages compatible with numeric formats
    for f_ in ['SA', 'SB', 'SC']:
        df[f_]= df[f_].apply(_strip_dots)

    # Convert total concentration indications to flags
    df['flag'] = df.CT.apply(_num_flags)

    # Convert to numeric type
    for v_ in col_names[2:]:
        df[v_] = pd.to_numeric(df[v_], errors='coerce')

    # Convert to xarray
    dataset = df.to_xarray()

    # Add land flags
    dataset['flag'] = dataset.flag.where(~dataset.flag.isnull(), 4)

    # Add time coordinate
    date_str = re.findall('[0-9]{8}', file_)[0]
    date = pd.Timestamp(f'{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}')
    dataset = dataset.expand_dims({'time': [date]})

    # --------
    # Metadata
    # --------

    # Coordinate metadata
    dataset['lon'].attrs['standard_name'] = 'longitude'
    dataset['lon'].attrs['long_name'] = 'Longitude'
    dataset['lon'].attrs['units'] = 'degrees west'
    dataset['lon'].attrs['axis'] = 'X'
    dataset['lat'].attrs['standard_name'] = 'latitude'
    dataset['lat'].attrs['long_name'] = 'Latitude'
    dataset['lat'].attrs['units'] = 'degrees north'
    dataset['lat'].attrs['axis'] = 'Y'
    dataset['time'].attrs['standard_name'] = 'time'
    dataset['time'].attrs['long_name'] = 'Time'
    dataset['time'].attrs['axis'] = 'T'

    # Concentrations metadata
    dataset['CT'].attrs['long_name'] = 'Sea ice total concentration'
    dataset['CT'].attrs['units'] = '1/10 m^2/m^2'
    dataset['CA'].attrs['long_name'] = 'Sea ice first class concentration'
    dataset['CA'].attrs['units'] = '1/10 m^2/m^2'
    dataset['CB'].attrs['long_name'] = 'Sea ice second class concentration'
    dataset['CB'].attrs['units'] = '1/10 m^2/m^2'
    dataset['CC'].attrs['long_name'] = 'Sea ice third class concentration'
    dataset['CC'].attrs['units'] = '1/10 m^2/m^2'

    # Stage metadata
    _values = '1 2 3 4 5 6 7 8 9 10 40'
    _ice_thick = "<10 <10 10-30 10-15 15-30 >30 30-70 30-50 50-70 70-120 >120"
    _ice_type = """new nilas young grey grey-white first-year thin-first-year
                   first-stage-thin-first-year second-stage-thin-first-year
                   medium-first-year-ice thick-first-year-ice"""
    dataset['SA'].attrs['long_name'] = 'Sea ice first class stage of developpment'
    dataset['SB'].attrs['long_name'] = 'Sea ice second class stage of developpment'
    dataset['SC'].attrs['long_name'] = 'Sea ice third class stage of developpment'
    for l_ in 'ABC':
        dataset[f'S{l_}'].attrs['units'] = 'code'
        dataset[f'S{l_}'].attrs['values'] = _values
        dataset[f'S{l_}'].attrs['ice_type'] = _ice_type
        dataset[f'S{l_}'].attrs['ice_thick_cm'] = _ice_thick

    # Form metadata
    _values = '1 2 3 4 5 6 7 8 9'
    _ice_width = "- <2 2-20 20-100 100-500 500-2000 2000-10000 >10000 - -"
    _ice_type = """pancake small-cake cake small-floe medium-floe big-floe
                   vast-floe giant-floe fast-ice iceberg"""
    dataset['FA'].attrs['long_name'] = 'Sea ice first class form'
    dataset['FB'].attrs['long_name'] = 'Sea ice second class form'
    dataset['FC'].attrs['long_name'] = 'Sea ice third class form'
    for l_ in 'ABC':
        dataset[f'F{l_}'].attrs['units'] = 'code'
        dataset[f'F{l_}'].attrs['values'] = _values
        dataset[f'F{l_}'].attrs['ice_type'] = _ice_type
        dataset[f'F{l_}'].attrs['ice_width_m'] = _ice_thick

    # Flag metadata
    dataset['flag'].attrs['long_name'] = 'data type'
    dataset['flag'].attrs['values'] = '0 1 2 3 4'
    dataset['flag'].attrs['meanings'] = 'ice water missing fast-ice land'

    # Global metadata
    dataset.attrs = {'Conventions': 'CF-1.8',
                     'title': 'Gridded Canadian Ice Service egg code data',
                     'institution': 'Maurice Lamontagne Institute',
                     'source': 'CIS, processed with https://github.com/jeanlucshaw/shp2dex',
                     'description': 'Ice charts gridded using a point-in-polygon routine.',
                     'history': '',
                     'contact': 'Jean-Luc.Shaw@dfo-mpo.gc.ca'}

    # Set variable range attributes
    for v in [*dataset.data_vars, 'lon', 'lat']:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', RuntimeWarning)
            dataset[v].attrs['data_min'] = dataset[v].min().values
            dataset[v].attrs['data_max'] = dataset[v].max().values

    # Add creation time stamp
    dataset.attrs['history'] = 'Created: %s' % datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    return dataset

# -------
# Testing
# -------

# ds = dex2ds('GEC_H_20190325.dex')

# ---
# CLI
# ---
if __name__ == "__main__":

    # Manage input argument
    parser = ap.ArgumentParser(usage=__doc__)
    parser.add_argument('filename',
                        help='Expression designating the file(s) to process',
                        nargs='+')
    parser.add_argument('-o',
                        '--outname',
                        help='Name of the netcdf file to produce (single input file only)',
                        default=None)
    args = parser.parse_args()

    for filename in args.filename:
        # By default use the input file name as the output file name
        if (args.outname == None) | (len(args.filename) > 1):
            stem, _ = os.path.splitext(os.path.basename(filename))
            outname = '%s.nc' % stem

        # Otherwise, use the user specified name
        else:
            outname = args.outname

        # Read and convert to xarray Dataset
        ds = dex2ds(filename)

        # Save to netcdf
        enc = {v_: dict(zlib=True, complevel=5) for v_ in ds.data_vars}
        ds.to_netcdf(outname, encoding=enc, engine='netcdf4')


