# the caching decorator for helpers functions

class NotFound: pass

class Debug_MasterCache(dict):
    def get(self, newKey, default):
        ret = dict.get(self, newKey, NotFound)
        if ret is not NotFound:
            print("usek: "+format(newKey, '#067b'))
            if Cache.masterCache[newKey]['key'] != newKey:
                print("ERROR: key stored in cache is not the same as the new key !!!!")
                print("      "+format(self[newKey]['key'], '#067b')+" key in cache")
            return ret
        else:
            return default

    def __setitem__(self, newKey, value):
        dict.__setitem__(self, newKey, value)
        if newKey != 0:
            print("newk: "+format(newKey, '#067b'))

class Debug_Cache(dict):
    def get(self, name, default):
        ret = dict.get(self, name, NotFound)
        if ret is not NotFound:
            if name in Cache.funcs:
                print("cache found for {}: {}".format(name, self[name]))
            return ret
        else:
            return default

    def __setitem__(self, name, value):
        dict.__setitem__(self, name, value)
        if name != 'key' and name in Cache.funcs:
            print("cache added for {}: {}".format(name, self[name]))

    def validate(self, name, ret):
        if ret != self[name]:
            print("ERROR: cache ({}) != current ({}) for {}".format(self[name], ret, name))

class VersionedCache(object):
    def __init__(self):
        self.cache = {}
        self.masterCache = {}
        self.funcs = set()
        self.lambdas = set()
        self.debug = False

    def reset(self):
        # reinit the whole cache
        key = 0

        if self.debug:
            self.masterCache = Debug_MasterCache()
            self.cache = Debug_Cache()
            self.cache['key'] = key
        else:
            self.masterCache = { }
            self.cache = { }

        self.masterCache[key] = self.cache

    def update(self, newKey):
        cache = self.masterCache.get(newKey, None)
        if cache is None:
            cache = Debug_Cache(key=newKey) if self.debug else { }
            self.cache = cache
            self.masterCache[newKey] = cache
        else:
            self.cache = cache

    def decorator(self, func):
        name = func.__name__
        self.funcs.add(name)
        return self._decorate(name, func)

    # for lambdas
    def ldeco(self, name, func):
        self.lambdas.add(name)
        return self._decorate(name, func)

    def _decorate(self, name, func):
        def _decorator(arg):
            ret = self.cache.get(name, None)
            if ret is not None:
                if self.debug and name in self.funcs:
                    ret = func(arg)
                    self.cache.validate(name, ret)
                return ret
            else:
                ret = func(arg)
                self.cache[name] = ret
                return ret
        return _decorator

Cache = VersionedCache()

class RequestCache(object):
    def __init__(self):
        self.results = {}

    def request(self, request, *args):
        return ''.join([request] + [str(arg) for arg in args])

    def store(self, request, result):
        self.results[request] = result

    def get(self, request):
        return self.results[request] if request in self.results else None

    def reset(self):
        self.results.clear()
