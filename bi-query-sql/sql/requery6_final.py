#!/usr/bin/env python3
import subprocess, json, os

SQL_DIR = '/root/.openclaw/workspace/bi-query-sql/sql'
TALOS = os.path.expanduser('~/.talos/bin/talos')
ENV = dict(os.environ)
ENV['SKILL_NAME'] = 'bi-query-sql'
ENV['SKILL_ID'] = '2453'
ENV['SKILL_VERSION'] = 'V24'

SID = '367929496'

splits = [
    ("gmt_msg_gen >= '2026-06-24 21:30:00' AND gmt_msg_gen < '2026-06-24 22:00:00'", "2130_2200"),
    ("gmt_msg_gen >= '2026-06-24 22:00:00'", "after2200"),
]

all_rows_split = []

for condition, label in splits:
    sql = f"""SELECT 
  session_id, gmt_msg_gen, is_from_phx_host, valid_payload,
  get_json_object(msg_extension, '$.PHXExtensionOrderStatus') AS order_status
FROM ba_phx.phx_mdw_detail_message_sync
WHERE dt = '20260624' AND session_id = '{SID}' AND {condition}
ORDER BY gmt_msg_gen"""
    
    sql_file = os.path.join(SQL_DIR, f'rq6_{label}.sql')
    with open(sql_file, 'w') as f:
        f.write(sql)
    
    print(f"{label}...", end=' ')
    r = subprocess.run([TALOS,'query','submit','--scene','SKILL','--region','cn','--sql-file',sql_file], capture_output=True, text=True, env=ENV)
    if r.returncode != 0:
        print(f"ERR: {r.stderr}"); continue
    qid = r.stdout.strip()
    
    r = subprocess.run([TALOS,'query','result','--qid',qid,'--wait','--region','cn','--timeout','600'], capture_output=True, text=True, env=ENV)
    if r.returncode != 0:
        print(f"ERR: {r.stderr}"); continue
    
    lines = r.stdout.strip().split('\n')
    meta = json.loads(lines[0])
    rows = []
    for line in lines[2:]:
        try:
            obj = json.loads(line)
            if 'session_id' in obj: rows.append(obj)
        except: pass
    
    print(f"total={meta.get('totalRows',0)}, got={len(rows)}")
    all_rows_split.extend(rows)

print(f"\nSplit total: {len(all_rows_split)}")

# Merge: take v3, remove session 367929496 day24 after 21:30, add new splits
with open(os.path.join(SQL_DIR, 'sql2_complete_v3.jsonl')) as f:
    all_rows = [json.loads(l) for l in f]

# Keep everything except this session's after-2130 data on day 24
kept = []
for r in all_rows:
    if r['session_id'] == SID and '2026-06-24' in r.get('gmt_msg_gen','') and r['gmt_msg_gen'] >= '2026-06-24 21:30:00':
        continue
    kept.append(r)

kept.extend(all_rows_split)
kept.sort(key=lambda r: (r['session_id'], r.get('gmt_msg_gen', '')))

# Deduplicate by (session_id, gmt_msg_gen, valid_payload)
seen = set()
deduped = []
for r in kept:
    key = (r['session_id'], r.get('gmt_msg_gen',''), r.get('valid_payload',''))
    if key not in seen:
        seen.add(key)
        deduped.append(r)

output = os.path.join(SQL_DIR, 'sql2_final_complete.jsonl')
with open(output, 'w') as f:
    for row in deduped:
        f.write(json.dumps(row, ensure_ascii=False) + '\n')

print(f"Final total (deduped): {len(deduped)} rows")
print(f"Output: {output}")
