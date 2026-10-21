import re
with open('/root/.openclaw/workspace/stock-sim/standalone.html') as f:
    html = f.read()
# Remove empty td cells left behind: <td class="py-3 px-4 text-green-400">+25.64%"></td>
html = re.sub(r'(<td class="py-3 px-4 text-(?:green|red)-400">[\+\-]?[\d,\.]+%)">', r'\1', html)
html = re.sub(r'(<td class="py-3 px-4 text-(?:green|red)-400">[\+\-]?[\d,\.]+%)"></td>', r'\1</td>', html)
with open('/root/.openclaw/workspace/stock-sim/standalone.html', 'w') as f:
    f.write(html)
print('ok')
