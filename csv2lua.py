import json

from pathlib import Path
import pandas as pd
import numpy as np


class NpEncoder(json.JSONEncoder):
    # pylint: disable=W0221
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


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
    _P = Path("./tables/partner.csv")
    _T = pd.read_csv(_P)
    _10_girls = set()
    for _r in range(len(_T)):
        if _T.iloc[_r][8] == 250:
            _10_girls.add(_T.iloc[_r][0])

    _dict = {}
    _dict_all = all_girls(_lang=_lang)
    for _k in _dict_all:
        if _k in _10_girls:
            _dict[_dict_all[_k]] = _k

    if _lua:
        for _k in _dict:
            _r_new = f"[\"{_k}\"] = {_dict[_k]},"
            print(_r_new)
    else:
        _list = list(_dict.keys())
        for _i in range(len(_list)):
            print(_list[-_i - 1])
    print(len(_dict))


def all_girls(_lang="zh_tw"):
    _P = Path(f"./tables/{_lang}/partner_text_{_lang}.csv")
    _T = pd.read_csv(_P)
    _dict = {}
    for _r in range(len(_T)):
        _k = _T.iloc[_r][1].replace(u'\xa0', ' ')
        if _k in _dict:
            _dict[_k].append(_T.iloc[_r].id)
        else:
            _dict[_k] = [_T.iloc[_r].id]

    _dict_new = {}
    for _k in _dict:
        for _v in _dict[_k]:
            if _v // 10000 == 75:
                _dict_new[_v] = _k

    _out = Path(f"./misc/tables/girls_{_lang}.json")
    with open(_out, 'w') as _f:
        json.dump(_dict, _f, indent=4, ensure_ascii=False, cls=NpEncoder)

    return _dict_new


def print_equips(_lang="zh_tw", _slot=6, _lua=True):
    _P = Path(f"./tables/{_lang}/equip_text_{_lang}.csv")
    _T = pd.read_csv(_P)
    _dict = {}
    for _r in range(len(_T)):
        if _T.iloc[_r][1] in _dict:
            _dict[_T.iloc[_r][1]].append(_T.iloc[_r].id)
        else:
            _dict[_T.iloc[_r][1]] = [_T.iloc[_r].id]
    # for _k in _dict:
    #     _dict[_k] = np.max(_dict[_k])
    _list = list(_dict.items())
    _list = sorted(_list, key=lambda x: x[1])
    _equips = {}
    for _k, _v in _list:
        for __v in _v:
            if _slot == __v // 10000:
                _equips[f"{_k} P{str(__v)[-1]}"] = __v
            if _slot == __v // 1000:
                _equips[f"{_k}"] = __v

    if _lua:
        for _k in _equips:
            print(f"[\"{_k}\"] = {_equips[_k]},")
    else:
        _list = list(_equips.keys())
        for _i in range(len(_list)):
            print(_list[-_i - 1])
    print(len(_equips))

    _out = Path("./misc/tables/antiques.json")
    with open(_out, 'w') as _f:
        json.dump(_equips, _f, indent=4, ensure_ascii=False, cls=NpEncoder)


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

    _out = Path("./misc/tables/crystals.json")
    with open(_out, 'w') as _f:
        json.dump(_dict, _f, indent=4, ensure_ascii=False, cls=NpEncoder)


def print_lab(_lua=True):
    _P = Path("./tables/guild_skill.csv")
    _T = pd.read_csv(_P)
    for _r in range(len(_T)):
        _R = _T.iloc[_r]
        if _lua:
            _r_new = "{" + f"skill_id={_R.id},skill_lv={_R.lv_max}" + "},"
            print(_r_new)
        else:
            print(_R.id)


def trans_cores():
    _cn = Path("./misc/tables/crystals.json")
    _en = Path("./misc/tables/crystals_en.json")
    with open(_cn, 'r') as _f:
        _dict_cn = {_v: _k for _k, _v in json.load(_f).items()}
    with open(_en, 'r') as _f:
        _dict_en = {_v: _k for _k, _v in json.load(_f).items()}

    _dict_trans = {_dict_cn[_k]: _dict_en[_k] for _k in _dict_cn}
    _out = Path("./misc/tables/crystals_trans.json")
    with open(_out, 'w') as _f:
        json.dump(_dict_trans, _f, indent=4, ensure_ascii=False, cls=NpEncoder)


def sports(_name):
    with open(Path("./misc/tables/girls_en.json"), 'r') as _f:
        _girls = json.load(_f)
    _id = _girls[_name][-1]
    _T = pd.read_csv(Path("./combined_tables/monster.csv"))
    _Ti = _T[_T["partner_link"] == _id]
    _Ti = _Ti[_Ti["id"] // 1000 == 89]
    if len(_Ti) != 1:
        print(_name, _id, _Ti)
    return _Ti.iloc[0]["id"]


if __name__ == "__main__":
    # print_pets(_lang="zh_tw", _lua=False)
    # print_lab()
    # print_equips(_lang="zh_tw", _lua=False)
    # print_cores(_lang="en_en", _lua=False)
    # trans_cores()
    # print(all_girls(_lang="en_en"))
    # print_10_girls(_lang="zh_tw", _lua=False)
    _TEAM = [
        "Mika",
        "Empress Saint",
        "Rogue",
        "Monica",
        "Teresa",
        "Ithil",
        "Sivney",
        "Estel",
        "Skye",
        "Trinity",
        "N-Gen Iron Fist",
        "Turin",
    ]
    print(",\n".join([str(sports(_n)) for _n in _TEAM]))
