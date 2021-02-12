import pandas as pd
import os
import datetime
import fsspec

import xarray as xr
def add_time_info(df,verbose=False):
    '''add start, stop and nt for all zstores in df'''
    starts = []; stops = []; nts = []; calendars = []; units = []; ttypes = []
    dz = df.copy()
    for index, row in df.iterrows():
        zstore = row.zstore
        ds = xr.open_zarr(fsspec.get_mapper(zstore),consolidated=True) 
        start = 'NA'
        start = 'NA'
        nt = '1'
        if 'time' in ds.coords:
            ttype = str(type(ds.time.values[0]))
            dstime = ds.time.values.astype('str')
            start = dstime[0][:10]
            stop = dstime[-1][:10]
            calendar = ds.time.encoding['calendar']
            unit = ds.time.encoding['units']
            nt = len(dstime)
            if verbose:
                print(zstore,start,stop,nt)
        starts += [start]
        stops += [stop]
        nts += [nt]
        calendars += [calendar]
        units += [unit]
        ttypes += [ttype]

    dz['start'] = starts
    dz['stop'] = stops
    dz['nt'] = nts
    dz['calendar'] = calendars
    dz['time_units'] = units
    dz['time_type'] = ttypes
    return dz

# define a simple search on keywords
def search_df(df, verbose= False, **search):
    '''search by keywords - if list, then match exactly, otherwise match as substring'''
    # keys is only used in verbose
    keys = ['activity_id','institution_id','source_id','experiment_id','member_id', 'table_id', 'variable_id', 'grid_label','version']
    d = df
    for skey in search.keys():
        
        if isinstance(search[skey], str):  # match a string as a substring
            d = d[d[skey].str.contains(search[skey])]
        else:
            dk = []
            for key in search[skey]:       # match a list of strings exactly
                dk += [d[d[skey]==key]]
            d = pd.concat(dk)
            keys.remove(skey)
    if verbose:
        for key in keys:
            print(key,' = ',list(d[key].unique()))      
    return d

from functools import partial
def getFolderSize(p):
    prepend = partial(os.path.join, p)
    return sum([(os.path.getsize(f) if os.path.isfile(f) else
                 getFolderSize(f)) for f in map(prepend, os.listdir(p))])

def remove_from_GC(gsurl,execute=False):
    '''gsurl is a GC zstore, use execute=False to test, execute=True to remove'''
    remove_from_GC_bucket(gsurl,execute=execute)
    remove_from_GC_listing(gsurl,execute=execute)
    return

def remove_from_local(gsurl,execute=False):
    '''gsurl is a GC zstore, use execute=False to test, execute=True to remove'''  
    remove_from_drives(gsurl,execute=execute)
    ret = remove_from_shelf(gsurl,execute=execute)
    if ret==1:
        remove_from_local_listings(gsurl,execute=execute)
    else:
        print('zstore is not in any shelf listings')
    return

def remove_from_GC_bucket(gsurl,execute=False):
    '''delete old version in GC'''
    command = '/usr/bin/gsutil -m rm -r '+ gsurl[:-1]
    if execute:
        os.system(command) 
    else:
        print(command)
    return

