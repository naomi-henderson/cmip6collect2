import myconfig
from mydataset import id2dict, dir2url
from glob import glob
import os
from subprocess import Popen, PIPE
import pandas as pd
import time

def doit(command,verbose=False): 
    cmd = command.split(' ')
    try:
        p = Popen(cmd, stdout=PIPE, stderr=PIPE, text=True)
    except:
        print(f'failure: {cmd}')
        return 1
    
    stdout, stderr = p.communicate()

    if verbose:
        print(stdout)
        print(stderr)

    return 0

def set_bnds_as_coords(ds):
    new_coords_vars = [var for var in ds.data_vars if 'bnds' in var
                       or 'bounds' in var]
    ds = ds.set_coords(new_coords_vars)
    return ds

def set_bnds_as_coords_drop_height(ds):
    ds = set_bnds_as_coords(ds)
    if 'height' in ds.coords:
        ds = ds.drop('height')
    return ds

def set_bnds_as_coords_drop_bnds(ds):
    ds = set_bnds_as_coords(ds)
    if 'bnds' in ds.coords:
        ds = ds.drop('bnds')
    return ds


from functools import partial
def getFolderSize(p):
    prepend = partial(os.path.join, p)
    return sum([(os.path.getsize(f) if os.path.isfile(f) else
                                  getFolderSize(f)) for f in
                map(prepend, os.listdir(p))])

def exception_handler(func):   
    def inner_function(*args, **kwargs):
        #print(f'call {func.__name__}:')
        try:
            result = func(*args, **kwargs) 
        except:
            result = f"{func.__name__} failed"
        return result
    return inner_function

def str_match(x,y):
    return (x==y)|(x=='all')

def id_match(x,y):
    result = True
    x_tup = x.split('/')
    y_tup = y.split('/')
    result = [str_match(x,y) for x,y in zip(x_tup,y_tup)]
    return False not in result

def read_codes(ds_dir):
    dex = pd.read_csv('csv/error_codes.csv',skipinitialspace=True)
    codes = []
    for item, row in dex.iterrows():
        if id_match(row.ds_dir,ds_dir):
            codes += [row.code]
    return codes

@exception_handler
def Check(ds_dir,dir2local):
    gsurl = dir2url(ds_dir)+'/'
    local = dir2local(ds_dir)
    exception = ''

    df_GCS = myconfig.df_GCS
    fs = myconfig.fs

    codes = read_codes(ds_dir)
    if 'noUse' in codes:
        exception =  'noUse in codes'
        return 1, exception 

    cstore = df_GCS[df_GCS.zstore == gsurl]
    if len(cstore) > 0:
        exception = 'store already in cloud catalog'
        return 1, exception 

    # is zarr already in cloud?  Unreliable
    try:
        contents = fs.ls(gsurl)
    except:
        contents = []

    if any("zmetadata" in s for s in contents):
        exception = 'store already in cloud'
        return 1, exception 
    
    # does zarr exist on active drive?  
    contents = glob(f'{local}/*')
    if any("zmetadata" in s for s in contents):
        exception = 'store already exists locally, but not in cloud'
        return 2, exception 
    
    return 0, exception

import requests
import shutil
@exception_handler
def Download(ds_dir):
    gfiles = []
    check_size = True
    
    df_needed = myconfig.df_needed

    df = df_needed[df_needed.ds_dir == ds_dir]

    nversions = df.version_id.nunique()
    if nversions > 1:
       codes = read_codes(ds_dir)
       if 'allow_versions' in codes:
           print('allowing multiple versions',df.version_id.unique())
       else:
           print('keeping only last version of',nversions)
           lastversion = df.version_id.unique()[-1]
           df = df[df.version_id == lastversion]
    
    lendf = len(df)
    dfstartn = df.start.nunique()
    if lendf != dfstartn:
       trouble = f"noUse, netcdf files overlapping in time? {lendf} and {dfstartn}"
       return [],2,trouble

    files = sorted(df.ncfile.unique())
    tmp = myconfig.local_source_prefix

    for file in files:
        save_file = tmp + file
        df_file = df[df.ncfile == file]
        expected_size = int(df_file.file_size.values[0])
        url = df_file.url.values[0]
        print(url)

        if os.path.isfile(save_file):
            if abs(os.path.getsize(save_file) - expected_size) <= 1000 :
                gfiles += [save_file]
                continue  # already have, don't need to get it again
        try:
            #r = requests.get(url, timeout=3.1, stream=True)
            r = requests.get(url, timeout=(5, 14), stream=True)
            #print(r.headers['content-type'])
            with open(save_file, 'wb') as f:
                shutil.copyfileobj(r.raw, f)  
            command = f'touch {save_file}'
            doit(command)
        except:
            trouble = 'Server not responding for: ' + url 
            return [],1,trouble

        if check_size:
            actual_size = os.path.getsize(save_file)
            if actual_size != expected_size:
                if abs(actual_size - expected_size) > 200:
                    trouble = 'netcdf download not complete'
                    return [],1,trouble

        gfiles += [save_file]
        time.sleep(2)
                           
    return sorted(gfiles),0,''

import warnings
import datetime
import numpy as np
import xarray as xr
@exception_handler
def ReadFiles(ds_dir, gfiles, dir2dict):
    table_id = dir2dict(ds_dir)['table_id']

    dstr = ''
    # guess chunk size by looking a first file: (not always a good choice - e.g. cfc11)
    nc_size = os.path.getsize(gfiles[0])

    ds = xr.open_dataset(gfiles[0])
    svar = ds.variable_id
    nt = ds[svar].shape[0]

    chunksize_optimal = 5e7
    chunksize = max(int(nt*chunksize_optimal/nc_size),1)
    preprocess = set_bnds_as_coords
    join = 'exact'

    codes = read_codes(ds_dir)
    if 1==1:
        for code in codes:
            if 'deptht' in code:
                fix_string = '/usr/bin/ncrename -d .deptht\,olevel -v .deptht\,olevel -d .deptht_bounds\,olevel_bounds -v .deptht_bounds\,olevel_bounds '
                for gfile in gfiles:
                    dstr += f'fixing deptht trouble in gfile:{gfile}'
                    if doit(f'{fix_string} {gfile}'):
                        print('fix_string did not execute')
            if 'remove_files' in code:
                command = '/bin/rm nctemp/*NorESM2-LM*1230.nc'
                if doit(command):
                    print('file not removed')
                gfiles = [file for file in gfiles if ('1231.nc' in
                                                      file)]
            if 'fix_time' in code:
                preprocess = convert2gregorian
            if 'drop_height' in codes:
                preprocess = set_bnds_as_coords_drop_height
            if 'drop_bnds' in codes:
                preprocess = set_bnds_as_coords_drop_bnds
            if 'override' in code:
                join = 'override'

    df7 = 'none'
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")

        try:
            if 'time' in ds.coords:  
                df7 = xr.open_mfdataset(gfiles,
                                        preprocess=preprocess,
                                        data_vars='minimal',
                                        chunks={'time': chunksize}, use_cftime=True,
                                        join=join, combine='nested',
                                        concat_dim='time')
            else: # fixed in time, no time grid
                df7 = xr.open_mfdataset(gfiles,
                                        preprocess=set_bnds_as_coords,
                                        combine='by_coords',
                                        join=join,
                                        data_vars='minimal')
        except:
            dstr = 'noUse, error in open_mfdataset'
            return df7,2,dstr
                
    if 1==1:
        for code in codes:
            if 'drop_tb' in code: # to_zarr cannot do chunking with time_bounds/time_bnds which is cftime (an object, not float)
                timeb = [var for var in df7.coords if 'time_bnds' in
                         var or 'time_bounds' in var][0]
                df7 = df7.drop(timeb)
            if 'time_' in code:
                [y1,y2] = code.split('_')[-1].split('-')
                df7 = df7.sel(time=slice(str(y1)+'-01-01',str(y2)+'-12-31'))
            if '360_day' in code:
                year = gfiles[0].split('-')[-2][-6:-2]
                df7['time'] = cftime.num2date(np.arange(df7.time.shape[0]), units='months since '+year+'-01-16', calendar='360_day')
                #print('encoding time as 360_day from year = ',year)
            if 'noleap' in code:
                year = gfiles[0].split('-')[-2][-6:-2]
                df7['time'] = xr.cftime_range(start=year,
                                              periods=df7.time.shape[0],
                                              freq='MS',
                                              calendar='noleap').shift(15, 'D')
                #print('encoding time as noleap from year = ',year)
            if 'missing' in code:
                del df7[svar].encoding['missing_value']

    #     check time grid to make sure there are no gaps in
#     concatenated data (open_mfdataset checks for mis-ordering)
    if 'time' in ds.coords:
        year = sorted(list(set(df7.time.dt.year.values)))
        print(np.diff(year).sum(), len(year))
        if 'abrupt-4xCO2' in ds_dir:
            print('exception made for disjoint time intervals')
        elif '3hr' in table_id:
            if not (np.diff(year).sum() == len(year)-1) | (np.diff(year).sum() == len(year)-2):
                dstr = 'noUse, trouble with 3hr time grid'
                return df7,2,dstr
        elif 'dec' in table_id:
            if not (np.diff(year).sum()/10 == len(year)) | (np.diff(year).sum()/10 == len(year)-1):
                dstr = 'noUse, trouble with dec time grid'
                return df7,2,dstr
        elif 'clim' in table_id:
            # IPSL seems to have two disjoint climatologies - ???
            # abrupt-4xCO2 also has multiple climatologies - ???
            # Dec 23, 2020 - decided to allow whatever time grid is provided
            print('exception made for clim table_id time intervals')
            #if len(year) != 1:
            #    dstr = 'noUse, trouble with clim time grid'
            #    return df7,2,dstr
        else:
            if not np.diff(year).sum() == len(year)-1:
                dstr = 'noUse, trouble with time grid'
                return df7,2,dstr

    dsl = xr.open_dataset(gfiles[0])
    tracking_id = dsl.tracking_id
    if len(gfiles) > 1:
        for file in gfiles[1:]:
            dsl = xr.open_dataset(file)
            tracking_id += '\n'+dsl.tracking_id
    df7.attrs['tracking_id'] = tracking_id

    date = str(datetime.datetime.now().strftime("%Y-%m-%d"))
    nstatus = date + ';created; by gcs.cmip6.ldeo@gmail.com'
    df7.attrs['status'] = nstatus

    
    if 'time' in df7.coords:
        nt = len(df7.time.values)
        chunksize = min(chunksize,max(1,int(nt/2)))
        df7 = df7.chunk(chunks={'time' : chunksize})   # yes, do it again

    return df7, 0, ''

@exception_handler
def SaveAsZarr(ds_dir, ds, dir2local):
    zbdir = dir2local(ds_dir)
    gsurl = dir2url(ds_dir)
    variable_id = ds.variable_id

    if os.path.isfile(zbdir+'/.zmetadata'):
        print('zarr already exists locally')
        return 0,''

    try:
        ds.to_zarr(zbdir, consolidated=True, mode='w')
    except:
        return 2,f'noUse, to_zarr failure'

    if not os.path.isfile(zbdir+'/.zmetadata'):
        return 3,f'{zbdir}: to_zarr not complete'
    
    return 0, ''

@exception_handler
def Upload(ds_dir, dir2local):   
    zbdir = dir2local(ds_dir)
    gsurl = dir2url(ds_dir)
    fs = myconfig.fs

    # upload to cloud
    if doit(f'/usr/bin/gsutil -m cp -r {zbdir} {gsurl}'):
        assert False, f'/usr/bin/gsutil -m cp -r {zbdir} {gsurl} FAILED'
        
    size_remote = fs.du(gsurl)
    size_local = getFolderSize(zbdir)
    if abs(size_remote - size_local) > 100: 
        assert False, f'{zbdir}/{gsurl} zarr not completely uploaded'

    try:
        ds = xr.open_zarr(fs.get_mapper(gsurl), consolidated=True)
        exception = f'successfully uploaded to {gsurl}'
    except:
        assert False, f'{gsurl} does not load properly'

    return 0, exception

@exception_handler
def Cleanup(ds_dir, gfiles, dir2local, nc_remove = True, zarr_remove = False):   
    zbdir = dir2local(ds_dir)
    
    if zarr_remove:
        if doit(f'/bin/rm -rf {zbdir}'):
            print(f'{zbdir} not removed')

    if nc_remove:
        for gfile in gfiles:
             if doit('/bin/rm -f '+ gfile):
                  print(f'{gfile} not removed')

    return 0, ''
