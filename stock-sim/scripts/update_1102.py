import json

path = '/root/.openclaw/workspace/stock-sim/data/portfolio.json'
with open(path) as f:
    data = json.load(f)

# 11月2日收盘价（由前一收盘价×当日涨跌幅推算）
prices = {
    'NVDA': (206.61 * (1 - 0.0126), -1.26),
    'MSFT': (521.91 * (1 - 0.0283), -2.83),
    'QQQ':  (695.11 * (1 - 0.0107), -1.07),
}
for t, (p, chg) in prices.items():
    prices[t] = (round(p, 2), chg)

total_mv = 0.0
for ticker, pos in data['positions'].items():
    price, chg = prices[ticker]
    pos['prev_price'] = pos['cur_price']
    pos['cur_price'] = price
    pos['today_chg_pct'] = chg
    pos['market_value'] = round(pos['shares'] * price, 2)
    pos['pnl'] = round(pos['market_value'] - pos['cost_basis'], 2)
    pos['pnl_pct'] = round(pos['pnl'] / pos['cost_basis'] * 100, 2)
    pos['unrealized_pnl'] = pos['pnl']
    pos['unrealized_pnl_pct'] = pos['pnl_pct']
    total_mv += pos['market_value']

total_mv = round(total_mv, 2)
cash = data['account']['cash']
total_value = round(cash + total_mv, 2)
prev_total = data['account']['total_value']
daily_pnl = round(total_value - prev_total, 2)
total_pnl = round(total_value - data['meta']['initial_capital'], 2)
total_pnl_pct = round(total_pnl / 100000 * 100, 2)

note = ("收盘复盘：道指51983.98(+0.41%) 标普500 7541.40(-0.51%) 纳指25164.32(-1.07%) | "
        "NVDA $204.01 (-1.26%) | MSFT $507.15 (-2.83%) | QQQ $687.66 (约-1.07%估算) | "
        "费半-3.37%续跌，油价暴跌(WTI -7.36%报96.46)因美伊谈判现进展，道指独涨、资金离开AI芯片流向价值股，金龙指数+2.25%")

snap = {
    "date": "2026-11-02",
    "total_value": total_value,
    "cash": cash,
    "market_value": total_mv,
    "invested": total_mv,
    "daily_pnl": daily_pnl,
    "total_pnl": total_pnl,
    "total_pnl_pct": total_pnl_pct,
    "return_pct": total_pnl_pct,
    "note": note
}

acct = data['account']
acct['total_value'] = total_value
acct['market_value'] = total_mv
acct['invested'] = total_mv
acct['total_unrealized_pnl'] = round(total_pnl, 2)
acct['total_pnl'] = total_pnl
acct['total_pnl_pct'] = total_pnl_pct
acct['return_pct'] = total_pnl_pct
acct['daily_pnl'] = daily_pnl
acct['last_update'] = "2026-11-02"
acct['snapshots'].append(snap)
acct['market_context'] = {
    "sp500": 7541.40, "sp500_change_pct": -0.51,
    "nasdaq": 25164.32, "nasdaq_change_pct": -1.07,
    "dow": 51983.98, "dow_change_pct": 0.41
}

data['snapshots'].append(snap)
data['market_context'] = acct['market_context']

with open(path, 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("NVDA:", data['positions']['NVDA']['cur_price'], data['positions']['NVDA']['pnl_pct'])
print("MSFT:", data['positions']['MSFT']['cur_price'], data['positions']['MSFT']['pnl_pct'])
print("QQQ:", data['positions']['QQQ']['cur_price'], data['positions']['QQQ']['pnl_pct'])
print(f"total={total_value} daily={daily_pnl} total_pnl={total_pnl} ({total_pnl_pct}%)")
