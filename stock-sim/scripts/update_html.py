#!/usr/bin/env python3
"""Update standalone.html from portfolio.json"""
import json, os

BASE = '/root/.openclaw/workspace/stock-sim'
DATA = os.path.join(BASE, 'data', 'portfolio.json')
HTML = os.path.join(BASE, 'standalone.html')

with open(DATA, 'r') as f:
    d = json.load(f)

meta = d['meta']
acc = d['account']
pos = d['positions']
snaps = d['snapshots']
mc = d['market_context']

# Build positions rows
pos_rows = []
for ticker, p in pos.items():
    color = 'green' if p['pnl'] >= 0 else 'red'
    today_color = 'green' if p['today_chg_pct'] >= 0 else 'red'
    today_sign = '+' if p['today_chg_pct'] >= 0 else ''
    pos_rows.append(f'''        <tr class="border-t border-gray-700 hover:bg-gray-700/50">
            <td class="py-3 px-4 font-bold text-{color}-400">{ticker}</td>
            <td class="py-3 px-4">${p['cost_price']:.2f}</td>
            <td class="py-3 px-4">${p['cur_price']:.2f}</td>
            <td class="py-3 px-4">{p['shares']}</td>
            <td class="py-3 px-4">${p['market_value']:.2f}</td>
            <td class="py-3 px-4 text-{color}-400">{p['pnl_pct']:+.2f}%</td>
            <td class="py-3 px-4 text-{today_color}-400">{today_sign}{p['today_chg_pct']:.2f}%</td>
        </tr>''')

# Build snapshot rows (most recent 15)
snap_rows = []
for s in reversed(snaps[-15:]):
    color = 'green' if s['return_pct'] >= 0 else 'red'
    snap_rows.append(f'''        <tr class="border-t border-gray-700 hover:bg-gray-700/50">
            <td class="py-2 px-4">{s['date']}</td>
            <td class="py-2 px-4 font-bold">${s['total_value']:,.2f}</td>
            <td class="py-2 px-4 text-{color}-400">{s['return_pct']:+.2f}%</td>
            <td class="py-2 px-4 text-gray-400 text-xs">{s['note']}</td>
        </tr>''')

# Chart data
labels = [s['date'] for s in snaps]
values = [s['total_value'] for s in snaps]

# Return color
ret_color = 'green' if acc['total_value'] >= 100000 else 'red'
ret_sign = '+' if acc['total_value'] >= 100000 else ''
ret_pct = (acc['total_value'] - 100000) / 100000 * 100

# Market change colors
sp_color = 'green' if mc['sp500_change_pct'] >= 0 else 'red'
nas_color = 'green' if mc['nasdaq_change_pct'] >= 0 else 'red'
dow_color = 'green' if mc['dow_change_pct'] >= 0 else 'red'
sp_sign = '+' if mc['sp500_change_pct'] >= 0 else ''
nas_sign = '+' if mc['nasdaq_change_pct'] >= 0 else ''
dow_sign = '+' if mc['dow_change_pct'] >= 0 else ''

last_date = snaps[-1]['date'] if snaps else ''

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>上海巴菲特 | 美股模拟盘</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body class="bg-gray-900 text-white min-h-screen">
    <div class="container mx-auto px-4 py-8 max-w-6xl">
        <!-- Header -->
        <header class="mb-8">
            <h1 class="text-4xl font-bold bg-gradient-to-r from-yellow-400 to-yellow-600 bg-clip-text text-transparent">
                🏆 上海巴菲特
            </h1>
            <p class="text-gray-400 mt-2">美股虚拟模拟盘 | {meta['strategy']}策略</p>
            <p class="text-sm text-gray-500">最后更新: {last_date}</p>
        </header>

        <!-- Market Overview -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
            <div class="bg-gray-800 rounded-lg p-4 border border-gray-700">
                <div class="text-sm text-gray-400">标普500</div>
                <div class="text-2xl font-bold">{mc['sp500']:,.2f}</div>
                <div class="text-{sp_color}-400 text-sm">{'📈' if mc['sp500_change_pct']>=0 else '📉'} {sp_sign}{mc['sp500_change_pct']:.2f}%</div>
            </div>
            <div class="bg-gray-800 rounded-lg p-4 border border-gray-700">
                <div class="text-sm text-gray-400">纳斯达克</div>
                <div class="text-2xl font-bold">{mc['nasdaq']:,.2f}</div>
                <div class="text-{nas_color}-400 text-sm">{'📈' if mc['nasdaq_change_pct']>=0 else '📉'} {nas_sign}{mc['nasdaq_change_pct']:.2f}%</div>
            </div>
            <div class="bg-gray-800 rounded-lg p-4 border border-gray-700">
                <div class="text-sm text-gray-400">道琼斯</div>
                <div class="text-2xl font-bold">{mc['dow']:,.2f}</div>
                <div class="text-{dow_color}-400 text-sm">{'📈' if mc['dow_change_pct']>=0 else '📉'} {dow_sign}{mc['dow_change_pct']:.2f}%</div>
            </div>
        </div>
        <div class="bg-gray-800 rounded-lg p-3 mb-8 border border-gray-700 text-sm text-gray-400">
            📰 {mc['note']}
        </div>

        <!-- Account Summary -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
            <div class="bg-gray-800 rounded-lg p-4 border border-yellow-500/30">
                <div class="text-sm text-gray-400">总资产</div>
                <div class="text-2xl font-bold text-yellow-400">${acc['total_value']:,.2f}</div>
            </div>
            <div class="bg-gray-800 rounded-lg p-4 border border-gray-700">
                <div class="text-sm text-gray-400">累计收益</div>
                <div class="text-2xl font-bold text-{ret_color}-400">${acc['total_value']-100000:,.2f}</div>
                <div class="text-{ret_color}-400 text-sm">{ret_sign}{ret_pct:.2f}%</div>
            </div>
            <div class="bg-gray-800 rounded-lg p-4 border border-gray-700">
                <div class="text-sm text-gray-400">可用现金</div>
                <div class="text-2xl font-bold">${acc['cash']:,.2f}</div>
            </div>
            <div class="bg-gray-800 rounded-lg p-4 border border-gray-700">
                <div class="text-sm text-gray-400">持仓市值</div>
                <div class="text-2xl font-bold">${acc['invested']:,.2f}</div>
            </div>
        </div>

        <!-- Positions Table -->
        <div class="bg-gray-800 rounded-lg p-6 mb-8 border border-gray-700">
            <h2 class="text-xl font-bold mb-4 text-yellow-400">📊 当前持仓</h2>
            <div class="overflow-x-auto">
                <table class="w-full text-sm">
                    <thead>
                        <tr class="text-gray-400 text-left">
                            <th class="py-2 px-4">标的</th>
                            <th class="py-2 px-4">成本价</th>
                            <th class="py-2 px-4">现价</th>
                            <th class="py-2 px-4">持仓量</th>
                            <th class="py-2 px-4">市值</th>
                            <th class="py-2 px-4">持仓盈亏%</th>
                            <th class="py-2 px-4">今日涨跌%</th>
                        </tr>
                    </thead>
                    <tbody>
{'\n'.join(pos_rows)}
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Chart -->
        <div class="bg-gray-800 rounded-lg p-6 mb-8 border border-gray-700">
            <h2 class="text-xl font-bold mb-4 text-yellow-400">📈 资产走势</h2>
            <canvas id="portfolioChart" height="100"></canvas>
        </div>

        <!-- Snapshot History -->
        <div class="bg-gray-800 rounded-lg p-6 mb-8 border border-gray-700">
            <h2 class="text-xl font-bold mb-4 text-yellow-400">📜 历史净值</h2>
            <div class="overflow-x-auto">
                <table class="w-full text-sm">
                    <thead>
                        <tr class="text-gray-400 text-left">
                            <th class="py-2 px-4">日期</th>
                            <th class="py-2 px-4">总资产</th>
                            <th class="py-2 px-4">收益率</th>
                            <th class="py-2 px-4">备注</th>
                        </tr>
                    </thead>
                    <tbody>
{'\n'.join(snap_rows)}
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Footer -->
        <footer class="text-center text-gray-500 text-sm mt-8">
            <p>⚠️ 本模拟盘为虚拟交易，不构成真实投资建议</p>
            <p class="mt-1">上海巴菲特 · 万能小汪分身 🐕</p>
        </footer>
    </div>

    <script>
        const ctx = document.getElementById('portfolioChart').getContext('2d');
        new Chart(ctx, {{
            type: 'line',
            data: {{
                labels: {json.dumps(labels)},
                datasets: [{{
                    label: '总资产',
                    data: {json.dumps(values)},
                    borderColor: '#FACC15',
                    backgroundColor: 'rgba(250, 204, 21, 0.1)',
                    fill: true,
                    tension: 0.3,
                    pointRadius: 2,
                    pointHoverRadius: 5
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{ labels: {{ color: '#9CA3AF' }} }},
                    tooltip: {{
                        callbacks: {{
                            label: (ctx) => '$' + ctx.parsed.y.toLocaleString('en-US', {{minimumFractionDigits:2}})
                        }}
                    }}
                }},
                scales: {{
                    x: {{ ticks: {{ color: '#6B7280', maxTicksLimit: 10 }}, grid: {{ color: '#374151' }} }},
                    y: {{ ticks: {{ color: '#6B7280', callback: v => '$'+v.toLocaleString() }}, grid: {{ color: '#374151' }} }}
                }}
            }}
        }});
    </script>
</body>
</html>'''

with open(HTML, 'w', encoding='utf-8') as f:
    f.write(html)

print('standalone.html updated successfully')
