# the caching decorator for helpers functions

class NotFound: pass

class Debug_MasterCache(dict):
    def __contains__(self, newKey):
        has_newKey = dict.__contains__(self, newKey)
        if has_newKey:
            print("usek: "+format(newKey, '#067b'))
            if Cache.masterCache[newKey]['key'] != newKey:
                print("ERROR: key stored in cache is not the same as the new key !!!!")
                print("      "+format(self[newKey]['key'], '#067b')+" key in cache")
        return has_newKey

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

class Cache:
    cache = {}
    masterCache = {}
    funcs = set()
    lambdas = set()
    debug = False

    @staticmethod
    def reset():
        # reinit the whole cache
        key = 0

        if Cache.debug:
            Cache.masterCache = Debug_MasterCache()
            Cache.cache = Debug_Cache()
        else:
            Cache.masterCache = { }
            Cache.cache = { }

        Cache.cache['key'] = key
        Cache.masterCache[key] = Cache.cache

    @staticmethod
    def update(newKey):
        if newKey in Cache.masterCache:
            Cache.cache = Cache.masterCache[newKey]
        else:
            Cache.cache = Debug_Cache() if Cache.debug else { }
            Cache.cache['key'] = newKey
            Cache.masterCache[newKey] = Cache.cache

    @staticmethod
    def decorator(func):
        name = func.__name__
        Cache.funcs.add(name)
        return Cache._decorate(name, func)

    # for lambdas
    @staticmethod
    def ldeco(name, func):
        Cache.lambdas.add(name)
        return Cache._decorate(name, func)

    @staticmethod
    def _decorate(name, func):
        def _decorator(self):
            ret = Cache.cache.get(name, None)
            if ret is not None:
                if Cache.debug and name in Cache.funcs:
                    ret = func(self)
                    Cache.cache.validate(name, ret)
                return ret
            else:
                ret = func(self)
                Cache.cache[name] = ret
                return ret
        return _decorator

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
