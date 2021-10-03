import numpy as np
import pandas as pd

UPDATE_VE = {"SSR": 40, "SR": 14, "R": 10}
MAX_LV = {"SSR": 50, "SR": 40, "R": 30}
REWARDS = [(3, 6, 48, 60), (4, 6, 60, 60), (0, 2, 0, 25)]


def rarity(_s):
    if _s > 0.0015:
        return "SSR"
    if _s > 0.0005:
        return "SR"
    return "R"


BOSSES = pd.read_csv('bosses.csv')
BOSSES.set_index("Boss", inplace=True)

GIRLS = pd.read_csv('girls.csv')
for _k in ["Buff HP", "Buff Attack", "Buff Armor"]:
    GIRLS[_k] = GIRLS[_k].str.rstrip('%').astype('float') / 100.0
GIRLS.fillna(0, inplace=True)
GIRLS["Total"] = GIRLS["Buff HP"] + GIRLS["Buff Attack"] + GIRLS["Buff Armor"]
GIRLS["Rarity"] = GIRLS["Total"].apply(rarity)
GIRLS.set_index("Name", inplace=True)

TEAM = {}
TEAM['GIRLS'] = {_: 1 for _ in GIRLS.index.tolist()}
TEAM["VE"] = 0
TEAM["STAGE"] = 1
TEAM["MAP"] = (5, 1)

VE0 = 0
T = {"SSR": [], "SR": [], "R": []}
MAT = []
RES = {}


def reset_team():
    global TEAM, VE0, T, MAT, RES
    TEAM = {}
    TEAM['GIRLS'] = {_: 1 for _ in GIRLS.index.tolist()}
    TEAM["VE"] = 0
    TEAM["STAGE"] = 1
    TEAM["MAP"] = (5, 1)

    VE0 = 0
    T = {"SSR": [], "SR": [], "R": []}
    MAT = []
    RES = {}


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


def ve(_lv):
    return np.dot(_lv - 1, T["UP"])


def s2ve(_stage, _map):
    _s = 0
    for _i in range(_stage - 1):
        _r = get_rewards(_i + 1)
        _s += 5 * _r[1] + _r[3]
    _r = get_rewards(_stage)
    _s += _map[0] * _r[1] + _map[1] * _r[3]
    return _s


def get_rewards(_stage):
    if _stage <= 25:
        return REWARDS[0]
    if _stage <= 50:
        return REWARDS[1]
    return REWARDS[2]


def read_team(_t):
    global VE0, T, MAT

    VE0 = _t['VE']
    for _girl in _t['GIRLS']:
        if _t['GIRLS'][_girl] >= 1:
            _rarity = GIRLS.loc[_girl]["Rarity"]
            T[_rarity].append(_girl)
            MAT.append(GIRLS.loc[_girl][:6])
            VE0 += (_t['GIRLS'][_girl] - 1) * UPDATE_VE[_rarity]
    VE0 -= s2ve(_t["STAGE"], _t["MAP"])
    MAT = np.array(MAT)
    T["ALL"] = T["SSR"] + T["SR"] + T["R"]
    T["UP"] = [UPDATE_VE["SSR"]] * len(T["SSR"])
    T["UP"] += [UPDATE_VE["SR"]] * len(T["SR"])
    T["UP"] += [UPDATE_VE["R"]] * len(T["R"])
    T["UP"] = np.array(T["UP"], dtype=int)

    T["MAX"] = [MAX_LV["SSR"]] * len(T["SSR"])
    T["MAX"] += [MAX_LV["SR"]] * len(T["SR"])
    T["MAX"] += [MAX_LV["R"]] * len(T["R"])
    T["MAX"] = np.array(T["MAX"], dtype=int)

    T["MASK"] = np.zeros((len(T["ALL"]), 3), dtype=int)
    T["MASK"][:, 0] = T["UP"] == UPDATE_VE["SSR"]
    T["MASK"][:, 1] = T["UP"] == UPDATE_VE["SR"]
    T["MASK"][:, 2] = T["UP"] == UPDATE_VE["R"]


def reset():
    return np.ones(len(T["ALL"]), dtype=int)


def get_status(_lv):
    _status = np.sum((MAT[:, :3].T * _lv).T, axis=0)
    _multiplicator = np.sum((MAT[:, 3:].T * _lv).T, axis=0)
    return np.floor((1 + _multiplicator) * _status)


def upgradable(_lv, _max=None):
    if _max is not None:
        return np.matmul(_max - _lv, T["MASK"])
    return np.matmul(T["MAX"] - _lv, T["MASK"])


def n2lv_up(_ve, _lv, _max=None):
    _v = _ve
    _n = {"SSR": 0, "SR": 0, "R": 0}
    _up = upgradable(_lv, _max=_max)

    _temp = np.min([_v // UPDATE_VE["SSR"], _up[0]])
    _temp = np.random.randint(np.max([_temp - 50, 0]), _temp + 1)
    _v -= _temp * UPDATE_VE["SSR"]
    _n["SSR"] = _temp

    _temp = np.min([_v // UPDATE_VE["SR"], _up[1]])
    _v -= _temp * UPDATE_VE["SR"]
    _n["SR"] = _temp

    _temp = np.min([_v // UPDATE_VE["SSR"], _up[0] - _n["SSR"]])
    _v -= _temp * UPDATE_VE["SSR"]
    _n["SSR"] += _temp

    _temp = np.min([_v // UPDATE_VE["R"], _up[2]])
    _v -= _temp * UPDATE_VE["R"]
    _n["R"] = _temp

    return _n


def lv_down(_lv, _size=3):
    _inds = np.where(_lv > _size + 2)[0]
    if len(_inds) > 0:
        _i = np.random.choice(_inds, size=_size)
        _lv[_i] -= _size
    _lv[np.where(_lv <= _size)[0]] = 1
    return _lv


def lv_up(_ve, _lv, _max=None):
    _lv = lv_down(_lv)
    _ve_old = ve(_lv)
    _start = 0
    _end = 0

    if _ve_old < _ve:
        _ve = _ve - _ve_old
        _n = n2lv_up(_ve, _lv, _max=_max)
        for _r in _n:
            _end += len(T[_r])
            # print(_start, _end, MAT[_start], MAT[_end - 1])
            while _n[_r] > 0:
                _i = np.random.randint(_start, _end)
                if _lv[_i] < MAX_LV[_r]:
                    if _max is None or _lv[_i] < _max[_i]:
                        _lv[_i] += 1
                        _n[_r] -= 1
            _start = _end
        return _lv

    _lv = reset()
    _n = n2lv_up(_ve, _lv, _max=_max)

    for _r in _n:
        _end += len(T[_r])
        # print(_start, _end, MAT[_start], MAT[_end - 1])
        while _n[_r] > 0:
            _i = np.random.randint(_start, _end)
            if _lv[_i] < MAX_LV[_r]:
                if _max is None or _lv[_i] < _max[_i]:
                    _lv[_i] += 1
                    _n[_r] -= 1
        _start = _end

    return _lv


def good(_lv, _boss):
    _hp, _atk, _arm = _boss
    _hp0, _atk0, _arm0 = get_status(_lv)
    _turns_0 = np.ceil(_hp / np.maximum(_atk0 - _arm, 50))
    _turns_1 = np.ceil(_hp0 / np.maximum(_atk - _arm0, 50))
    return _turns_0 < _turns_1


def ok(_stage, _ve_ex=0, _max=None, _trial=100):
    _VE = _ve_ex + VE0 + s2ve(_stage, (0, 1))
    if _stage in RES:
        _lv = np.copy(RES[_stage][1])
    else:
        _lv = reset()

    for _ in range(_trial):
        _lv = lv_up(_VE, _lv, _max=_max)
        if good(_lv, BOSSES.loc[_stage]):
            if _stage in RES:
                if _ve_ex < RES[_stage][0]:
                    RES[_stage] = (_ve_ex, _lv)
            else:
                RES[_stage] = (_ve_ex, _lv)
            return True
    return False


def recheck(_goal, _trial, _left, _right):
    while True:
        print("Range:", _left, _right)
        _temp = int((_left + _right) / 2)

        if _temp == _left:
            return _right

        if ok(_goal, _ve_ex=_temp, _trial=_trial):
            _right = _temp
        else:
            _left = _temp


def get_ve(_goal, _trial=100, _l=0, _r=512):
    _left = _l
    _right = _r

    if ok(_goal, _ve_ex=_left, _trial=_trial):
        return _left

    if not ok(_goal, _ve_ex=_right, _trial=_trial):
        return None

    return recheck(_goal, _trial, _left, _right)


def deeper_search(_goal, _steps=2):
    _factors = [_steps + _i + 1 for _i in range(_steps)]
    _l = 0
    _r = 512
    _trial = 100
    _res = get_ve(_goal, _trial=_trial, _l=_l, _r=_r)
    while _res is None:
        _l = _r
        _r *= 2
        if _r > 10240:
            print(f"Your team is insufficient for Stage {_goal}.")
            return None
        print(_l, _r)
        _res = get_ve(_goal, _trial=_trial, _l=_l, _r=_r)

    _right = _res
    for _f in _factors:
        _trial *= 5
        _left = _f * _right // (_f + 1)
        _right = recheck(_goal, _trial, _left, _right)
    return _right


def print_lv(_lv):
    _s = "Levels: \n"
    for _i, _l in enumerate(_lv):
        if _l > 1:
            _s += f"\t{T['ALL'][_i]}:" + " " * 5 + f"\t{_l}\n"
    print(_s)


def calc(_goal, _steps=1):
    _EXTRA = deeper_search(_goal, _steps=_steps)
    assert RES[_goal][0] == _EXTRA, f"{RES[_goal]}"

    if _EXTRA is None:
        return
    _REAL = ve(RES[_goal][1])
    _EXTRA_REAL = _REAL - VE0 - s2ve(_goal, (0, 1))
    print(
        f"\nYou need {_EXTRA_REAL} more VE to pass Stage {_goal} ({_REAL} in total)."
    )
    _s = "Levels: \n"
    print_lv(RES[_goal][1])


def check_fin(_goal):
    if _goal in RES:
        _MAX = RES[_goal][1]
        for _i in range(1, _goal):
            _STAGE = _goal - _i
            while _STAGE not in RES:
                if ok(_STAGE, _ve_ex=RES[_goal][0], _max=_MAX):
                    break
            _MAX = RES[_STAGE][1]
            _win = "LOSE"
            if good(_MAX, BOSSES.loc[_STAGE]):
                _win = "WIN"
            print(f"Stage {_STAGE}: {_win}")
            print_lv(RES[_STAGE][1])


if __name__ == "__main__":
    reset_team()
    TEAM['GIRLS'] = {
        'Lucifer': 22,
        # 'Michael': 1,
        # 'Dracula': 1,
        # 'Saint': 1,
        # 'Nobunaga': 1,
        'KongMing': 10,
        # 'Marynari': 1,
        'Robin': 40,
        'Sisha': 40,
        'Mythra': 40,
        'Athena': 40,
        # 'Kenshin': 1,
        # 'Reo': 1,
        # 'Poppi': 1,
        'Jade': 1,
        'Ursula': 1,
        'Kitty': 1,
        'Samurai': 2,
        'Tula': 2,
        'Edward': 1,
        'King': 1,
        'Donna': 1,
        'Nobuna': 1,
        'Annabelle': 1,
        'Harley': 1,
        'Magician': 1,
        'Caitlin': 1
    }
    TEAM['VE'] = 60
    TEAM['STAGE'] = 31
    TEAM['MAP'] = (5, 1)
    read_team(TEAM)
    GOAL = 31
    calc(GOAL, _steps=3)
    check_fin(GOAL)
