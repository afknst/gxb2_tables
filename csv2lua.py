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


def print_boxes(_lang="zh_tw"):
    _P = Path("./tables/giftbox_optional.csv")
    _PR = Path(f"./tables/{_lang}/item_text_{_lang}.csv")
    _T = pd.read_csv(_P)
    _TR = pd.read_csv(_PR)

    _T['id'] = _T['id'].apply(int).apply(str)
    _TR['id'] = _TR['id'].apply(int).apply(str)

    def _id2name(_id):
        if '#' in _id:
            _id, _num = _id.split('#')
            if int(_num) == 1:
                _num = ''
            else:
                _num = _num + ' x '
        else:
            _num = ''
        _TS = _TR[_TR['id'] == _id]
        assert len(_TS) == 1, _id

        if _TS.iloc[0]['brief'] == '造型':
            return _num + _TS.iloc[0]['desc']
        return _num + _TS.iloc[0]['name']

    def _split(_items):
        return _items.split('|')

    def _items2name(_items):
        return [_id2name(_) for _ in _items]

    _BOXES = _T['id'].apply(_id2name)
    _ITEMS = _T['item'].apply(_split).apply(_items2name)
    _T_RES = pd.DataFrame(data={
        'ID': _T['id'],
        'BOX_NAME': _BOXES,
        'ITEMS': _ITEMS,
    })
    _T_RES.sort_values("ID", inplace=True)
    _T_RES.set_index("ID", inplace=True)
    _T_RES.to_csv("./misc/tables/giftbox_optional_with_names.csv")


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

    _out = Path("./misc/tables/antiques.json")
    with open(_out, 'w') as _f:
        json.dump(_equips, _f, indent=4, ensure_ascii=False, cls=NpEncoder)

    _equips = {_equips[_k]: _k for _k in _equips}
    _list = sorted(list(_equips.keys()))
    if _lua:
        for _k in _list:
            print(f"[\"{_equips[_k]}\"] = {_k},")
    else:
        for _i in range(len(_list)):
            print(_equips[_list[-_i - 1]])
        print(len(_equips))


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
    _GRADES = {
        1: 'BLUE',
        2: 'YELLOW',
        3: 'PURPLE',
        4: 'GREEN',
        5: 'RED',
        6: 'ORANGE',
        7: 'PINK',
    }
    _P = Path("./tables/equip.csv")
    _T = pd.read_csv(_P)
    _T = _T[_T.id // 1000 == 5]
    _dict = {}
    # print(len(_T))
    for _r in range(len(_T)):
        _R = _T.iloc[_r]
        _stats = buff2desc(_R.base1, _R.base2, _R.base3, _lang=_lang)
        _stats = f"{_GRADES[_R.qlt]}{_R.star} {_stats}"
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


def print_lab(_lua=True, _page=1):
    _P = Path("./tables/guild_skill.csv")
    _T = pd.read_csv(_P)
    _T = _T[_T.reset // 10 == _page - 1]
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


def print_tables():
    print("SERVANTS = {")
    print_pets(_lang="zh_tw")
    print_pets(_lang="en_en")
    print("}\n")

    print("ANTIQUES = {")
    print_equips(_lang="zh_tw")
    print_equips(_lang="en_en")
    print("}\n")

    print("CORES = {")
    print_cores(_lang="zh_tw")
    print_cores(_lang="en_en")
    print("}\n")

    print("GUILD_1ST_PAGE = {")
    print_lab()
    print("}\n")

    print("GUILD_FULL = {")
    print_lab()
    print_lab(_page=2)
    print("}\n")


if __name__ == "__main__":
    # print_pets(_lang="zh_tw", _lua=False)
    # print_lab()
    # print_equips(_lang="en_en", _lua=True)
    # print_cores(_lang="zh_tw", _lua=True)
    # trans_cores()
    # print(all_girls(_lang="en_en"))
    # print_10_girls(_lang="en_en", _lua=True)
    # _TEAM = [
    #     "Sivney",
    #     "Nephilim",
    #     "Vivian",
    #     "Kassy",
    #     "Monica",
    #     "Angelica",
    #     "Holly",
    #     "Apate",
    #     "Kassy",
    #     "Teresa",
    #     "Diana",
    #     "Skye",
    # ]
    # print(",\n".join([str(sports(_n)) for _n in _TEAM]))

    # print_boxes()
    print_tables()
