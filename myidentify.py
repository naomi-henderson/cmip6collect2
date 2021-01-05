import requests
import zarr
import fsspec

def tracking2version(zstore,method='fsspec'):

    client = requests.session()
    baseurl =  'http://hdl.handle.net/api/handles/'
    query1 = '?type=IS_PART_OF'
    query2 = '?type=VERSION_NUMBER'

    # get the `netcdf_tracking_ids` from the zstore metadata
    if method == 'fsspec':
        mapper = fsspec.get_mapper(zstore)
    else:
        mapper = zstore        
    group = zarr.open_consolidated(mapper)     
    tracking_ids = group.attrs['tracking_id']
        
    # query the dataset handler to obtain `dataset_tracking_id` and `version`
    versions = []
    datasets = []
    for file_tracking_id in tracking_ids.split('\n')[0:1]:
        url = baseurl+file_tracking_id[4:]+query1
        r = client.get(url)
        try:
            r.raise_for_status()
            dataset_tracking_id = r.json()['values'][0]['data']['value']
        except:
            #assert False , f"{zstore}: {tracking_ids} , tracking_id not found"
            dataset_tracking_id = 'unknown'
            print(f"{zstore}: {tracking_ids}, {url} , dataset tracking_id not found")
            
        datasets += [dataset_tracking_id]
        if ';' in dataset_tracking_id:
            # multiple dataset_ids erroneously reported
            dtracks = dataset_tracking_id.split(';')
            vs = []
            for dtrack in dtracks:
                url2 = baseurl + dtrack[4:] + query2
                r = client.get(url2)
                try:
                    r.raise_for_status()
                    v = r.json()['values'][0]['data']['value']
                except:
                    #assert False,f"{zstore}: {file_tracking_id} , tracking_id not found"
                    print(f"{zstore}: {tracking_ids}, {url2} , dataset tracking_id not found")
                    v = 'unknown'
                
                vs += [v]
            v = sorted(vs)[-1]    
        else:
            url2 = baseurl + dataset_tracking_id[4:] + query2
            r = client.get(url2)
            try:
                r.raise_for_status()
                v = r.json()['values'][0]['data']['value']
            except:
                #assert False,f"{zstore}: {dtrack} , tracking_id not found"
                print(f"{zstore}: {tracking_ids}, {url2} , dataset tracking_id not found")
                v = 'unknown'
            
        versions += [v]

    version_id = list(set(versions))
    dataset_id = list(set(datasets))

    assert len(version_id)==1
    
    return dataset_id[0], version_id[0]

