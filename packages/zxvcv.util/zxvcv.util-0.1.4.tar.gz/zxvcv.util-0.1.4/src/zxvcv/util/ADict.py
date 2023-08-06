

class ADict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self, dct:dict={}):
        for key, value in dct.items():
            if hasattr(value, 'keys'):
                value = ADict(value)
            self[key] = value
