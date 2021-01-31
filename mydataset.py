import myconfig
    
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

def dir2dict(zdir):
    tup = tuple(zdir.split('/'))
    return id2dict(tup)

id2dict = id2dict_(myconfig.target_keys2)
dir2url = dir2url_(myconfig.target_prefix2)
