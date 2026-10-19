import json

path = '/root/.openclaw/workspace/stock-sim/data/portfolio.json'
with open(path) as f:
    data = json.load(f)

# 2026-10-16 美股收盘（个股收盘价按新闻报道涨跌幅推算）
prices = {
    'QQQ': (711.26, -2.30),   # 纳指100 ETF，随科技股抛售
    'NVDA': (213.97, -1.50),  # 跌超1%，取-1.5%
    'MSFT': (532.43, -1.30),  # 跌超1%，取-1.3%
}

prev_mv = data['account']['market_value']
cash = data['account']['cash']

total_mv = 0
for ticker, pos in data['positions'].items():
    price, chg = prices[ticker]
    pos['cur_price'] = price
    pos['market_value'] = round(pos['shares'] * price, 2)
    pos['unrealized_pnl'] = round(pos['market_value'] - pos['cost_basis'], 2)
    pos['unrealized_pnl_pct'] = round(pos['unrealized_pnl'] / pos['cost_basis'] * 100, 2)
    pos['pnl'] = pos['unrealized_pnl']
    pos['pnl_pct'] = pos['unrealized_pnl_pct']
    pos['today_chg_pct'] = chg
    total_mv += pos['market_value']

total_mv = round(total_mv, 2)
total_value = round(cash + total_mv, 2)
total_pnl = round(total_value - data['meta']['initial_capital'], 2)
daily_pnl = round(total_mv - prev_mv, 2)

data['account'].update({
    'total_value': total_value,
    'invested': total_mv,
    'market_value': total_mv,
    'total_unrealized_pnl': total_pnl,
    'total_pnl': total_pnl,
    'total_pnl_pct': round(total_pnl / 100000 * 100, 2),
    'daily_pnl': daily_pnl,
    'last_update': '2026-10-16',
})

note = ("收盘复盘：NVDA $213.97 (约-1.5%) | MSFT $532.43 (约-1.3%) | QQQ $711.26 (约-2.3%) | "
        "标普500 7659.44(-1.09%) 道指52002.41(-0.34%) 纳指26140.03(-2.14%) | "
        "恐慌蔓延：VIX四个月首破22，费半-3.83%八连跌追平2006年以来最长，存储概念-6.28%；"
        "CoreWeave -12%（周跌25%，债务超510亿美元）拖垮AI融资链情绪；布油5个月来首触110美元，"
        "通胀+AI融资双重担忧，资金逃向能源/食品饮料等防御板块；本周纳指-4.48%创6月以来最差单周，道指逆势+0.67%")

snap = {
    'date': '2026-10-16',
    'total_value': total_value,
    'cash': cash,
    'market_value': total_mv,
    'invested': total_mv,
    'daily_pnl': daily_pnl,
    'total_pnl': total_pnl,
    'total_pnl_pct': round(total_pnl / 100000 * 100, 2),
    'return_pct': round(total_pnl / 100000 * 100, 2),
    'note': note,
}

acct_snaps = [s for s in data['account'].get('snapshots', []) if s.get('date') != '2026-10-16']
acct_snaps.append(snap)
data['account']['snapshots'] = acct_snaps

top_snaps = [s for s in data.get('snapshots', []) if s.get('date') != '2026-10-16']
top_snaps.append(snap)
data['snapshots'] = top_snaps

data['market_context'] = {
    'sp500': 7659.44,
    'sp500_change_pct': -1.09,
    'nasdaq': 26140.03,
    'nasdaq_change_pct': -2.14,
    'dow': 52002.41,
    'dow_change_pct': -0.34,
}

with open(path, 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("QQQ MV:", data['positions']['QQQ']['market_value'], "PnL%:", data['positions']['QQQ']['unrealized_pnl_pct'])
print("NVDA MV:", data['positions']['NVDA']['market_value'], "PnL%:", data['positions']['NVDA']['unrealized_pnl_pct'])
print("MSFT MV:", data['positions']['MSFT']['market_value'], "PnL%:", data['positions']['MSFT']['unrealized_pnl_pct'])
print("Total MV:", total_mv, "| Total:", total_value, "| DailyPnL:", daily_pnl, "| TotalPnL:", total_pnl, "(%s%%)" % data['account']['total_pnl_pct'])
