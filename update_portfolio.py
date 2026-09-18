#!/usr/bin/env python3
"""Update portfolio.json with 2026-09-18 closing prices."""
import json

# 2026-09-18 closing data
CLOSING = {
    "QQQ":   {"price": 716.95, "prev": 704.72, "today_chg_pct": 1.71},
    "NVDA":  {"price": 222.27, "prev": 219.34, "today_chg_pct": 1.34},
    "MSFT":  {"price": 497.75, "prev": 490.30, "today_chg_pct": 1.50},
}

INDEX = {
    "sp500":    {"close": 7650.50,  "chg_pct": 0.17},
    "nasdaq":   {"close": 26522.54, "chg_pct": 0.39},
    "dow":      {"close": 51682.64, "chg_pct": -0.18},
}

with open("/root/.openclaw/workspace/stock-sim/data/portfolio.json", "r") as f:
    data = json.load(f)

# Update positions
for ticker, info in CLOSING.items():
    pos = data["positions"][ticker]
    pos["cur_price"] = info["price"]
    pos["market_value"] = round(pos["shares"] * info["price"], 2)
    pos["pnl"] = round(pos["market_value"] - pos["cost_basis"], 2)
    pos["pnl_pct"] = round((pos["market_value"] - pos["cost_basis"]) / pos["cost_basis"] * 100, 2)
    pos["today_chg_pct"] = info["today_chg_pct"]
    pos["unrealized_pnl"] = round(pos["market_value"] - pos["cost_basis"], 2)
    pos["unrealized_pnl_pct"] = round((pos["market_value"] - pos["cost_basis"]) / pos["cost_basis"] * 100, 2)

# Recalculate account
market_value = sum(p["market_value"] for p in data["positions"].values())
total_value = round(market_value + data["account"]["cash"], 2)
invested = sum(p["cost_basis"] for p in data["positions"].values())
prev_total = data["account"]["total_value"]
daily_pnl = round(total_value - prev_total, 2)
total_pnl = round(total_value - data["meta"]["initial_capital"], 2)
total_pnl_pct = round(total_pnl / data["meta"]["initial_capital"] * 100, 2)

data["account"]["total_value"] = total_value
data["account"]["invested"] = round(invested, 2)
data["account"]["market_value"] = round(market_value, 2)
data["account"]["total_unrealized_pnl"] = round(market_value - invested, 2)
data["account"]["daily_pnl"] = daily_pnl
data["account"]["last_update"] = "2026-09-18"

# Update market context
data["market_context"] = {
    "sp500": INDEX["sp500"]["close"],
    "sp500_change_pct": INDEX["sp500"]["chg_pct"],
    "nasdaq": INDEX["nasdaq"]["close"],
    "nasdaq_change_pct": INDEX["nasdaq"]["chg_pct"],
    "dow": INDEX["dow"]["close"],
    "dow_change_pct": INDEX["dow"]["chg_pct"],
}

# Add snapshot
snapshot = {
    "date": "2026-09-18",
    "total_value": total_value,
    "cash": data["account"]["cash"],
    "market_value": round(market_value, 2),
    "daily_pnl": daily_pnl,
    "total_pnl": total_pnl,
    "total_pnl_pct": total_pnl_pct,
    "return_pct": total_pnl_pct,
    "note": f"收盘复盘：NVDA ${CLOSING['NVDA']['price']:.2f} (+{CLOSING['NVDA']['today_chg_pct']:.2f}%) | MSFT ${CLOSING['MSFT']['price']:.2f} (+{CLOSING['MSFT']['today_chg_pct']:.2f}%) | QQQ ${CLOSING['QQQ']['price']:.2f} (+{CLOSING['QQQ']['today_chg_pct']:.2f}%) | 标普500 {INDEX['sp500']['close']:.2f}({INDEX['sp500']['chg_pct']:+.2f}%) 道指{INDEX['dow']['close']:.2f}({INDEX['dow']['chg_pct']:+.2f}%) 纳指{INDEX['nasdaq']['close']:.2f}({INDEX['nasdaq']['chg_pct']:+.2f}%) | 半导体板块继续走强，三大指数涨跌分化，纳指三连阳"
}

# Avoid duplicate if re-run
existing = [s for s in data.get("snapshots", []) if s.get("date") == "2026-09-18"]
if existing:
    data["snapshots"] = [s for s in data["snapshots"] if s.get("date") != "2026-09-18"]

data.setdefault("snapshots", []).append(snapshot)

# Add account snapshot as well
acc_snapshot = {
    "date": "2026-09-18",
    "total_value": total_value,
    "cash": data["account"]["cash"],
    "invested": round(invested, 2),
    "return_pct": total_pnl_pct,
    "note": snapshot["note"],
}
existing_acc = [s for s in data.get("account", {}).get("snapshots", []) if s.get("date") == "2026-09-18"]
if existing_acc:
    data["account"]["snapshots"] = [s for s in data["account"]["snapshots"] if s.get("date") != "2026-09-18"]
data["account"].setdefault("snapshots", []).append(acc_snapshot)

with open("/root/.openclaw/workspace/stock-sim/data/portfolio.json", "w") as f:
    json.dump(data, f, indent=2)

print("Portfolio updated successfully.")
print(f"Total Value: ${total_value:,.2f}")
print(f"Daily PnL: ${daily_pnl:+,.2f}")
print(f"Total PnL: ${total_pnl:+,.2f} ({total_pnl_pct:+.2f}%)")
for t, p in data["positions"].items():
    print(f"  {t}: ${p['cur_price']:.2f} | MV: ${p['market_value']:,.2f} | PnL: {p['pnl_pct']:+.2f}%")
