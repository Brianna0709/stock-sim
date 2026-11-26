import json, re

PPATH = '/mnt/openclaw/.openclaw/workspace/stock-sim/data/portfolio.json'
IPATH = '/mnt/openclaw/.openclaw/workspace/stock-sim/index.html'

with open(PPATH) as f:
    data = json.load(f)

with open(IPATH) as f:
    html = f.read()

payload = {
    "meta": data["meta"],
    "account": data["account"],
    "positions": data["positions"],
    "market_context": data.get("market_context", {}),
    "trades": data.get("trades", []),
    "pending_plan": data.get("pending_plan", []),
}
payload["account"]["refreshed_at"] = "2026-10-30 06:05 (北京时间)"

new_block = "window.__PORTFOLIO_DATA__ = " + json.dumps(payload, ensure_ascii=False, indent=2) + ";"

html = re.sub(r'window\.__PORTFOLIO_DATA__ = \{.*?\n\};', new_block, html, count=1, flags=re.S)

with open(IPATH, 'w') as f:
    f.write(html)

print("index.html data block updated:", len(new_block), "chars")
print("total_value:", payload["account"]["total_value"], "daily:", payload["account"]["daily_pnl"])
