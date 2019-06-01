
def mpath(m, path_parts = [], default = None):
    '''mpath takes a dictionary, a path specified as an array of keys into the dict and returns a value or the default'''
    for part in path_parts:
        if m != None and part in m:
            m = m[part]
        else:
            return default
    return m
