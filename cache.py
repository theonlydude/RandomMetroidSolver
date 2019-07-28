# the caching decorator for helpers functions

class Cache:
    cache0 = {}
    cache1 = {}
    cache2 = {}
    cache3 = {}
    cache4 = {}

    @staticmethod
    def reset():
        Cache.cache0 = {}
        Cache.cache1 = {}
        Cache.cache2 = {}
        Cache.cache3 = {}
        Cache.cache4 = {}

    @staticmethod
    def decorator(func):
        def _decorator(self):
            if func.__name__ in Cache.cache0:
#                print("cache found for {}: {}".format(func.__name__, Cache.cache[func.__name__]))
#                ret = func(self)
#                if ret != Cache.cache[func.__name__]:
#                    print("ERROR: cache ({}) != current ({}) for {}".format(Cache.cache[func.__name__], ret, func.__name__))
                return Cache.cache0[func.__name__]
            else:
                ret = func(self)
                Cache.cache0[func.__name__] = ret
#                print("cache added for {}: {}".format(func.__name__, Cache.cache[func.__name__]))
                return ret
        return _decorator

    @staticmethod
    def decoratorn(cache):
        def _decoratorn(func):
            def __decoratorn(self, *args):
                key = func.__name__ + '.'.join([str(a) for a in args])
                if key in cache:
                    return cache[key]
                else:
                    ret = func(self, *args)
                    cache[key] = ret
                    return ret
            return __decoratorn
        return _decoratorn
