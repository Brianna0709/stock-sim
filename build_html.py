#!/usr/bin/env python3
"""Build standalone HTML with latest portfolio data"""
import json

# Read portfolio
with open('/root/.openclaw/workspace/stock-sim/data/portfolio.json', 'r') as f:
    portfolio = json.load(f)

# Extract data
market = portfolio['market_context']
account = portfolio['account']
positions = portfolio['positions']
snapshots = portfolio['snapshots']

# Calculate totals
total_pnl = sum(p['pnl'] for p in positions.values())
total_return_pct = ((account['total_value'] - 100000) / 100000) * 100

# Format numbers
def fmt_money(n): return f"${n:,.2f}"
def fmt_pct(n): return f"{n:+.2f}%"
def fmt_shares(n): return f"{n:.2f}"

# Generate position rows
pos_rows = ""
for ticker, p in positions.items():
    color = "green" if p['today_chg_pct'] >= 0 else "red"
    arrow = "📈" if p['today_chg_pct'] >= 0 else "📉"
    pos_rows += f'''                        <tr class="border-b border-gray-700">
                            <td class="py-3 font-bold">{ticker}</td>
                            <td class="py-3">{fmt_shares(p['shares'])}</td>
                            <td class="py-3">${p['cost_price']:.2f}</td>
                            <td class="py-3">${p['cur_price']:.2f}</td>
                            <td class="py-3">{fmt_money(p['market_value'])}</td>
                            <td class="py-3 text-green-400">{fmt_money(p['pnl'])} ({fmt_pct(p['pnl_pct'])})</td>
                            <td class="py-3 text-{color}-400">{arrow} {fmt_pct(p['today_chg_pct'])}</td>
                        </tr>
'''

# Generate chart data
labels = [s['date'] for s in snapshots]
values = [s['total_value'] for s in snapshots]
labels_js = json.dumps(labels)
values_js = json.dumps(values)

# Generate trade rows
trades = portfolio['trades'][::-1]  # Reverse for display
trade_rows = ""
for t in trades:
    if t['type'] == 'init':
        trade_rows += f'''                <div class="flex justify-between items-center py-2 border-b border-gray-700">
                    <span class="text-gray-400">{t['date']}</span>
                    <span>🚀 {t['note']}</span>
                    <span class="font-bold">{fmt_money(t['amount'])}</span>
                </div>
'''
    elif t['type'] == 'buy':
        trade_rows += f'''                <div class="flex justify-between items-center py-2 border-b border-gray-700">
                    <span class="text-gray-400">{t['date']}</span>
                    <span>🟢 买入 {t['ticker']} × {fmt_shares(t['shares'])}</span>
                    <span class="font-bold"><span class='text-green-400'>-{fmt_money(t['amount'])}</span></span>
                </div>
'''

# Build HTML
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
            <p class="text-gray-400 mt-2">美股虚拟模拟盘 | 中线稳健成长策略</p>
            <p class="text-sm text-gray-500">最后更新: 2026-05-11</p>
        </header>

        <!-- Market Overview -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
            <div class="bg-gray-800 rounded-lg p-4 border border-gray-700">
                <div class="text-sm text-gray-400">标普500</div>
                <div class="text-2xl font-bold">{market['sp500']:,.2f}</div>
                <div class="{'text-green-400' if market['sp500_change_pct'] >= 0 else 'text-red-400'} text-sm">{'📈' if market['sp500_change_pct'] >= 0 else '📉'} {fmt_pct(market['sp500_change_pct'])}</div>
            </div>
            <div class="bg-gray-800 rounded-lg p-4 border border-gray-700">
                <div class="text-sm text-gray-400">纳斯达克</div>
                <div class="text-2xl font-bold">{market['nasdaq']:,.2f}</div>
                <div class="{'text-green-400' if market['nasdaq_change_pct'] >= 0 else 'text-red-400'} text-sm">{'📈' if market['nasdaq_change_pct'] >= 0 else '📉'} {fmt_pct(market['nasdaq_change_pct'])}</div>
            </div>
            <div class="bg-gray-800 rounded-lg p-4 border border-gray-700">
                <div class="text-sm text-gray-400">道琼斯</div>
                <div class="text-2xl font-bold">{market['dow']:,.2f}</div>
                <div class="{'text-green-400' if market['dow_change_pct'] >= 0 else 'text-red-400'} text-sm">{'📈' if market['dow_change_pct'] >= 0 else '📉'} {fmt_pct(market['dow_change_pct'])}</div>
            </div>
        </div>

        <!-- Account Summary -->
        <div class="bg-gradient-to-r from-blue-900 to-blue-800 rounded-lg p-6 mb-8 border border-blue-700">
            <h2 class="text-xl font-bold mb-4">💰 账户概览</h2>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div>
                    <div class="text-sm text-blue-200">总资产</div>
                    <div class="text-2xl font-bold">{fmt_money(account['total_value'])}</div>
                </div>
                <div>
                    <div class="text-sm text-blue-200">累计收益</div>
                    <div class="text-2xl font-bold text-green-400">+{fmt_money(account['total_value'] - 100000)}</div>
                </div>
                <div>
                    <div class="text-sm text-blue-200">收益率</div>
                    <div class="text-2xl font-bold text-green-400">+{total_return_pct:.2f}%</div>
                </div>
                <div>
                    <div class="text-sm text-blue-200">可用现金</div>
                    <div class="text-2xl font-bold">{fmt_money(account['cash'])}</div>
                </div>
            </div>
        </div>

        <!-- Positions -->
        <div class="bg-gray-800 rounded-lg p-6 mb-8 border border-gray-700">
            <h2 class="text-xl font-bold mb-4">📊 当前持仓</h2>
            <div class="overflow-x-auto">
                <table class="w-full">
                    <thead>
                        <tr class="text-left text-gray-400 border-b border-gray-700">
                            <th class="pb-3">标的</th>
                            <th class="pb-3">股数</th>
                            <th class="pb-3">成本价</th>
                            <th class="pb-3">现价</th>
                            <th class="pb-3">市值</th>
                            <th class="pb-3">持仓盈亏</th>
                            <th class="pb-3">今日涨跌</th>
                        </tr>
                    </thead>
                    <tbody>
{pos_rows}                    </tbody>
                </table>
            </div>
        </div>

        <!-- Performance Chart -->
        <div class="bg-gray-800 rounded-lg p-6 mb-8 border border-gray-700">
            <h2 class="text-xl font-bold mb-4">📈 收益曲线</h2>
            <canvas id="performanceChart" height="100"></canvas>
        </div>

        <!-- Trade History -->
        <div class="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <h2 class="text-xl font-bold mb-4">📝 交易记录</h2>
            <div class="space-y-2">
{trade_rows}            </div>
        </div>

        <footer class="mt-8 text-center text-gray-500 text-sm">
            <p>⚠️ 本模拟盘为虚拟交易，不构成真实投资建议</p>
            <p class="mt-1">数据仅供参考，投资有风险，入市需谨慎</p>
        </footer>
    </div>

    <script>
        // Performance Chart
        const ctx = document.getElementById('performanceChart').getContext('2d');
        const chartData = {{
            labels: {labels_js},
            datasets: [{{
                label: '总资产',
                data: {values_js},
                borderColor: '#10b981',
                backgroundColor: 'rgba(16, 185, 129, 0.1)',
                fill: true,
                tension: 0.4
            }}]
        }};
        
        new Chart(ctx, {{
            type: 'line',
            data: chartData,
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{ display: false }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: false,
                        grid: {{ color: '#374151' }},
                        ticks: {{ color: '#9ca3af' }}
                    }},
                    x: {{
                        grid: {{ display: false }},
                        ticks: {{ color: '#9ca3af' }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
'''

# Write HTML
with open('/root/.openclaw/workspace/stock-sim/standalone.html', 'w') as f:
    f.write(html)

print("✅ Standalone HTML updated successfully!")
print(f"📊 Total Value: {fmt_money(account['total_value'])}")
print(f"📈 Total Return: +{total_return_pct:.2f}%")
