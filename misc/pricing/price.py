import json
from scipy.special import comb, factorial

price = {}


def print_price(_price):
    for k in _price.keys():
        l = len(f'{k}')
        s = ' ' * (25 - l)
        kk = "{:.2e}".format(_price[k])
        if isinstance(_price[k], int) or _price[k].is_integer():
            kk = int(_price[k])
        print(f'  {k}:{s}\t{kk}')
    print()


def get_price_from_tuple(_name, _tuple: "(QUANTITY, PROBABILITY)}"):
    return _tuple[0] * _tuple[1] * price[_name]


def get_price(_item: "{'NAME': (QUANTITY, PROBABILITY)}"):
    _price = 0
    for _i in _item:
        assert _i in price
        if isinstance(_item[_i], tuple):
            _price += get_price_from_tuple(_i, _item[_i])
        elif isinstance(_item[_i], list):
            for _ti in _item[_i]:
                assert isinstance(_ti, tuple)
                _price += get_price_from_tuple(_i, _ti)
    return _price


def equal_price(_quantity_self, _name_dist, _quantity_dist):
    assert _name_dist in price
    return price[_name_dist] * _quantity_dist / _quantity_self


price['gem'] = 1
price['gold'] = equal_price(4e6, 'gem', 50)
price['juice'] = 1.5 * price['gold']
price['bento'] = equal_price(500, 'gold', 1e6)
price['chisel'] = 0.5 * price['bento']

price['custom_box_15k'] = 15e3 * price['bento']

price['cap_blue'] = equal_price(10, 'gold', 0.5e6)
price['cap_purple'] = 130
price['seal'] = 2.5 * price['cap_purple']
price['rune'] = price['cap_purple'] * 0.5

price['girlbox_n'] = 0.6 * 60 * price['rune']
price['girlbox_ad'] = 80 * price['rune']
price['antique_box_n'] = 0.5 * price['girlbox_n']
price['antique_shard_orange'] = 0.2 * price['antique_box_n'] / 50.
price['antique_shard_red'] = 0
price['lucky_crystal'] = price['antique_box_n'] / 80

price['shard_3'] = equal_price(20, 'gold', 0.5e6)
price['shard_4'] = 100 / 89
price['shard_5'] = (8 * 30 * price['shard_4'] + 4 * 20 * price['shard_3']) / 50

price['girlbox_useless'] = 50 * price['shard_5']
price['skin'] = 1000
price['skin_useless'] = 50

price['shard_4_ad'] = 2 * price['shard_4']
price['shard_5_ad'] = (8 * 30 * price['shard_4_ad'] +
                       4 * 20 * price['shard_3']) / 50
price['shard_5_elite'] = get_price({
    'girlbox_n': (1 / 50, 0.03),
    'shard_5': (1, 0.97),
})
price['shard_5_elite_ad'] = get_price({
    'girlbox_ad': (1 / 50, 0.1),
    'shard_5_ad': (1, 0.9),
})
price['lunar_badge'] = price['shard_5_elite'] / 120
price['solar_badge'] = price['shard_5_elite_ad'] / 240
# price['HE80_raid_n'] = 89 * price['shard_4'] + 87 * price['lunar_badge']
# price['HE80_raid_ad'] = 89 * price['shard_4'] + 87 * price['solar_badge']
price['elite_badge'] = 1.5 * price['shard_5_elite'] * 50

price['portfolio'] = price['girlbox_n'] / 15e3

price['doll_6_n'] = 6 * price['shard_5'] * 50 + 2550 * price['bento']
price['doll_6_ad'] = 6 * price['shard_5_ad'] * 50 + 2550 * price['bento']
price['doll_9'] = 28 * price['shard_5'] * 50 + 9050 * price['bento']
price['doll_10'] = 64 * price['shard_5'] * 50 + 26900 * price['bento']

price['gear_set_5'] = (2500 + 60e6 * price['gold']) / 2
price['gear_set_6'] = 3 * price['gear_set_5']
# price['gear_set_4_ti'] = (1500 + 40e6 * price['gold']) / 2
price['gear_set_4'] = price['gear_set_5'] / 3
price['gear_set_3'] = price['gear_set_4'] / 3
price['gear_set_2'] = price['gear_set_3'] / 3
price['gear_set_1'] = price['gear_set_2'] / 3

# price['class_gear_set_ti'] = price['gear_set_6'] + 4000 + 80e6 * price['gold']
price['class_gear_set'] = 150 * price['rune']
price['antique_p2w'] = 1.5 * price['class_gear_set']
price['elementium'] = (price['antique_p2w'] -
                       23.8 * price['cap_purple']) / (3600 - 2380)

price['ticket_yellow'] = 25
price['ticket_purple'] = get_price({
    'girlbox_n': (1, 0.006),
    'shard_4_ad': (30, 0.067),
    'cap_purple': (1, 0.165),
    'seal': (1, 0.085),
    'bento': (600, 0.224),
    'gold': (2.1e6, 0.4),
    'antique_shard_orange': (10, 0.011),
})
price['ticket_yellow_real'] = 10 / 8 * get_price({
    'shard_5': (50, 0.001),
    'shard_4': (30, 0.02),
    'gold': (375e3, 0.34),
    'gear_set_1': (1 / 4, 0.015),
    'juice': (100e3, 0.26),
    'bento': (60, 0.169),
}) + get_price({
    'seal': (11, 1),
    'ticket_purple': (14, 1),
    'rune': (5, 1),
    'shard_5': (50, 1),
    'shard_5_elite': (50, 1),
}) / 320

price['ticket_yellow'] = min(
    price['ticket_yellow'],
    price['ticket_yellow_real'],
)
del price['ticket_yellow_real']

price['ticket_league'] = equal_price(10, 'gold', 0.5e6)

# https://docs.google.com/spreadsheets/d/14LepRzkMoStHXfFlnGFAPcUH99zCoALY6m0qysrRlgA/edit#gid=95120154
price['intern_1'] = get_price({
    'gem': (4, 0.6),
    'cap_blue': (1, 0.4),
})
price['intern_2'] = get_price({
    'gem': (8, 0.4),
    'cap_blue': (2, 0.4),
    'shard_3': (7.5, 0.2),
})
price['intern_3'] = get_price({
    'gem': (22.5, 0.4),
    'cap_blue': (3, 0.2),
    'shard_3': (16, 0.2),
    'ticket_league': (1, 0.2),
})
price['intern_4'] = get_price({
    'gem': (50, 0.4),
    'cap_purple': (1, 0.1),
    'shard_4': (6, 0.2),
    'ticket_league': (2, 0.1),
    'ticket_yellow': (1, 0.1),
    'chisel': (175, 0.1),
})
price['intern_5'] = get_price({
    'gem': (90, 0.3),
    'cap_purple': (2, 0.05),
    'shard_4': (15, 0.2),
    'ticket_league': (3, 0.25),
    'ticket_yellow': (2, 0.05),
    'shard_5': (2, 0.05),
    'chisel': (350, 0.1),
})
price['intern_6'] = get_price({
    'gem': (150, 0.4),
    'seal': (1, 0.05),
    'shard_5': (4, 0.2),
    'portfolio': (40, 0.15),
    'shard_5_elite': (3, 0.1),
    'cap_purple': (3, 0.05),
})
price['intern_7'] = get_price({
    'gem': (315, 0.5),
    'seal': (2, 0.05),
    'shard_5': (15, 0.175),
    'portfolio': (90, 0.15),
    'shard_5_elite': (15, 0.075),
})
price['intern'] = get_price({
    'intern_1': (1, 0.256),
    'intern_2': (1, 0.27),
    'intern_3': (1, 0.232),
    'intern_4': (1, 0.15),
    'intern_5': (1, 0.08),
    'intern_6': (1, 0.01),
    'intern_7': (1, 0.002),
})
price['scroll_green'] = get_price({
    'intern_1': (1, 0.2),
    'intern_2': (1, 0.27),
    'intern_3': (1, 0.35),
    'intern_4': (1, 0.18),
})
price['scroll_purple'] = get_price({
    'intern_4': (1, 0.56),
    'intern_5': (1, 0.35),
    'intern_6': (1, 0.07),
    'intern_7': (1, 0.02),
})

price['crystal_purple'] = 10 * equal_price(50, 'chisel', 28 * 50)
price['cookie_yellow'] = equal_price(500, 'chisel', 15 * 50)
price['cookie_blue'] = equal_price(100, 'chisel', 24 * 50)

price['floppy_disk'] = 0
price['usb_disk'] = 0.75

price['bread'] = 2
price['wood'] = 0
price['crystal_blue'] = 1 / 10 * price['crystal_purple']

price['chest_1'] = get_price({
    'wood': (15, 1),
    'crystal_blue': (3, 1),
    'gold': (100e3, 0.2),
    'juice': (100e3, 0.2),
    'shard_3': (10, 0.16),
    'shard_4': (3, 0.16),
    'chisel': (80, 0.12),
    'bento': (80, 0.16),
})

price['chest_2'] = get_price({
    'wood': (30, 1),
    'crystal_blue': (6, 1),
    'cookie_yellow': (60, 0.11),
    'shard_4': (4, 0.17),
    'gold': (150e3, 0.2),
    'bento': (100, 0.17),
    'shard_3': (15, 0.17),
    'juice': (150e3, 0.18),
})

price['chest_3'] = get_price({
    'wood': (45, 1),
    'crystal_blue': (9, 1),
    'gold': (200e3, 0.12),
    'juice': (200e3, 0.12),
    'bento': (120, 0.1),
    'chisel': (120, 0.1),
    'cookie_blue': (10, 0.1),
    'cookie_yellow': (80, 0.08),
    'shard_4': (6, 0.15),
    'shard_5': (2, 0.1),
    'ticket_yellow': (1, 0.1),
    'gem': (30, 0.03),
})

price['chest_4'] = get_price({
    'wood': (60, 1),
    'crystal_blue': (12, 1),
    'shard_5_elite': (2 * 1, 0.02),
    'ticket_yellow': (2 * 2, 0.06),
    'gem': (2 * 40, 0.03),
    'shard_5': (2 * 4, 0.1),
    'antique_shard_red': (2 * 1, 0.08),
    'shard_4': (2 * 10, 0.15),
    'scroll_purple': (2 * 1, 0.03),
    'cookie_blue': (2 * 10, 0.06),
    'cookie_yellow': (2 * 70, 0.09),
    'chisel': (2 * 140, 0.09),
    'juice': (2 * 250e3, 0.1),
    'gold': (2 * 250e3, 0.1),
    'bento': (2 * 140, 0.09),
})

price['chest_5'] = get_price({
    'wood': (75, 1),
    'crystal_blue': (15, 1),
    'floppy_disk': (2 * 100, 0.08),
    'bento': (2 * 250, 0.08),
    'crystal_purple': (2 * 10, 0.05),
    'gold': (2 * 300e3, 0.05),
    'gem': (2 * 50, 0.05),
    'shard_5_elite': (2 * 2, 0.03),
    'scroll_purple': (2 * 2, 0.06),
    'cookie_blue': (2 * 25, 0.05),
    'ticket_purple': (2 * 1, 0.06),
    'usb_disk': (2 * 30, 0.05),
    'chisel': (2 * 250, 0.08),
    'cap_purple': (2 * 1, 0.06),
    'antique_shard_red': (2 * 2, 0.06),
    'juice': (2 * 300e3, 0.08),
    'shard_5': (2 * 5, 0.1),
    'ticket_yellow': (2 * 3, 0.06),
})

price['chest_6'] = get_price({
    'wood': (90, 1),
    'crystal_blue': (18, 1),
    'juice': (2 * 350e3, 0.08),
    'gold': (2 * 350e3, 0.05),
    'crystal_purple': (2 * 15, 0.05),
    'seal': (2 * 1, 0.03),
    'usb_disk': (2 * 40, 0.05),
    'gem': (2 * 80, 0.05),
    'antique_shard_orange': (2 * 1, 0.06),
    'scroll_purple': (2 * 2, 0.06),
    'ticket_yellow': (2 * 5, 0.06),
    'ticket_purple': (2 * 1, 0.06),
    'cap_purple': (2 * 2, 0.06),
    'shard_5_elite': (2 * 3, 0.03),
    'shard_5': (2 * 8, 0.07),
    'cookie_blue': (2 * 30, 0.05),
    'floppy_disk': (2 * 120, 0.08),
    'chisel': (2 * 300, 0.08),
    'bento': (2 * 300, 0.08),
})

price['new_chest'] = get_price({
    'bread': (-15, 1),
    'chest_4': (1, 0.3),
    'chest_5': (1, 0.45),
    'chest_6': (1, 0.25),
})

# 2 of the 5 girls in a ticket are in the same Faction: 4-Star Girl shards5
# 3 of the 5 girls in a ticket are in the same Faction: 4-Star Girl shards30
# 4 of the 5 girls in a ticket are in the same Faction: 5-Star Girl shards50
# all of the 5 girls in a ticket are from the same Faction: Elite Badge
# 5 different Factions: 10 pull ticket

# 3 stars distribution: [5, 5, 5, 5, 1, 1]
_p0 = 5 / 22
_p1 = 17 / 22
_p2 = 1 / 22
price['scratch_card'] = get_price({
    'shard_3': (5 * 20, 1),
    'shard_4': [
        (5, 4 * comb(5, 2) * _p0**2 * _p1**3),
        (30, 4 * comb(5, 3) * _p0**3 * _p1**2),
    ],
    'shard_5': (50, 4 * comb(5, 4) * _p0**4 * _p1),
    'elite_badge': (1, 4 * _p0**5),
    'cap_purple':
    (10, factorial(5) * (4 * _p0**3 * _p2**2 + 2 * _p0**4 * _p2)),
})

price['jigsaw'] = get_price({
    'shard_4': (10 * 8, 1),
    'shard_5': (2 * 8 + 74, 1),
    'gold': (200e3 * 24, 1),
    'ticket_yellow': (25, 1),
    'ticket_purple': (10, 1),
    'cap_purple': (15, 1),
    'seal': (5, 1),
}) / 168

print_price(price)

with open('price.json', 'w') as fp:
    fp.seek(0)
    json.dump(price, fp, indent=4)
    fp.truncate()
