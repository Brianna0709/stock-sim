import json

path = '/mnt/openclaw/.openclaw/workspace/stock-sim/data/portfolio.json'
with open(path, 'r') as f:
    data = json.load(f)

# 2026-10-06（美东周二）收盘价（富途确认）
prices = {
    'QQQ': 760.93,
    'NVDA': 239.24,
    'MSFT': 529.30
}
today_str = "2026-10-06"

prev = {k: data['positions'][k]['cur_price'] for k in prices}

total_market_value = 0
total_cost = 0
daily_pnl = 0.0
chgs = {}

for symbol in ['QQQ', 'NVDA', 'MSFT']:
    pos = data['positions'][symbol]
    new_price = prices[symbol]
    old_price = prev[symbol]
    shares = pos['shares']
    cost_price = pos['cost_price']

    market_value = round(shares * new_price, 2)
    cost_basis = round(shares * cost_price, 2)
    unrealized_pnl = round(market_value - cost_basis, 2)
    unrealized_pnl_pct = round(unrealized_pnl / cost_basis * 100, 2)
    daily_change_pct = round((new_price - old_price) / old_price * 100, 2)
    daily_pnl_change = round(shares * (new_price - old_price), 2)

    pos['cur_price'] = new_price
    pos['market_value'] = market_value
    pos['pnl'] = unrealized_pnl
    pos['pnl_pct'] = unrealized_pnl_pct
    pos['unrealized_pnl'] = unrealized_pnl
    pos['unrealized_pnl_pct'] = unrealized_pnl_pct
    pos['today_chg_pct'] = daily_change_pct

    total_market_value += market_value
    total_cost += cost_basis
    daily_pnl += daily_pnl_change
    chgs[symbol] = daily_change_pct
    print(f"{symbol}: ${new_price} ({daily_change_pct:+.2f}%) 市值 ${market_value} 盈亏 {unrealized_pnl_pct:+.2f}%")

cash = data['account']['cash']
total_value = round(cash + total_market_value, 2)
total_pnl = round(total_value - 100000, 2)
total_pnl_pct = round(total_pnl / 100000 * 100, 2)

data['account']['total_value'] = total_value
data['account']['invested'] = round(total_market_value, 2)
data['account']['total_unrealized_pnl'] = round(total_market_value - total_cost, 2)
data['account']['daily_pnl'] = round(daily_pnl, 2)
data['account']['market_value'] = round(total_market_value, 2)
data['account']['total_pnl'] = total_pnl
data['account']['total_pnl_pct'] = total_pnl_pct
data['account']['last_update'] = today_str

data['market_context'] = {
    'sp500': 7818.93, 'sp500_change_pct': 0.58,
    'nasdaq': 27599.79, 'nasdaq_change_pct': 0.45,
    'dow': 51521.28, 'dow_change_pct': 0.49
}

note = (f"收盘复盘：NVDA ${prices['NVDA']} ({chgs['NVDA']:+.2f}%) | MSFT ${prices['MSFT']} ({chgs['MSFT']:+.2f}%) | "
        f"QQQ ${prices['QQQ']} ({chgs['QQQ']:+.2f}%) | 标普500 7818.93(+0.58% 首次收于7800上方) "
        f"道指51521.28(+0.49%) 纳指27599.79(+0.45% 双双创收盘新高) | "
        f"标普纳指双创新高：美债收益率自多年高位回落+油价企稳(G7释放油储)，AI芯片与电力股领涨"
        f"(Marvell+5.8%、博通+3.7%、AMD+2.8%、Constellation+12%)；存储续跌(希捷-9%、西数-7%、SK海力士-6%)；"
        f"英伟达微涨市值逼近6万亿，市场转向Q3财报季与周三美联储会议纪要")

snap_acc = {
    'date': today_str,
    'total_value': total_value,
    'cash': cash,
    'market_value': round(total_market_value, 2),
    'daily_pnl': round(daily_pnl, 2),
    'total_pnl': total_pnl,
    'total_pnl_pct': total_pnl_pct,
    'note': note
}
data['account']['snapshots'] = [s for s in data['account']['snapshots'] if s['date'] != today_str]
data['account']['snapshots'].append(snap_acc)

snap_top = {
    'date': today_str,
    'total_value': total_value,
    'cash': cash,
    'invested': round(total_market_value, 2),
    'return_pct': total_pnl_pct,
    'note': note
}
data['snapshots'] = [s for s in data['snapshots'] if s['date'] != today_str]
data['snapshots'].insert(0, snap_top)

with open(path, 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\n总资产: ${total_value} | 累计收益: ${total_pnl} ({total_pnl_pct:+.2f}%) | 今日盈亏: ${round(daily_pnl,2):,.2f}")
print("portfolio.json 已更新")
