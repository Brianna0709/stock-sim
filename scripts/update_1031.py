import json

PATH = "/root/.openclaw/workspace/stock-sim/data/portfolio.json"

with open(PATH) as f:
    data = json.load(f)

# 2026-10-30 (Friday) official closes
closes = {
    "NVDA": {"price": 206.61, "chg": -3.30},
    "MSFT": {"price": 521.91, "chg": -1.55},
    "QQQ":  {"price": 695.11, "chg": -2.83},
}

prev = {
    "NVDA": 213.66,
    "MSFT": 530.14,
    "QQQ": 715.34,
}

total_mv = 0.0
for tkr, pos in data["positions"].items():
    c = closes[tkr]
    pos["prev_price"] = prev[tkr]
    pos["cur_price"] = c["price"]
    pos["today_chg_pct"] = c["chg"]
    mv = round(pos["shares"] * c["price"], 2)
    pos["market_value"] = mv
    pos["unrealized_pnl"] = round(mv - pos["cost_basis"], 2)
    pos["unrealized_pnl_pct"] = round((mv / pos["cost_basis"] - 1) * 100, 2)
    pos["pnl"] = pos["unrealized_pnl"]
    pos["pnl_pct"] = pos["unrealized_pnl_pct"]
    total_mv += mv

total_mv = round(total_mv, 2)
cash = data["account"]["cash"]
total_value = round(cash + total_mv, 2)
prev_total = data["account"]["snapshots"][-1]["total_value"] if data["account"]["snapshots"] else 100000
daily_pnl = round(total_value - prev_total, 2)
total_pnl = round(total_value - data["meta"]["initial_capital"], 2)
total_pnl_pct = round(total_pnl / data["meta"]["initial_capital"] * 100, 2)

acct = data["account"]
acct["invested"] = total_mv
acct["market_value"] = total_mv
acct["total_value"] = total_value
acct["total_unrealized_pnl"] = round(total_pnl, 2)
acct["total_pnl"] = total_pnl
acct["total_pnl_pct"] = total_pnl_pct
acct["return_pct"] = total_pnl_pct
acct["daily_pnl"] = daily_pnl
acct["last_update"] = "2026-10-30"

snapshot = {
    "date": "2026-10-30",
    "total_value": total_value,
    "cash": cash,
    "market_value": total_mv,
    "invested": total_mv,
    "daily_pnl": daily_pnl,
    "total_pnl": total_pnl,
    "total_pnl_pct": total_pnl_pct,
    "return_pct": total_pnl_pct,
    "note": ("收盘复盘：纳指25437.00(-2.86% 六月以来最差单日) 标普500 7580.07(-1.82%) 道指51770.31(-1.09%) | "
             "NVDA $206.61 (-3.30%) | MSFT $521.91 (-1.55%) | QQQ $695.11 (约-2.83%估算) | "
             "周四盘后英特尔Q4指引暴雷(指引EPS $0.25 vs 预期$0.43)开盘暴跌29%+市值蒸发1500亿美元，亚马逊财报不及预期跌7%，"
             "财报连环雷+中期选举不确定性+月末获利了结，资金撤离AI核心流向能源(+1.91%)/必需消费(+1.38%)防御板块，"
             "科技板块-4.24%领跌，费半-7.20%创2020年3月以来最大单日跌幅，纳指较近期高点回撤约8%")
}
acct["snapshots"].append(snapshot)
data["snapshots"].append(snapshot)

data["market_context"] = {
    "sp500": 7580.07,
    "sp500_change_pct": -1.82,
    "nasdaq": 25437.00,
    "nasdaq_change_pct": -2.86,
    "dow": 51770.31,
    "dow_change_pct": -1.09,
}

with open(PATH, "w") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("positions:")
for t, p in data["positions"].items():
    print(f"  {t}: cur={p['cur_price']} chg={p['today_chg_pct']}% mv={p['market_value']} pnl={p['unrealized_pnl']} ({p['unrealized_pnl_pct']}%)")
print(f"total_value={total_value} daily_pnl={daily_pnl} total_pnl={total_pnl} ({total_pnl_pct}%)")
