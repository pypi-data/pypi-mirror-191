import os
import sys


class _Apaths:
    _init = False
    _origin = ''
    _py_ver = sys.version_info

    def __init__(self, target_path):
        if not os.path.isdir(target_path):
            raise FileNotFoundError(f'{target_path} is not exists.')
        self._init = True
        self._origin = target_path

    def __len__(self):
        return len(self._list_dirs(self._origin)) if self._init else -1

    def list_dirs(self) -> list:
        return self._list_dirs(self._origin) if self._init else []

    def _list_dirs(self, _target, _include_files=None) -> list:
        if _include_files is None:
            _include_files = []

        for _paths in os.listdir(_target):
            _fullpath = os.path.join(_target, _paths)
            if os.path.isdir(_fullpath):
                self._list_dirs(_fullpath, _include_files)
            else:
                if self._py_ver[0] >= 3 and self._py_ver[1] >= 9:
                    _dir = _fullpath.removeprefix(self._origin).removesuffix(_paths).removeprefix(os.sep).removesuffix(os.sep)
                else:
                    _dir = self._remove_preffix(_fullpath, self._origin)
                    _dir = self._remove_suffix(_dir, _paths)
                    _dir = self._remove_preffix(_dir, os.sep)
                    _dir = self._remove_suffix(_dir, os.sep)
                _include_files.append((_fullpath, _dir, _paths))
        return _include_files

    def _remove_suffix(self, input_string, suffix):
        if suffix and input_string.endswith(suffix):
            return input_string[:-len(suffix)]
        return input_string

    def _remove_preffix(self, input_string, prefix):
        if prefix and input_string.startswith(prefix):
            return input_string[len(prefix):]
        return input_string


def apath(target_path: str) -> _Apaths:
    return _Apaths(target_path)
