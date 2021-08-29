import os
from time import time

import tables
import numpy as np

from luvly_constants import TRANS, NEXT, X, II, index_X, EXIT
from luvly_constants import MULTIPLICATOR, NK, NX, N_OPTIONS, K_ADV, K_RUDDER
from luvly_pre import G_0_0, load, save

OUTPUT = 'D.h5'
if os.path.exists(OUTPUT):
    EXIT(0)

N_MAX = 108
D_SHAPE = (N_MAX + 1, 4, NK, NX)
T = tables.open_file(OUTPUT, 'w')
D = T.create_carray(
    '/',
    'D',
    atom=tables.UInt8Atom(),
    shape=D_SHAPE,
    filters=tables.Filters(complib='blosc:zstd', complevel=7),
)


def train(_N):
    # pylint: disable=too-many-statements
    if _N == 0:
        return

    def init(_n):
        # (0,3), (1,2), (2,1), (3,0)
        if _n == 1:
            _G0 = [G_0_0]
        else:
            _G0 = [load(f'G_{_n-_j-1}_{_j}') for _j in [3, 2, 1, 0] if _j < _n]
        _shape = (NK, NX)
        _G1 = [
            -np.ones(_shape), -np.ones(_shape), -np.ones(_shape),
            -np.ones(_shape)
        ]
        _D1 = [
            -np.ones(_shape), -np.ones(_shape), -np.ones(_shape),
            -np.ones(_shape)
        ]

        _u_current = np.array(
            [
                [1, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0],
                [0, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 1, 0],
                [2 * _n, 0, 0, 0, 0, 1],
            ],
            dtype=np.uint8,
        )
        _CURRENT_INDEX = index_X(np.matmul(X, _u_current))
        return _G0, _G1, _D1, G_0_0[0][_CURRENT_INDEX]

    G0, G1, D1, CURRENT_GAIN = init(_N)

    def get_gain(_i, _j, _k, _tr):
        _sum = _i + _j

        if _sum == _N - 1:
            if _j == 3:
                assert _k == K_ADV
            return G0[-1 - _j][_k][II[_tr]]

        if _sum == _N:
            assert _k in [K_ADV, K_RUDDER]
            _G = G1[-1 - _j][_k][II[_tr]]
            assert np.all(_G >= 0), f'{_i}, {_j}, {_k}, {_tr}, {_G}'
            return _G

        raise TypeError(f"{(_i, _j, _k, _tr)}: not computed.")

    def gain_0(_i, _j, _k):
        # print(_i, _j, _k)
        _G = np.zeros(NX)

        for _d, _nd in NEXT[_k].items():
            for _next, _p in _nd.items():
                _i1 = _next[0] + _i - 1
                _j1 = _next[1] + _j
                _k1 = _next[2]
                _tr = TRANS[_k][_k1]
                _G += _p * get_gain(_i1, _j1, _k1, _tr)

        return _G / MULTIPLICATOR

    def fill_0(_i, _j, _k):
        # print(_i, _j, _k)
        _G = np.zeros((NX, 2))
        _G[:, 0] = gain_0(_i, _j, _k)
        _G[:, 1] = CURRENT_GAIN

        _D = np.argmax(_G, axis=1)
        _D1 = np.expand_dims(_D, axis=1)
        return 7 * _D, np.take_along_axis(_G, _D1, axis=1).flatten()

    def fill_1(_i, _j, _k):
        # print(_i, _j, _k)
        _G = np.zeros((NX, N_OPTIONS))

        if _i > 0 and _j < 3:
            _G[:, 0] = gain_0(_i, _j, _k)

        for _d, _nd in NEXT[_k].items():
            _mp = 0
            for _next, _p in _nd.items():
                _i1 = _next[0] + _i
                _j1 = _next[1] + _j - 1
                _k1 = _next[2]
                _tr = TRANS[_k][_k1]
                _G[:, _d] += _p * get_gain(_i1, _j1, _k1, _tr)
                _mp += _p
            _G[:, _d] /= _mp
        _G[:, 7] = CURRENT_GAIN

        _D = np.argmax(_G, axis=1)
        _D1 = np.expand_dims(_D, axis=1)
        return _D, np.take_along_axis(_G, _D1, axis=1).flatten()

    def fill(_i, _j, _k):
        print(_i, _j, _k)

        if _i > 0 and _j == 0:
            _fill = fill_0
        elif _i >= 0 and _j > 0:
            _fill = fill_1
        else:
            return -np.ones(NX), -np.ones(NX)

        _t0 = time()
        _gain = _fill(_i, _j, _k)
        print(time() - _t0)

        return _gain

    def fin(_n):
        if _n == 1:
            return
        for _j in [3, 2, 1, 0]:
            if _j < _n:
                os.remove(f'G_{_n-_j-1}_{_j}.npy')
                # os.rename(f'G_{_n-_j-1}_{_j}.npy', f'fin_G/G_{_n-_j-1}_{_j}.npy')

    D1[-1][K_RUDDER], G1[-1][K_RUDDER] = fill(_N, 0, K_RUDDER)
    D1[-2][K_RUDDER], G1[-2][K_RUDDER] = fill(_N - 1, 1, K_RUDDER)
    D1[-3][K_RUDDER], G1[-3][K_RUDDER] = fill(_N - 2, 2, K_RUDDER)

    D1[-2][K_ADV], G1[-2][K_ADV] = fill(_N - 1, 1, K_ADV)
    D1[-3][K_ADV], G1[-3][K_ADV] = fill(_N - 2, 2, K_ADV)
    D1[-4][K_ADV], G1[-4][K_ADV] = fill(_N - 3, 3, K_ADV)

    if _N - 3 >= 0:
        assert np.all(G1[0][K_ADV] >= 0)
        save(G1[0], f'G_{_N - 3}_3')

        assert np.all(D1[0][K_ADV] >= 0)
        D[_N - 3, 3, :, :] = D1[0].astype(np.uint8)

    for _J in range(3):
        for _K in range(NK):
            if _J == 0 and _K in [K_RUDDER]:
                continue
            if _J in [1, 2] and _K in [K_ADV, K_RUDDER]:
                continue
            if _J > 0:
                D1[-1 - _J][_K], G1[-1 - _J][_K] = fill(_N - _J, _J, _K)
                continue
            D1[-1 - _J][_K], G1[-1 - _J][_K] = fill(_N - _J, _J, _K)

        if _N - _J >= 0:
            assert np.all(G1[-1 - _J] >= 0)
            save(G1[-1 - _J], f'G_{_N - _J}_{_J}')

            assert np.all(D1[-1 - _J] >= 0)
            D[_N - _J, _J, :, :] = D1[-1 - _J].astype(np.uint8)

    fin(_N)

    print("I'm fine.")


if __name__ == "__main__":
    for N in range(N_MAX + 1):
        train(N)
    T.close()
