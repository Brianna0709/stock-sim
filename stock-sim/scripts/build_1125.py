import json, re

PPATH = '/root/.openclaw/workspace/stock-sim/data/portfolio.json'
HROOT = '/root/.openclaw/workspace/stock-sim/standalone.html'

with open(PPATH) as f:
    data = json.load(f)
acc = data['account']
mc = acc['market_context']

with open(HROOT) as f:
    html = f.read()

html = re.sub(r'最后更新: \d{4}-\d{2}-\d{2}', f"最后更新: {acc['last_update']}", html)

def setnum(html, label, value, pct):
    pat = rf'(<div class="text-sm text-gray-400">{label}</div>\s*<div class="text-2xl font-bold">)[\d,\.]+(</div>\s*<div class="text-(?:red|green)-400 text-sm">)[📉📈]\s*[-+]?[\d\.]+%'
    arrow = '📈' if pct >= 0 else '📉'
    sign = '+' if pct >= 0 else ''
    return re.sub(pat, rf'\g<1>{value:,.2f}\g<2>{arrow} {sign}{pct:.2f}%', html)

html = setnum(html, '标普500', mc['sp500'], mc['sp500_change_pct'])
html = setnum(html, '纳斯达克', mc['nasdaq'], mc['nasdaq_change_pct'])
html = setnum(html, '道琼斯', mc['dow'], mc['dow_change_pct'])

total_pnl = acc['total_value'] - 100000
total_pnl_pct = total_pnl / 100000 * 100

html = re.sub(r'(<div class="text-sm text-gray-400">总资产</div>\s*<div class="text-2xl font-bold text-yellow-400">)\$[\d,\.]+',
              f"\\g<1>${acc['total_value']:,.2f}", html)
html = re.sub(r'(<div class="text-sm text-gray-400">累计收益</div>\s*<div class="text-2xl font-bold (?:text-green-400|text-red-400)">)[-+]?\$[\d,\.]+',
              f"\\g<1>${total_pnl:,.2f}", html)
html = re.sub(r'(<div class="text-sm text-gray-400">累计收益</div>\s*<div class="text-2xl font-bold (?:text-green-400|text-red-400)">\$[\d,\.]+</div>\s*<div class="text-(?:green-400|red-400) text-sm">)[-+]?[\d\.]+%',
              f"\\g<1>{'+' if total_pnl_pct>=0 else ''}{total_pnl_pct:.2f}%", html)
html = re.sub(r'(<div class="text-sm text-gray-400">可用现金</div>\s*<div class="text-2xl font-bold">)\$[\d,\.]+',
              f"\\g<1>${acc['cash']:,.2f}", html)
html = re.sub(r'(<div class="text-sm text-gray-400">持仓市值</div>\s*<div class="text-2xl font-bold">)\$[\d,\.]+',
              f"\\g<1>${acc['invested']:,.2f}", html)

cls = 'text-green-400' if acc['daily_pnl'] >= 0 else 'text-red-400'
html = re.sub(r'(<div class="text-sm text-gray-400">当日盈亏</div>\s*<div class="text-2xl font-bold (?:text-red-400|text-green-400)">)[-+\$][\d,\.\-]+',
              f"\\g<1>${acc['daily_pnl']:,.2f}", html)
html = re.sub(r'(<div class="text-sm text-gray-400">当日盈亏</div>\s*<div class="text-2xl font-bold )(?:text-red-400|text-green-400)(">)',
              rf'\g<1>{cls}\g<2>', html)

# --- positions table rows by ticker anchor
rows = {
    'QQQ':  {'price': '$644.10', 'mv': '$16,739.13', 'pct': '+11.59%', 'chg': '-2.32%'},
    'NVDA': {'price': '$146.00', 'mv': '$12,557.34', 'pct': '-16.28%', 'chg': '-3.30%'},
    'MSFT': {'price': '$499.24', 'mv': '$26,973.54', 'pct': '+34.87%', 'chg': '-1.78%'},
}
for sym in ['QQQ', 'NVDA', 'MSFT']:
    pos = data['positions'][sym]
    r = rows[sym]
    i = html.find(f'>{sym}</td>')
    j = html.find('</tr>', i)
    seg = html[i:j]
    seg2 = seg.replace(r['price'], f"${pos['cur_price']:,.2f}")
    seg2 = seg2.replace(r['mv'], f"${pos['market_value']:,.2f}")
    seg2 = seg2.replace(r['pct'], f"{'+' if pos['unrealized_pnl_pct']>=0 else ''}{pos['unrealized_pnl_pct']:.2f}%")
    seg2 = seg2.replace(r['chg'], f"{'+' if pos['today_chg_pct']>=0 else ''}{pos['today_chg_pct']:.2f}%")
    html = html[:i] + seg2 + html[j:]

# --- news line: replace the 📰 ... </div> block
html = re.sub(r'📰[^<]*</div>',
              '📰 三大指数盘中史诗级反转：道指一度跌1105点后翻红，纳指盘中-4.6%、纳指100一度触及技术性熊市；10月核心PCE 3.3%创三年新高，12月加息预期站上90%；美国拟对14个贸易伙伴加征关税；英伟达-3.9%(盘中-9%)，Meta+3%、惠普+11%；VIX升7.3%至28.29</div>',
              html, count=1)

# --- chart arrays + snapshot table
snaps = acc['snapshots']
seen, clean = set(), []
for s in snaps:
    if s['date'] in seen:
        continue
    seen.add(s['date'])
    clean.append(s)
clean.sort(key=lambda s: s['date'])

labels = json.dumps([s['date'] for s in clean])
values = json.dumps([round(s['total_value'], 2) for s in clean])
html = re.sub(r'(const\s+chartLabels\s*=\s*)(\[.*?\])(\s*;?)', lambda m: m.group(1) + labels + m.group(3), html, flags=re.S)
html = re.sub(r'(const\s+chartData\s*=\s*)(\[.*?\])(\s*;?)', lambda m: m.group(1) + values + m.group(3), html, flags=re.S)

out = []
for s in reversed(clean[:40]):
    pct = s.get('return_pct', s.get('total_pnl_pct', 0))
    c2 = 'text-green-400' if pct >= 0 else 'text-red-400'
    out.append(
        '<tr class="border-t border-gray-700 hover:bg-gray-700/50">'
        f'<td class="py-3 px-4 text-gray-300">{s["date"]}</td>'
        f'<td class="py-3 px-4">${s["total_value"]:,.2f}</td>'
        f'<td class="py-3 px-4 {c2}">{"+" if pct>=0 else ""}{pct:.2f}%</td>'
        f'<td class="py-2 px-4 text-gray-400 text-xs">{s.get("note","")}</td></tr>'
    )
new_tbody = '<tbody>\n' + '\n'.join(out) + '\n                    </tbody>'
idx = html.find('📜 历史净值')
seg_start = html.find('<tbody>', idx)
seg_end = html.find('</tbody>', seg_start) + len('</tbody>')
html = html[:seg_start] + new_tbody + html[seg_end:]

with open(HROOT, 'w') as f:
    f.write(html)

print("standalone.html updated")
print(f"总资产 ${acc['total_value']:,.2f} 日盈亏 ${acc['daily_pnl']:,.2f} 累计 {total_pnl_pct:+.2f}% 快照 {len(clean)}")
for s in ['QQQ', 'NVDA', 'MSFT']:
    p = data['positions'][s]
    print(f"  {s}: ${p['cur_price']} ({p['today_chg_pct']:+.2f}%) mv=${p['market_value']:,.2f} pnl={p['unrealized_pnl_pct']:+.2f}%")
