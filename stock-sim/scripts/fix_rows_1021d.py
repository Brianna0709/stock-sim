with open('/root/.openclaw/workspace/stock-sim/standalone.html') as f:
    html = f.read()
old = html
html = html.replace('">text-green-400>', '"></td><td class="py-3 px-4 text-green-400">')
html = html.replace('">text-red-400>', '"></td><td class="py-3 px-4 text-red-400">')
with open('/root/.openclaw/workspace/stock-sim/standalone.html', 'w') as f:
    f.write(html)
print('changed' if html != old else 'nochange')
