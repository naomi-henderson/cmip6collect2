import myconfig
class url2dict_:
    def __init__(self, keys, drop=[]):
        self.keys = keys
        self.drop = drop

    def __call__(self, url):
        tup = tuple(url.split('/')[-len(self.keys):])
        mdict = dict(zip(self.keys,tup))
        for key in self.drop:
            mdict.pop(key, None)
        return mdict
    
class dict2dir_:
    def __init__(self, zformat):
        self.zformat = zformat

    def __call__(self, zarrdict):
        return self.zformat % zarrdict

def dir2id(zdir):
    return tuple(zdir.split('/'))
    
def dict2id(dict):
    return dir2id(dict2dir(dict))

class dir2url_:
    def __init__(self, prefix):
        self.prefix = prefix

    def __call__(self, dir):
        return self.prefix + dir

class id2dict_:
    def __init__(self, keys):
        self.keys = keys

    def __call__(self, id):
        return dict(zip(self.keys,id))

def id2dir(id):
    return dict2dir(id2dict(id))

def dir2dict(dir):
    return id2dict(dir2id(dir))    


surl2dict = url2dict_(myconfig.source_keys,myconfig.drop_keys)
turl2dict = url2dict_(myconfig.target_keys)

dict2dir = dict2dir_(myconfig.target_format)
id2dict = id2dict_(myconfig.target_keys)

dir2url = dir2url_(myconfig.target_prefix)

dir2local = dir2url_(myconfig.local_target_prefix)
