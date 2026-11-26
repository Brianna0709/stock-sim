import json, re

PPATH = '/root/.openclaw/workspace/stock-sim/data/portfolio.json'
HROOT = '/root/.openclaw/workspace/stock-sim/standalone.html'

data = json.load(open(PPATH))
acc = data['account']
html = open(HROOT).read()

snaps = acc['snapshots']
seen, clean = set(), []
for s in snaps:
    if s['date'] in seen:
        continue
    seen.add(s['date'])
    clean.append(s)
clean.sort(key=lambda s: s['date'])
clean = clean[-70:]

labels = json.dumps([s['date'] for s in clean])
values = json.dumps([round(s['total_value'], 2) for s in clean])

html = re.sub(r'(\n\s*labels: )\[.*?\](\s*,\n)', lambda m: m.group(1) + labels + m.group(2), html, count=1, flags=re.S)
html = re.sub(r'(\n\s+data: )\[[\d\., ]+\](\s*,\n)', lambda m: m.group(1) + values + m.group(2), html, count=1, flags=re.S)

open(HROOT, 'w').write(html)
print('chart ok', len(clean), clean[-1])
print(labels[-80:])
print(values[-80:])
