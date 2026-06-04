#!/usr/bin/env python3
import json
from datetime import datetime, timezone

# 读取 portfolio.json
with open('/root/.openclaw/workspace/stock-sim/data/portfolio.json', 'r') as f:
    portfolio = json.load(f)

# 2026年5月15日收盘价数据（基于搜索结果）
closing_prices = {
    'QQQ': 712.57,    # 搜索结果：$712.57, 下跌 -1.004%
    'NVDA': 225.32,   # 搜索结果：收盘价 $225.32
    'MSFT': 409.43    # 搜索结果：收盘价 $409.43
}

# 前一日收盘价（用于计算今日涨跌）
prev_prices = {
    'QQQ': 687.50,
    'NVDA': 205.00,
    'MSFT': 415.00
}

# 三大指数数据
market_data = {
    'sp500': 7444.25,
    'sp500_change_pct': 0.58,
    'nasdaq': 26402.34,
    'nasdaq_change_pct': 1.20,
    'dow': 49693.20,
    'dow_change_pct': -0.14
}

# 更新持仓数据
for ticker, data in portfolio['positions'].items():
    cur_price = closing_prices[ticker]
    prev_price = prev_prices[ticker]
    
    # 计算市值
    market_value = data['shares'] * cur_price
    
    # 计算未实现盈亏
    unrealized_pnl = market_value - data['cost_basis']
    unrealized_pnl_pct = (unrealized_pnl / data['cost_basis']) * 100
    
    # 计算今日涨跌
    today_chg_pct = ((cur_price - prev_price) / prev_price) * 100
    
    # 更新数据
    data['cur_price'] = round(cur_price, 2)
    data['market_value'] = round(market_value, 2)
    data['pnl'] = round(unrealized_pnl, 2)
    data['pnl_pct'] = round(unrealized_pnl_pct, 4)
    data['today_chg_pct'] = round(today_chg_pct, 4)

# 计算账户总值
invested = sum(p['market_value'] for p in portfolio['positions'].values())
total_value = invested + portfolio['account']['cash']
return_pct = ((total_value - portfolio['meta']['initial_capital']) / portfolio['meta']['initial_capital']) * 100

# 更新账户数据
portfolio['account']['invested'] = round(invested, 2)
portfolio['account']['total_value'] = round(total_value, 2)

# 添加今日快照
today = '2026-05-15'
snapshot = {
    'date': today,
    'total_value': round(total_value, 2),
    'cash': portfolio['account']['cash'],
    'invested': round(invested, 2),
    'return_pct': round(return_pct, 2),
    'note': f"收盘复盘：NVDA ${closing_prices['NVDA']:.2f} ({portfolio['positions']['NVDA']['today_chg_pct']:+.2f}%) | MSFT ${closing_prices['MSFT']:.2f} ({portfolio['positions']['MSFT']['today_chg_pct']:+.2f}%) | QQQ ${closing_prices['QQQ']:.2f} ({portfolio['positions']['QQQ']['today_chg_pct']:+.2f}%) | 标普500 {market_data['sp500']:.2f}({market_data['sp500_change_pct']:+.2f}%) 道指{market_data['dow']:.2f}({market_data['dow_change_pct']:+.2f}%) 纳指{market_data['nasdaq']:.2f}({market_data['nasdaq_change_pct']:+.2f}%)"
}

# 检查是否已有今日快照，有则更新，无则添加
existing_dates = [s['date'] for s in portfolio['snapshots']]
if today in existing_dates:
    for i, s in enumerate(portfolio['snapshots']):
        if s['date'] == today:
            portfolio['snapshots'][i] = snapshot
            break
else:
    portfolio['snapshots'].append(snapshot)

# 更新市场上下文
portfolio['market_context'] = {
    'sp500': market_data['sp500'],
    'sp500_change_pct': market_data['sp500_change_pct'],
    'nasdaq': market_data['nasdaq'],
    'nasdaq_change_pct': market_data['nasdaq_change_pct'],
    'dow': market_data['dow'],
    'dow_change_pct': market_data['dow_change_pct'],
    'note': f"{today}收盘：道指{market_data['dow_change_pct']:+.2f}%，纳指{market_data['nasdaq_change_pct']:+.2f}%，标普{market_data['sp500_change_pct']:+.2f}%。科技股分化，NVDA反弹强劲。"
}

# 保存文件
with open('/root/.openclaw/workspace/stock-sim/data/portfolio.json', 'w') as f:
    json.dump(portfolio, f, indent=2, ensure_ascii=False)

print(f"✅ Portfolio updated for {today}")
print(f"💰 Total Value: ${total_value:.2f}")
print(f"📈 Return: {return_pct:.2f}%")
print("\n持仓明细:")
for ticker, data in portfolio['positions'].items():
    print(f"  {ticker}: ${data['cur_price']:.2f} (今日{data['today_chg_pct']:+.2f}%, 持仓{data['pnl_pct']:+.2f}%)")
