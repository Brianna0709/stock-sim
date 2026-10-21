import re

with open('/root/.openclaw/workspace/stock-sim/standalone.html', 'r') as f:
    html = f.read()

# Fix double $$ -> $
html = html.replace('$$', '$')
# Fix broken class attribute: <td class="py-3 px-4 text-green-400">+25.64%">text-green-400>+1.05%
# Pattern: cls">pct">cls2">pct2%  -> cls">pct%</td><td class="py-3 px-4 cls2">pct2%
html = re.sub(
    r'<td class="py-3 px-4 (text-green-400|text-red-400)">(.*?%)">(text-green-400|text-red-400)>(.*?%)',
    r'<td class="py-3 px-4 \1">\2</td><td class="py-3 px-4 \3">\4',
    html)

with open('/root/.openclaw/workspace/stock-sim/standalone.html', 'w') as f:
    f.write(html)

print('done')
