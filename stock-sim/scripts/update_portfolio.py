import json, datetime

# 读取现有portfolio
with open('/root/.openclaw/workspace/stock-sim/data/portfolio.json', 'r') as f:
    data = json.load(f)

# 8月13日收盘价
prices = {
    'QQQ': 721.80,
    'NVDA': 225.50,
    'MSFT': 502.50
}

# 前一日收盘价（portfolio中的cur_price）
prev_prices = {
    'QQQ': data['positions']['QQQ']['cur_price'],
    'NVDA': data['positions']['NVDA']['cur_price'],
    'MSFT': data['positions']['MSFT']['cur_price']
}

print("=== 前一日价格 ===")
for k, v in prev_prices.items():
    print(f"  {k}: ${v}")

print("\n=== 8月13日收盘价 ===")
for k, v in prices.items():
    chg = (v - prev_prices[k]) / prev_prices[k] * 100
    print(f"  {k}: ${v} ({'+' if chg>=0 else ''}{chg:.2f}%)")

# 更新每个持仓
total_market_value = 0
total_cost = 0
daily_pnl = 0

for symbol in ['QQQ', 'NVDA', 'MSFT']:
    pos = data['positions'][symbol]
    new_price = prices[symbol]
    old_price = prev_prices[symbol]
    
    shares = pos['shares']
    cost_price = pos['cost_price']
    
    market_value = round(shares * new_price, 2)
    cost_basis = round(shares * cost_price, 2)
    unrealized_pnl = round(market_value - cost_basis, 2)
    unrealized_pnl_pct = round((unrealized_pnl / cost_basis) * 100, 2)
    
    daily_change_pct = round((new_price - old_price) / old_price * 100, 2)
    daily_pnl_change = round(shares * (new_price - old_price), 2)
    
    pos['cur_price'] = new_price
    pos['market_value'] = market_value
    pos['unrealized_pnl'] = unrealized_pnl
    pos['unrealized_pnl_pct'] = unrealized_pnl_pct
    
    total_market_value += market_value
    total_cost += cost_basis
    daily_pnl += daily_pnl_change
    
    print(f"\n=== {symbol} ===")
    print(f"  持仓: {shares} 股")
    print(f"  成本: ${cost_price}")
    print(f"  收盘: ${new_price}")
    print(f"  市值: ${market_value}")
    print(f"  盈亏: ${unrealized_pnl} ({unrealized_pnl_pct}%)")
    print(f"  今日涨跌: {daily_change_pct}% (${daily_pnl_change})")

# 更新账户级数据
cash = data['account']['cash']
total_value = round(cash + total_market_value, 2)
initial_capital = 100000
total_pnl = round(total_value - initial_capital, 2)
total_pnl_pct = round((total_pnl / initial_capital) * 100, 2)

data['account']['total_value'] = total_value
data['account']['total_unrealized_pnl'] = round(total_market_value - total_cost, 2)
data['account']['daily_pnl'] = round(daily_pnl, 2)

# 更新快照日期
today_str = "2026-08-13"
data['account']['last_update'] = today_str

# 更新快照
if 'snapshots' not in data['account']:
    data['account']['snapshots'] = []

data['account']['snapshots'].append({
    'date': today_str,
    'total_value': total_value,
    'cash': cash,
    'market_value': round(total_market_value, 2),
    'daily_pnl': round(daily_pnl, 2),
    'total_pnl': total_pnl,
    'total_pnl_pct': total_pnl_pct
})

print(f"\n=== 账户总结 ===")
print(f"  现金: ${cash}")
print(f"  持仓市值: ${round(total_market_value, 2)}")
print(f"  总资产: ${total_value}")
print(f"  累计收益: ${total_pnl} ({total_pnl_pct}%)")
print(f"  今日盈亏: ${round(daily_pnl, 2)}")

# 写入文件
with open('/root/.openclaw/workspace/stock-sim/data/portfolio.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("\n✅ portfolio.json 已更新")
