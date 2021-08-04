import numpy as np
import pandas as pd

BOSSES = pd.read_csv('bosses.csv')
GIRLS = pd.read_csv('girls.csv')[[
    "Name", "Star", "base_hp", "base_atk", "base_arm"
]]
GIRLS.set_index("Name", inplace=True)

SKILLS = {
    "Dracula": (0, 0, 0.05),
    "Nono": (0, 0, 0.1),
    "Hynel": (0.1, 0, 0),
    "Fleur": (0, 0.125, 0),
    "Meimi": (0, 0, 0.1),
    "Michael": (0.1, 0.12, 0),
    "Saint": (0.1, 0, 0.1),
    "Nobunaga": (0.12, 0.08, 0),
    "KongMing": (0, 0.1, 0.1),
}

AC0 = 54
VE0 = 110
R = set([
    "Lucifer",
    "Skarivine",
    "Cayla",
    "Vanees",
    "Maidam",
    "Aegis",
    "Handana",
    "Lin AI",
    "Witch",
    "Stella",
])
SR = set([
    "Dracula",
    "Nono",
    "Hynel",
    "Fleur",
    "Meimi",
])
SSR = set([
    "Michael",
    "Saint",
    "Nobunaga",
    "KongMing",
])

# TEAM = set([
#     "Michael",
#     "Saint",
#     "KongMing",
#     *SR,
#     "Lucifer",
#     "Skarivine",
#     "Cayla",
#     # "Vanees",
#     "Maidam",
#     "Aegis",
#     "Handana",
#     "Lin AI",
#     "Witch",
#     "Stella",
# ])

TEAM = set([
    # "Michael",
    # "Saint",
    # "Nobunaga",
    "KongMing",
    # "Dracula",
    "Nono",
    # "Hynel",
    # "Fleur",
    # "Meimi",
    "Lucifer",
    "Skarivine",
    "Cayla",
    "Vanees",
    "Maidam",
    "Aegis",
    "Handana",
    "Lin AI",
    "Witch",
    "Stella",
])
# TEAM = set([*SSR, *SR, *R])
TEAM_R = TEAM.intersection(R)
TEAM_SR = TEAM.intersection(SR)
TEAM_SSR = TEAM.intersection(SSR)
GOAL = 13
VE0 = 212


def get_status(_lv):
    _status = np.array((0, 0, 0), dtype=np.float64)
    _multiplicator = np.array((0, 0, 0), dtype=np.float64)

    for _k, _v in _lv.items():
        if _k in SKILLS:
            _multiplicator += _v * np.array(SKILLS[_k], dtype=np.float64)
        _s = GIRLS.loc[_k]
        _status[0] += _v * _s["base_hp"]
        _status[1] += _v * _s["base_atk"]
        _status[2] += _v * _s["base_arm"]

    return np.round((1 + _multiplicator / 100) * _status)


def upgradable(_lv):
    _SSR = [_ for _ in TEAM_SSR if _lv[_] < 50]
    _SR = [_ for _ in TEAM_SR if _lv[_] < 40]
    _R = [_ for _ in TEAM_R if _lv[_] < 30]
    return _SSR, _SR, _R


def lv_up(_ve, _ret=False, _current=None):
    _v = _ve
    if _current is not None:
        _lv = _current
    else:
        _lv = {_: 1 for _ in TEAM}

    while True:
        if _v < 10:
            break
        _SSR, _SR, _R = upgradable(_lv)
        if len(_SSR) + len(_SR) + len(_R) == 0:
            break

        if len(_SSR) > 0 and _v >= 20:
            _girl = np.random.choice(_SSR)
            _lv[_girl] += 1
            _v -= 20
            continue

        if len(_SR) > 0 and _v >= 14:
            if len(_SR) > 1 and "Dracula" in _SR:
                _SR.remove("Dracula")
            _girl = np.random.choice(_SR)
            _lv[_girl] += 1
            _v -= 14
            continue

        if len(_R) > 0 and _v >= 10:
            _girl = np.random.choice(_R)
            _lv[_girl] += 1
            _v -= 10
            continue

    if _ret:
        return get_status(_lv), _lv
    return get_status(_lv)


def ac2ve(_ac):
    _nSSR = _ac * 0.02
    _nSR = _ac * 0.15
    _nR = _ac * 0.83

    if _nSSR > 3:
        _veSSR = (_nSSR - 3) * 100
    else:
        _veSSR = 0

    if _nSR > 5:
        _veSR = (_nSR - 5) * 15
    else:
        _veSR = 0

    if _nR > 9:
        _veR = (_nR - 9) * 3
    else:
        _veR = 0

    return _veSSR + _veSR + _veR


def ok(_ext, _ret=False):
    _VE = VE0 + _ext
    _TRIAL = 200

    for _i in range(GOAL):
        _hp, _atk, _arm = BOSSES.loc[_i]
        _pass = False
        _VE += 50

        for _ in range(_TRIAL):
            if _ret:
                (_hp0, _atk0, _arm0), _lv = lv_up(_VE, _ret)
            else:
                _hp0, _atk0, _arm0 = lv_up(_VE)

            _t0 = np.ceil(_hp / np.maximum(_atk0 - _arm, 50))
            _t1 = np.ceil(_hp0 / np.maximum(_atk - _arm0, 50))
            # print(t0, t1)

            if _t0 < _t1:
                if _i == GOAL - 1:
                    if _ret:
                        return True, _lv
                    return True

                # print(_i + 1, _VE, int(_hp0), int(_atk0), int(_arm0))
                _VE += 100
                _hp0, _atk0, _arm0 = lv_up(_VE)
                _pass = True
                break

        if not _pass:
            if _ret:
                return False, None
            return False

    if _ret:
        return False, None
    return False


def get_ve(_l=0, _r=512):
    _left = _l
    _right = _r
    assert ok(_right, True)[0]

    _ok, _lv = ok(_left, True)
    if _ok:
        print(_left)
        print(_lv)
        return

    while True:
        print(_left, _right)
        _temp = int((_left + _right) / 2)

        if _temp == _left:
            print(_right)
            print(_lv)
            return

        _ok, _lv1 = ok(_temp, True)
        if _ok:
            _right = _temp
            _lv = _lv1
        else:
            _left = _temp


# print(ac2ve(54 + 60 + 32 + 17) + 900 + 480 + 270)
get_ve(_l=0, _r=256)
