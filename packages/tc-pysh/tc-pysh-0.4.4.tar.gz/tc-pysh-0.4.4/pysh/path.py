import os
import os.path
from typing import Union, Optional, Iterator, TypeVar


SPath = Union["AbsolutePath", str]  # String or AbsPath


class Path(os.PathLike):
    "Base class for a PathLike object used throughout the package."
    def __init__(self, *components: str):
        self.components = [c for c in components if c]

    @property
    def base(self) -> "str":
        """Base name as a string

        :example:
        >>> AbsolutePath.from_str("/a/b/c").base
        "c"
        """
        if self.components:
            return self.components[-1]
        else:
            return ""

    @property
    def dir(self) -> "Path":
        """Directory name as a path

        :example:
        >>> AbsolutePath.from_str("/a/b/c").dir
        AbsolutePath.from_str("/a/b")
        """
        if self.components:
            return self.__class__(*self.components[:-1])
        else:
            return self.__class__.empty()

    def to_str(self) -> str:
        """Represent the path object as a unix path.
        :example:
        >>> AbsolutePath.from_str("/a/b/c")
        "/a/b/c"
        """
        return "/".join(self.components)

    def __str__(self) -> str:
        return self.to_str()

    def __fspath__(self) -> str:
        return self.to_str()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}.from_str({self.to_str()!r})"

    def __contains__(self, name: str) -> bool:
        return name in self.components

    def __iter__(self) -> Iterator[str]:
        yield from self.components

    @classmethod
    def empty(cls) -> "Path":
        return cls()

    def __gt__(self, other: "Path") -> bool:
        return self.to_str() > other.to_str()

    def __lt__(self, other: "Path") -> bool:
        return self.to_str() < other.to_str()

    def __ge__(self, other: "Path") -> bool:
        return self.to_str() > other.to_str()

    def __le__(self, other: "Path") -> bool:
        return self.to_str() < other.to_str()


class AbsolutePath(Path):
    "Absolute PathLike"

    def to_str(self) -> str:
        return "/" + super().to_str()

    def relative_to(self, other: Optional["AbsolutePath"]) -> "RelativePath":
        """Return a path pointing to the same place as self, but relative to a reference.

        :param other: (optional, AbsolutePath.from_str("/")) reference path
        """
        ref = other or cwd()
        components = ref.components.copy()

        common = 0
        for i, (a, b) in enumerate(zip(self.components, ref.components)):
            if a == b:
                common += 1
            else:
                break

        components = [".."] * (len(components) - common) + self.components[common:]
        return RelativePath(*components)

    def exists(self) -> bool:
        """Return True if this path point to an existing directory or file."""
        return os.path.exists(self.to_str())

    def isfile(self) -> bool:
        """Return True if this path point to an existing file."""
        return os.path.isfile(self.to_str())

    def isdir(self) -> bool:
        """Return True if this path point to an existing directory."""
        return os.path.isdir(self.to_str())

    @classmethod
    def empty(cls):
        return cls("")

    @classmethod
    def from_str(cls, path: str) -> "AbsolutePath":
        assert path.startswith("/")
        components = [
            os.path.expanduser(comp)
            for comp in path.split("/")
            if comp != "." and comp != ""
        ]
        return AbsolutePath(*components)

    def add(self, path: Union["RelativePath", str]) -> "AbsolutePath":
        """Return a new AbsolutePath with components appended to this path."""
        if isinstance(path, RelativePath):
            return path.at(self)
        else:
            return RelativePath.from_str(path).at(self)

    @classmethod
    def from_rel(cls, path: Union["RelativePath", str]):
        """Return a new AbsolutePath made from a relative path.

        :param path: a path reltive to current working directory
        """
        if isinstance(path, RelativePath):
            return path.at(cwd())
        else:
            return RelativePath.from_str(path).at(cwd())


class RelativePath(Path):
    "Relative PathLike"
    T = TypeVar("T", AbsolutePath, "RelativePath")

    def at(self, other: T) -> T:
        """Combine this with another path."""
        return other.__class__(*other.components, *self.components)

    @classmethod
    def from_str(cls, path: str) -> "RelativePath":
        assert not path.startswith("/")
        components = [
            os.path.expanduser(comp) for comp in path.split("/") if comp != "."
        ]
        return RelativePath(*components)

    def add(self, path: Union["RelativePath", str]) -> "RelativePath":
        """Return a new RelativePath with components appended to this path."""
        if isinstance(path, RelativePath):
            return path.at(self)
        else:
            return RelativePath.from_str(path).at(self)


def ensure_path(path: Union[Path, str]) -> Path:
    """Make a path from the parameter.

    :param path: a str or a Path. If path is a str, return a path made from it.
    If path is a Path, return it as is.
    """
    if isinstance(path, Path):
        return path
    if path.startswith("/"):
        return AbsolutePath.from_str(path)
    else:
        return RelativePath.from_str(path)


def ensure_abs_path(path: SPath) -> AbsolutePath:
    """Make an AbsolutePath from the parameter.

    :param path: a str or a Path. If path is a str, return a path made from it.
    If path is a Path, return it as is.
    If path is relative, instanciate it from current working directory.
    """
    p = ensure_path(path)
    if isinstance(p, AbsolutePath):
        return p
    elif isinstance(p, RelativePath):
        return p.at(cwd())
    else:
        raise NotImplementedError()


def cwd() -> AbsolutePath:
    """Return an AbsolutePath to the current working directory."""
    return AbsolutePath.from_str(os.getcwd())
