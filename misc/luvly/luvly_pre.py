import numpy as np

from luvly_constants import X, X_SHAPE, PRICE, CORAL_REWARDS, NK


def gain_coral(_c):
    _c0 = _c.astype(np.int16)
    _gc = np.zeros(len(_c))
    for _cr in CORAL_REWARDS:
        for _i in CORAL_REWARDS[_cr]:
            _gc += PRICE[_i] * CORAL_REWARDS[_cr][_i] * (_c0 >= _cr)
    _c0 -= 300
    for _cr in CORAL_REWARDS:
        for _i in CORAL_REWARDS[_cr]:
            _gc += PRICE[_i] * CORAL_REWARDS[_cr][_i] * (_c0 >= _cr)
    return _gc


def pearl_knapsack():
    v = [0] + [PRICE['usb_disk'] * 2000] * 2
    v += [PRICE['crystal_purple'] * 250] * 6
    v += [PRICE['juice'] * 2e6] * 10
    v += [PRICE['gold'] * 0.5e6] * 1

    v_dict = {}
    for i, j in enumerate(v):
        v_dict[i] = j
    del v_dict[0]
    v = v_dict

    w = [0] + [10] * 2 + [8] * 6 + [2] * 10 + [1] * 1

    w_dict = {}
    for i, j in enumerate(w):
        w_dict[i] = j
    del w_dict[0]
    w = w_dict

    assert len(v) == len(w)
    n = len(w)
    W = X_SHAPE[1] - 1

    m = np.zeros((n + 1, W + 1), dtype=int)
    for i in range(1, n + 1):
        for j in range(W + 1):
            if w[i] > j:
                m[i, j] = m[i - 1, j]
            else:
                m[i, j] = max(m[i - 1, j], m[i - 1, j - w[i]] + v[i])
    return v, w, m, n


PEARL_KNAPSACK = pearl_knapsack()


def knapsack(i, j):
    _, w, m, _ = PEARL_KNAPSACK
    if i == 0:
        return set()
    if m[i, j] > m[i - 1, j]:
        return set({i}).union(knapsack(i - 1, j - w[i]))
    return knapsack(i - 1, j)


def get_gain_pearl():
    v, _, _, n = PEARL_KNAPSACK

    def get_gain(_set):
        _g = 0
        for _i in _set:
            _g += v[_i]
        return _g

    _gp = np.zeros(X_SHAPE[1])
    for _p in range(X_SHAPE[1]):
        _gp[_p] = get_gain(knapsack(n, _p))

    return _gp


GP = get_gain_pearl()


def gain(_c, _p):
    return gain_coral(_c) + GP[_p]


G0 = gain(X[:, 0], X[:, 1])
G_0_0 = np.zeros((NK, len(X)))
for ti in range(NK):
    G_0_0[ti] = G0


def save(_A, _name):
    with open(f'{_name}.npy', 'wb') as _f:
        np.save(_f, np.array(_A))


def load(_name):
    with open(f'{_name}.npy', 'rb') as _f:
        return np.load(_f)
