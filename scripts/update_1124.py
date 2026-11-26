import json

P = "/root/.openclaw/workspace/stock-sim/data/portfolio.json"
d = json.load(open(P))

prices = {"QQQ": 643.39, "NVDA": 155.38, "MSFT": 496.13}
chg = {"QQQ": -1.07, "NVDA": -6.25, "MSFT": 0.74}  # QQQ ≈-1.17% 估算 / NVDA 新闻 -5.86% / MSFT +0.74%

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
acc["last_update"] = "2026-11-24"
acc["market_context"] = {
    "sp500": 7201.09, "sp500_change_pct": -0.50,
    "nasdaq": 23733.53, "nasdaq_change_pct": -1.48,
    "dow": 50018.69, "dow_change_pct": 0.85,
}

note = ("收盘复盘(2026-11-24周二)：道指50018.69(+0.85% 涨423点) 标普500 7201.09(-0.50%) 纳指23733.53(-1.48%) | "
        "NVDA $155.38(-5.86% 周一+32%后回吐 市值回落至3.74万亿) | MSFT $496.13(+0.74% 逆势抗跌) | QQQ $643.39(约-1.17%估算 纳指100) | "
        "费半-7.88%报8832.5 存储芯片重挫(美光-11.01%/闪迪-11.13%/西数-7.84%/希捷-7.23%) AMD-8.86% 台积电-3.96% Lumentum-10%；"
        "Anthropic(ANT)跌6.54%报81.91 上市第四日跌破83美元发行价；苹果+1.43%逆势；市场重估AI资本开支回报+美国可能上调对欧关税，"
        "资金转向道指价值股；明日(周三)核心PCE通胀数据+初请失业金人数")
snap = {"date": "2026-11-24", "total_value": total, "cash": cash, "market_value": mv, "invested": mv,
        "daily_pnl": daily, "total_pnl": acc["total_pnl"], "total_pnl_pct": acc["total_pnl_pct"],
        "return_pct": acc["total_pnl_pct"], "note": note}
acc["snapshots"].append(snap)
d["snapshots"].append(snap)

json.dump(d, open(P, "w"), ensure_ascii=False, indent=2)
print("OK", total, mv, unreal, daily, acc["total_pnl_pct"])
for t, p in d["positions"].items():
    print(t, p["cur_price"], p["market_value"], p["pnl_pct"], p["today_chg_pct"])
