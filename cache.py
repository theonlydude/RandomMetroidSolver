# the caching decorator for helpers functions

class Cache:
    cache = {}
    masterCache = {}

    @staticmethod
    def reset():
        # reinit the whole cache
        key = 0
        Cache.masterCache = {}
        Cache.cache = {'key': key}
        Cache.masterCache[key] = Cache.cache

    @staticmethod
    def update(newKey):
        if newKey in Cache.masterCache:
#            print("usek: "+format(newKey, '#067b'))
#            if Cache.masterCache[newKey]['key'] != newKey:
#                print("ERROR: key stored in cache is not the same as the new key !!!!")
#                print("      "+format(Cache.masterCache[newKey]['key'], '#067b')+" key in cache")
            Cache.cache = Cache.masterCache[newKey]
        else:
#            print("newk: "+format(newKey, '#067b'))
            Cache.cache = {'key': newKey}
            Cache.masterCache[newKey] = Cache.cache

    @staticmethod
    def decorator(func):
        name = func.__name__
        def _decorator(self):
            ret = Cache.cache.get(name, None)
            if ret is not None:
#                print("cache found for {}: {}".format(name, Cache.cache[func.__name__]))
#                ret = func(self)
#                if ret != Cache.cache[name]:
#                    print("ERROR: cache ({}) != current ({}) for {}".format(Cache.cache[name], ret, name))
                return ret
            else:
                ret = func(self)
                Cache.cache[name] = ret
#                print("cache added for {}: {}".format(name, Cache.cache[name]))
                return ret
        return _decorator

    # for lambdas
    @staticmethod
    def ldeco(name, func):
        def _decorator(self):
            ret = Cache.cache.get(name, None)
            if ret is not None:
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
