import json

path = "/root/.openclaw/workspace/stock-sim/data/portfolio.json"
with open(path) as f:
    data = json.load(f)

closes = {"QQQ": (659.51, 656.95), "NVDA": (150.96, 155.46), "MSFT": (508.29, 506.24)}

total_mv = 0.0
for tkr, pos in data["positions"].items():
    cur, prev = closes[tkr]
    pos["prev_price"] = prev
    pos["cur_price"] = cur
    mv = round(pos["shares"] * cur, 2)
    pos["market_value"] = mv
    pos["pnl"] = round(mv - pos["cost_basis"], 2)
    pos["pnl_pct"] = round((mv / pos["cost_basis"] - 1) * 100, 2)
    pos["unrealized_pnl"] = pos["pnl"]
    pos["unrealized_pnl_pct"] = pos["pnl_pct"]
    pos["today_chg_pct"] = round((cur / prev - 1) * 100, 2)
    total_mv += mv
total_mv = round(total_mv, 2)
cash = data["account"]["cash"]
total_value = round(cash + total_mv, 2)
prev_total = data["account"]["total_value"]
daily_pnl = round(total_value - prev_total, 2)
total_pnl = round(total_value - 100000, 2)
total_pnl_pct = round(total_pnl / 1000, 2)

acct = data["account"]
acct.update({
    "total_value": total_value,
    "invested": total_mv,
    "market_value": total_mv,
    "total_unrealized_pnl": total_pnl,
    "daily_pnl": daily_pnl,
    "total_pnl": total_pnl,
    "total_pnl_pct": total_pnl_pct,
    "return_pct": total_pnl_pct,
    "last_update": "2026-11-18",
})
acct["market_context"] = {
    "sp500": 7323.63, "sp500_change_pct": -0.23,
    "nasdaq": 24429.88, "nasdaq_change_pct": 0.42,
    "dow": 50198.17, "dow_change_pct": -1.11,
}

note = ("收盘复盘：道指50198.17(-1.11%) 标普500 7323.63(-0.23% 五连跌) 纳指24429.88(+0.42%) | "
        "NVDA $150.96 (-2.89% 五连跌 财报超预期仍高开低走) | MSFT $508.29 (+0.40%) | QQQ $659.51 (+0.39%) | "
        "英伟达Q3营收/EPS/Q4指引全面超预期但临时CEO交接+出口管制不确定引发多家投行下调评级，资金转向AMD(+5.31%)/博通(+3.64%)；"
        "CMS拟扩大Medicare Advantage审计，联合健康/哈门那跌约8%拖累道指；美联储10月纪要偏鹰(数位官员提及12月或加息超25bp)，美元创19个月新高，10Y美债收益率5.07%附近；"
        "WTI -3.2%报83.26；亚马逊涨近4%支撑纳指翻红；明日关注Anthropic IPO(ANT, 估值最高1.4万亿美元)与沃尔玛财报")

snap = {
    "date": "2026-11-18",
    "total_value": total_value,
    "cash": cash,
    "market_value": total_mv,
    "invested": total_mv,
    "daily_pnl": daily_pnl,
    "total_pnl": total_pnl,
    "total_pnl_pct": total_pnl_pct,
    "return_pct": total_pnl_pct,
    "note": note,
}
acct["snapshots"].append(snap)
data["snapshots"].append(snap)

with open(path, "w") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("MV:", total_mv, "Total:", total_value, "Daily:", daily_pnl, "TotalPnL:", total_pnl, f"({total_pnl_pct}%)")
for t, p in data["positions"].items():
    print(t, p["cur_price"], p["today_chg_pct"], p["pnl_pct"])
