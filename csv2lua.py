from pathlib import Path
import pandas as pd
import numpy as np


def print_pets(_lang="en_en", _lua=True):
    _P = Path(f"./tables/{_lang}/pet_text_{_lang}.csv")
    _T = pd.read_csv(_P)

    for _r in range(len(_T)):
        if _lua:
            _r_new = f"[\"{_T.iloc[_r][1]}\"] = {_T.iloc[_r].id},"
            print(_r_new)
        else:
            print(_T.iloc[_r][1])


def print_10_girls(_lang="en_en", _lua=True):
    _P = Path("./tables/zh_tw/partner_exskill_text_zh_tw.csv")
    _T = pd.read_csv(_P)
    _10_girls = set()
    for _r in range(len(_T)):
        _10_girls.add(_T.iloc[_r][1])

    _dict = {}
    _dict_zh = all_girls(_lang="zh_tw")
    for _k in _dict_zh:
        if _k in _10_girls:
            _dict[_k] = _dict_zh[_k]

    _P = Path(f"./tables/{_lang}/partner_text_{_lang}.csv")
    _T = pd.read_csv(_P)
    for _k in _dict:
        if _lua:
            _r_new = f"[\"{_T[_T.id == _dict[_k]].iloc[0][1]}\"] = {_dict[_k]},"
            print(_r_new)
        else:
            print(_k)


def all_girls(_lang="zh_tw"):
    _P = Path(f"./tables/{_lang}/partner_text_{_lang}.csv")
    _T = pd.read_csv(_P)
    _dict = {}
    for _r in range(len(_T)):
        if _T.iloc[_r][1] in _dict:
            _dict[_T.iloc[_r][1]].append(_T.iloc[_r].id)
        else:
            _dict[_T.iloc[_r][1]] = [_T.iloc[_r].id]
    for _k in _dict:
        _dict[_k] = np.max(_dict[_k])
    return _dict


def print_equips(_lang="zh_tw", _slot=6, _lua=True):
    _P = Path(f"./tables/{_lang}/equip_text_{_lang}.csv")
    _T = pd.read_csv(_P)
    _dict = {}
    for _r in range(len(_T)):
        if _T.iloc[_r][1] in _dict:
            _dict[_T.iloc[_r][1]].append(_T.iloc[_r].id)
        else:
            _dict[_T.iloc[_r][1]] = [_T.iloc[_r].id]
    for _k in _dict:
        _dict[_k] = np.max(_dict[_k])
    _list = list(_dict.items())
    _list = sorted(_list, key=lambda x: x[1])
    for _k, _v in _list:
        if _v // 1000 == _slot:
            if _lua:
                _r_new = f"[\"{_k}\"] = {_v},"
                print(_r_new)
            else:
                print(_k)


def buff2desc(*_buffs, _lang="zh_tw"):
    _P = Path(f"./tables/{_lang}/buff_text_{_lang}.csv")
    _T = pd.read_csv(_P)
    _descs = []
    for _b in _buffs:
        if isinstance(_b, str):
            _name = _b[:_b.index("#")]
            _descs.append(_T[_T["name"] == _name].iloc[0].desc)
    return '/'.join(_descs)


def print_cores(_lang="en_en", _lua=True):
    _P = Path("./tables/equip.csv")
    _T = pd.read_csv(_P)
    _T = _T[_T.id // 100 == 57]
    _T = _T[_T.star == 3]
    _dict = {}
    # print(len(_T))
    for _r in range(len(_T)):
        _R = _T.iloc[_r]
        _stats = buff2desc(_R.base1, _R.base2, _R.base3, _lang=_lang)
        _dict[_stats] = _R.id
    _list = list(_dict.items())
    _list = sorted(_list, key=lambda x: x[1])
    for _k, _v in _list:
        if _lua:
            _r_new = f"[\"{_k}\"] = {_v},"
            print(_r_new)
        else:
            print(_k)


if __name__ == "__main__":
    print_pets(_lang="zh_tw", _lua=False)
