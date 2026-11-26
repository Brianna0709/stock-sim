import json

path = '/root/.openclaw/workspace/stock-sim/data/portfolio.json'
with open(path) as f:
    data = json.load(f)

# 2026-10-14 US close
closes = {
    'NVDA': {'price': 221.51, 'chg': -3.07},
    'MSFT': {'price': 533.69, 'chg': -1.80},
    'QQQ':  {'price': 731.00, 'chg': -2.00},  # est: Nasdaq -1.88%, mega-cap tech led losses
}

mv_total = 0.0
for ticker, pos in data['positions'].items():
    c = closes[ticker]
    pos['cur_price'] = c['price']
    pos['today_chg_pct'] = c['chg']
    pos['market_value'] = round(pos['shares'] * c['price'], 2)
    pos['pnl'] = round(pos['market_value'] - pos['cost_basis'], 2)
    pos['pnl_pct'] = round(pos['pnl'] / pos['cost_basis'] * 100, 2)
    pos['unrealized_pnl'] = pos['pnl']
    pos['unrealized_pnl_pct'] = pos['pnl_pct']
    mv_total += pos['market_value']

acct = data['account']
mv_total = round(mv_total, 2)
prev_total = acct['total_value']
new_total = round(acct['cash'] + mv_total, 2)
daily_pnl = round(new_total - prev_total, 2)
total_pnl = round(new_total - 100000, 2)

note = ("收盘复盘：NVDA $221.51 (-3.07%) | MSFT $533.69 (-1.80%) | QQQ $731.00 (约-2.0%估算) | "
        "标普500 7718.94(-1.11%) 道指51621.48(-0.09%) 纳指26692.87(-1.88%) | "
        "9月CPI超预期(同比3.7%)推升美债收益率与加息押注，费半-4.3%六连跌创去年5月以来最长；"
        "CoreWeave -15%、甲骨文-9%，存储全线下挫；苹果逆势+0.5%市值破5万亿美元；防御板块(医药/油气/食品)领涨")

ret_pct = round(total_pnl / 100000 * 100, 2)
snap = {
    'date': '2026-10-14',
    'total_value': new_total,
    'cash': acct['cash'],
    'market_value': mv_total,
    'invested': mv_total,
    'daily_pnl': daily_pnl,
    'total_pnl': total_pnl,
    'total_pnl_pct': ret_pct,
    'return_pct': ret_pct,
    'note': note,
}
acct['snapshots'].append(snap)
if 'snapshots' in data and isinstance(data['snapshots'], list) and data['snapshots'] is not acct['snapshots']:
    data['snapshots'].append(dict(snap))

acct['total_value'] = new_total
acct['invested'] = mv_total
acct['market_value'] = mv_total
acct['total_unrealized_pnl'] = total_pnl
acct['total_pnl'] = total_pnl
acct['total_pnl_pct'] = ret_pct
acct['daily_pnl'] = daily_pnl
acct['last_update'] = '2026-10-14'
data['market_context'] = {
    'sp500': 7718.94, 'sp500_change_pct': -1.11,
    'nasdaq': 26692.87, 'nasdaq_change_pct': -1.88,
    'dow': 51621.48, 'dow_change_pct': -0.09,
}

with open(path, 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"total={new_total} mv={mv_total} daily={daily_pnl} cum={total_pnl} ({ret_pct}%)")
for t, p in data['positions'].items():
    print(t, p['cur_price'], p['market_value'], p['pnl_pct'], p['today_chg_pct'])
