import os
import re
import json
import csv
from pathlib import Path

import luadata

MAIN_DIR = Path("../src_Jul_09/data/tables/")
LUA_FILES = list(MAIN_DIR.glob('**/*.lua'))

DIST = Path("./tables/")
if not DIST.exists():
    os.mkdir(DIST)


def save2csv(_file_path, _dict):
    _nk = len(_dict["keys"])
    _rk = {_i: _k for _k, _i in _dict["keys"].items()}
    _nk_real = max(_rk.keys())
    assert _nk_real == len(next(iter(_dict["rows"].items()))[1])
    for _i in range(1, _nk_real + 1):
        if _i not in _rk:
            _rk[_i] = f"unknown_{_i}"
            print(f"KeyError: {_file_path}")
            print(f"Add column {_i}: {_rk[_i]}")

    _keys = [_rk[_i + 1] for _i in range(_nk)]
    with open(_file_path, 'w') as _file:
        _writer = csv.writer(_file)
        _writer.writerow(_keys)
        for _id in _dict["rows"]:
            _writer.writerow(_dict["rows"][_id])


def save2json(_file_path, _dict):
    with open(_file_path, 'w') as _file:
        _file.seek(0)
        json.dump(_dict, _file, indent=4, ensure_ascii=False)
        _file.truncate()


def lua_convert(_file_path, _out=".csv"):
    _out = _out.lower()
    assert _out in [".csv", ".json"]

    if _out == ".csv":
        _converter = save2csv
    elif _out == ".json":
        _converter = save2json

    _index = _file_path.parts.index('tables')
    _dist = Path('.').joinpath(*_file_path.parts[_index:]).with_suffix(_out)
    if not _dist.exists():
        _dist.mkdir(parents=True, exist_ok=True)
    if _dist.is_dir():
        _dist.rmdir()

    with open(_file_path, 'r') as _file:
        _data = _file.read().replace('return table', '')
        if " = import(" in _data:
            print(f"Ignore: {_file_path}")
            return

        _to_sub = re.findall(r'(?s)\[\[(.*?)\]\]', _data)
        for _s in _to_sub:
            _new_s = _s.replace("'", r"\'").replace('"', r'\"')
            _data = _data.replace(_s, _new_s)
        _data = _data.replace('[[[', '"[').replace(']]]', ']"')
        _data = _data.replace('[[', '"').replace(']]', '"')

        _dict = luadata.unserialize(_data, encoding="utf-8", multival=False)
        if "keys" in _dict and "rows" in _dict:
            _converter(_dist, _dict)


for _lua_file in LUA_FILES:
    print(_lua_file)
    lua_convert(_lua_file)
