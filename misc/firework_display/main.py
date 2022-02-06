from itertools import combinations
from pathlib import Path

import dill
import numpy as np


def save_all(_A,
             _name: str or Path,
             *args,
             _mode="wb",
             _ext=None,
             saver=None,
             **kwargs):
    _name = Path(_name)
    if _ext is not None:
        _name = _name.with_suffix(_ext)

    with open(_name, _mode) as _f:
        saver(_A, _f, *args, **kwargs)


def load_all(_name: str or Path,
             *args,
             _mode="rb",
             _ext=None,
             loader=None,
             **kwargs):
    _name = Path(_name)
    if _ext is not None:
        _name = _name.with_suffix(_ext)

    with open(_name, _mode) as _f:
        return loader(_f, *args, **kwargs)


def psave(_A, _name):
    save_all(_A, _name, _ext=".p", saver=dill.dump)


def pload(_name):
    return load_all(_name, _ext=".p", loader=dill.load)


def get_spark_targets(s: int):
    sr = s // 3
    sc = s % 3
    return set([3 * sr, 3 * sr + 1, 3 * sr + 2, sc, sc + 3, sc + 6])


SPARKS = {s: get_spark_targets(s) for s in range(9)}
P = {s: {i: 3**(s - i) / 4**s for i in range(s + 1)} for s in range(1, 9)}
C = {
    s: {i: list(combinations(range(s), i))
        for i in range(s + 1)}
    for s in range(1, 9)
}


def tuple_assign(t: tuple, i: int, v: int):
    l = list(t)
    l[i] = v
    return tuple(l)


def combine(res: dict, partial_res: dict):
    for h in partial_res:
        if h in res:
            res[h] += partial_res[h]
        else:
            res[h] = partial_res[h]


def execute(a: tuple, sparks: list, factor=1):
    res = {}
    sparks1 = []
    optionals = []
    targets = set()
    for d in sparks:
        targets = targets.union(SPARKS[d])
    for i in targets:
        if a[i] == 0:
            optionals.append(i)
        if a[i] == 1:
            a = tuple_assign(a, i, 2)
            sparks1.append(i)

    s = len(optionals)
    if s > 0:
        for i in range(s + 1):
            p = P[s][i]
            c = C[s][i]
            for inds in c:
                a1 = a
                for ind in inds:
                    a1 = tuple_assign(a1, optionals[ind], 1)
                combine(res, {a1: factor * p})
    else:
        combine(res, {a: factor})
    return res, sparks1


def execute_all(current: dict, sparks: list):
    if not sparks:
        return current

    res = {}
    for t in current:
        current_new, sparks_new = execute(t, sparks, factor=current[t])
        combine(res, execute_all(current_new, sparks_new))
    return res


class State:

    def __init__(self, a: tuple):
        self.a = a
        self.before = {d: {} for d in range(9)}
        self.after = {d: {} for d in range(9)}
        self.cost = None
        self.cost_d = {d: None for d in range(9)}

    def add_before(self, before: tuple, d: int, p: float):
        self.before[d][before] = p

    def add_after(self, after: tuple, d: int, p: float):
        self.after[d][after] = p


class AllFireworkStates:

    def __init__(self):
        self.states = {}
        self.end = (2, 2, 2, 2, 2, 2, 2, 2, 2)
        self.added = set([self.end])
        self.get_state_by_tuple(self.end).cost = 0

    def add(self, before: State, after: State, d: int, p: float):
        self.states[before.a] = before
        self.states[after.a] = after
        before.add_after(after.a, d, p)
        after.add_before(before.a, d, p)

    def get_state_by_tuple(self, a: tuple):
        if a not in self.states:
            self.states[a] = State(a)
        return self.states[a]

    def add_next_of(self, before: State):
        for d in range(9):
            if before.a[d] == 2:
                continue

            current, sparks = execute(tuple_assign(before.a, d, 2), [d])
            for t, p in execute_all(current, sparks).items():
                self.add(before, self.get_state_by_tuple(t), d, p)

    def add_all(self, start: tuple):
        if start in self.added:
            return

        s0 = self.get_state_by_tuple(start)
        self.add_next_of(s0)
        self.added.add(start)

        ts = set()
        for d in range(9):
            ts = ts.union(set(list(s0.after[d])))

        for t in ts:
            self.add_all(t)

    def get_cost_of_tuple(self, t: tuple):
        assert t in self.added
        s = self.get_state_by_tuple(t)

        if s.cost is not None:
            return s.cost
        s.cost = np.min([self.get_cost_d_of_tuple(t, d) for d in range(9)])
        return s.cost

    def get_cost_d_of_tuple(self, t: tuple, d: int):
        assert t in self.added
        s = self.get_state_by_tuple(t)

        if s.cost_d[d] is not None:
            return s.cost_d[d]

        if len(s.after[d]) < 1:
            s.cost_d[d] = np.inf
            return s.cost_d[d]

        cost_d = 0
        for t1 in s.after[d]:
            cost_d += s.after[d][t1] * (1 + self.get_cost_of_tuple(t1))
        s.cost_d[d] = cost_d
        return s.cost_d[d]


if __name__ == '__main__':
    S0 = (0, 0, 0, 0, 0, 0, 0, 0, 0)

    # FW = AllFireworkStates()
    # FW.add_all(S0)
    # print(len(FW.added))
    # print(FW.get_cost_of_tuple(S0))
    # psave(FW, "FW")

    FW = pload("FW")
    print(FW.get_cost_of_tuple(S0))
    # print(FW.get_state_by_tuple(tuple_assign(S0, 0, 2)).cost_d)
