#!/usr/bin/env python3
import json

path = '/root/.openclaw/workspace/stock-sim/data/portfolio.json'
with open(path) as f:
    data = json.load(f)

closes = {
    'QQQ': (747.65, -1.33),
    'NVDA': (230.48, -2.94),
    'MSFT': (522.61, -1.35),
}

for tkr, (px, chg) in closes.items():
    p = data['positions'][tkr]
    p['cur_price'] = px
    p['today_chg_pct'] = chg
    p['market_value'] = round(p['shares'] * px, 2)
    p['pnl'] = round(p['market_value'] - p['cost_basis'], 2)
    p['pnl_pct'] = round(p['pnl'] / p['cost_basis'] * 100, 2)
    p['unrealized_pnl'] = p['pnl']
    p['unrealized_pnl_pct'] = p['pnl_pct']

acc = data['account']
prev_total = acc['total_value']
mv = round(sum(p['market_value'] for p in data['positions'].values()), 2)
total = round(acc['cash'] + mv, 2)
acc['market_value'] = mv
acc['invested'] = mv
acc['total_value'] = total
acc['total_unrealized_pnl'] = round(total - acc['cash'] - data['meta']['initial_capital'], 2)
acc['daily_pnl'] = round(total - prev_total, 2)
acc['last_update'] = '2026-10-08'
acc['total_pnl'] = round(total - data['meta']['initial_capital'], 2)
acc['total_pnl_pct'] = round(acc['total_pnl'] / data['meta']['initial_capital'] * 100, 2)

note = ("收盘复盘：NVDA $230.48 (-2.94%) | MSFT $522.61 (-1.35%) | QQQ $747.65 (-1.33%) | "
        "标普500 7765.36(-0.47%) 道指51231.64(+0.10%) 纳指27193.34(-1.25%) | "
        "OpenAI年化收入被曝低于预期200亿美元引发AI支出担忧，芯片股重挫(费半-3.39%)；油价大涨(WTI+3.29%报91.18、布油重上104)推升通胀忧虑；"
        "资金避险轮动：能源+2.9%/必需消费+2.1%领涨，科技-1.8%领跌；10年期美债收益率从5.365%高点回落至5.231%")

snap = {
    'date': '2026-10-08',
    'total_value': total,
    'cash': acc['cash'],
    'market_value': mv,
    'invested': mv,
    'daily_pnl': acc['daily_pnl'],
    'total_pnl': acc['total_pnl'],
    'total_pnl_pct': acc['total_pnl_pct'],
    'return_pct': acc['total_pnl_pct'],
    'note': note,
}
acc['snapshots'].append(snap)
data['snapshots'].append(snap)

data['market_context'] = {
    'sp500': 7765.36,
    'sp500_change_pct': -0.47,
    'nasdaq': 27193.34,
    'nasdaq_change_pct': -1.25,
    'dow': 51231.64,
    'dow_change_pct': 0.10,
}

with open(path, 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('total_value:', total, '| daily_pnl:', acc['daily_pnl'], '| total_pnl:', acc['total_pnl'], "({}%)".format(acc['total_pnl_pct']))
for t in closes:
    p = data['positions'][t]
    print(t, p['cur_price'], p['market_value'], p['pnl_pct'])
