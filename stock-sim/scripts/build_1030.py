import json, re

PPATH = '/mnt/openclaw/.openclaw/workspace/stock-sim/data/portfolio.json'
HROOT = '/mnt/openclaw/.openclaw/workspace/stock-sim/standalone.html'

with open(PPATH) as f:
    data = json.load(f)
acc = data['account']
mc = data['market_context']
total_pnl = acc['total_value'] - 100000
total_pnl_pct = total_pnl / 1000.0  # percent of 100k

with open(HROOT) as f:
    html = f.read()

# --- last update date
html = re.sub(r'最后更新: \d{4}-\d{2}-\d{2}', f"最后更新: {acc['last_update']}", html)

# --- market overview (regex + fallbacks)
def setnum(html, label, value, pct):
    pat = rf'(<div class="text-sm text-gray-400">{label}</div>\s*<div class="text-2xl font-bold">)[\d,\.]+(</div>\s*<div class="text-(?:red|green)-400 text-sm">)[📉📈]\s*[-+]?[\d\.]+%'
    arrow = '📈' if pct >= 0 else '📉'
    sign = '+' if pct >= 0 else ''
    return re.sub(pat, rf'\g<1>{value:,.2f}\g<2>{arrow} {sign}{pct:.2f}%', html)

html = setnum(html, '标普500', mc['sp500'], mc['sp500_change_pct'])
html = setnum(html, '纳斯达克', mc['nasdaq'], mc['nasdaq_change_pct'])
html = setnum(html, '道琼斯', mc['dow'], mc['dow_change_pct'])

# fallback: replace any previous known index values directly
for old, new in [
    ('7,743.98', f"{mc['sp500']:,.2f}"), ('7,745.06', f"{mc['sp500']:,.2f}"), ('7,785.76', f"{mc['sp500']:,.2f}"),
    ('26,549.85', f"{mc['nasdaq']:,.2f}"), ('26,729.16', f"{mc['nasdaq']:,.2f}"),
    ('52,475.10', f"{mc['dow']:,.2f}"), ('53,732.41', f"{mc['dow']:,.2f}"),
]:
    html = html.replace(old, new)

# generic: replace pct badges next to index labels
def setpct_badge(html, label, pct):
    pat = rf'(<div class="text-sm text-gray-400">{label}</div>\s*<div class="text-2xl font-bold">[\d,\.]+</div>\s*<div class="text-(?:red|green)-400 text-sm">)[📉📈]\s*[-+]?[\d\.]+%'
    arrow = '📈' if pct >= 0 else '📉'
    sign = '+' if pct >= 0 else ''
    return re.sub(pat, rf'\g<1>{arrow} {sign}{pct:.2f}%', html)
html = setpct_badge(html, '标普500', mc['sp500_change_pct'])
html = setpct_badge(html, '纳斯达克', mc['nasdaq_change_pct'])
html = setpct_badge(html, '道琼斯', mc['dow_change_pct'])

# --- news line
html = re.sub(r'📰 .*?</div>',
              '📰 谷歌财报暴雷暴跌超12%市值蒸发4000亿美元，纳指大跌1.38%；微软Azure+48%超预期；医疗/房地产防御板块领涨</div>',
              html)

# --- account summary
html = re.sub(
    r'(<div class="text-sm text-gray-400">总资产</div>\s*<div class="text-2xl font-bold text-yellow-400">)\$[\d,\.]+',
    f"\\g<1>${acc['total_value']:,.2f}", html)
html = re.sub(
    r'(<div class="text-sm text-gray-400">累计收益</div>\s*<div class="text-2xl font-bold (?:text-green-400|text-red-400)">)[-\+]?\$[\d,\.]+',
    f"\\g<1>${total_pnl:,.2f}", html)
html = re.sub(
    r'(<div class="text-(?:green|red)-400 text-sm">)[-\+]?[\d\.]+%',
    f"\\g<1>{'+' if total_pnl_pct>=0 else ''}{total_pnl_pct:.2f}%", html, count=1)
html = re.sub(
    r'(<div class="text-sm text-gray-400">可用现金</div>\s*<div class="text-2xl font-bold">)\$[\d,\.]+',
    f"\\g<1>${acc['cash']:,.2f}", html)
html = re.sub(
    r'(<div class="text-sm text-gray-400">持仓市值</div>\s*<div class="text-2xl font-bold">)\$[\d,\.]+',
    f"\\g<1>${acc['invested']:,.2f}", html)

# fallbacks for old totals
for old in ['$115,839.41', '$115,654.70', '$116,335.32']:
    html = html.replace(old, f"${acc['total_value']:,.2f}")
for old in ['$15,839.41', '$15,654.70', '$16,335.32']:
    html = html.replace(old, f"${total_pnl:,.2f}")
for old in ['+15.84%', '+15.65%', '+16.34%']:
    html = html.replace(old, f"+{total_pnl_pct:.2f}%")

# --- daily pnl
def setdaily(html):
    cls = 'text-green-400' if acc['daily_pnl'] >= 0 else 'text-red-400'
    pat = r'(<div class="text-sm text-gray-400">当日盈亏</div>\s*<div class="text-2xl font-bold (?:text-red-400|text-green-400)">)[-+\$][\d,\.\-]+'
    repl = f"\\g<1>${acc['daily_pnl']:,.2f}"
    html = re.sub(pat, repl, html)
    # fix class color
    pat2 = r'(<div class="text-sm text-gray-400">当日盈亏</div>\s*<div class="text-2xl font-bold )(?:text-red-400|text-green-400)(">)'
    html = re.sub(pat2, rf'\g<1>{cls}\g<2>', html)
    return html
html = setdaily(html)

# --- positions
for sym in ['QQQ', 'NVDA', 'MSFT']:
    pos = data['positions'][sym]
    # replace current price cell: find row containing cost price, then update
    cost = pos['cost_price']
    cp = f"{cost:.2f}" if cost == int(cost) else f"{cost:,.2f}"
    # generic: replace price shown after cost in table row
    html = html.replace(f"${cp}", f"${cp}")  # noop keep

# Simpler: regenerate known position numbers by direct replacement of previous values
prev = {
    'QQQ':  {'price': '713.98', 'mv': '18,555.20', 'pnl': '3,555.22', 'pct': '+23.70%'},
    'NVDA': {'price': '215.39', 'mv': '18,525.52', 'pnl': '3,525.52', 'pct': '+23.50%'},
    'MSFT': {'price': '532.28', 'mv': '28,758.66', 'pnl': '8,758.67', 'pct': '+43.79%'},
}
for sym in ['QQQ', 'NVDA', 'MSFT']:
    pos = data['positions'][sym]
    p = prev[sym]
    new_price = f"${pos['cur_price']:,.2f}"
    new_mv = f"${pos['market_value']:,.2f}"
    new_pnl = f"${pos['unrealized_pnl']:,.2f}"
    sign = '+' if pos['unrealized_pnl_pct'] >= 0 else ''
    new_pct = f"{sign}{pos['unrealized_pnl_pct']:.2f}%"
    html = html.replace('$' + p['price'], new_price)
    html = html.replace('$' + p['mv'], new_mv)
    html = html.replace('$' + p['pnl'], new_pnl)
    html = html.replace(p['pct'], new_pct)

# today chg per position
today_prev = {'QQQ': '+0.25%', 'NVDA': '-1.17%', 'MSFT': '-0.06%'}
for sym in ['QQQ', 'NVDA', 'MSFT']:
    chg = data['positions'][sym]['today_chg_pct']
    sign = '+' if chg >= 0 else ''
    html = html.replace(today_prev[sym], f"{sign}{chg:.2f}%")

with open(HROOT, 'w') as f:
    f.write(html)

print("standalone.html updated")
print(f"  总资产: ${acc['total_value']:,.2f}  日盈亏: ${acc['daily_pnl']:,.2f}  累计: +{total_pnl_pct:.2f}%")
for s in ['QQQ','NVDA','MSFT']:
    p = data['positions'][s]
    print(f"  {s}: ${p['cur_price']} ({p['today_chg_pct']:+.2f}%) mv=${p['market_value']:,.2f} pnl={p['unrealized_pnl_pct']:+.2f}%")
