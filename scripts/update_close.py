import json, collections

path = '/root/.openclaw/workspace/stock-sim/data/portfolio.json'
with open(path) as f:
    data = json.load(f, object_pairs_hook=collections.OrderedDict)

closes = {
    'NVDA': (156.15, -4.12),
    'MSFT': (518.01, -1.12),
    'QQQ':  (661.84, -2.65),
}

market_value = 0.0
for tkr, pos in data['positions'].items():
    price, chg = closes[tkr]
    pos['prev_price'] = pos['cur_price']
    pos['cur_price'] = price
    pos['market_value'] = round(pos['shares'] * price, 2)
    pos['pnl'] = round(pos['market_value'] - pos['cost_basis'], 2)
    pos['pnl_pct'] = round(pos['pnl'] / pos['cost_basis'] * 100, 2)
    pos['unrealized_pnl'] = pos['pnl']
    pos['unrealized_pnl_pct'] = pos['pnl_pct']
    pos['today_chg_pct'] = chg
    market_value += pos['market_value']

market_value = round(market_value, 2)
cash = data['account']['cash']
total_value = round(cash + market_value, 2)
prev_total = data['account']['total_value']
invested = market_value
total_pnl = round(total_value - 100000, 2)

acc = data['account']
acc['total_value'] = total_value
acc['invested'] = invested
acc['total_unrealized_pnl'] = round(total_pnl, 2)
acc['daily_pnl'] = round(total_value - prev_total, 2)
acc['last_update'] = '2026-11-16'
acc['total_pnl'] = total_pnl
acc['total_pnl_pct'] = round(total_pnl / 1000, 2) / 10
acc['return_pct'] = acc['total_pnl_pct']
acc['market_value'] = market_value
acc['market_context'] = {
    'sp500': 7416.59, 'sp500_change_pct': -1.92,
    'nasdaq': 24509.76, 'nasdaq_change_pct': -2.49,
    'dow': 51608.17, 'dow_change_pct': -1.41,
}

note = ("收盘复盘：道指51608.17(-1.41%) 标普500 7416.59(-1.92%) 纳指24509.76(-2.49%) | "
        "NVDA $156.15 (-4.12%) | MSFT $518.01 (-1.12%) | QQQ $661.84 (-2.65%) | "
        "财报前夕恐慌蔓延：黄仁勋辞职余波+财政部长贝森特公开喊话要求英伟达外聘CEO，七巨头全线下跌，"
        "芯片股重挫(美光-7.62%/英特尔-7.02%/台积电-6.34%/AMD-5.58%)，光通信崩跌(Lumentum-8.48%)，"
        "VIX飙升19.8%至23.13；明日盘后NVDA财报+周四Anthropic IPO成AI交易两大生死考验")

snap = collections.OrderedDict([
    ('date', '2026-11-16'),
    ('total_value', total_value),
    ('cash', cash),
    ('market_value', market_value),
    ('daily_pnl', acc['daily_pnl']),
    ('total_pnl', total_pnl),
    ('total_pnl_pct', acc['total_pnl_pct']),
    ('return_pct', acc['total_pnl_pct']),
    ('note', note),
])
acc['snapshots'].append(snap)
acc['snapshots'] = acc['snapshots'][-400:]
if 'snapshots' in data and data['snapshots'] is not acc['snapshots']:
    data['snapshots'].append(snap)
    data['snapshots'] = data['snapshots'][-400:]

with open(path, 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('total_value', total_value, 'mv', market_value, 'daily', acc['daily_pnl'], 'pnl_pct', acc['total_pnl_pct'])
