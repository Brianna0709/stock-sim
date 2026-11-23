import json, sys

fid = sys.argv[1]
p = '/root/.openclaw/agents/main/sessions/%s.jsonl' % fid
fh = open(p)
n = 0
for line in fh:
    try:
        o = json.loads(line)
    except Exception:
        continue
    if o.get('type') != 'message':
        continue
    m = o.get('message', {})
    role = m.get('role')
    content = m.get('content')
    texts = []
    if isinstance(content, list):
        for c in content:
            if isinstance(c, dict) and c.get('type') == 'text':
                texts.append(c.get('text', ''))
    elif isinstance(content, str):
        texts.append(content)
    for t in texts:
        t = t.strip()
        if t:
            n += 1
            print('(%s) %s :: %s' % (role, o.get('timestamp', '')[:16], t[:260].replace('\n', ' | ')))
print('--- total texts:', n)
