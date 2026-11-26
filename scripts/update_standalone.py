import json, re

with open('/mnt/openclaw/.openclaw/workspace/stock-sim/data/portfolio.json', 'r') as f:
    data = json.load(f)

with open('/mnt/openclaw/.openclaw/workspace/stock-sim/standalone.html', 'r') as f:
    html = f.read()

mc = data['market_context']
acc = data['account']

# Update last update date
html = re.sub(r'最后更新: \d{4}-\d{2}-\d{2}', f'最后更新: {acc["last_update"]}', html)

# Update market overview numbers
html = re.sub(
    r'(<div class="text-sm text-gray-400">标普500</div>\s*<div class="text-2xl font-bold">)[\d,\.]+(</div>\s*<div class="text-(red|green)-400 text-sm">)[📉📈]\s*[\-+]?[\d\.]+%',
    f'\\g<1>{mc["sp500"]:,.2f}\\g<2>📉 {mc["sp500_change_pct"]:.2f}%',
    html
)
html = re.sub(
    r'(<div class="text-sm text-gray-400">纳斯达克</div>\s*<div class="text-2xl font-bold">)[\d,\.]+(</div>\s*<div class="text-(red|green)-400 text-sm">)[📉📈]\s*[\-+]?[\d\.]+%',
    f'\\g<1>{mc["nasdaq"]:,.2f}\\g<2>📉 {mc["nasdaq_change_pct"]:.2f}%',
    html
)
html = re.sub(
    r'(<div class="text-sm text-gray-400">道琼斯</div>\s*<div class="text-2xl font-bold">)[\d,\.]+(</div>\s*<div class="text-(red|green)-400 text-sm">)[📉📈]\s*[\-+]?[\d\.]+%',
    f'\\g<1>{mc["dow"]:,.2f}\\g<2>📉 {mc["dow_change_pct"]:.2f}%',
    html
)

# Fallback direct replacements for market data
html = html.replace('7,785.76', f"{mc['sp500']:,.2f}")
html = html.replace('7,745.06', f"{mc['sp500']:,.2f}")
html = html.replace('26,729.16', f"{mc['nasdaq']:,.2f}")
html = html.replace('26,644.91', f"{mc['nasdaq']:,.2f}")
html = html.replace('53,732.41', f"{mc['dow']:,.2f}")
html = html.replace('53,459.78', f"{mc['dow']:,.2f}")

# Update news context line
html = re.sub(r'📰 .*?</div>', f'📰 美债收益率创19年新高，半导体板块集体回调，地缘风险持续</div>', html)

# Update account summary values
total_pnl = acc['total_value'] - 100000
total_pnl_pct = (total_pnl / 100000) * 100

# Replace specific dollar amounts (account summary section)
html = re.sub(
    r'(<div class="text-sm text-gray-400">总资产</div>\s*<div class="text-2xl font-bold text-yellow-400">)\$[\d,\.]+',
    f'\\g<1>${acc["total_value"]:,.2f}',
    html
)
html = re.sub(
    r'(<div class="text-sm text-gray-400">累计收益</div>\s*<div class="text-2xl font-bold text-green-400">)\$[\d,\.]+',
    f'\\g<1>${total_pnl:,.2f}',
    html
)
html = re.sub(
    r'(<div class="text-green-400 text-sm">)\+[\d\.]+%',
    f'\\g<1>{"+" if total_pnl_pct >= 0 else ""}{total_pnl_pct:.2f}%',
    html
)
html = re.sub(
    r'(<div class="text-sm text-gray-400">可用现金</div>\s*<div class="text-2xl font-bold">)\$[\d,\.]+',
    f'\\g<1>${acc["cash"]:,.2f}',
    html
)
html = re.sub(
    r'(<div class="text-sm text-gray-400">持仓市值</div>\s*<div class="text-2xl font-bold">)\$[\d,\.]+',
    f'\\g<1>${acc["invested"]:,.2f}',
    html
)

# Also do direct replacements as fallback
html = html.replace('$115,131.27', f"${acc['total_value']:,.2f}")
html = html.replace('$114,296.66', f"${acc['total_value']:,.2f}")
html = html.replace('$15,131.27', f"${total_pnl:,.2f}")
html = html.replace('$14,296.66', f"${total_pnl:,.2f}")
html = html.replace('+15.13%', f"{'+' if total_pnl_pct >= 0 else ''}{total_pnl_pct:.2f}%")
html = html.replace('+14.30%', f"{'+' if total_pnl_pct >= 0 else ''}{total_pnl_pct:.2f}%")
html = html.replace('$64,296.63', f"${acc['invested']:,.2f}")
html = html.replace('$64,131.24', f"${acc['invested']:,.2f}")

# Update daily PNL in performance section
html = re.sub(
    r'(<div class="text-sm text-gray-400">当日盈亏</div>\s*<div class="text-2xl font-bold text-red-400">)\$[\-\d,\.]+',
    f'\\g<1>${acc["daily_pnl"]:,.2f}',
    html
)
html = html.replace('$-834.61', f"${acc['daily_pnl']:,.2f}")
html = html.replace('$-171.93', f"${acc['daily_pnl']:,.2f}")

# Update position table values
for sym in ['QQQ', 'NVDA', 'MSFT']:
    pos = data['positions'][sym]
    
    # Find and replace position row values
    # Cost price
    old_cost = { 'QQQ': '577.18', 'NVDA': '174.40', 'MSFT': '370.17' }[sym]
    # Current price
    old_price_14 = { 'QQQ': '731.07', 'NVDA': '225.16', 'MSFT': '480.53' }[sym]
    old_price_17 = { 'QQQ': '729.87', 'NVDA': '225.16', 'MSFT': '480.53' }[sym]
    
    html = html.replace(f'${old_price_14}', f"${pos['cur_price']:,.2f}")
    html = html.replace(f'${old_price_17}', f"${pos['cur_price']:,.2f}")
    
    # Market values (old)
    old_mv_14 = { 'QQQ': '19,012.84', 'NVDA': '19,365.83', 'MSFT': '25,962.65' }[sym]
    old_mv_17 = { 'QQQ': '18,968.15', 'NVDA': '19,365.83', 'MSFT': '25,962.65' }[sym]
    
    html = html.replace(f'${old_mv_14}', f"${pos['market_value']:,.2f}")
    html = html.replace(f'${old_mv_17}', f"${pos['market_value']:,.2f}")
    
    # PNL values
    old_pnl_14 = { 'QQQ': '4,012.86', 'NVDA': '4,365.83', 'MSFT': '5,962.66' }[sym]
    old_pnl_17 = { 'QQQ': '3,968.17', 'NVDA': '4,365.83', 'MSFT': '5,962.66' }[sym]
    
    html = html.replace(f'${old_pnl_14}', f"${pos['unrealized_pnl']:,.2f}")
    html = html.replace(f'${old_pnl_17}', f"${pos['unrealized_pnl']:,.2f}")
    
    # PNL pct
    old_pct_14 = { 'QQQ': '+26.78%', 'NVDA': '+29.11%', 'MSFT': '+29.81%' }[sym]
    old_pct_17 = { 'QQQ': '+26.45%', 'NVDA': '+29.11%', 'MSFT': '+29.81%' }[sym]
    new_pct = f"{'+' if pos['unrealized_pnl_pct'] >= 0 else ''}{pos['unrealized_pnl_pct']:.2f}%"
    
    html = html.replace(old_pct_14, new_pct)
    html = html.replace(old_pct_17, new_pct)

with open('/mnt/openclaw/.openclaw/workspace/stock-sim/standalone.html', 'w') as f:
    f.write(html)

print("✅ standalone.html 已更新")
print(f"   总资产: ${acc['total_value']:,.2f}")
print(f"   当日盈亏: ${acc['daily_pnl']:,.2f}")
