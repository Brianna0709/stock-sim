import json

path = '/root/.openclaw/workspace/stock-sim/data/portfolio.json'
with open(path) as f:
    data = json.load(f)

# 2026-10-01 美东收盘价（东方财富/财联社）
prices = {
    'NVDA': (230.86, 1.09),
    'MSFT': (512.76, -0.02),
    'QQQ':  (738.82, 0.04),
}

for tkr, (px, chg) in prices.items():
    p = data['positions'][tkr]
    p['cur_price'] = px
    p['market_value'] = round(p['shares'] * px, 2)
    p['unrealized_pnl'] = round(p['market_value'] - p['cost_basis'], 2)
    p['unrealized_pnl_pct'] = round(p['unrealized_pnl'] / p['cost_basis'] * 100, 2)
    p['pnl'] = p['unrealized_pnl']
    p['pnl_pct'] = p['unrealized_pnl_pct']
    p['today_chg_pct'] = chg

mv = round(sum(p['market_value'] for p in data['positions'].values()), 2)
inv = round(sum(p['cost_basis'] for p in data['positions'].values()), 2)
cash = data['account']['cash']
total = round(cash + mv, 2)
prev_total = data['account']['total_value']
daily = round(total - prev_total, 2)
pnl = round(total - data['meta']['initial_capital'], 2)
pnl_pct = round(pnl / 100000 * 100, 2)

acc = data['account']
acc.update({
    'total_value': total, 'invested': inv, 'market_value': mv,
    'total_unrealized_pnl': pnl, 'daily_pnl': daily,
    'total_pnl': pnl, 'total_pnl_pct': pnl_pct,
    'last_update': '2026-10-01',
})
acc['snapshots'].append({
    'date': '2026-10-01',
    'total_value': total, 'cash': cash, 'market_value': mv,
    'invested': inv, 'daily_pnl': daily, 'total_pnl': pnl,
    'total_pnl_pct': pnl_pct, 'return_pct': pnl_pct,
    'note': '收盘复盘：NVDA $230.86 (+1.09%) | MSFT $512.76 (-0.02%) | QQQ $738.82 (约+0.04%估算) | 标普500 7666.45(+0.19%) 道指50926.56(+0.04%) 纳指26871.60(+0.04%) | 10年期美债收益率盘中破5.34%创2002年4月来新高后回落，三大指数微涨；油价大涨(WTI+2.71%布油+4.37%，美国向中东增兵至多1万人+第三艘航母)；英伟达+1.09%创5月中旬以来收盘新高，光通信领涨(Coherent+10.9%)、存储走强(美光+3%)；苹果-0.81%、谷歌-1.7%，金龙指数-1.03%'
})
data['market_context'] = {
    'sp500': 7666.45, 'sp500_change_pct': 0.19,
    'nasdaq': 26871.60, 'nasdaq_change_pct': 0.04,
    'dow': 50926.56, 'dow_change_pct': 0.04,
}

with open(path, 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('MV:', mv, 'Total:', total, 'Daily:', daily, 'PnL:', pnl, f'{pnl_pct}%')
for t in data['positions']:
    p = data['positions'][t]
    print(t, p['cur_price'], p['market_value'], f"{p['unrealized_pnl_pct']}%")
