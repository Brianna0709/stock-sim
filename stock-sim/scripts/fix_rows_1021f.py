import re
with open('/root/.openclaw/workspace/stock-sim/standalone.html') as f:
    html = f.read()
# Match: <td class="...">+25.64%"></td>  (attribute ends with % then ">, empty content, </td>)
# i.e. the td tag is: <td class="py-3 px-4 text-green-400">+25.64%">  then </td>
html = re.sub(
    r'<td class="py-3 px-4 text-(?:green|red)-400">([\+\-]?[\d,\.]+%)"></td>\s*(<td class="py-3 px-4 text-(?:green|red)-400">[\+\-]?[\d,\.]+%</td>)',
    r'<td class="py-3 px-4">\1</td>\1x\2',
    html)
with open('/root/.openclaw/workspace/stock-sim/standalone.html', 'w') as f:
    f.write(html)
print('ok')
