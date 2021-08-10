import json
import numpy as np

with open('price.json', 'r') as f:
    PRICE = json.load(f)


def get_price(_item):
    _p = 0
    for k, v in _item.items():
        _p += PRICE[k] * v
    return _p


# $0
item_0 = {}
item_0['girlbox_ad'] = 1
item_0['antique_shard_orange'] = 50
# item_0['cap_purple'] = 30
# item_0['ticket_purple'] = 4
# item_0['girlbox_useless'] = 1
# item_0['shard_5_elite'] = 50
# item_0['skin_useless'] = 1
p0 = get_price(item_0)
print(p0)

# $10
item_1 = {}
item_1['cap_purple'] = 10
item_1['ticket_purple'] = 2
item_1['girlbox_ad'] = 1
item_1['antique_shard_orange'] = 50
item_1['seal'] = 4
item_1['gem'] = 888 * 2
item_1['juice'] = 10e6 * 2
# item_1['cap_purple'] = 30
# item_1['ticket_purple'] = 2
# item_1['shard_5_elite'] = 50
# item_1['skin_useless'] = 1
# item_1['seal'] = 5 + 4
# item_1['shard_5_ad'] = 50
# item_1['gem'] = 888 * 2
# item_1['juice'] = 10e6 * 2
p1 = get_price(item_1)
print(p1, (p1 - p0) / 10)

# $30
item_2 = {}
item_2['seal'] = 4 + 2
item_2['shard_5_ad'] = 50 * 2
item_2['gem'] = 888 * 4 + 275 * 2
item_2['ticket_purple'] = 2
item_2['juice'] = 10e6 * 2
item_2['gold'] = 10e6 * 2
item_2['class_gear_set'] = 1
item_2['rune'] = 25
p2 = get_price(item_2)
print(p2, (p2 - p0) / 30, (p2 - p1) / 20)
