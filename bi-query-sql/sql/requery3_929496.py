#!/usr/bin/env python3
"""
Re-query session 367929496 by splitting across days to avoid 100-row preview limit.
"""
import subprocess
import json
import os

SQL_DIR = '/root/.openclaw/workspace/bi-query-sql/sql'
TALOS = os.path.expanduser('~/.talos/bin/talos')

ENV = dict(os.environ)
ENV['SKILL_NAME'] = 'bi-query-sql'
ENV['SKILL_ID'] = '2453'
ENV['SKILL_VERSION'] = 'V24'

SID = '367929496'
days = ['20260623','20260624','20260625','20260626','20260627','20260628','20260629']

all_session_rows = []

for day in days:
    sql = f"""SELECT 
  session_id, 
  gmt_msg_gen, 
  is_from_phx_host, 
  valid_payload,
  get_json_object(msg_extension, '$.PHXExtensionOrderStatus') AS order_status
FROM ba_phx.phx_mdw_detail_message_sync
WHERE dt = '{day}'
  AND session_id = '{SID}'
ORDER BY gmt_msg_gen"""
    
    sql_file = os.path.join(SQL_DIR, f'requery3_{day}.sql')
    with open(sql_file, 'w') as f:
        f.write(sql)
    
    print(f"Day {day}...", end=' ')
    
    submit_cmd = [TALOS, 'query', 'submit', '--scene', 'SKILL', '--region', 'cn', '--sql-file', sql_file]
    result = subprocess.run(submit_cmd, capture_output=True, text=True, env=ENV)
    if result.returncode != 0:
        print(f"SUBMIT ERROR: {result.stderr}")
        continue
    qid = result.stdout.strip()
    
    result_cmd = [TALOS, 'query', 'result', '--qid', qid, '--wait', '--region', 'cn', '--timeout', '600']
    result = subprocess.run(result_cmd, capture_output=True, text=True, env=ENV)
    if result.returncode != 0:
        print(f"RESULT ERROR: {result.stderr}")
        continue
    
    lines = result.stdout.strip().split('\n')
    meta = json.loads(lines[0])
    batch_total = meta.get('totalRows', 0)
    
    data_rows = []
    for line in lines[2:]:
        try:
            row = json.loads(line)
            if 'session_id' in row:
                data_rows.append(row)
        except:
            pass
    
    print(f"total={batch_total}, collected={len(data_rows)}")
    all_session_rows.extend(data_rows)

print(f"\nTotal rows for session {SID}: {len(all_session_rows)}")

# Merge with final data
with open(os.path.join(SQL_DIR, 'sql2_final.jsonl')) as f:
    all_rows = [json.loads(l) for l in f]

# Remove old rows for this session
all_rows = [r for r in all_rows if r['session_id'] != SID]
all_rows.extend(all_session_rows)

# Sort by session_id, gmt_msg_gen
all_rows.sort(key=lambda r: (r['session_id'], r.get('gmt_msg_gen', '')))

output = os.path.join(SQL_DIR, 'sql2_complete.jsonl')
with open(output, 'w') as f:
    for row in all_rows:
        f.write(json.dumps(row, ensure_ascii=False) + '\n')

print(f"Grand total: {len(all_rows)} rows")
print(f"Output: {output}")
