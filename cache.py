# the caching decorator for helpers functions

class NotFound: pass

class Debug_MasterCache(dict):
    def get(self, newKey, default):
        ret = dict.get(self, newKey, NotFound)
        if ret is not NotFound:
            print("usek: "+format(newKey, '#067b'))
            if Cache.masterCache[newKey].key != newKey:
                print("ERROR: key stored in cache is not the same as the new key !!!!")
                print("      "+format(self[newKey].key, '#067b')+" key in cache")
            return ret
        else:
            return default

    def __setitem__(self, newKey, value):
        dict.__setitem__(self, newKey, value)
        if newKey != 0:
            print("newk: "+format(newKey, '#067b'))

class Debug_Cache(list):
    def __init__(self, key, size):
        list.__init__(self, [ None ] * size)
        self.key = key

    def __getitem__(self, slot):
        ret = list.__getitem__(self, slot)
        if ret is not None:
            if slot in Cache.debug_slots:
                name = Cache.debug_slots[slot]
                print("cache found for {}: {}".format(name, ret))
            return ret
        else:
            return None

    def __setitem__(self, slot, value):
        list.__setitem__(self, slot, value)
        if slot in Cache.debug_slots:
            name = Cache.debug_slots[slot]
            print("cache added for {}: {}".format(name, value))

    def validate(self, name, slot, ret):
        value_in_cache = list.__getitem__(self, slot)
        if ret != value_in_cache:
            print("ERROR: cache ({}) != current ({}) for {}".format(value_in_cache, ret, name))

class VersionedCache(object):
    __slots__ = ( 'cache', 'masterCache', 'debug', 'key', 'next_slot',
    'debug_slots', 'size' )

    def __init__(self):
        self.cache = []
        self.masterCache = {}
        self.debug = False
        self.key = None
        self.next_slot = 0
        self.debug_slots = { }
        self.size = 0

    def reset(self):
        # reinit the whole cache
        self.masterCache = Debug_MasterCache() if self.debug else { }
        self.update(0)

    def update(self, newKey):
        if self.key == newKey and not self.debug:
            return
        cache = self.masterCache.get(newKey, None)
        if cache is None:
            cache = Debug_Cache(newKey, self.size) if self.debug else [ None ] * self.size
            self.masterCache[newKey] = cache
            self.cache = cache
            self.key = newKey
        else:
            self.cache = cache
            self.key = newKey

    def decorator(self, func):
        name = func.__name__
        slot = self._new_slot(name)
        self.debug_slots[slot] = name
        return self._decorate(name, slot, func)

    # for lambdas
    def ldeco(self, name, func):
        slot = self._new_slot(name)
        return self._decorate(name, slot, func)

    def _new_slot(self, name):
        slot = self.next_slot
        self.next_slot += 1
        self.size += 1
        return slot

    def _decorate(self, name, slot, func):
        def _decorator(arg):
            ret = self.cache[slot]
            if ret is not None:
                # TODO: Commented-out, because this function can get
                # called 500K times or more during a run, and so this
                # conditional measurably affects performance.
                # if self.debug and slot in self.debug_slots:
                #     ret = func(arg)
                #     self.cache.validate(name, slot, ret)
                return ret
            else:
                ret = func(arg)
                self.cache[slot] = ret
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
