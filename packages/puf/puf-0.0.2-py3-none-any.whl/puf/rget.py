# encoding: utf8
from collections.abc import Sequence, Mapping


def rget(obj, *ks):
    for k in ks:
        if isinstance(obj, Mapping):
            obj = obj[k]
        elif isinstance(obj, Sequence):
            k = int(k)
            obj = obj[k]
        else:
            raise AttributeError(k)
    return obj


def rget1(obj, key: str):
    if not key:
        return obj
    keys = key.split(".")
    return rget(obj, *keys)
