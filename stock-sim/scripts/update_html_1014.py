import json, re

DATA = '/root/.openclaw/workspace/stock-sim/data/portfolio.json'
HTML = '/mnt/openclaw/.openclaw/workspace/stock-sim/standalone.html'

with open(DATA) as f:
    data = json.load(f)
with open(HTML) as f:
    html = f.read()

acc = data['account']
mc = data['market_context']
today = acc['last_update']

html = re.sub(r'最后更新: \d{4}-\d{2}-\d{2}', f'最后更新: {today}', html)

# market overview cards
html = re.sub(
    r'(<div class="text-sm text-gray-400">标普500</div>\s*<div class="text-2xl font-bold">)[\d,\.]+(</div>\s*<div class="text-(?:red|green)-400 text-sm">)[📉📈]\s*[\-+]?[\d\.]+%',
    lambda m: f'{m.group(1)}{mc["sp500"]:,.2f}{m.group(2)}📉 {mc["sp500_change_pct"]:.2f}%',
    html, count=1)
html = re.sub(
    r'(<div class="text-sm text-gray-400">纳斯达克</div>\s*<div class="text-2xl font-bold">)[\d,\.]+(</div>\s*<div class="text-(?:red|green)-400 text-sm">)[📉📈]\s*[\-+]?[\d\.]+%',
    lambda m: f'{m.group(1)}{mc["nasdaq"]:,.2f}{m.group(2)}📉 {mc["nasdaq_change_pct"]:.2f}%',
    html, count=1)
html = re.sub(
    r'(<div class="text-sm text-gray-400">道琼斯</div>\s*<div class="text-2xl font-bold">)[\d,\.]+(</div>\s*<div class="text-(?:red|green)-400 text-sm">)[📉📈]\s*[\-+]?[\d\.]+%',
    lambda m: f'{m.group(1)}{mc["dow"]:,.2f}{m.group(2)}📉 {mc["dow_change_pct"]:.2f}%',
    html, count=1)

news = '📰 9月CPI同比3.7%超预期，加息担忧+美债收益率跳升，费半-4.3%六连跌；苹果逆势+0.5%市值破5万亿美元，防御板块领涨'
html = re.sub(r'📰 .*?</div>', news + '</div>', html, count=1)

total_pnl = acc['total_value'] - 100000
total_pnl_pct = total_pnl / 100000 * 100
sign = '+' if total_pnl_pct >= 0 else ''

def sub1(pattern, repl, s):
    return re.sub(pattern, repl, s, count=1)

html = sub1(r'(<div class="text-sm text-gray-400">总资产</div>\s*<div class="text-2xl font-bold text-yellow-400">)\$[\d,\.]+',
            lambda m: f'{m.group(1)}${acc["total_value"]:,.2f}', html)
html = sub1(r'(<div class="text-sm text-gray-400">累计收益</div>\s*<div class="text-2xl font-bold text-green-400">)\$[\d,\.]+',
            lambda m: f'{m.group(1)}${total_pnl:,.2f}', html)
# 累计收益颜色：下跌日改红
html = sub1(r'<div class="text-2xl font-bold text-green-400">\$16,884\.29</div>\s*<div class="text-green-400 text-sm">\+18\.41%',
            f'<div class="text-2xl font-bold text-red-400">${total_pnl:,.2f}</div><div class="text-red-400 text-sm">{sign}{total_pnl_pct:.2f}%', html)
html = sub1(r'<div class="text-green-400 text-sm">\+18\.41%', f'<div class="text-red-400 text-sm">{sign}{total_pnl_pct:.2f}%', html)
html = sub1(r'(<div class="text-sm text-gray-400">可用现金</div>\s*<div class="text-2xl font-bold">)\$[\d,\.]+',
            lambda m: f'{m.group(1)}${acc["cash"]:,.2f}', html)
html = sub1(r'(<div class="text-sm text-gray-400">持仓市值</div>\s*<div class="text-2xl font-bold">)\$[\d,\.]+',
            lambda m: f'{m.group(1)}${acc["invested"]:,.2f}', html)

# 当日盈亏
html = sub1(r'(<div class="text-sm text-gray-400">当日盈亏</div>\s*<div class="text-2xl font-bold text-(?:red|green)-400">)\$[\-\d,\.]+',
            lambda m: f'{m.group(1)}${acc["daily_pnl"]:,.2f}', html)

# positions table
for sym in ['QQQ', 'NVDA', 'MSFT']:
    pos = data['positions'][sym]
    row_pat = re.compile(
        r'(<td class="py-3 px-4 font-bold text-(?:green|red)-400">' + sym + r'</td>\s*'
        r'<td class="py-3 px-4">\$[\d,\.]+</td>\s*)'
        r'<td class="py-3 px-4">\$[\d,\.]+</td>\s*'
        r'(<td class="py-3 px-4">[\d\.]+</td>\s*)'
        r'<td class="py-3 px-4">\$[\d,\.]+</td>\s*'
        r'<td class="py-3 px-4 text-(?:green|red)-400">[+\-][\d\.]+%</td>\s*'
        r'<td class="py-3 px-4 text-(?:green|red)-400">[+\-][\d\.]+%</td>')
    pnl_cls = 'green' if pos['pnl_pct'] >= 0 else 'red'
    chg_cls = 'green' if pos['today_chg_pct'] >= 0 else 'red'
    new_row = (f'\\g<1><td class="py-3 px-4">${pos["cur_price"]:,.2f}</td>'
               f'\\g<2><td class="py-3 px-4">${pos["market_value"]:,.2f}</td>'
               f'<td class="py-3 px-4 text-{pnl_cls}-400">{"+" if pos["pnl_pct"]>=0 else ""}{pos["pnl_pct"]:.2f}%</td>'
               f'<td class="py-3 px-4 text-{chg_cls}-400">{"+" if pos["today_chg_pct"]>=0 else ""}{pos["today_chg_pct"]:.2f}%</td>')
    html, n = row_pat.subn(new_row, html, count=1)
    if n != 1:
        print(f'WARN: position row {sym} not replaced (n={n})')

# history table: insert today's row after <tbody> in history section
note = acc['snapshots'][-1]['note']
note_esc = note.replace('|', '|')
hist_row = (f'<tr class="border-t border-gray-700 hover:bg-gray-700/50">\n'
            f'            <td class="py-2 px-4">{today}</td>\n'
            f'            <td class="py-2 px-4 font-bold">${acc["total_value"]:,.2f}</td>\n'
            f'            <td class="py-2 px-4 {"text-green-400" if total_pnl_pct>=0 else "text-red-400"}">{sign}{total_pnl_pct:.2f}%</td>\n'
            f'            <td class="py-2 px-4 text-gray-400 text-xs">{note}</td>\n'
            f'        </tr>\n')
hist_marker = re.search(r'📜 历史净值.*?<tbody>\s*\n', html, re.S)
if hist_marker:
    idx = hist_marker.end()
    html = html[:idx] + hist_row + html[idx:]
else:
    print('WARN: history tbody not found')

# chart labels & data: append today
m = re.search(r'labels: \[(.*?)\]', html)
labels = m.group(1)
if f'"{today}"' not in labels:
    html = html.replace(labels, labels.rstrip() + f', "{today}"', 1)
m = re.search(r'data: \[(.*?)\]', html)
vals = m.group(1)
if str(acc['snapshots'][-1]['total_value']) not in vals:
    html = html.replace(vals, vals.rstrip() + f', {acc["snapshots"][-1]["total_value"]}', 1)

with open(HTML, 'w') as f:
    f.write(html)

print('HTML updated OK')
