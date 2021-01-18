import requests
import zarr
import fsspec
import warnings
import myconfig
warnings.simplefilter('always', UserWarning)

def id2jdict(id):
    client = requests.session()
    baseurl =  'http://hdl.handle.net/api/handles/'

    url = f'{baseurl}{id[4:]}'
    r = client.get(url)
    r.raise_for_status()
    dict2 = r.json()
    dtype = [s['type'] for s in dict2['values']]
    ddata = [s['data']['value'] for s in dict2['values']]
    return dict(zip(dtype,ddata))

def gsurl2search(gsurl):
    values = gsurl[11:-1].split('/')
    keys = myconfig.target_keys
    return dict(zip(keys,values))

def gsurl2tracks(gsurl):
    mapper = fsspec.get_mapper(gsurl)
    group = zarr.open_consolidated(mapper)
    tracks = group.attrs['tracking_id']
    tracking_ids = tracks.split('\n')

    if len(tracking_ids) != len(set(tracking_ids)):
        msg = f'\nnetcdf file tracking_ids are NOT UNIQUE!\n{tracking_ids}\n'
        warnings.warn("\n" + msg)

    return tracks

def _get_dsid(tracks):
    ids = []
    for track in tracks.split('\n'):
        jdict = id2jdict(track)
        ds_tracking_id = jdict['IS_PART_OF']
        ids += [ds_tracking_id]
        
    if len(set(ids)) > 1:
        warnings.warn(f'\n\nmultiple dataset_ids correspond to the dataset tracking_ids!\n{ids}\n')

    return ds_tracking_id

def _get_dsdict(tracks):
    # TEST FOR MULTIPLE DATASETS? 
    ds_tracking_id = _get_dsid(tracks).split(';')
    if len(set(ds_tracking_id)) > 1:
        warnings.warn(f'multiple dataset_ids correspond to the dataset tracking_ids!\n{ds_tracking_id}')
    ds_tracking_id = ds_tracking_id[0]
    jdict = id2jdict(ds_tracking_id)
    return jdict

def tracks2cloudversion(tracks):
    ds_tracking_id = _get_dsid(tracks)
    if len(set(ds_tracking_id.split(';'))) > 1:
        warnings.warn(f'multiple dataset_ids correspond to the dataset tracking_ids!\n{ds_tracking_id}')

    versions = []
    for dsid in ds_tracking_id.split(';'):
        jdict = id2jdict(dsid)
        versions += [jdict['VERSION_NUMBER']]
         
    return (sorted(list(set(versions))),jdict)

def tracks2version(tracks):
    (version_cloud,jdict) = tracks2cloudversion(tracks)
    print('current version from GC tracks = ',version_cloud)

    (version_latest, jdict) = dict2lversion(jdict)

    return version_latest, jdict

def dict2lversion(jdict):

    while 'REPLACED_BY' in jdict.keys():  # is there a newer version? keep going until we find the most recent
        ds_id = jdict['REPLACED_BY']
        warnings.warn(f'\n\n*** Newer version exists, see: http://hdl.handle.net/{ds_id}\n')
        jdict = id2jdict(ds_id)

    version_latest = jdict['VERSION_NUMBER']
    
    if 'ERRATA_IDS' in jdict.keys():
        eid = jdict['ERRATA_IDS']
        warnings.warn(f'\n\n*** Errata exists, see: https://errata.es-doc.org/static/view.html?uid={eid}\n')

    return version_latest, jdict

def tracks2source(tracks):
    jdict =  _get_dsdict(tracks)

    (version, jdict) = dict2lversion(jdict)

    return jdict2source(jdict)

def dsid2source(dsid):
    jdict = id2jdict(dsid)
    return jdict2source(jdict)

def jdict2source(jdict):
    surls = []
    for track in jdict['HAS_PARTS'].split(';'):
        jdict_file = id2jdict(track)
        keys = jdict_file.keys()
        if 'URL_ORIGINAL_DATA' in keys:        
            url = jdict_file['URL_ORIGINAL_DATA'].split('"')[1]
            surls += [url]
        elif 'URL_REPLICA' in keys:
            url = jdict_file['URL_REPLICA'].split('"')[1]
            surls += [url]
    return sorted(surls) 
