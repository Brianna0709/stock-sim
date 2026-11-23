import json, glob

files = [
'0675dc41-3bbc-4544-b261-061fc1ea8100','ce238971-0da5-4765-9a9f-1c5e36ff1819','2920185d-99fc-4006-9569-a5bd7ce692ee',
'01789d15-31c3-48e8-a981-060c64907bd3','628a2a99-4512-47cc-807f-228d049e2349','28acadcd-a907-4512-82ac-cfed62e52f2a','5ec80075-6cda-429d-8b46-faf8d31885fb',
'61b0b16a-6cec-4e1a-9cea-9384369b4a39','a63ba4ce-00f1-4b75-9f25-bec08cc7b15f','daf6dd1d-d90d-482a-a48f-edc545258b0b',
'0bb07e68-2b6d-4527-9c9e-94b131787446','91ff710e-4c11-44a1-a450-f19fa63b3c35','f77d60e7-4986-4c2c-9229-67d7313d6e4d',
'3129adf6-f31a-4f46-9bc1-a35168c73ccc','2cb414c8-b0db-4f44-8116-b11d5dfa79fa','3eaacbc8-79f6-4eb4-a355-57267eef2b52']
out = open('/root/.openclaw/workspace/scripts/week_assistant.txt', 'w')
for fid in files:
    p = '/root/.openclaw/agents/main/sessions/%s.jsonl' % fid
    first_line = None
    msgs = []
    with open(p) as fh:
        for line in fh:
            try:
                o = json.loads(line)
            except Exception:
                continue
            if first_line is None and o.get('type') == 'message':
                first_line = o
            if o.get('type') != 'message':
                continue
            m = o.get('message', {})
            if m.get('role') != 'assistant':
                continue
            content = m.get('content')
            texts = []
            if isinstance(content, list):
                for c in content:
                    if isinstance(c, dict) and c.get('type') == 'text':
                        texts.append(c.get('text', ''))
            for t in texts:
                if t.strip():
                    msgs.append(t.strip())
    out.write('=' * 20 + ' ' + fid + '\n')
    if first_line is not None:
        c = first_line.get('message', {}).get('content')
        t0 = ''
        if isinstance(c, list):
            for x in c:
                if isinstance(x, dict) and x.get('type') == 'text':
                    t0 = x.get('text', '')
                    break
        out.write('FIRST_USER: ' + t0[:200].replace('\n', ' | ') + '\n')
    for t in msgs[-3:]:
        out.write('ASSISTANT: ' + t[:800].replace('\n', ' | ') + '\n')
out.close()
print('done')
