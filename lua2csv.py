import re
import json
import csv
from pathlib import Path

import luadata
import pandas as pd

MAIN_DIR = Path("../src/data/tables/")
TO_COMBINE = [
    "dropbox",
    "item",
    "main_plot",
    "monster",
    "partner_plot",
    "partner_warmup_plot",
    "skill",
    "sound",
]


def save2csv(_file_path, _dict):
    _rk = {_i: _k for _k, _i in _dict["keys"].items()}
    _nk_real = max(_rk.keys())
    assert _nk_real == len(next(iter(_dict["rows"].items()))[1])
    for _i in range(1, _nk_real + 1):
        if _i not in _rk:
            _rk[_i] = f"unknown_{_i}"
            print(f"[KEYERROR] {_file_path}")
            print(f"[ADDED COLUMN {_i}] {_rk[_i]}")

    _keys = [_rk[_i + 1] for _i in range(_nk_real)]
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
        _data = _file.read()
        if " = import(" in _data:
            print(f"[IGNORED] {_file_path}")
            return

        _data = _data.replace('return table', '')
        _to_sub = re.findall(r'(?s)\[\[(.*?)\]\]', _data)
        for _s in _to_sub:
            _new_s = _s.replace("'", r"\'").replace('"', r'\"')
            _data = _data.replace(_s, _new_s)
        _data = _data.replace('[[[', '"[').replace(']]]', ']"')
        _data = _data.replace('[[', '"').replace(']]', '"')

        _dict = luadata.unserialize(_data, encoding="utf-8", multival=False)
        if "keys" in _dict and "rows" in _dict and len(
                _dict["keys"]) > 0 and len(_dict["rows"]) > 0:
            _converter(_dist, _dict)
            print(f"[CONVERTED] {_file_path}")
        else:
            print(f"[IGNORED] {_file_path}")


if __name__ == "__main__":
    TABLES = Path("./tables/")
    TABLES.mkdir(parents=True, exist_ok=True)
    COMBINED_TABLES = Path("./combined_tables/")
    COMBINED_TABLES.mkdir(parents=True, exist_ok=True)

    LUA_FILES = sorted(MAIN_DIR.glob('**/*.lua'))
    for _lua_file in LUA_FILES:
        lua_convert(_lua_file)

    for _t in TO_COMBINE:
        CSV_FILES = sorted(TABLES.glob(f'./{_t}?.csv'))
        print("[TO COMBINE]", *CSV_FILES)

        COMBINED_CSV = pd.concat([pd.read_csv(_) for _ in CSV_FILES])
        COMBINED_CSV.sort_values("id", inplace=True)
        COMBINED_CSV.set_index("id", inplace=True)
        COMBINED_CSV.to_csv(COMBINED_TABLES / f"{_t}.csv")

        print("[COMBINED]", COMBINED_TABLES / f"{_t}.csv")
