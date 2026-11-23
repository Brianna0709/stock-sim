import json, re

PPATH = '/root/.openclaw/workspace/stock-sim/data/portfolio.json'
HROOT = '/root/.openclaw/workspace/stock-sim/standalone.html'

with open(PPATH) as f:
    data = json.load(f)
acc = data['account']
mc = acc['market_context']
total_pnl = acc['total_value'] - 100000
total_pnl_pct = total_pnl / 100000 * 100

with open(HROOT) as f:
    html = f.read()

# --- last update date
html = re.sub(r'最后更新: \d{4}-\d{2}-\d{2}', f"最后更新: {acc['last_update']}", html)

# --- market overview (numbers + pct badges)
def setnum(html, label, value, pct):
    pat = rf'(<div class="text-sm text-gray-400">{label}</div>\s*<div class="text-2xl font-bold">)[\d,\.]+(</div>\s*<div class="text-(?:red|green)-400 text-sm">)[📉📈]\s*[-+]?[\d\.]+%'
    arrow = '📈' if pct >= 0 else '📉'
    sign = '+' if pct >= 0 else ''
    return re.sub(pat, rf'\g<1>{value:,.2f}\g<2>{arrow} {sign}{pct:.2f}%', html)

html = setnum(html, '标普500', mc['sp500'], mc['sp500_change_pct'])
html = setnum(html, '纳斯达克', mc['nasdaq'], mc['nasdaq_change_pct'])
html = setnum(html, '道琼斯', mc['dow'], mc['dow_change_pct'])

# --- news line
html = re.sub(r'📰 三大指数齐跌超2%：七巨头全线走低，英伟达六连跌收$146；Anthropic上市首日+17%市值1.27万亿抽血新云链(Nebius-9.39%/CoreWeave-6.10%)；AMD遭做空机构Hunterbrook指控跌8%；美联储纪要鹰派+美元走强，AI交易全面降温</div>',
              '📰 黄仁勋辞任后英伟达连续两日拖累大盘(市值跌破4万亿美元)，汇丰下调评级；费半-3.43%芯片股遭抛售，Meta+2.90%领涨七巨头；资金继续从AI硬件流向软件与防御</div>',
              html)

# --- account summary
html = re.sub(
    r'(<div class="text-sm text-gray-400">总资产</div>\s*<div class="text-2xl font-bold text-yellow-400">)\$[\d,\.]+',
    f"\\g<1>${acc['total_value']:,.2f}", html)
html = re.sub(
    r'(<div class="text-sm text-gray-400">累计收益</div>\s*<div class="text-2xl font-bold (?:text-green-400|text-red-400)">)[-\+]?\$[\d,\.]+',
    f"\\g<1>${total_pnl:,.2f}", html)
html = re.sub(
    r'(<div class="text-sm text-gray-400">累计收益</div>\s*<div class="text-2xl font-bold (?:text-green-400|text-red-400)">\$[\d,\.]+</div>\s*<div class="text-(?:green-400|red-400) text-sm">)[-\+]?[\d\.]+%',
    f"\\g<1>{'+' if total_pnl_pct>=0 else ''}{total_pnl_pct:.2f}%", html)
html = re.sub(
    r'(<div class="text-sm text-gray-400">可用现金</div>\s*<div class="text-2xl font-bold">)\$[\d,\.]+',
    f"\\g<1>${acc['cash']:,.2f}", html)
html = re.sub(
    r'(<div class="text-sm text-gray-400">持仓市值</div>\s*<div class="text-2xl font-bold">)\$[\d,\.]+',
    f"\\g<1>${acc['invested']:,.2f}", html)

# --- daily pnl
cls = 'text-green-400' if acc['daily_pnl'] >= 0 else 'text-red-400'
pat = r'(<div class="text-sm text-gray-400">当日盈亏</div>\s*<div class="text-2xl font-bold (?:text-red-400|text-green-400)">)[-+\$][\d,\.\-]+'
html = re.sub(pat, f"\\g<1>${acc['daily_pnl']:,.2f}", html)
pat2 = r'(<div class="text-sm text-gray-400">当日盈亏</div>\s*<div class="text-2xl font-bold )(?:text-red-400|text-green-400)(">)'
html = re.sub(pat2, rf'\g<1>{cls}\g<2>', html)

# --- positions table rows (current values as of 2026-11-12 build)
prev = {
    'QQQ':  {'price': '659.51', 'mv': '17,139.61', 'pnl': '2,139.63', 'pct': '+14.26%', 'chg': '+0.39%'},
    'NVDA': {'price': '150.96', 'mv': '12,983.95', 'pnl': '-2,016.05', 'pct': '-13.44%',  'chg': '-2.89%'},
    'MSFT': {'price': '508.29', 'mv': '27,462.50', 'pnl': '7,462.51', 'pct': '+37.31%', 'chg': '+0.40%'},
}
for sym in ['QQQ', 'NVDA', 'MSFT']:
    pos = data['positions'][sym]
    p = prev[sym]
    html = html.replace('$' + p['price'], f"${pos['cur_price']:,.2f}")
    html = html.replace('$' + p['mv'], f"${pos['market_value']:,.2f}")
    html = html.replace('$' + p['pnl'], f"${pos['unrealized_pnl']:,.2f}")
    sign = '+' if pos['unrealized_pnl_pct'] >= 0 else ''
    html = html.replace(p['pct'], f"{sign}{pos['unrealized_pnl_pct']:.2f}%")
    html = html.replace(p['chg'], f"{'+' if pos['today_chg_pct']>=0 else ''}{pos['today_chg_pct']:.2f}%")

# --- rebuild chart arrays + snapshot table rows from account snapshots
snaps = acc['snapshots']
seen = set()
clean = []
for s in snaps:
    if s['date'] in seen:
        continue
    seen.add(s['date'])
    clean.append(s)
clean.sort(key=lambda s: s['date'])

labels = json.dumps([s['date'] for s in clean])
values = json.dumps([round(s['total_value'], 2) for s in clean])

def arr_repl(m):
    return m.group(1) + labels + m.group(3)
html = re.sub(r'(const\s+chartLabels\s*=\s*)(\[.*?\])((\s*;?))', lambda m: m.group(1) + labels + m.group(3), html, flags=re.S)
html = re.sub(r'(const\s+chartData\s*=\s*)(\[.*?\])(\s*;?)', lambda m: m.group(1) + values + m.group(3), html, flags=re.S)

# snapshot history table rows
rows = []
for s in reversed(clean[:40]):
    pct = s.get('return_pct', s.get('total_pnl_pct', 0))
    cls2 = 'text-green-400' if pct >= 0 else 'text-red-400'
    note = s.get('note', '')
    rows.append(
        '<tr class="border-t border-gray-700 hover:bg-gray-700/50">'
        f'<td class="py-3 px-4 text-gray-300">{s["date"]}</td>'
        f'<td class="py-3 px-4">${s["total_value"]:,.2f}</td>'
        f'<td class="py-3 px-4 {cls2}">{"+" if pct>=0 else ""}{pct:.2f}%</td>'
        f'<td class="py-2 px-4 text-gray-400 text-xs">{note}</td></tr>'
    )
new_tbody = '<tbody>\n' + '\n'.join(rows) + '\n                    </tbody>'
# replace the snapshot history table tbody (the one containing 历史净值 section)
idx = html.find('📜 历史净值')
seg_start = html.find('<tbody>', idx)
seg_end = html.find('</tbody>', seg_start) + len('</tbody>')
html = html[:seg_start] + new_tbody + html[seg_end:]

with open(HROOT, 'w') as f:
    f.write(html)

print("standalone.html updated")
print(f"  总资产: ${acc['total_value']:,.2f}  日盈亏: ${acc['daily_pnl']:,.2f}  累计: {'+' if total_pnl_pct>=0 else ''}{total_pnl_pct:.2f}%  快照数: {len(clean)}")
for s in ['QQQ','NVDA','MSFT']:
    p = data['positions'][s]
    print(f"  {s}: ${p['cur_price']} ({p['today_chg_pct']:+.2f}%) mv=${p['market_value']:,.2f} pnl={p['unrealized_pnl_pct']:+.2f}%")
