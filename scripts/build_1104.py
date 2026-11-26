import json, re

PPATH = '/root/.openclaw/workspace/stock-sim/data/portfolio.json'
HROOT = '/root/.openclaw/workspace/stock-sim/standalone.html'

with open(PPATH) as f:
    data = json.load(f)
acc = data['account']
mc = data['account']['market_context']
total_pnl = acc['total_value'] - 100000
total_pnl_pct = total_pnl / 1000.0

with open(HROOT) as f:
    html = f.read()

# --- last update date
html = re.sub(r'最后更新: \d{4}-\d{2}-\d{2}', f"最后更新: {acc['last_update']}", html)

# --- market overview
def setnum(html, label, value, pct):
    pat = rf'(<div class="text-sm text-gray-400">{label}</div>\s*<div class="text-2xl font-bold">)[\d,\.]+(</div>\s*<div class="text-(?:red|green)-400 text-sm">)[📉📈]\s*[-+]?[\d\.]+%'
    arrow = '📈' if pct >= 0 else '📉'
    sign = '+' if pct >= 0 else ''
    return re.sub(pat, rf'\g<1>{value:,.2f}\g<2>{arrow} {sign}{pct:.2f}%', html)

html = setnum(html, '标普500', mc['sp500'], mc['sp500_change_pct'])
html = setnum(html, '纳斯达克', mc['nasdaq'], mc['nasdaq_change_pct'])
html = setnum(html, '道琼斯', mc['dow'], mc['dow_change_pct'])

for old, new in [
    ('7,743.98', f"{mc['sp500']:,.2f}"), ('7,569.30', f"{mc['sp500']:,.2f}"),
    ('26,549.85', f"{mc['nasdaq']:,.2f}"), ('25,372.01', f"{mc['nasdaq']:,.2f}"),
    ('52,475.10', f"{mc['dow']:,.2f}"), ('51,786.72', f"{mc['dow']:,.2f}"), ('51,786.30', f"{mc['dow']:,.2f}"),
]:
    html = html.replace(old, new)

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
              '📰 中期选举民主党横扫参众两院，道指暴涨1569点创2025年4月以来最佳单日；但AI硬件遭抛售(费半-3.8%)，油价崩盘超8%(中东停战希望)</div>',
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

for old in ['$115,610.34', '$114,079.49', '$115,839.41']:
    html = html.replace(old, f"${acc['total_value']:,.2f}")
for old in ['$14,079.49', '$15,610.34', '$15,839.41']:
    html = html.replace(old, f"${total_pnl:,.2f}")
for old in ['+14.08%', '+15.61%', '+15.84%']:
    html = html.replace(old, f"+{total_pnl_pct:.2f}%")

# --- daily pnl
cls = 'text-green-400' if acc['daily_pnl'] >= 0 else 'text-red-400'
pat = r'(<div class="text-sm text-gray-400">当日盈亏</div>\s*<div class="text-2xl font-bold (?:text-red-400|text-green-400)">)[-+\$][\d,\.\-]+'
html = re.sub(pat, f"\\g<1>${acc['daily_pnl']:,.2f}", html)
pat2 = r'(<div class="text-sm text-gray-400">当日盈亏</div>\s*<div class="text-2xl font-bold )(?:text-red-400|text-green-400)(">)'
html = re.sub(pat2, rf'\g<1>{cls}\g<2>', html)

# --- positions table rows (grep-derived values as of 2026-11-03 build)
prev = {
    'QQQ':  {'price': '715.34',  'mv': '18555.20', 'pnl': '3555.22', 'pct': '+23.94%', 'chg': '-1.42%'},
    'NVDA': {'price': '213.66',  'mv': '18525.52', 'pnl': '3525.52', 'pct': '+22.51%', 'chg': '-0.80%'},
    'MSFT': {'price': '530.14',  'mv': '28758.66', 'pnl': '8758.67', 'pct': '+43.22%', 'chg': '-0.16%'},
}
for sym in ['QQQ', 'NVDA', 'MSFT']:
    pos = data['positions'][sym]
    p = prev[sym]
    sign = '+' if pos['unrealized_pnl_pct'] >= 0 else ''
    html = html.replace('$' + p['price'], f"${pos['cur_price']:,.2f}")
    if p['mv']:
        html = html.replace('$' + p['mv'], f"${pos['market_value']:,.2f}")
        html = html.replace('$' + p['pnl'], f"${pos['unrealized_pnl']:,.2f}")
        html = html.replace(p['pct'], f"{sign}{pos['unrealized_pnl_pct']:.2f}%")
    html = html.replace(p['chg'], f"{'+' if pos['today_chg_pct']>=0 else ''}{pos['today_chg_pct']:.2f}%")

with open(HROOT, 'w') as f:
    f.write(html)

print("standalone.html updated")
print(f"  总资产: ${acc['total_value']:,.2f}  日盈亏: ${acc['daily_pnl']:,.2f}  累计: +{total_pnl_pct:.2f}%")
for s in ['QQQ','NVDA','MSFT']:
    p = data['positions'][s]
    print(f"  {s}: ${p['cur_price']} ({p['today_chg_pct']:+.2f}%) mv=${p['market_value']:,.2f} pnl={p['unrealized_pnl_pct']:+.2f}%")
