with open('/root/.openclaw/workspace/stock-sim/standalone.html') as f:
    html = f.read()
old = html
html = html.replace('%"></td>', '%</td>')
with open('/root/.openclaw/workspace/stock-sim/standalone.html', 'w') as f:
    f.write(html)
print('changed' if html != old else 'nochange')
