# main memory
__MEM = dict()


def set_mem(key, obj):
    __MEM[key] = obj


def get(key, default=None):
    return __MEM.get(key, default)


def delete(key):
    if key in __MEM:
        del __MEM[key]
