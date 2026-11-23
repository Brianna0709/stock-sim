import json

files = [
'0675dc41-3bbc-4544-b261-061fc1ea8100','ce238971-0da5-4765-9a9f-1c5e36ff1819','2920185d-99fc-4006-9569-a5bd7ce692ee','8738fadc-497d-48cd-b16b-a15d7d961d8d',
'6b40e5b1-c378-4937-8679-2cde849d0fb6','01789d15-31c3-48e8-a981-060c64907bd3','628a2a99-4512-47cc-807f-228d049e2349','28acadcd-a907-4512-82ac-cfed62e52f2a','5ec80075-6cda-429d-8b46-faf8d31885fb',
'61b0b16a-6cec-4e1a-9cea-9384369b4a39','a63ba4ce-00f1-4b75-9f25-bec08cc7b15f','daf6dd1d-d90d-482a-a48f-edc545258b0b',
'0bb07e68-2b6d-4527-9c9e-94b131787446','91ff710e-4c11-44a1-a450-f19fa63b3c35','f77d60e7-4986-4c2c-9229-67d7313d6e4d',
'3129adf6-f31a-4f46-9bc1-a35168c73ccc','2cb414c8-b0db-4f44-8116-b11d5dfa79fa','3eaacbc8-79f6-4eb4-a355-57267eef2b52',
'f2280bc5-391a-4ee8-816b-d993b726ec99','50bb3bd7-9696-4345-9958-cd33608cc029']

for fid in files:
    p = '/root/.openclaw/agents/main/sessions/%s.jsonl' % fid
    print('=' * 20, fid)
    try:
        fh = open(p)
    except Exception as e:
        print('ERR', e)
        continue
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
        if not isinstance(content, list):
            continue
        for c in content:
            if isinstance(c, dict) and c.get('type') == 'text':
                t = c.get('text', '').strip()
                if not t:
                    continue
                if role == 'user':
                    # skip cron task instructions and system-ish messages
                    if t.startswith('[cron') or t.startswith('[system') or t.startswith('Use the message tool'):
                        continue
                    print('- USER', o.get('timestamp', '')[:16], t[:400].replace('\n', ' | '))
    fh.close()
