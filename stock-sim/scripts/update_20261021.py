import json

prices = {"NVDA": 221.97, "MSFT": 532.95, "QQQ": 725.18}
chg = {"NVDA": 2.54, "MSFT": 0.20, "QQQ": 1.05}

with open('/root/.openclaw/workspace/stock-sim/data/portfolio.json') as f:
    data = json.load(f)

total_mv = 0
for t, p in data['positions'].items():
    price = prices[t]
    shares = p['shares']
    mv = round(shares * price, 2)
    pnl = round(mv - p['cost_basis'], 2)
    pnl_pct = round(pnl / p['cost_basis'] * 100, 2)
    p['cur_price'] = price
    p['market_value'] = mv
    p['pnl'] = pnl
    p['pnl_pct'] = pnl_pct
    p['today_chg_pct'] = chg[t]
    p['unrealized_pnl'] = pnl
    p['unrealized_pnl_pct'] = pnl_pct
    total_mv += mv

total_mv = round(total_mv, 2)
cash = data['account']['cash']
total_value = round(cash + total_mv, 2)
prev_total = 116005.01
daily_pnl = round(total_value - prev_total, 2)
total_pnl = round(total_value - 100000, 2)
total_pnl_pct = round(total_pnl / 100000 * 100, 2)

data['account']['total_value'] = total_value
data['account']['invested'] = total_mv
data['account']['total_unrealized_pnl'] = total_pnl
data['account']['daily_pnl'] = daily_pnl
data['account']['last_update'] = '2026-10-21'
data['account']['market_value'] = total_mv
data['account']['total_pnl'] = total_pnl
data['account']['total_pnl_pct'] = total_pnl_pct
data['account']['return_pct'] = total_pnl_pct

note = ("收盘复盘：NVDA $221.97 (+2.54%) | MSFT $532.95 (+0.20%) | QQQ $725.18 (约+1.05%估算) | "
        "标普500 7757.17(+0.58%) 道指52856.09(+0.69%) 纳指26702.86(+1.05%) | "
        "SpaceX Q3营收146亿美元同比+161%、净利44亿美元扭亏，股价大涨7.79%市值超台积电，点燃AI情绪；"
        "黄仁勋GTC柏林发布DSX POD AI工厂，英伟达+2.54%；费半+1.97%，存储芯片普涨(西数+3.89%/希捷+3.22%)；"
        "超微电脑+9.55%、AI服务器概念爆发；Meta盘后财报营收646亿美元+26%续涨约4%；奈飞指引疲软-6%")

snap = {
    "date": "2026-10-21",
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
data['account']['snapshots'].append(snap)
data['snapshots'].append(snap)

data['market_context'] = {
    "sp500": 7757.17, "sp500_change_pct": 0.58,
    "nasdaq": 26702.86, "nasdaq_change_pct": 1.05,
    "dow": 52856.09, "dow_change_pct": 0.69
}

with open('/root/.openclaw/workspace/stock-sim/data/portfolio.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"total_mv={total_mv} total_value={total_value} daily_pnl={daily_pnl} total_pnl={total_pnl} pct={total_pnl_pct}")
for t, p in data['positions'].items():
    print(t, p['cur_price'], p['market_value'], p['pnl'], p['pnl_pct'])
