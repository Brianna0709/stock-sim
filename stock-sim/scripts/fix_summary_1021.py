import json, re

with open('/root/.openclaw/workspace/stock-sim/standalone.html') as f:
    html = f.read()

data = json.load(open('/root/.openclaw/workspace/stock-sim/data/portfolio.json'))
acc = data['account']
total_pnl = acc['total_value'] - 100000
total_pnl_pct = total_pnl / 100000 * 100

# 1. 累计收益卡片（当前是旧值 $16,005.01 +16.01% 且 class 错为 text-red-400）
html = re.sub(
    r'<div class="text-sm text-gray-400">累计收益</div>\s*<div class="text-2xl font-bold text-red-400">\$[\d,\.]+</div><div class="text-red-400 text-sm">[\+\-]?[\d,\.]+%',
    f'<div class="text-sm text-gray-400">累计收益</div>\\n                <div class="text-2xl font-bold text-green-400">${total_pnl:,.2f}</div><div class="text-green-400 text-sm">{total_pnl_pct:+.2f}%',
    html)
# fallback replace values directly
html = html.replace('$16,005.01', f'${total_pnl:,.2f}')

# 2. 持仓市值卡片 $66,004.98 -> new
html = html.replace('$66,004.98', f'${acc["market_value"]:,.2f}')

# 3. 历史净值表第一行的 note 应为最新快照（10-21），当前错误显示 10-06 的 note
note = acc['snapshots'][-1]['note']
# find the row with date 2026-10-21 and replace its note td
pat = re.compile(r'(<td class="py-2 px-4">2026-10-21</td>\s*<td class="py-2 px-4 font-bold">\$[\d,\.]+</td>\s*<td class="py-2 px-4 text-green-400">\+[\d\.]+%</td>\s*<td class="py-2 px-4 text-gray-400 text-xs">).*?(</td>)', re.S)
html, n = pat.subn(lambda m: m.group(1) + note + m.group(2), html, count=1)
print('note row fixed:', n)

with open('/root/.openclaw/workspace/stock-sim/standalone.html', 'w') as f:
    f.write(html)
print('done')
