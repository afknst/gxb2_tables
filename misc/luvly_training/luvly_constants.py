import json
import numpy as np

NEXT = {
    0: {
        1: {
            (0, 0, 1): 9
        },
        2: {
            (0, 0, 2): 4,
            (0, 0, 3): 2,
            (0, 0, 4): 1,
            (0, 0, 5): 1,
            (0, 0, 0): 1
        },
        3: {
            (0, 0, 6): 9
        },
        4: {
            (0, 0, 7): 9
        },
        5: {
            (0, 0, 8): 9
        },
        6: {
            (0, 0, 9): 9
        }
    },
    1: {
        1: {
            (0, 0, 2): 4,
            (0, 0, 3): 2,
            (0, 0, 4): 1,
            (0, 0, 5): 1,
            (0, 0, 0): 1
        },
        2: {
            (0, 0, 6): 9
        },
        3: {
            (0, 0, 7): 9
        },
        4: {
            (0, 0, 8): 9
        },
        5: {
            (0, 0, 9): 9
        },
        6: {
            (0, 0, 10): 9
        }
    },
    2: {
        1: {
            (0, 0, 6): 9
        },
        2: {
            (0, 0, 7): 9
        },
        3: {
            (0, 0, 8): 9
        },
        4: {
            (0, 0, 9): 9
        },
        5: {
            (0, 0, 10): 9
        },
        6: {
            (0, 0, 11): 9
        }
    },
    3: {
        1: {
            (0, 0, 7): 9
        },
        2: {
            (0, 0, 9): 9
        },
        3: {
            (0, 0, 11): 9
        },
        4: {
            (0, 0, 13): 9
        },
        5: {
            (0, 1, 15): 9
        },
        6: {
            (0, 0, 17): 9
        }
    },
    4: {
        1: {
            (0, 0, 6): 9
        },
        2: {
            (0, 0, 7): 9
        },
        3: {
            (0, 0, 8): 9
        },
        4: {
            (0, 0, 9): 9
        },
        5: {
            (0, 0, 10): 9
        },
        6: {
            (0, 0, 11): 9
        }
    },
    5: {
        1: {
            (0, 0, 1): 9
        },
        2: {
            (0, 0, 23): 9
        },
        3: {
            (0, 0, 22): 9
        },
        4: {
            (0, 0, 21): 9
        },
        5: {
            (0, 0, 20): 9
        },
        6: {
            (0, 0, 19): 9
        }
    },
    6: {
        1: {
            (0, 0, 7): 9
        },
        2: {
            (0, 0, 8): 9
        },
        3: {
            (0, 0, 9): 9
        },
        4: {
            (0, 0, 10): 9
        },
        5: {
            (0, 0, 11): 9
        },
        6: {
            (0, 0, 12): 9
        }
    },
    7: {
        1: {
            (0, 0, 8): 9
        },
        2: {
            (0, 0, 9): 9
        },
        3: {
            (0, 0, 10): 9
        },
        4: {
            (0, 0, 11): 9
        },
        5: {
            (0, 0, 12): 9
        },
        6: {
            (0, 0, 13): 9
        }
    },
    8: {
        1: {
            (0, 0, 9): 9
        },
        2: {
            (0, 0, 10): 9
        },
        3: {
            (0, 0, 11): 9
        },
        4: {
            (0, 0, 12): 9
        },
        5: {
            (0, 0, 13): 9
        },
        6: {
            (0, 0, 14): 9
        }
    },
    9: {
        1: {
            (0, 0, 10): 9
        },
        2: {
            (0, 0, 11): 9
        },
        3: {
            (0, 0, 12): 9
        },
        4: {
            (0, 0, 13): 9
        },
        5: {
            (0, 0, 14): 9
        },
        6: {
            (0, 1, 15): 9
        }
    },
    10: {
        2: {
            (0, 0, 11): 18
        },
        4: {
            (0, 0, 12): 18
        },
        6: {
            (0, 0, 13): 18
        }
    },
    11: {
        1: {
            (0, 0, 12): 9
        },
        2: {
            (0, 0, 13): 9
        },
        3: {
            (0, 0, 14): 9
        },
        4: {
            (0, 1, 15): 9
        },
        5: {
            (0, 0, 16): 9
        },
        6: {
            (0, 0, 17): 9
        }
    },
    12: {
        1: {
            (0, 0, 13): 9
        },
        2: {
            (0, 0, 14): 9
        },
        3: {
            (0, 1, 15): 9
        },
        4: {
            (0, 0, 16): 9
        },
        5: {
            (0, 0, 17): 9
        },
        6: {
            (0, 0, 18): 9
        }
    },
    13: {
        1: {
            (0, 0, 14): 9
        },
        2: {
            (0, 1, 15): 9
        },
        3: {
            (0, 0, 16): 9
        },
        4: {
            (0, 0, 17): 9
        },
        5: {
            (0, 0, 18): 9
        },
        6: {
            (0, 0, 19): 9
        }
    },
    14: {
        1: {
            (0, 1, 15): 9
        },
        2: {
            (0, 0, 16): 9
        },
        3: {
            (0, 0, 17): 9
        },
        4: {
            (0, 0, 18): 9
        },
        5: {
            (0, 0, 19): 9
        },
        6: {
            (1, 0, 20): 9
        }
    },
    15: {
        1: {
            (0, 0, 16): 9
        },
        2: {
            (0, 0, 17): 9
        },
        3: {
            (0, 0, 18): 9
        },
        4: {
            (0, 0, 19): 9
        },
        5: {
            (1, 0, 20): 9
        },
        6: {
            (0, 0, 21): 9
        }
    },
    16: {
        1: {
            (0, 0, 17): 9
        },
        2: {
            (0, 0, 18): 9
        },
        3: {
            (0, 0, 19): 9
        },
        4: {
            (1, 0, 20): 9
        },
        5: {
            (0, 0, 21): 9
        },
        6: {
            (0, 0, 22): 9
        }
    },
    17: {
        1: {
            (0, 0, 18): 9
        },
        2: {
            (0, 0, 19): 9
        },
        3: {
            (1, 0, 20): 9
        },
        4: {
            (0, 0, 21): 9
        },
        5: {
            (0, 0, 22): 9
        },
        6: {
            (0, 0, 23): 9
        }
    },
    18: {
        1: {
            (0, 0, 19): 9
        },
        2: {
            (1, 0, 20): 9
        },
        3: {
            (0, 0, 21): 9
        },
        4: {
            (0, 0, 22): 9
        },
        5: {
            (0, 0, 23): 9
        },
        6: {
            (0, 0, 1): 9
        }
    },
    19: {
        1: {
            (1, 0, 20): 9
        },
        2: {
            (0, 0, 21): 9
        },
        3: {
            (0, 0, 22): 9
        },
        4: {
            (0, 0, 23): 9
        },
        5: {
            (0, 0, 1): 9
        },
        6: {
            (0, 0, 2): 4,
            (0, 0, 3): 2,
            (0, 0, 4): 1,
            (0, 0, 5): 1,
            (0, 0, 0): 1
        }
    },
    20: {
        1: {
            (0, 0, 21): 9
        },
        2: {
            (0, 0, 22): 9
        },
        3: {
            (0, 0, 23): 9
        },
        4: {
            (0, 0, 1): 9
        },
        5: {
            (0, 0, 2): 4,
            (0, 0, 3): 2,
            (0, 0, 4): 1,
            (0, 0, 5): 1,
            (0, 0, 0): 1
        },
        6: {
            (0, 0, 6): 9
        }
    },
    21: {
        1: {
            (0, 0, 22): 9
        },
        2: {
            (0, 0, 23): 9
        },
        3: {
            (0, 0, 1): 9
        },
        4: {
            (0, 0, 2): 4,
            (0, 0, 3): 2,
            (0, 0, 4): 1,
            (0, 0, 5): 1,
            (0, 0, 0): 1
        },
        5: {
            (0, 0, 6): 9
        },
        6: {
            (0, 0, 7): 9
        }
    },
    22: {
        1: {
            (0, 0, 23): 9
        },
        2: {
            (0, 0, 1): 9
        },
        3: {
            (0, 0, 2): 4,
            (0, 0, 3): 2,
            (0, 0, 4): 1,
            (0, 0, 5): 1,
            (0, 0, 0): 1
        },
        4: {
            (0, 0, 6): 9
        },
        5: {
            (0, 0, 7): 9
        },
        6: {
            (0, 0, 8): 9
        }
    },
    23: {
        1: {
            (0, 0, 1): 9
        },
        2: {
            (0, 0, 2): 4,
            (0, 0, 3): 2,
            (0, 0, 4): 1,
            (0, 0, 5): 1,
            (0, 0, 0): 1
        },
        3: {
            (0, 0, 6): 9
        },
        4: {
            (0, 0, 7): 9
        },
        5: {
            (0, 0, 8): 9
        },
        6: {
            (0, 0, 9): 9
        }
    }
}

TRANS = {
    0: {
        0: 0,
        1: 1,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 11,
        7: 10,
        8: 10,
        9: 12
    },
    1: {
        0: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 11,
        7: 10,
        8: 10,
        9: 12,
        10: 10
    },
    2: {
        6: 11,
        7: 10,
        8: 10,
        9: 12,
        10: 10,
        11: 10
    },
    3: {
        7: 10,
        9: 12,
        11: 10,
        13: 14,
        15: 13,
        17: 13
    },
    4: {
        6: 16,
        7: 15,
        8: 15,
        9: 17,
        10: 15,
        11: 15
    },
    5: {
        1: 0,
        23: 0,
        22: 0,
        21: 0,
        20: 0,
        19: 0
    },
    6: {
        7: 0,
        8: 0,
        9: 2,
        10: 0,
        11: 0,
        12: 0
    },
    7: {
        8: 0,
        9: 2,
        10: 0,
        11: 0,
        12: 0,
        13: 7
    },
    8: {
        9: 2,
        10: 0,
        11: 0,
        12: 0,
        13: 7,
        14: 8
    },
    9: {
        10: 0,
        11: 0,
        12: 0,
        13: 7,
        14: 8,
        15: 6
    },
    10: {
        11: 0,
        12: 0,
        13: 7
    },
    11: {
        12: 0,
        13: 7,
        14: 8,
        15: 6,
        16: 6,
        17: 6
    },
    12: {
        13: 7,
        14: 8,
        15: 6,
        16: 6,
        17: 6,
        18: 9
    },
    13: {
        14: 1,
        15: 0,
        16: 0,
        17: 0,
        18: 4,
        19: 5
    },
    14: {
        15: 0,
        16: 0,
        17: 0,
        18: 4,
        19: 5,
        20: 3
    },
    15: {
        16: 0,
        17: 0,
        18: 4,
        19: 5,
        20: 3,
        21: 3
    },
    16: {
        17: 0,
        18: 4,
        19: 5,
        20: 3,
        21: 3,
        22: 3
    },
    17: {
        18: 4,
        19: 5,
        20: 3,
        21: 3,
        22: 3,
        23: 3
    },
    18: {
        19: 2,
        20: 0,
        21: 0,
        22: 0,
        23: 0,
        1: 1
    },
    19: {
        20: 0,
        21: 0,
        22: 0,
        23: 0,
        1: 1,
        0: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0
    },
    20: {
        21: 0,
        22: 0,
        23: 0,
        1: 1,
        0: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 11
    },
    21: {
        22: 0,
        23: 0,
        1: 1,
        0: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 11,
        7: 10
    },
    22: {
        23: 0,
        1: 1,
        0: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 11,
        7: 10,
        8: 10
    },
    23: {
        1: 1,
        0: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 11,
        7: 10,
        8: 10,
        9: 12
    }
}

UT = np.array(
    [
        [
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 1],
        ],
        [
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 0],
            [0, 2, 0, 0, 0, 1],
        ],
        [
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 0],
            [0, 3, 0, 0, 0, 1],
        ],
        [
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0],
            [1, 0, 0, 0, 1, 0],
            [3, 0, 0, 0, 0, 1],
        ],
        [
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0],
            [1, 0, 0, 0, 1, 0],
            [3, 0, 0, 0, 1, 1],
        ],
        [
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0],
            [1, 0, 0, 0, 1, 0],
            [3, 3, 0, 0, 0, 1],
        ],
        [
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [1, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 0],
            [3, 0, 0, 0, 0, 1],
        ],
        [
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [1, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 0],
            [3, 0, 0, 1, 0, 1],
        ],
        [
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [1, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 0],
            [3, 2, 0, 0, 0, 1],
        ],
        [
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [1, 0, 0, 1, 0, 0],
            [1, 0, 0, 0, 1, 0],
            [6, 0, 0, 0, 1, 1],
        ],
        [
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [1, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 0],
            [3, 0, 0, 0, 0, 1],
        ],
        [
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [1, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 0],
            [3, 0, 1, 0, 0, 1],
        ],
        [
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [1, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 0],
            [3, 3, 0, 0, 0, 1],
        ],
        [
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [1, 0, 1, 0, 0, 0],
            [1, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 0],
            [6, 0, 0, 0, 0, 1],
        ],
        [
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [1, 0, 1, 0, 0, 0],
            [1, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 0],
            [6, 0, 0, 1, 0, 1],
        ],
        [
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [2, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 0],
            [6, 0, 0, 0, 0, 1],
        ],
        [
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [2, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 0],
            [6, 0, 1, 0, 0, 1],
        ],
        [
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [2, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 0],
            [6, 3, 0, 0, 0, 1],
        ],
    ],
    dtype=np.uint8,
)

X_SHAPE = (400, 80, 3, 3, 3, 1)

X = np.array(
    [[c, p, cl0, cl1, cl2, 1] for c in range(X_SHAPE[0])
     for p in range(X_SHAPE[1]) for cl0 in range(X_SHAPE[2])
     for cl1 in range(X_SHAPE[3]) for cl2 in range(X_SHAPE[4])],
    dtype=np.uint16,
)

NX = len(X)

IND_MIN = X[-1]
IND_MUL = np.array([
    X_SHAPE[-2] * X_SHAPE[-3] * X_SHAPE[-4] * X_SHAPE[-5],
    X_SHAPE[-2] * X_SHAPE[-3] * X_SHAPE[-4],
    X_SHAPE[-2] * X_SHAPE[-3],
    X_SHAPE[-2],
    1,
    0,
])


def index_X(_X0):
    _X1 = np.minimum(_X0, IND_MIN)
    return np.matmul(_X1, IND_MUL)


def trans_X(_X0, _tr):
    _X1 = np.matmul(_X0, UT[_tr])
    return np.minimum(_X1, IND_MIN)


II = np.zeros((len(UT), NX), dtype=np.uint32)
for _i, _ui in enumerate(UT):
    II[_i] = index_X(np.matmul(X, _ui))

with open('../pricing/price.json', 'r') as f:
    PRICE = json.load(f)

CORAL_REWARDS = {
    40: {
        'scratch_card': 10,
    },
    80: {
        'cap_purple': 10,
    },
    110: {
        'shard_5_elite': 50,
    },
    140: {
        'custom_box_15k': 1,
    },
    170: {
        'doll_6_n': 1,
    },
    200: {
        'girlbox_n': 1,
    },
    230: {
        'skin': 1,
    },
    260: {
        'girlbox_ad': 1,
    },
    300: {
        'doll_9': 1,
    },
}

MULTIPLICATOR = 54
NK = len(NEXT)
N_OPTIONS = 8  # 0, 1-6, 7
K_ADV = 15
K_RUDDER = 20
