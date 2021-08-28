import sys
import numpy as np

from luvly_constants import trans_X, TRANS, NEXT

N_MAX = 108


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

        self.start = start
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
        self.verbose = verbose
        self.print_status()

    def print_status(self):
        if self.verbose:
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
        return self.X[0] + 2 * (self.I + self.J), self.X[1]

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
                _d = _strategy(self.get_status(), **kwargs)
                self.assign(_d)
                if _d == 7:
                    break
        return self


def luvly_helper(_I, _J, _K, _X):
    return 0


def fin():
    print("\nI'm fine.")
    sys.exit(0)


def inputter(_msg):
    _temp = input(_msg)

    if _temp.lower() in ['exit', 'quit', 'q']:
        fin()

    if _temp.isnumeric():
        return int(_temp)

    print("Invalid input.")
    fin()
    return None


def input_rolled(_t0):
    _d = inputter("Rolled = ? (1-6) ")
    _c = None
    if dist(_t0, 2) == _d:
        _c = inputter("Conch = ? (1-9) ")
    return _d, _c


if __name__ == '__main__':
    START = {
        "RUDDER": 15,
        "ADV_RUDDER": 2,
        "TILE": 6,
        "CORAL": 100,
        "PEARL": 100,
        "CORAL_LEVELS": (1, 1, 2),
        "CONCH": None,  # None or 1-9
    }
    L = Luvly(start=START, verbose=True)

    while True:
        I, J, K, X = L.get_status()
        T = k2t(K)
        if I < 1 and J < 1:
            break
        if J < 1:
            print("No Adv. Rudder. Please use Rudder.")
            d, c = input_rolled(T)
            L.rolled(d, c)
        else:
            d = luvly_helper(I, J, K, X)
            print(f"Helper: {d}.")
            if d != 0:
                print("=" * 30)
                print("=" * 30)
                print("=" * 30)
                print("=" * 30)
                print(d)
            if d == 0:
                print("Please use Rudder.")
                d, c = input_rolled(T)
                L.rolled(d, c)
            elif dist(T, 2) == d:
                c = inputter("Conch = ? (1-9) ")
                L.asigned(d, c)
            else:
                L.asigned(d)
    fin()
