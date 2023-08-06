# encoding: utf8
import logging
import re


log = logging.getLogger(__name__)


class Field:
    def __init__(self, name=""):
        self.name = name

    def __set_name__(self, owner, name):
        if not self.name:
            self.name = name

    def __repr__(self):
        return self.name

class IntField(Field): pass

class CharField(Field): pass

class DateField(Field): pass

class DateTimeField(Field): pass


ucw: re.Pattern = re.compile(r"[A-Z]+[a-z0-9_]*")

def class_to_table(name: str) -> str:
    buf = []
    pos = 0
    while True:
        m = ucw.search(name, pos)
        if not m:
            break

        if pos == 0 and m.start() > 0:
            buf.append(name[:m.start()])

        s = name[m.start(): m.end()].lower()
        buf.append(s)
        pos = m.end()

    return "_".join(buf)


class Options:
    def __init__(self, table: str, fields: dict):
        self.table = table
        self.fields = fields

    def db(self):
        raise NotImplemented

    def __repr__(self):
        return "<table %s, (%s)>" % (
            self.table,
            ", ".join(map(str, self.fields.values()))
        )


class NotFound(RuntimeError): pass


class QuerySet:
    def __init__(self):
        pass

    def __len__(self):
        pass

    def __iter__(self):
        return self

    def __next__(self):
        pass

    def __getitem__(self, idx):
        pass


class Manager:
    # https://docs.djangoproject.com/en/4.1/topics/db/queries/
    def __init__(self, model, opts):
        self.model = model
        self.opts = opts

    def all(self):
        raise NotImplemented

    def range_by_pk(self, offset=0, bufsize=100):
        while True:
            buf = self.filter(pk__gt=offset)[:bufsize]
            if len(buf) == 0:
                break

            for i in buf:
                yield i

            if len(buf) < bufsize:
                break

            offset = buf[-1].pk

    def raw(self):
        # https://docs.djangoproject.com/en/4.1/topics/db/sql/
        raise NotImplemented

    def create(self, **kwargs):
        raise NotImplemented

    def delete(self, pk=None, **kwargs):
        raise NotImplemented

    def filter(self, **kwargs):
        raise NotImplemented

    def exclude(self, **kwargs):
        raise NotImplemented

    def get(self, pk=None, **kwargs):
        sql = "SELECT %s FROM %s WHERE %s LIMIT 1"
        return sql


class Meta(type):
    def __new__(metacls, name, bases, ns, **kwargs):
        fields = {k: v for k, v in ns.items() if isinstance(v, Field)}
        if not (ns["__module__"] == "puf.model" and name == "Model"):
            table = kwargs.get("table", None)
            if not table:
                table = class_to_table(name)

            opts = Options(table, fields)
            ns["_opts"] = opts
            # ns["__init__"] = make_init(fields)

        return super().__new__(metacls, name, bases, ns)

    def __init__(cls, name, bases, ns, **kwargs):
        log.debug("new model cls: %s, %s, %s, %s", name, bases, ns, kwargs)
        if hasattr(cls, "_opts"):
            cls.objects = Manager(cls, cls._opts)


class Model(metaclass=Meta):
    def save(self):
        raise NotImplemented

    def delete(self):
        raise NotImplemented
