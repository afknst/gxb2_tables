import os

import tables
import numpy as np
import matplotlib.pyplot as plt

from luvly_constants import trans_X, TRANS, NEXT, index_X, EXIT

N_MAX = 108
D_FILE = 'D.h5'
assert os.path.exists(D_FILE)
T = tables.open_file(D_FILE)
D = T.root.D


# 1	空投	獲得普通資源自選寶箱*1
# 2	晴空	陽光普照萬物生長，隨機資源格的等級+1（資源格等級都最高則無效）
# 3	順風而行	下次旋轉船舵時，前進的格子數翻倍
# 4	雙份快樂	下次旋轉船舵時，會連續旋轉2次
# 5	運勢上升	下次經過或停留在珊瑚樹時，可以獲得雙倍的珊瑚枝！
# 6	傾盆小雨	陰雨連綿，隨機資源格的等級-1（資源格等級都最低則無效）
# 7	浪兒	海浪席捲，下次前進時如停留在資源格，獎勵會被無情的浪兒沖走。
# 8	磁場錯亂	海域磁場混亂，下一次變為倒退旋轉到的點數。（無法獲得獎勵及升級格子）
# 9	陸遜的怨念	失散多日的陸遜要抓你回去，拉芙麗回到起點位置。
def conch2k(_c):
    assert _c in range(1, 9 + 1)
    if _c in [1, 2, 6, 7]:
        return 2
    if _c in [3, 4]:
        return 3
    if _c == 5:
        return 4
    if _c == 8:
        return 5
    return 0


# 2: 2, NOTHING (1, 2, 6, 7)
# 3: 2, DOUBLE (3, 4)
# 4: 2, DOUBLE_CORAL (5)
# 5: 2, BACKWARDS (8)
def k2t(_i):
    if _i <= 1:
        return _i
    if _i <= 5:
        return 2
    return _i - 3


def dist(_t1, _t2):
    _d = _t2 - _t1
    if _d < 0:
        _d += 20
    return _d


def half_of(_d):
    if _d in [1, 2]:
        _h = 1
    if _d in [3, 4]:
        _h = 2
    if _d in [5, 6]:
        _h = 3
    return _h


def luvly_helper(_I, _J, _K, _X):
    return D[_I, _J, _K, index_X(_X)]


def benchmark(_I, _J, _K, _X):
    _d = dist(k2t(_K), 12)
    if (_J > 0) and (3 <= _d <= 6) and (_K != 10):
        return _d
    if (_J > 0) and (_K == 3):
        return 5
    if _I == 0:
        return 6
    return 0


class Luvly:
    def __init__(self, start=None, verbose=False):
        start = start or {
            "RUDDER": 78,
            "ADV_RUDDER": 0,
            "TILE": 0,
            "CORAL": 0,
            "PEARL": 0,
            "CORAL_LEVELS": (1, 1, 1),
            "CONCH": None,  # None or 1-9
        }

        if "RUDDER" not in start:
            start["RUDDER"] = 78
        if "ADV_RUDDER" not in start:
            start["ADV_RUDDER"] = 0
        if "TILE" not in start:
            start["TILE"] = 0
        if "CORAL" not in start:
            start["CORAL"] = 0
        if "PEARL" not in start:
            start["PEARL"] = 0
        if "CORAL_LEVELS" not in start:
            start["CORAL_LEVELS"] = (1, 1, 1)
        if "CONCH" not in start:
            start["CONCH"] = None

        self.I = start["RUDDER"]
        self.J = start["ADV_RUDDER"]
        _t = start["TILE"]
        if _t <= 1:
            self.K = _t
        elif _t == 2:
            assert start["CONCH"] is not None
            self.K = conch2k(start["CONCH"])
        else:
            self.K = _t + 3
        self.X = np.array(
            [
                start["CORAL"],
                start["PEARL"] // 5,
                start["CORAL_LEVELS"][0] - 1,
                start["CORAL_LEVELS"][1] - 1,
                start["CORAL_LEVELS"][2] - 1,
                1,
            ],
            dtype=np.uint16,
        )
        self.start = (self.I, self.J, self.K, self.X)
        self.verbose = verbose
        self.print_status()

    def reset(self):
        self.I, self.J, self.K, self.X = self.start

    def update(self):
        self.start = (self.I, self.J, self.K, self.X)

    def print_status(self, _force=False):
        if self.verbose or _force:
            _effect = ""
            if self.K == 3:
                _effect = "Double:\tTrue"
            if self.K == 4:
                _effect = "Double Coral:\tTrue"
            if self.K == 5:
                _effect = "Backwards:\tTrue"
            if self.K == 10:
                _effect = "Half:\tTrue"

            print("\n===========Current Status===========")
            print(f"Tile:\t{k2t(self.K)}\t{_effect}")
            print(f"Rudder:\t{self.I}\tAdv. Rudder:\t{self.J}")
            print(f"Coral:\t{self.X[0]}\tPearl:\t\t{self.X[1]*5}")
            print(f"Coral levels:\t{self.X[2:5]+1}")
            print("===========Current Status===========\n")

    def luvly_print(self, *sth):
        if self.verbose:
            print(*sth)

    def get_status(self):
        return self.I, self.J, self.K, self.X

    def get_gain(self):
        return self.X[0] + 2 * (self.I + self.J), 5 * self.X[1]

    def assign(self, _d):
        _print = self.luvly_print
        _print(f'\nAssign: {_d}')
        if _d == 0:
            self.roll()
        elif _d == 7:
            _print(f"Wait for recycle: {self.get_status()}")
        elif self.J < 1:
            _print(f"No adv rudder: {self.get_status()}")
        else:
            self.J -= 1
            _print(f"Use adv rudder: {self.J+1} -> {self.J}")
            self.advance(_d)

    def roll(self):
        if self.I < 1:
            self.luvly_print(f"No rudder: {self.get_status()}")
            return
        _d = np.random.choice(list(NEXT[self.K].keys()))
        self.I -= 1
        self.advance(_d)

    def rolled(self, _d, _conch=None):
        self.I -= 1
        self.advance(_d, _conch=_conch)

    def asigned(self, _d, _conch=None):
        self.J -= 1
        self.advance(_d, _conch=_conch)

    def go_to_next(self, _next):
        self.luvly_print(f"Advance: {k2t(self.K)} -> {k2t(_next[2])}")
        _tr = TRANS[self.K][_next[2]]
        self.I += _next[0]
        self.J += _next[1]
        self.K = _next[2]
        self.X = trans_X(self.X, _tr)
        self.print_status()

    def advance(self, _d, _conch=None):
        _dd = int(_d)
        if self.K == 10:
            _dd = half_of(_dd) * 2
        _next = NEXT[self.K][_dd]
        if len(_next) == 1:
            for _n in _next:
                self.go_to_next(_n)
        else:
            _conch = _conch or np.random.randint(1, 9 + 1)
            self.go_to_next((0, 0, conch2k(_conch)))

    def keep_rolling(self, _strategy, verbose=False, **kwargs):
        self.verbose = verbose
        while self.I > 0 or self.J > 0:
            if self.J == 0:
                self.assign(0)
            else:
                _d = _strategy(*self.get_status(), **kwargs)
                self.assign(_d)
                if _d == 7:
                    break
        return self

    def sim(self, _strategy, _M=10000):
        _res = []
        for _ in range(_M):
            _res.append(self.keep_rolling(_strategy).get_gain())
            self.reset()
        return np.array(_res)

    def get_estimate(self, _strategy=benchmark, _M=1000):
        _res = self.sim(_strategy, _M=_M)
        _mc, _mp = np.mean(_res, axis=0)
        _dmc = 1.96 * np.sqrt(np.mean((_res[:, 0] - _mc)**2) / _M)
        _dmp = 1.96 * np.sqrt(np.mean((_res[:, 1] - _mp)**2) / _M)
        return _mc, _mp, _dmc, _dmp


def fin():
    print("\nI'm fine.")
    # T.close()
    EXIT(0)


def inputter(_msg):
    _temp = input(_msg)

    if _temp.lower() in ['yes', 'y']:
        return "Y"

    if _temp.lower() in ['exit', 'quit', 'q', 'no', 'n']:
        fin()

    if _temp.isnumeric():
        return int(_temp)

    print(f"Invalid input: {_temp}.")
    fin()
    return None


def input_rolled(_t0):
    _d = inputter("Rolled = ? (1-6) ")
    if _d not in range(1, 6 + 1):
        print(f"Invalid input: {_d}.")
        fin()

    _c = None
    if dist(_t0, 2) == _d:
        _c = inputter("Conch = ? (1-9) ")
        if _c not in range(1, 9 + 1):
            print(f"Invalid input: {_c}.")
            fin()
    return _d, _c


def guide(_luvly, _helper, _M=1000):
    _I, _J, _K, _X = _luvly.get_status()
    _luvly.print_status(_force=True)
    if _I < 1 and _J < 1:
        fin()

    _mc, _mp, _dmc, _dmp = _luvly.get_estimate(_M=_M)
    print("Estimate:")
    print(f"\tAVERAGE CORAL: {_mc:.2f} ± {_dmc:.2f}")
    print(f"\tAVERAGE PEARL: {_mp:.2f} ± {_dmp:.2f}\n")

    _T = k2t(_K)
    _d = _helper(_I, _J, _K, _X)
    print(f"Helper: {_d}.")
    if _d == 7:
        print("Please wait for recycle.")
        fin()

    if _J < 1:
        print("No Adv. Rudder. Please use Rudder.")
        _d, _c = input_rolled(_T)
        _luvly.rolled(_d, _c)
    else:
        if _d != 0:
            _check = inputter(f"Asigned {_d}? (Y/N) ")
            if _check != "Y":
                print(f"Invalid input: {_check}.")
                fin()
        if _d == 0:
            print("Please use Rudder.")
            _d, _c = input_rolled(_T)
            _luvly.rolled(_d, _c)
        elif dist(_T, 2) == _d:
            _c = inputter("Conch = ? (1-9) ")
            if _c not in range(1, 9 + 1):
                print(f"Invalid input: {_c}.")
                fin()
            _luvly.asigned(_d, _c)
        else:
            _luvly.asigned(_d)
    _luvly.update()
    guide(_luvly, _helper, _M=_M)


def res_analyse(_res, _plot=True):
    _M = len(_res)

    print("=====Coral=====")
    for _k in [170, 200, 230, 260, 300, 340]:
        print(f"{_k}:\t{np.count_nonzero(_res[:, 0] >= _k) / _M}")
    print(f"mean:\t{np.mean(_res[:, 0])}\nstd:\t{np.std(_res[:, 0])}")
    print(f"min:\t{np.min(_res[:, 0])}\nmax:\t{np.max(_res[:, 0])}")

    if _plot:
        _, ax = plt.subplots()
        ax.hist(_res[:, 0], bins=20, density=True)
        plt.title('Coral')
        plt.show()

    print("=====Pearl=====")
    for _k in [140, 180, 220, 260, 300, 340]:
        print(f"{_k}:\t{np.count_nonzero(_res[:, 1] >= _k) / _M}")
    print(f"mean:\t{np.mean(_res[:, 1])}\nstd:\t{np.std(_res[:, 1])}")
    print(f"min:\t{np.min(_res[:, 1])}\nmax:\t{np.max(_res[:, 1])}")

    if _plot:
        _, ax = plt.subplots()
        ax.hist(_res[:, 1], bins=20, density=True)
        plt.title('Pearl')
        plt.show()


if __name__ == '__main__':
    # This is the default value
    START = {
        "RUDDER": 80,  # 0-108
        "ADV_RUDDER": 1,  # 0-2
        "TILE": 12,  # 0-20, see Tiles indexing
        "CORAL": 9,  # 0-400
        "PEARL": 0,  # 0-400
        "CORAL_LEVELS": (1, 1, 1),  # 1-3 for each
        "CONCH": None,  # None or 1-9, see Conch
    }
    L = Luvly(start=START)
    guide(L, luvly_helper)
