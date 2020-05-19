# the caching decorator for helpers functions

class Cache:
    cache = {}

    @staticmethod
    def reset():
        Cache.cache = {}

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

    def store(self, result, request, *args):
        h = self.getHashString(request, args)
        self.results[h] = result

    def get(self, request, *args):
        h = self.getHashString(request, args)
        return self.results[h] if h in self.results else None

    def reset(self):
        self.results = {}

    def getHashString(self, request, args):
        return ''.join([request] + [str(arg) for arg in args])
