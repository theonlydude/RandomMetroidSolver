# the caching decorator for helpers functions

class Cache:
    cache = {}

    @staticmethod
    def reset():
        Cache.cache = {}

    @staticmethod
    def decorator(func):
        def _decorator(self, *args, **kwargs):
            if func.__name__ in Cache.cache:
#                print("cache found for {}: {}".format(func.__name__, Cache.cache[func.__name__]))
#                ret = func(self, *args, **kwargs)
#                if ret != Cache.cache[func.__name__]:
#                    print("ERROR: cache ({}) != current ({}) for {}".format(Cache.cache[func.__name__], ret, func.__name__))
                return Cache.cache[func.__name__]
            else:
                ret = func(self, *args, **kwargs)
                Cache.cache[func.__name__] = ret
#                print("cache added for {}: {}".format(func.__name__, Cache.cache[func.__name__]))
                return ret
        return _decorator
