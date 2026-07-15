#!/usr/bin/env python3
"""
Re-query individual sessions from problematic batches.
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

# All sessions from B4 (except 367964194 already done), B6, B7 that might be truncated
# We re-query all of them individually to get accurate counts
sessions_to_requery = [
    # B4 - totalRows was 181
    '367794105','367820450','367929496','367780519',
    # B6 - totalRows was 107
    '367849291','367901985','367916312','367801015',
    # B7 - totalRows was 109
    '367842139','367922438','367951926','367915376',
]

requery_results = {}

for sid in sessions_to_requery:
    sql = f"""SELECT 
  session_id, 
  gmt_msg_gen, 
  is_from_phx_host, 
  valid_payload,
  get_json_object(msg_extension, '$.PHXExtensionOrderStatus') AS order_status
FROM ba_phx.phx_mdw_detail_message_sync
WHERE dt BETWEEN '20260623' AND '20260629'
  AND session_id = '{sid}'
ORDER BY session_id, gmt_msg_gen"""
    
    sql_file = os.path.join(SQL_DIR, f'requery2_{sid}.sql')
    with open(sql_file, 'w') as f:
        f.write(sql)
    
    print(f"Querying session {sid}...", end=' ')
    
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
    
    requery_results[sid] = data_rows
    print(f"total={batch_total}, collected={len(data_rows)}")

# Merge
print("\n=== Merging ===")
with open(os.path.join(SQL_DIR, 'sql2_all_results_merged.jsonl')) as f:
    all_rows = [json.loads(l) for l in f]

print(f"Before: {len(all_rows)}")

requeried_sids = set(requery_results.keys())
all_rows = [r for r in all_rows if r['session_id'] not in requeried_sids]
print(f"After removing: {len(all_rows)}")

for sid, rows in requery_results.items():
    all_rows.extend(rows)

output = os.path.join(SQL_DIR, 'sql2_final.jsonl')
with open(output, 'w') as f:
    for row in all_rows:
        f.write(json.dumps(row, ensure_ascii=False) + '\n')

print(f"Final total: {len(all_rows)} rows")
print(f"Output: {output}")
