import myconfig
from mydataset import dir2url, dir2local, dir2dict
from glob import glob
import os
from subprocess import Popen, PIPE
import pandas as pd

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
def Check(ds_dir):
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
        return 2, exception 

    # is zarr already in cloud?  Unreliable
    try:
        contents = fs.ls(gsurl)
    except:
        contents = []

    if any("zmetadata" in s for s in contents):
        exception = 'store already in cloud'
        return 3, exception 
    
    # does zarr exist on active drive?  
    contents = glob(f'{local}/*')
    if any("zmetadata" in s for s in contents):
        exception = 'store already exists locally, but not in cloud'
        return 4, exception 
    
    return 0, exception

import requests
import shutil
@exception_handler
def Download(ds_dir):
    gfiles = []
    check_size = True
    
    df_needed = myconfig.df_needed

    df = df_needed[df_needed.ds_dir == ds_dir]

    if len(df) != df.start.nunique():
       trouble = "netcdf files overlapping in time?"
       return [],1,trouble
    
    files = sorted(df.ncfile.unique())
    tmp = myconfig.local_source_prefix

    for file in files:
        save_file = tmp + file
        print(save_file)
        df_file = df[df.ncfile == file]
        expected_size = df_file.file_size.values[0]
        url = df_file.url.values[0]

        if os.path.isfile(save_file):
            if abs(os.path.getsize(save_file) - expected_size) <= 1000 :
                gfiles += [save_file]
                continue
        try:
            r = requests.get(url, timeout=3.1, stream=True)
            #print(r.headers['content-type'])
            with open(save_file, 'wb') as f:
                shutil.copyfileobj(r.raw, f)  
            doit(f'touch {save_file}')
            #time.sleep( 1 )  # does not help
        except:
            trouble = 'Server not responding for: ' + url 
            return [],2,trouble

        if check_size:
            actual_size = os.path.getsize(save_file)
            if actual_size != expected_size:
                if abs(actual_size - expected_size) > 200:
                    trouble = 'netcdf download not complete'
                    return [],3,trouble

        gfiles += [save_file]
                           
    return sorted(gfiles),0,''

import warnings
import datetime
import numpy as np
import xarray as xr
@exception_handler
def ReadFiles(ds_dir, gfiles):
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
            dstr = 'error in open_mfdataset'
            return df7,1,dstr
                
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
        if '3hr' in table_id:
            if not (np.diff(year).sum() == len(year)-1) | (np.diff(year).sum() == len(year)-2):
                dstr = 'trouble with 3hr time grid'
                return df7,2,dstr
        elif 'dec' in table_id:
            if not (np.diff(year).sum()/10 == len(year)) | (np.diff(year).sum()/10 == len(year)-1):
                dstr = 'trouble with dec time grid'
                return df7,3,dstr
        else:
            if not np.diff(year).sum() == len(year)-1:
                dstr = 'trouble with time grid'
                return df7,4,dstr

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
        chunksize = min(chunksize,int(nt/2))
        df7 = df7.chunk(chunks={'time' : chunksize})   # yes, do it again

    return df7, 0, ''

@exception_handler
def SaveAsZarr(ds_dir, ds):
    zbdir = dir2local(ds_dir)
    gsurl = dir2url(ds_dir)
    variable_id = ds.variable_id
    if os.path.isfile(zbdir+'/.zmetadata'):
        print('zarr already exists')
        return 0,''

    try:
        ds.to_zarr(zbdir, consolidated=True, mode='w')
    except:
        return 2,f'{zbdir:} to_zarr failure'

    if not os.path.isfile(zbdir+'/.zmetadata'):
        return 3,'to_zarr failure'
    
    return 0, ''

@exception_handler
def Upload(ds_dir):   
    zbdir = dir2local(ds_dir)
    gsurl = dir2url(ds_dir)

    fs = myconfig.fs

    # upload to cloud
    if doit(f'/usr/bin/gsutil -m cp -r {zbdir} {gsurl}'):
        print(f'/usr/bin/gsutil -m cp -r {zbdir} {gsurl}')
        return gsurl, 1, 'not uploaded correctly'
        
    size_remote = fs.du(gsurl)
    size_local = getFolderSize(zbdir)
    if abs(size_remote - size_local) > 100: 
        return gsurl, 2,'zarr not completely uploaded'

    try:
        ds = xr.open_zarr(fs.get_mapper(gsurl), consolidated=True)
        print(f'successfully uploaded as {gsurl}')
    except:
        return gsurl, 3,'store did not get saved to GCS properly'

    return gsurl, 0, ''

@exception_handler
def Cleanup(ds_dir, gfiles):   
    zbdir = dir2local(ds_dir)
    
    #if doit(f'/bin/rm -rf {zbdir}'):
    #    print(f'{zbdir} not removed')

    for gfile in gfiles:
        if doit('/bin/rm -f '+ gfile):
              print(f'{gfile} not removed')

    return 0, ''
