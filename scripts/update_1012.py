import json

path = '/root/.openclaw/workspace/stock-sim/data/portfolio.json'
with open(path) as f:
    data = json.load(f)

# Oct 12, 2026 US close
closes = {
    'NVDA': {'price': 226.32, 'chg': -1.29},
    'MSFT': {'price': 541.15, 'chg': 1.14},
    'QQQ':  {'price': 749.88, 'chg': -0.35},
}
prev_total = data['account']['total_value']

mv_total = 0
for tkr, pos in data['positions'].items():
    c = closes[tkr]
    pos['cur_price'] = c['price']
    pos['today_chg_pct'] = c['chg']
    pos['market_value'] = round(pos['shares'] * c['price'], 2)
    pos['pnl'] = round(pos['market_value'] - pos['cost_basis'], 2)
    pos['pnl_pct'] = round(pos['pnl'] / pos['cost_basis'] * 100, 2)
    pos['unrealized_pnl'] = pos['pnl']
    pos['unrealized_pnl_pct'] = pos['pnl_pct']
    mv_total += pos['market_value']

mv_total = round(mv_total, 2)
cash = data['account']['cash']
total = round(cash + mv_total, 2)
daily_pnl = round(total - prev_total, 2)
total_pnl = round(total - data['meta']['initial_capital'], 2)
total_pnl_pct = round(total_pnl / data['meta']['initial_capital'] * 100, 2)

note = ("收盘复盘：NVDA $226.32 (-1.29%) | MSFT $541.15 (+1.14%) | QQQ $749.88 (约-0.35%估算) | "
        "标普500 7807.24(-0.06%) 道指51850.55(+0.38% 涨195点) 纳指27245.90(-0.44%) | "
        "三大指数涨跌不一，标普纳指自纪录高位回落；费半-2.67%，存储光通信重挫(Lumentum-9.8%、Coherent-7.9%、闪迪-6%、美光-3.9%)；"
        "Meta+3.38%领涨七姐妹，苹果+1.29%微软+1.14%；油气/必需消费领涨，油价连涨(WTI+1.43%报93.16布油105.93)，"
        "俄美启动柴油供应谈判；资金避险轮动明显")

snap = {
    'date': '2026-10-12',
    'total_value': total,
    'cash': cash,
    'market_value': mv_total,
    'invested': mv_total,
    'daily_pnl': daily_pnl,
    'total_pnl': total_pnl,
    'total_pnl_pct': total_pnl_pct,
    'return_pct': total_pnl_pct,
    'note': note,
}
data['account']['snapshots'].append(snap)
data['snapshots'].append(snap)

acct = data['account']
acct.update({
    'cash': cash,
    'total_value': total,
    'invested': mv_total,
    'total_unrealized_pnl': round(total_pnl, 2),
    'daily_pnl': daily_pnl,
    'last_update': '2026-10-12',
    'market_value': mv_total,
    'total_pnl': total_pnl,
    'total_pnl_pct': total_pnl_pct,
})
data['market_context'] = {
    'sp500': 7807.24, 'sp500_change_pct': -0.06,
    'nasdaq': 27245.90, 'nasdaq_change_pct': -0.44,
    'dow': 51850.55, 'dow_change_pct': 0.38,
}

with open(path, 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

for t, p in data['positions'].items():
    print(t, p['market_value'], str(p['pnl_pct']) + '%')
print('TOTAL=%s daily=%s cum=%s (%s%%)' % (total, daily_pnl, total_pnl, total_pnl_pct))
