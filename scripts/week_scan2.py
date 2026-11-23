import json, glob, os

out = open('/root/.openclaw/workspace/scripts/week_user_msgs.txt', 'w')
files = glob.glob('/root/.openclaw/agents/main/sessions/*.jsonl')
rows = []
for f in files:
    try:
        with open(f) as fh:
            first = json.loads(fh.readline())
            ts = first.get('timestamp', '')[:10]
    except Exception:
        continue
    rows.append((ts, f))
rows.sort()
for ts, f in rows:
    if not ('2026-11-01' <= ts <= '2026-11-07'):
        continue
    with open(f) as fh:
        for line in fh:
            try:
                o = json.loads(line)
            except Exception:
                continue
            if o.get('type') != 'message':
                continue
            m = o.get('message', {})
            if m.get('role') != 'user':
                continue
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
                if not t or t.startswith('[cron') or t.startswith('Current time') or t.startswith('Use the message tool'):
                    continue
                if t.startswith('[') and 'cron' in t[:30]:
                    continue
                out.write('%s %s :: %s\n' % (ts, o.get('timestamp', '')[11:16], t[:500].replace('\n', ' | ')))
out.close()
print('done')
