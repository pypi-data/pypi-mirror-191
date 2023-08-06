import re

from typing import Union, Optional, Iterable, Callable

from .path import AbsolutePath, RelativePath, Path, ensure_abs_path


PathPred = Callable[[AbsolutePath], bool]


class Query:
    def __init__(self, source: Iterable[Path], filter: Optional[PathPred] = None):
        self.source = source
        self._filter = filter

    def __iter__(self):
        for p in self.source:
            if isinstance(p, RelativePath):
                _p = AbsolutePath.from_rel(p)
            else:
                _p = p
            if self._filter is None or self._filter(_p):
                yield p

    def isfile(self):
        """Filter paths to keep only the files."""

        def isfile(p):
            return p.isfile()

        return Query(self, isfile)

    def isdir(self):
        """Filter the elements of the query to keep only the directories."""

        def isdir(p):
            return p.isdir()

        return Query(self, isdir)

    def name(self, pattern: Union[str, re.Pattern]):
        """Filter the elements of the query to keep only the ones matching `pattern`.

        :param pattern: a `str` or a `re.Pattern`, used as a regex to match the paths
        """
        if isinstance(pattern, re.Pattern):
            regex: re.Pattern = pattern
        else:
            regex = re.compile(pattern)

        def match(path: AbsolutePath):
            return bool(regex.fullmatch(path.base))

        return Query(self, match)

    def first(self):
        """Return the first element of the query."""
        return next(iter(self), None)

    def last(self):
        """Return the last element of the query."""
        it = None

        for it in self:
            pass

        return it

    def filter(self, pred: PathPred):
        """Create an arbitrary query filter from a predicate.

        :param pred: keep only the elements for which `pred(elem)` is true.
        """
        return Query(self, pred)

    def sort(self, key=None):
        """Sort the elements of the query.

        :param key: (optional) see :py:func:`sorted`
        """
        return Query(sorted(self, key=key))
