import os
import sys
import zipfile

import tables
import numpy as np

N_MAX = 108


def init():
    if not os.path.exists('fin_D'):
        with zipfile.ZipFile("fin_D.zip", "r") as zip_ref:
            zip_ref.extractall(".")

    _D = {}
    for _r, _d, _f in os.walk('fin_D'):
        for __f in _f:
            _p = os.path.join(_r, __f)
            _name = os.path.splitext(__f)[0]
            _D[_name] = tables.open_file(_p)
    return _D


Nt = 21

TILES = [(False, False, False, False, 0), (False, False, False, False, 1),
         (True, False, False, False, 2), (False, False, False, False, 2),
         (False, False, True, False, 2), (False, True, False, False, 2),
         (False, False, False, False, 3), (False, False, False, False, 4),
         (False, False, False, False, 5), (False, False, False, False, 6),
         (False, False, False, True, 7), (False, False, False, False, 8),
         (False, False, False, False, 9), (False, False, False, False, 10),
         (False, False, False, False, 11), (False, False, False, False, 12),
         (False, False, False, False, 13), (False, False, False, False, 14),
         (False, False, False, False, 15), (False, False, False, False, 16),
         (False, False, False, False, 17), (False, False, False, False, 18),
         (False, False, False, False, 19), (False, False, False, False, 20)]
TILES_INDEX = {k: v for v, k in enumerate(TILES)}
LEVELS = [(s4, s5, s6) for s4 in [1, 2, 3] for s5 in [1, 2, 3]
          for s6 in [1, 2, 3]]
MUT = np.array([70 * 27, 27, 1])


def dist(_t1, _t2):
    _d = _t2 - _t1
    if _d < 0:
        _d += Nt - 1
    return _d


def half_of(_d):
    if _d in [1, 2]:
        _h = 1
    if _d in [3, 4]:
        _h = 2
    if _d in [5, 6]:
        _h = 3
    return _h


def s2a(_s):
    _cl = _s[4] * 9 + _s[5] * 3 + _s[6] - 13
    _t = TILES_INDEX[_s[7:]]
    return (_s[0], _s[1], _s[2], _s[3], _cl, _t)


def a2s(_a):
    return (_a[0], _a[1], _a[2], _a[3], *LEVELS[_a[4]], *TILES[_a[5]])


def X_index(_a):
    _x_real = [np.min([_a[2], 309]), np.min([_a[3] // 5, 69]), _a[4]]
    return np.dot(_x_real, MUT)


class Luvly:
    # pylint: disable=too-many-instance-attributes

    def __init__(self, _s=None, verbose=False):
        _default = (N_MAX, 0, 0, 0, 1, 1, 1, False, False, False, False, 0)

        if _s is None:
            _status = _default
        else:
            if isinstance(_s, int):
                _status = (_s, *_default[1:])
            elif isinstance(_s, tuple):
                _l = len(_s)
                assert _l <= len(_default)
                _status = (*_s, *_default[_l:])
            else:
                raise TypeError("_s should be int or tuple.")

        self.coral_levels = {3: 1, 10: 1, 15: 1}

        (
            self.rudder,
            self.adv_rudder,
            self.coral,
            self.pearl,
            self.coral_levels[3],
            self.coral_levels[10],
            self.coral_levels[15],
            self.double,
            self.double_coral,
            self.backwards,
            self.half,
            self.t,
        ) = _status

        self.verbose = verbose
        self.print_status()

    def print_status(self):
        if self.verbose:
            _s = self.get_status()

            _effect = ""
            if self.double:
                _effect = "Double:\tTrue"
            if self.double_coral:
                _effect = "Double Coral:\tTrue"
            if self.backwards:
                _effect = "Backwards:\tTrue"
            if self.half:
                _effect = "Half:\tTrue"

            print("\n===========Current Status===========")
            print(f"Tile:\t{_s[-1]}\t{_effect}")
            print(f"Rudder:\t{_s[0]}\tAdv. Rudder:\t{_s[1]}")
            print(f"Coral:\t{_s[2]}\tPearl:\t\t{_s[3]}")
            print("===========Current Status===========\n")

    def luvly_print(self, *sth):
        if self.verbose:
            print(*sth)

    def land_on(self, _t, _conch=None):
        # pylint: disable=R0912,R0915

        if self.backwards:
            self.t = _t
            self.luvly_print(f"Lands on: {self.t}")
            self.backwards = False
            self.luvly_print(f"Backwards: {self.backwards}")
            return

        if self.double:
            _th = 12
            self.double = False
            self.luvly_print(f"Double: {self.double}")
        elif self.half:
            _th = 3
            self.half = False
            self.luvly_print(f"Half: {self.half}")
        else:
            _th = 6

        for _ct, _cl in self.coral_levels.items():
            if (1 <= dist(self.t, _ct) <= _th) and (dist(_ct, _t) <= _th):
                if self.double_coral:
                    self.coral += 2 * (_cl + 2)
                    self.double_coral = False
                else:
                    self.coral += _cl + 2
                self.luvly_print(f"Get coral: {self.coral}")

        self.t = _t
        self.luvly_print(f"Lands on: {self.t}")

        if _t in self.coral_levels.keys():
            if self.coral_levels[_t] < 3:
                self.coral_levels[_t] += 1
                self.luvly_print(f"Level up: {_t} {self.coral_levels[_t]}")

        if _t in [1, 11]:
            self.pearl += 10
            self.luvly_print(f"Get pearl: {self.pearl}")

        if _t in [6, 16]:
            self.pearl += 15
            self.luvly_print(f"Get pearl: {self.pearl}")

        if _t == 12:
            self.adv_rudder += 1
            self.luvly_print(f"Get adv rudder: {self.adv_rudder}")

        if _t == 17:
            self.rudder += 1
            self.luvly_print(f"Get rudder: {self.rudder}")

        if _t == 7:
            self.half = True
            self.luvly_print(f"Half: {self.half}")

        # Conch Block Effect:
        # 1 Gain an additional :rudder:  next turn.
        # 2 Teleport to starting point.
        # 3 Double the roll next turn.
        # 4 Randomly increase the level of a block by 1. If all are level 3, then no effect.
        # 5 Randomly decrease the level of a block by 1. If all are level 1, then no effect.
        # 6 Double the next :coral:  acquire.
        # 7 Get an :rescart:
        # 8 If next roll lands on a resource block, lose the corresponding resource.
        # 9 go backwards next turn
        if _t == 2:
            if _conch is None:
                _conch = np.random.randint(1, 9 + 1)

            self.luvly_print(f"Conch: {_conch}")

            if _conch == 1:
                self.rudder += 1
                self.luvly_print(f"Get rudder: {self.rudder}")

            if _conch == 2:
                self.t = 0
                self.luvly_print(f"Restart: {self.t}")

            if _conch == 3:
                self.double = True
                self.luvly_print(f"Double: {self.double}")

            if _conch == 6:
                self.double_coral = True
                self.luvly_print(f"Double coral: {self.double_coral}")

            if _conch == 9:
                self.backwards = True
                self.luvly_print(f"Backwards: {self.backwards}")

        self.print_status()

    def get_status(self):
        return (
            self.rudder,
            self.adv_rudder,
            self.coral,
            self.pearl,
            self.coral_levels[3],
            self.coral_levels[10],
            self.coral_levels[15],
            self.double,
            self.double_coral,
            self.backwards,
            self.half,
            self.t,
        )

    def assign(self, _d):
        self.luvly_print(f'\nAssign: {_d}')
        if _d == 0:
            self.roll()
        elif self.adv_rudder < 1:
            self.luvly_print(f"No adv rudder: {self.adv_rudder}")
        else:
            self.adv_rudder -= 1
            self.luvly_print(
                f"Use adv rudder: {self.adv_rudder+1}->{self.adv_rudder}")
            self.advance(_d)

    def roll(self):
        if self.rudder < 1:
            self.luvly_print(f"No rudder: {self.rudder}")
            return
        _d = np.random.randint(1, 6 + 1)
        self.rudder -= 1
        self.advance(_d)

    def rolled(self, _d, _conch=None):
        self.rudder -= 1
        self.advance(_d, _conch=_conch)
        return self.get_status()

    def asigned(self, _d, _conch=None):
        self.adv_rudder -= 1
        self.advance(_d, _conch=_conch)
        return self.get_status()

    def advance(self, _d, _conch=None):
        _dd = int(_d)

        if self.double:
            _dd *= 2
        if self.half:
            _dd = half_of(_dd)
        if self.backwards:
            _dd = -_dd

        _nt = self.t + _dd
        if _nt >= Nt:
            _nt = _nt - Nt + 1
        if _nt <= 0:
            _nt = _nt + Nt - 1

        self.luvly_print(f"Advance: {_dd} \t Go to {_nt}")
        self.land_on(_nt, _conch=_conch)

    def keep_rolling(self, _strategy, verbose=False, **kwargs):
        self.verbose = verbose
        while self.rudder > 0 or self.adv_rudder > 0:
            if self.adv_rudder == 0:
                self.assign(0)
            else:
                _a = s2a(self.get_status())
                _d = _strategy(_a, **kwargs)
                self.assign(_d)
        return self

    # _s: Tuple
    def start_from(self, _s):
        (
            self.rudder,
            self.adv_rudder,
            self.coral,
            self.pearl,
            self.coral_levels[3],
            self.coral_levels[10],
            self.coral_levels[15],
            self.double,
            self.double_coral,
            self.backwards,
            self.half,
            self.t,
        ) = _s
        self.luvly_print(f"Start from: {self.get_status()}")
        return self

    # _a: NumPy Array
    def start_from_array(self, _a):
        return self.start_from(a2s(_a))


def luvly_helper(_a):
    if _a[1] > 3 and _a[-1] == 15:
        return 4
    _n = min(_a[0] + _a[1], N_MAX)
    _a_dummy = (_n - _a[1], *_a[1:])
    _i2 = X_index(_a_dummy)
    return D[f'D_{_a_dummy[0]}_{_a_dummy[1]}'].root.D[_a[-1]][_i2]


def fin():
    for _D in D.values():
        _D.close()
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


def input_rolled(_s):
    _d = inputter("Rolled = ? (1-6) ")
    _c = None
    if dist(_s[-1], 2) == _d:
        _c = inputter("Conch = ? (1-9) ")
    return _d, _c


if __name__ == '__main__':
    D = init()
    # S0 = (12, 1, 214, 160, 3, 3, 3, False, False, False, False, 19)
    S0 = (12, 1, 185, 190, 3, 3, 3, False, False, False, False, 12)
    L = Luvly(_s=S0, verbose=True)

    while True:
        s = L.get_status()
        if s[0] < 1 and s[1] < 1:
            break
        if s[1] < 1:
            print("No Adv. Rudder. Please use Rudder.")
            d, c = input_rolled(s)
            L.rolled(d, c)
        else:
            a = s2a(s)
            d = luvly_helper(a)
            print(f"Helper: {d}.")
            if d != 0:
                print("=" * 30)
                print("=" * 30)
                print("=" * 30)
                print("=" * 30)
                print(d)
            if d == 0:
                print("Please use Rudder.")
                d, c = input_rolled(s)
                L.rolled(d, c)
            elif dist(s[-1], 2) == d:
                c = inputter("Conch = ? (1-9) ")
                L.asigned(d, c)
            else:
                L.asigned(d)
    fin()
