with open('/root/.openclaw/workspace/stock-sim/standalone.html') as f:
    html = f.read()
old = html
html = html.replace('116005.01]', '116005.01, 116732.62]')
html = html.replace('📰 科技股分化：道指续创新高，纳指回调',
                    '📰 SpaceX财报点燃AI情绪：Q3营收+161%扭亏为盈，市值超台积电；黄仁勋GTC柏林放大招，费半+1.97%，三大指数集体收涨')
with open('/root/.openclaw/workspace/stock-sim/standalone.html', 'w') as f:
    f.write(html)
print('changed' if html != old else 'nochange')
