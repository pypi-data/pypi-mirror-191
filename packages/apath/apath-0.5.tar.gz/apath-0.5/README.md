# 🎭 [apath](https://gitlab.univmind.net/bebestcode/apath) for Python [![PyPI version](https://badge.fury.io/py/apath.svg)](https://pypi.python.org/pypi/playwright/)

Advanced path library for python 3.

## Example

```py
from apath import apath

paths = apath(target_path=target_path)
for fullpath, dirs, file in paths.list_dirs():
    print(fullpath, dirs, file)
```
