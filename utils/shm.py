import json

class SHM(object):
    msgHeader = 3
    bufSize = 800*1024

    def __init__(self, shmName=None):
        # temporary bugfix while not fixed in python
        from multiprocessing import shared_memory
        remove_shm_from_resource_tracker()
        if shmName is None:
            self.shm = shared_memory.SharedMemory(create=True, size=SHM.bufSize)
        else:
            self.shm = shared_memory.SharedMemory(shmName)

    def writeMsgJson(self, msgJson):
        # write msg size, then message
        msgBytes = json.dumps(msgJson).encode('utf-8')
        msgSize = len(msgBytes)
        assert msgSize + SHM.msgHeader <= self.shm.size, "Msg is bigger than shm {}/{}".format(msgSize, self.shm.size)
        self.shm.buf[0:SHM.msgHeader] = msgSize.to_bytes(SHM.msgHeader, byteorder='little')
        self.shm.buf[SHM.msgHeader:SHM.msgHeader+msgSize] = msgBytes

    def readMsgJson(self):
        msgSize = int.from_bytes(self.shm.buf[0:SHM.msgHeader], byteorder='little')
        msgBytes = self.shm.buf[SHM.msgHeader:SHM.msgHeader+msgSize]
        return json.loads(msgBytes.tobytes())

    def name(self):
        return self.shm.name

    def finish(self, father):
        self.shm.close()
        if father:
            self.shm.unlink()


def remove_shm_from_resource_tracker():
    """Monkey-patch multiprocessing.resource_tracker so SharedMemory won't be tracked
    More details at: https://bugs.python.org/issue38119
    """
    from multiprocessing import resource_tracker

    def fix_register(name, rtype):
        if rtype == "shared_memory":
            return
        return resource_tracker._resource_tracker.register(self, name, rtype)
    resource_tracker.register = fix_register

    def fix_unregister(name, rtype):
        if rtype == "shared_memory":
            return
        return resource_tracker._resource_tracker.unregister(self, name, rtype)
    resource_tracker.unregister = fix_unregister

    if "shared_memory" in resource_tracker._CLEANUP_FUNCS:
        del resource_tracker._CLEANUP_FUNCS["shared_memory"]
