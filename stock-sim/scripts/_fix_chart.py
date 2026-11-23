import json, re

PPATH = '/root/.openclaw/workspace/stock-sim/data/portfolio.json'
HROOT = '/root/.openclaw/workspace/stock-sim/standalone.html'

with open(PPATH) as f:
    data = json.load(f)
snaps = data['account']['snapshots']
seen = set(); clean = []
for s in snaps:
    if s['date'] in seen:
        continue
    seen.add(s['date']); clean.append(s)
clean.sort(key=lambda s: s['date'])
labels = json.dumps([s['date'] for s in clean])
values = json.dumps([round(s['total_value'], 2) for s in clean])

with open(HROOT) as f:
    html = f.read()

# chart arrays (inline Chart config)
html = re.sub(r'(labels:\s*)\[.*?\](,)',
              lambda m: m.group(1) + labels + m.group(2), html, count=1, flags=re.S)
html = re.sub(r"(data:\s*)\[.*?(\],\n\s+borderColor)",
              lambda m: m.group(1) + values + m.group(2), html, count=1, flags=re.S)

# snapshot history table rows
rows = []
for s in reversed(clean[:40]):
    pct = s.get('return_pct', s.get('total_pnl_pct', 0))
    cls2 = 'text-green-400' if pct >= 0 else 'text-red-400'
    rows.append(
        '<tr class="border-t border-gray-700 hover:bg-gray-700/50">'
        f'<td class="py-3 px-4 text-gray-300">{s["date"]}</td>'
        f'<td class="py-3 px-4">${s["total_value"]:,.2f}</td>'
        f'<td class="py-3 px-4 {cls2}">{"+" if pct>=0 else ""}{pct:.2f}%</td>'
        f'<td class="py-2 px-4 text-gray-400 text-xs">{s.get("note","")}</td></tr>'
    )
new_tbody = '<tbody>\n' + '\n'.join(rows) + '\n                    </tbody>'
idx = html.find('📜 历史净值')
seg_start = html.find('<tbody>', idx)
seg_end = html.find('</tbody>', seg_start) + len('</tbody>')
html = html[:seg_start] + new_tbody + html[seg_end:]

with open(HROOT, 'w') as f:
    f.write(html)
print('done, snapshots:', len(clean))
