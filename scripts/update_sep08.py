import json

# Read portfolio
with open('/mnt/openclaw/.openclaw/workspace/stock-sim/data/portfolio.json', 'r') as f:
    data = json.load(f)

# Sep 8, 2026 closing prices
prices = {
    'QQQ': 718.36,
    'NVDA': 225.73,
    'MSFT': 493.95
}

# Today's changes vs previous close
prev_prices = {
    'QQQ': 719.03,
    'NVDA': 230.36,
    'MSFT': 499.70
}

today_chg = {
    'QQQ': round((718.36 - 719.03) / 719.03 * 100, 2),
    'NVDA': round((225.73 - 230.36) / 230.36 * 100, 2),
    'MSFT': round((493.95 - 499.70) / 499.70 * 100, 2)
}

# Update positions
for sym in ['QQQ', 'NVDA', 'MSFT']:
    pos = data['positions'][sym]
    pos['cur_price'] = prices[sym]
    pos['today_chg_pct'] = today_chg[sym]
    pos['market_value'] = round(pos['shares'] * prices[sym], 2)
    pos['unrealized_pnl'] = round(pos['market_value'] - pos['cost_basis'], 2)
    pos['unrealized_pnl_pct'] = round(pos['unrealized_pnl'] / pos['cost_basis'] * 100, 2)
    pos['pnl'] = pos['unrealized_pnl']
    pos['pnl_pct'] = pos['unrealized_pnl_pct']

# Update account
mv = sum(data['positions'][s]['market_value'] for s in ['QQQ', 'NVDA', 'MSFT'])
data['account']['market_value'] = round(mv, 2)
data['account']['invested'] = round(mv, 2)
prev_total = data['account']['total_value']
data['account']['total_value'] = round(mv + data['account']['cash'], 2)
data['account']['daily_pnl'] = round(data['account']['total_value'] - prev_total, 2)
data['account']['total_unrealized_pnl'] = round(data['account']['total_value'] - 100000, 2)
data['account']['last_update'] = '2026-09-08'

# Update market context
data['market_context'] = {
    'sp500': 7673.52,
    'sp500_change_pct': -0.58,
    'nasdaq': 26421.41,
    'nasdaq_change_pct': -0.32,
    'dow': 52786.07,
    'dow_change_pct': -1.18
}

# Add snapshot
snapshot = {
    'date': '2026-09-08',
    'total_value': data['account']['total_value'],
    'cash': data['account']['cash'],
    'market_value': data['account']['market_value'],
    'daily_pnl': data['account']['daily_pnl'],
    'total_pnl': data['account']['total_unrealized_pnl'],
    'total_pnl_pct': round(data['account']['total_unrealized_pnl'] / 100000 * 100, 2),
    'note': f"收盘复盘：NVDA ${prices['NVDA']} ({today_chg['NVDA']:+.2f}%) | MSFT ${prices['MSFT']} ({today_chg['MSFT']:+.2f}%) | QQQ ${prices['QQQ']} ({today_chg['QQQ']:+.2f}%) | 标普500 7673.52(-0.58%) 道指52786.07(-1.18%) 纳指26421.41(-0.32%) | 美伊冲突升级油价飙涨，科技股全线承压，道指暴跌超600点",
    'return_pct': round(data['account']['total_unrealized_pnl'] / 100000 * 100, 2)
}
data['account']['snapshots'].append(snapshot)

# Also add to top-level snapshots
data['snapshots'].append({
    'date': '2026-09-08',
    'total_value': data['account']['total_value'],
    'cash': data['account']['cash'],
    'invested': data['account']['invested'],
    'return_pct': round(data['account']['total_unrealized_pnl'] / 100000 * 100, 2),
    'note': snapshot['note']
})

# Write back
with open('/mnt/openclaw/.openclaw/workspace/stock-sim/data/portfolio.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("✅ portfolio.json updated")
print(f"   Total Value: ${data['account']['total_value']:,.2f}")
print(f"   Daily PnL: ${data['account']['daily_pnl']:,.2f}")
print(f"   Total PnL: ${data['account']['total_unrealized_pnl']:,.2f} ({snapshot['return_pct']:.2f}%)")
for sym in ['QQQ', 'NVDA', 'MSFT']:
    p = data['positions'][sym]
    print(f"   {sym}: ${p['cur_price']:.2f} ({p['today_chg_pct']:+.2f}%) | MV: ${p['market_value']:,.2f} | PnL: ${p['unrealized_pnl']:,.2f} ({p['unrealized_pnl_pct']:+.2f}%)")
