import json

P = "/root/.openclaw/workspace/stock-sim/data/portfolio.json"
d = json.load(open(P))

prices = {"QQQ": 625.90, "NVDA": 149.30, "MSFT": 496.13}
chg = {"QQQ": -2.73, "NVDA": -3.91, "MSFT": -0.82}

prev_total = d["account"]["total_value"]

for t, pos in d["positions"].items():
    p = prices[t]
    pos["prev_price"] = pos["cur_price"]
    pos["cur_price"] = p
    pos["market_value"] = round(pos["shares"] * p, 2)
    pos["pnl"] = round(pos["market_value"] - pos["cost_basis"], 2)
    pos["pnl_pct"] = round(pos["pnl"] / pos["cost_basis"] * 100, 2)
    pos["unrealized_pnl"] = pos["pnl"]
    pos["unrealized_pnl_pct"] = pos["pnl_pct"]
    pos["today_chg_pct"] = chg[t]

mv = round(sum(p["market_value"] for p in d["positions"].values()), 2)
cash = d["account"]["cash"]
total = round(mv + cash, 2)
unreal = round(sum(p["pnl"] for p in d["positions"].values()), 2)
daily = round(total - prev_total, 2)

acc = d["account"]
acc["market_value"] = mv
acc["invested"] = mv
acc["total_value"] = total
acc["total_unrealized_pnl"] = unreal
acc["total_pnl"] = round(total - 100000, 2)
acc["total_pnl_pct"] = round((total - 100000) / 1000, 2)
acc["return_pct"] = acc["total_pnl_pct"]
acc["daily_pnl"] = daily
acc["last_update"] = "2026-11-25"
acc["market_context"] = {
    "sp500": 7182.78, "sp500_change_pct": -0.25,
    "nasdaq": 23585.80, "nasdaq_change_pct": -0.62,
    "dow": 50182.95, "dow_change_pct": 0.33,
}

note = ("收盘复盘(2026-11-25周三)：道指50182.95(+0.33% 涨164点 盘中一度-1105点后翻红) 标普500 7182.78(-0.25% 盘中最低-3.2%) 纳指23585.80(-0.62% 盘中最低-4.6%) | "
        "NVDA $149.30(-3.91% 盘中一度跌近9%) | MSFT $496.13(-0.82%) | QQQ $625.90(-2.73% 估算 纳指100盘中触及技术性熊市) | "
        "10月核心PCE同比3.3%创2023年11月以来新高、整体PCE 3.8%，强化12月加息25bp押注；美国政府提议对14个贸易伙伴加征新关税(欧20%/日韩15%)；"
        "费半-0.65% 美光-4.5% AMD-1.75% 甲骨文-4% 谷歌-2% 亚马逊-3%；Meta+3%、IBM+3.31%、Salesforce+2%、惠普+11%、闪迪-5.5%、Ambarella-19%(指引暴雷)；"
        "Anthropic(ANT)低开高走+1%；材料+1.84%/房地产+0.84%领涨，非必需消费-0.98%/科技-0.97%领跌；VIX+7.3%至28.29；感恩节前交易清淡+Burry称组合'几乎满仓做多'促成尾盘修复")
snap = {"date": "2026-11-25", "total_value": total, "cash": cash, "market_value": mv, "invested": mv,
        "daily_pnl": daily, "total_pnl": acc["total_pnl"], "total_pnl_pct": acc["total_pnl_pct"],
        "return_pct": acc["total_pnl_pct"], "note": note}
acc["snapshots"].append(snap)
d["snapshots"].append(snap)

json.dump(d, open(P, "w"), ensure_ascii=False, indent=2)
print("OK", total, mv, unreal, daily, acc["total_pnl_pct"])
for t, p in d["positions"].items():
    print(t, p["cur_price"], p["market_value"], p["pnl_pct"], p["today_chg_pct"])
