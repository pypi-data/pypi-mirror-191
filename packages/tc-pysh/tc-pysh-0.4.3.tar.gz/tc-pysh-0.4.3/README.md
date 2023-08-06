# Pysh

## About

Pysh aims at providing the tools required to write in Python the script I would have written in bash before.

Python provide a more robust, and more powerful environment for scripting and makes the script easier to maintain and extend.
Pysh makes it possible to write file manipulation script just as quickly as in bash.

It should be good both for quick one-of scripts, as well as more complex reusable small programs.

## Installation

Be careful: the `pysh` name was already taken on PyPI, it is a different package, that I have nothing to do with.
My package is named `tc-pysh`

```sh
pip install tc-pysh
```

## Usage

At the center of pysh is the path facilities: `pysh.AbsolutePath` and `pysh.RelativePath` are objects representing locations in the file system taht are easy to manipulate and use with pysh utils, as well as with most of python standard library thanks to `os.PathLike`.

`pysh.utils` provides equivalents of the commonly used commands in bash scripts such as `mv`, `cp`, `rm`, `cat`, etc.

`pysh.ls` and `pysh.find` provides familiar interface to the `pysh.query` facilities, making it easy to browse a directory or arborescence, with tools likes sorting and filtering in the form of iterators, building on top of the standard library and the `re` standard module.

`pysh.file` provides a set of functions that are related to file *content*, like `grep`, `head` and `tail`.

Here is an example of using `ls` to print the sizes of all text files of a directory.
```python
from pysh import ls
from pysh.file import size, human

for f in ls().name(r".*\.txt").sort():
    s = size(f) 
    s, u = human(s)

    print(str(f), s, u)
```
