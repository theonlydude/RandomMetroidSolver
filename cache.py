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
        def _decorator(self):
            if func.__name__ in Cache.cache:
#                print("cache found for {}: {}".format(func.__name__, Cache.cache[func.__name__]))
#                ret = func(self)
#                if ret != Cache.cache[func.__name__]:
#                    print("ERROR: cache ({}) != current ({}) for {}".format(Cache.cache[func.__name__], ret, func.__name__))
                return Cache.cache[func.__name__]
            else:
                ret = func(self)
                Cache.cache[func.__name__] = ret
#                print("cache added for {}: {}".format(func.__name__, Cache.cache[func.__name__]))
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
