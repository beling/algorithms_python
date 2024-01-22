#!/usr/bin/env python3
# Piotr Beling, 2023

class ListBasedDict:
    """Dictionary that stores a list of key-value pairs and mimics the interface of the built-in dict type."""
        
    def __init__(self, iterable = ()):
        """Constructs a dictionary containing key/value pairs from the given iterable."""
        self.data = list(iterable)
    
    def _index_of(self, key):
        """Returns the index of the element with the given key in data."""
        for i, (k, _) in enumerate(self.data):
            if k == key:
                return i
        raise KeyError(key)
    
    def __len__(self):
        return len(self.data)
    
    def __str__(self):
        #return str(self.data)
        return '{{{}}}'.format(', '.join(f'{k}: {v}' for k,v in self.data))
    
    def __getitem__(self, key):
        return self.data[self._index_of(key)][1]
    
    def __setitem__(self, key, value):
        try:
            self.data[self._index_of(key)] = (key, value)
        except KeyError:
            self.data.append((key, value))
            
    def __delitem__(self, key):
        del self.data[self._index_of(key)]
        
    def __iter__(self):
        for k, _ in self.data: yield k
        
    def items(self):
        #for e in self.data: yield e
        return self.data
    
    def values(self):
        for _, v in self.data: yield v
    
    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default
    
    def __contains__(self, key):
        try:
            self._index_of(key)
        except KeyError:
            return False
        else:
            return True
        
    def clear(self):
        self.data.clear()
        
    def copy(self):
        return ListBasedDict(self.data)
    
    @classmethod
    def fromkeys(cls, iterable, value=None):
        result = cls()
        for k in iterable: result[k] = value
        return result
        
if __name__ == "__main__":	# demo program:
    d = ListBasedDict()
    d[1] = "aa"
    d["ab"] = "bb"
    d["aza"] = "zzz"
    assert 1 in d
    assert d["ab"] == "bb"
    assert 2 not in d
    assert len(d) == 3
    del d[1]
    assert 1 not in d
    assert len(d) == 2
