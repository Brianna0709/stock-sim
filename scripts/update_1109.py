import json

path = "/root/.openclaw/workspace/stock-sim/data/portfolio.json"
with open(path) as f:
    d = json.load(f)

# 2026-11-09 收盘数据（东方财富/新华社收盘报道）
closes = {
    "QQQ":  (674.94, 2.87),    # 纳指100代理，约+2.87%（估算，跟随纳指+2.74%）
    "NVDA": (173.85, -4.27),
    "MSFT": (550.67, 2.75),
}

total_mv = 0.0
for t, (px, chg) in closes.items():
    p = d["positions"][t]
    p["prev_price"] = p["cur_price"]
    p["cur_price"] = px
    p["today_chg_pct"] = chg
    p["market_value"] = round(p["shares"] * px, 2)
    p["pnl"] = round(p["market_value"] - p["cost_basis"], 2)
    p["pnl_pct"] = round(p["pnl"] / p["cost_basis"] * 100, 2)
    p["unrealized_pnl"] = p["pnl"]
    p["unrealized_pnl_pct"] = p["pnl_pct"]
    total_mv += p["market_value"]

total_mv = round(total_mv, 2)
cash = d["account"]["cash"]
prev_mv = d["account"]["market_value"]
total_value = round(cash + total_mv, 2)
daily_pnl = round(total_mv - prev_mv, 2)
total_pnl = round(total_value - d["meta"]["initial_capital"], 2)
total_pnl_pct = round(total_pnl / d["meta"]["initial_capital"] * 100, 2)

note = ("收盘复盘：标普500 7549.94(+2.35%) 纳指25253.14(+2.74%) 道指52389.75(+2.15% 涨超1100点) | "
        "NVDA $173.85 (-4.27%) | MSFT $550.67 (+2.75%) | QQQ $674.94 (约+2.87%估算) | "
        "三大指数全线大涨逾2%：超跌反弹+费半暴涨近7%(AMD+8.9%/美光+4.2%/博通+6.5%)，特斯拉+5.5%、Meta+5.1%；"
        "但英伟达逆势大跌4.27%成七姐妹中唯一收跌，资金在AI内部大轮动；十一大板块全线上涨，工业+3.78%领涨")

snap = {
    "date": "2026-11-09",
    "total_value": total_value,
    "cash": cash,
    "market_value": total_mv,
    "daily_pnl": daily_pnl,
    "total_pnl": total_pnl,
    "total_pnl_pct": total_pnl_pct,
    "return_pct": total_pnl_pct,
    "note": note,
}

acct = d["account"]
acct.update({
    "total_value": total_value,
    "invested": total_mv,
    "total_unrealized_pnl": round(total_pnl, 2),
    "daily_pnl": daily_pnl,
    "total_pnl": total_pnl,
    "total_pnl_pct": total_pnl_pct,
    "return_pct": total_pnl_pct,
    "market_value": total_mv,
    "last_update": "2026-11-09",
    "market_context": {
        "sp500": 7549.94, "sp500_change_pct": 2.35,
        "nasdaq": 25253.14, "nasdaq_change_pct": 2.74,
        "dow": 52389.75, "dow_change_pct": 2.15,
    },
})
if not acct["snapshots"] or acct["snapshots"][-1].get("date") != "2026-11-09":
    acct["snapshots"].append(snap)
if "snapshots" in d:
    if not d["snapshots"] or d["snapshots"][-1].get("date") != "2026-11-09":
        d["snapshots"].append(snap)

with open(path, "w") as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

print("MV", total_mv, "total", total_value, "daily", daily_pnl, "totalPnL", total_pnl, total_pnl_pct)
for t in closes:
    p = d["positions"][t]
    print(t, p["cur_price"], p["pnl_pct"], p["today_chg_pct"])
