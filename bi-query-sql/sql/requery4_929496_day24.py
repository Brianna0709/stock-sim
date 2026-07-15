#!/usr/bin/env python3
"""
Re-query session 367929496 for day 20260624 split by time periods.
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

# Split by time: first half and second half of day
time_ranges = [
    ("00:00:00", "14:00:00", "morning"),
    ("14:00:00", "23:59:59", "afternoon"),
]

all_rows_day24 = []

for start_time, end_time, label in time_ranges:
    sql = f"""SELECT 
  session_id, 
  gmt_msg_gen, 
  is_from_phx_host, 
  valid_payload,
  get_json_object(msg_extension, '$.PHXExtensionOrderStatus') AS order_status
FROM ba_phx.phx_mdw_detail_message_sync
WHERE dt = '20260624'
  AND session_id = '{SID}'
  AND gmt_msg_gen >= '2026-06-24 {start_time}'
  AND gmt_msg_gen < '2026-06-24 {end_time}'
ORDER BY gmt_msg_gen"""
    
    sql_file = os.path.join(SQL_DIR, f'requery4_{label}.sql')
    with open(sql_file, 'w') as f:
        f.write(sql)
    
    print(f"{label} ({start_time}-{end_time})...", end=' ')
    
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
    all_rows_day24.extend(data_rows)

print(f"\nDay 20260624 total collected: {len(all_rows_day24)}")

# Merge: replace day 20260624 data for this session, keep day 20260627 data
with open(os.path.join(SQL_DIR, 'sql2_complete.jsonl')) as f:
    all_rows = [json.loads(l) for l in f]

# Remove all 367929496 rows
other_rows = [r for r in all_rows if r['session_id'] != SID]
session_rows_other_days = [r for r in all_rows if r['session_id'] == SID and '2026-06-24' not in r.get('gmt_msg_gen','')]

print(f"Other sessions: {len(other_rows)}")
print(f"Session {SID} other days: {len(session_rows_other_days)}")

final_rows = other_rows + session_rows_other_days + all_rows_day24
final_rows.sort(key=lambda r: (r['session_id'], r.get('gmt_msg_gen', '')))

output = os.path.join(SQL_DIR, 'sql2_complete_v2.jsonl')
with open(output, 'w') as f:
    for row in final_rows:
        f.write(json.dumps(row, ensure_ascii=False) + '\n')

print(f"Grand total: {len(final_rows)} rows")
print(f"Output: {output}")
