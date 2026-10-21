import json, re

with open('/root/.openclaw/workspace/stock-sim/standalone.html', 'r') as f:
    html = f.read()

data = json.load(open('/root/.openclaw/workspace/stock-sim/data/portfolio.json'))
pos = data['positions']

# Actual row format in standalone.html (cost price first, then current price)
for sym, p in pos.items():
    pnl_cls = 'text-green-400' if p['unrealized_pnl_pct'] >= 0 else 'text-red-400'
    day_cls = 'text-green-400' if p['today_chg_pct'] >= 0 else 'text-red-400'
    pat = re.compile(
        r'(<td class="py-3 px-4 font-bold text-green-400">' + sym + r'</td>\s*'
        r'<td class="py-3 px-4">\$)[\d,\.]+(</td>\s*'
        r'<td class="py-3 px-4">\$)[\d,\.]+(</td><td class="py-3 px-4">)[\d\.]+(</td>\s*'
        r'<td class="py-3 px-4">\$)[\d,\.]+(</td><td class="py-3 px-4 )(?:text-green-400|text-red-400)(">)[\+\-]?[\d,\.]+%(</td><td class="py-3 px-4 )(?:text-green-400|text-red-400)(">)[\+\-]?[\d\.]+%', re.S)
    repl = (f'\\g<1>${p["cost_price"]:,.2f}\\g<2>${p["cur_price"]:,.2f}\\g<3>{p["shares"]}\\g<4>${p["market_value"]:,.2f}'
            f'\\g<5>{pnl_cls}>+{p["unrealized_pnl_pct"]:.2f}%\\g<6>{day_cls}>{p["today_chg_pct"]:+.2f}%')
    html, n = pat.subn(repl, html)
    print(sym, 'replaced:', n)

with open('/root/.openclaw/workspace/stock-sim/standalone.html', 'w') as f:
    f.write(html)
print('done')
