import json


__all__ = ["encode", "decode", "load_file", "load_jsonl_file"]


def encode(obj):
    return json.dumps(obj)


def decode(obj):
    return json.loads(obj)


def load_file(filename):
    with open(filename) as fin:
        body = fin.read()
        return decode(body)


def load_jsonl_file(filename):
    with open(filename) as fin:
        res = []
        for line in fin:
            res.append(decode(line.strip()))
        return res
