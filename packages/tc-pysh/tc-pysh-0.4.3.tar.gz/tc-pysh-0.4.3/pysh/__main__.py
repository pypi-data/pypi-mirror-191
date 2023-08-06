import sys

from typing import Union, Callable

from . import *
from .path import *
from .file import *
from . import ls as _ls
from . import find as _find
from . import cd as _cd
from .path import cwd as _cwd
from .command import Command
from .interpreter import Interpreter

ls = Command(_ls)
find = Command(_find)
cd = Command(_cd)
cwd = Command(_cwd)


def main():
    interp.interact()


def set_ps1(prompt: Union[str, Callable]):
    if callable(prompt):
        class P:
            def __str__(self):
                return prompt()
        sys.ps1 = P()
    else:
        sys.ps1 = prompt


interp = Interpreter(local=locals())


if __name__ == "__main__":
    main()
