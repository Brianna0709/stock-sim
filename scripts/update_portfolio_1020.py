import json

path = 'data/portfolio.json'
with open(path) as f:
    data = json.load(f)

# 2026-10-20 (美东周二) 收盘价
prices = {'NVDA': 216.47, 'MSFT': 531.87, 'QQQ': 717.63}
chg = {'NVDA': -0.29, 'MSFT': -0.31, 'QQQ': -0.10}

prev_total = data['account']['total_value']

for t, p in prices.items():
    pos = data['positions'][t]
    pos['cur_price'] = p
    pos['market_value'] = round(pos['shares'] * p, 2)
    pos['pnl'] = round(pos['market_value'] - pos['cost_basis'], 2)
    pos['pnl_pct'] = round(pos['pnl'] / pos['cost_basis'] * 100, 2)
    pos['today_chg_pct'] = chg[t]
    pos['unrealized_pnl'] = pos['pnl']
    pos['unrealized_pnl_pct'] = pos['pnl_pct']

market_value = sum(pos['market_value'] for pos in data['positions'].values())
total_value = round(data['account']['cash'] + market_value, 2)
daily_pnl = round(total_value - prev_total, 2)
total_pnl = round(total_value - 100000, 2)
total_pnl_pct = round(total_pnl / 100000 * 100, 2)

data['account']['total_value'] = total_value
data['account']['invested'] = market_value
data['account']['market_value'] = market_value
data['account']['total_unrealized_pnl'] = total_pnl
data['account']['daily_pnl'] = daily_pnl
data['account']['total_pnl'] = total_pnl
data['account']['total_pnl_pct'] = total_pnl_pct
data['account']['last_update'] = '2026-10-20'
data['account']['return_pct'] = total_pnl_pct

note = ("收盘复盘：NVDA $216.47 (-0.29%) | MSFT $531.87 (-0.31%) | QQQ $717.63 (-0.10%) | "
        "标普500 7712.57(+0.29%) 道指52495.88(+1.02% 涨529点创历史新高) 纳指26424.82(-0.02%) | "
        "财报季轮动：3M+5%、诺格+4%领涨道指创新高；油价回落(WTI -1.8%报101.79)；科技巨头观望财报按兵不动，"
        "盘后道指期货+1.26%、纳指100期货+0.58%；苹果/谷歌/Meta跌超1%，特斯拉+1.54%")

snap = {
    "date": "2026-10-20",
    "total_value": total_value,
    "cash": data['account']['cash'],
    "market_value": market_value,
    "invested": market_value,
    "daily_pnl": daily_pnl,
    "total_pnl": total_pnl,
    "total_pnl_pct": total_pnl_pct,
    "return_pct": total_pnl_pct,
    "note": note
}
data['account']['snapshots'].append(snap)
data['snapshots'].append(snap)

data['market_context'] = {
    "sp500": 7712.57, "sp500_change_pct": 0.29,
    "nasdaq": 26424.82, "nasdaq_change_pct": -0.02,
    "dow": 52495.88, "dow_change_pct": 1.02
}

with open(path, 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"总资产: ${total_value:,.2f} | 日盈亏: ${daily_pnl:,.2f} | 累计: ${total_pnl:,.2f} (+{total_pnl_pct}%)")
for t, pos in data['positions'].items():
    print(f"{t}: ${pos['cur_price']} | 市值 ${pos['market_value']:,.2f} | 盈亏 {pos['pnl_pct']}%")
