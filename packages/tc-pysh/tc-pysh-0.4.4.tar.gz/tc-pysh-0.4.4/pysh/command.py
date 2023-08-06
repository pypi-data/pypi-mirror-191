from .path import Path


class Command:
    def __init__(self, obj):
        self.obj = obj

    def __call__(self, *args, **kwargs):
        return Command(self.obj(*args, **kwargs))

    def __getattr__(self, name):
        if name == "obj":
            return super().__getattribute__("obj")
        return Command(getattr(self.obj, name))

    def __repr__(self):
        if callable(self.obj):
            r = self.obj()
        else:
            r = self.obj

        if isinstance(r, Path):
            txt = str(r)
        elif hasattr(r, "__next__") or hasattr(r, "__iter__"):
            txt = "\n".join(map(str, r))
        else:
            txt = str(r)
        return txt
