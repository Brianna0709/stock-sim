import json, re

with open('/mnt/openclaw/.openclaw/workspace/stock-sim/data/portfolio.json', 'r') as f:
    data = json.load(f)

with open('/mnt/openclaw/.openclaw/workspace/stock-sim/standalone.html', 'r') as f:
    html = f.read()

acc = data['account']
mc = data['market_context']
today = acc['last_update']

# 最后更新日期
html = re.sub(r'最后更新: \d{4}-\d{2}-\d{2}', f'最后更新: {today}', html)

# 新闻行
html = re.sub(r'📰 .*?</div>',
              '📰 道指涨529点创历史新高(3M/诺格财报超预期)；油价回落WTI -1.8%；科技巨头财报前观望，纳指微跌0.02%，盘后期货全线上涨</div>',
              html, count=1)

total_pnl = acc['total_value'] - 100000
total_pnl_pct = total_pnl / 100000 * 100

def sub(pattern, repl, s):
    return re.sub(pattern, repl, s, count=1, flags=re.S)

# 账户摘要
html = sub(r'(<div class="text-sm text-gray-400">总资产</div>\s*<div class="text-2xl font-bold text-yellow-400">)\$[\d,\.]+',
           f'\\g<1>${acc["total_value"]:,.2f}', html)
html = sub(r'(<div class="text-sm text-gray-400">累计收益</div>\s*<div class="text-2xl font-bold text-green-400">)\$[\d,\.]+',
           f'\\g<1>${total_pnl:,.2f}', html)
html = sub(r'(<div class="text-sm text-gray-400">累计收益率</div>\s*<div class="text-2xl font-bold text-green-400">)[\+\-]?[\d,\.]+%',
           f'\\g<1>{total_pnl_pct:+.2f}%', html)
html = sub(r'(<div class="text-sm text-gray-400">可用现金</div>\s*<div class="text-2xl font-bold text-blue-400">)\$[\d,\.]+',
           f'\\g<1>${acc["cash"]:,.2f}', html)

# 市场概览
html = sub(r'(<div class="text-sm text-gray-400">标普500</div>\s*<div class="text-2xl font-bold">)[\d,\.]+(</div>\s*<div class="text-(?:red|green)-400 text-sm">)(?:📉|📈)\s*[\-+]?[\d\.]+%',
           f'\\g<1>{mc["sp500"]:,.2f}\\g<2>{"📈" if mc["sp500_change_pct"]>=0 else "📉"} {mc["sp500_change_pct"]:+.2f}%', html)
html = sub(r'(<div class="text-sm text-gray-400">纳斯达克</div>\s*<div class="text-2xl font-bold">)[\d,\.]+(</div>\s*<div class="text-(?:red|green)-400 text-sm">)(?:📉|📈)\s*[\-+]?[\d\.]+%',
           f'\\g<1>{mc["nasdaq"]:,.2f}\\g<2>{"📈" if mc["nasdaq_change_pct"]>=0 else "📉"} {mc["nasdaq_change_pct"]:+.2f}%', html)
html = sub(r'(<div class="text-sm text-gray-400">道琼斯</div>\s*<div class="text-2xl font-bold">)[\d,\.]+(</div>\s*<div class="text-(?:red|green)-400 text-sm">)(?:📉|📈)\s*[\-+]?[\d\.]+%',
           f'\\g<1>{mc["dow"]:,.2f}\\g<2>{"📈" if mc["dow_change_pct"]>=0 else "📉"} {mc["dow_change_pct"]:+.2f}%', html)

# 持仓行
for sym, pos in data['positions'].items():
    pnl_cls = 'text-green-400' if pos['unrealized_pnl_pct'] >= 0 else 'text-red-400'
    day_cls = 'text-green-400' if pos['today_chg_pct'] >= 0 else 'text-red-400'
    day_str = f"{pos['today_chg_pct']:+.2f}%"
    row_pat = re.compile(
        r'(<td class="py-3 px-4 font-bold">' + re.escape(sym) + r'</td>\s*'
        r'<td class="py-3 px-4">)\$[\d,\.]+(</td>\s*'
        r'<td class="py-3 px-4">)[\d\.]+(</td>\s*'
        r'<td class="py-3 px-4">\$)[\d,\.]+(</td>\s*'
        r'<td class="py-3 px-4 )(?:text-green-400|text-red-400)(">)[\+\-]?[\d,\.]+%(</td>\s*'
        r'<td class="py-3 px-4 )(?:text-green-400|text-red-400)(">)', re.S)
    repl = (f"\\g<1>${pos['cur_price']:,.2f}\\g<2>{pos['shares']}\\g<3>${pos['market_value']:,.2f}\\g<4>{pnl_cls}>"
            f"{pos['unrealized_pnl_pct']:+.2f}%\\g<5>{day_cls}>{day_str}\\g<6>")
    html, n = row_pat.subn(repl, html)
    print(sym, 'row replaced:', n)

# 历史净值表：插入最新快照行到 tbody 开头
note = data['snapshots'][0]['note']
new_row = (f'\n        <tr class="border-t border-gray-700 hover:bg-gray-700/50">\n'
           f'            <td class="py-2 px-4">{today}</td>\n'
           f'            <td class="py-2 px-4 font-bold">${acc["total_value"]:,.2f}</td>\n'
           f'            <td class="py-2 px-4 {"text-green-400" if total_pnl_pct>=0 else "text-red-400"}">{total_pnl_pct:+.2f}%</td>\n'
           f'            <td class="py-2 px-4 text-gray-400 text-xs">{note}</td>\n'
           f'        </tr>')
html = sub(r'(历史净值</h2>\s*<div class="overflow-x-auto">\s*<table class="w-full text-sm">\s*<thead>.*?</thead>\s*<tbody>)',
           f'\\g<1>{new_row}', html)

# Chart labels/data：从 account snapshots 重建（按日期升序、去重保留最后）
snaps = sorted({s['date']: s for s in acc['snapshots']}.values(), key=lambda s: s['date'])
labels = json.dumps([s['date'] for s in snaps], ensure_ascii=False)
vals = json.dumps([s['total_value'] for s in snaps])
html = re.sub(r'labels: \[.*?\]', f'labels: {labels}', html, count=1, flags=re.S)
html = re.sub(r'data: \[100000[^\]]*\]', f'data: {vals}', html, count=1)

with open('/mnt/openclaw/.openclaw/workspace/stock-sim/standalone.html', 'w') as f:
    f.write(html)

print('standalone.html updated:', today, f"${acc['total_value']:,.2f}", f"{total_pnl_pct:+.2f}%")
