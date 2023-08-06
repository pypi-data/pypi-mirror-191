import os
import collections
from itertools import islice
import re


def human(size, use_si=False):
    "Convert number of bytes into human readable size."
    s = size
    u = ""
    d = 10**3 if use_si else 2**10
    for unit in ("K", "M", "G", "T", "E", "P"):
        if s < d:
            break
        s /= d
        u = unit

    return s, u


def size(path):
    "Return the size of path in bytes."
    return os.stat(path).st_size


def head(path, n=10):
    "Iterate over the n first lines of path."
    with open(path) as f:
        return islice(f, n)


def tail(path, n=10):
    "Iterate over the n last lines of path."
    with open(path) as f:
        return _it_tail(n, f)


def skip(path, n=10):
    "Iterate over the lines of path after the nth."
    with open(path) as f:
        for _ in zip(range(n), f):
            pass
        return f


def before(path, n=10):
    "Iterate over the lines of path but stop before the last n."
    with open(path) as f:
        return _it_before(f)


def last(path):
    with open(path) as f:
        for l in f:
            last = l
    return last


def grep(path, pattern):
    "Iterate over the lines from path that match pattern."
    r = re.compile(pattern)
    with open(path) as f:
        for line in f:
            if r.match(line):
                yield line


def _it_tail(n, iterable):
    "Return an iterator over the last n items"
    return iter(collections.deque(iterable, maxlen=n))


def _it_before(n, iterable):
    "Return an iterator over the last n items"
    d = collections.deque(maxlen=n)
    for line in iterable:
        if len(d) == n:
            yield d.pop()

        d.appendleft(line)
