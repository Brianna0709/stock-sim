#!/usr/bin/env python3
"""
Re-query individual sessions that might have been truncated.
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

# Sessions to re-query individually (last session in each truncated batch + zero-data session)
sessions_to_requery = [
    '367964194',  # Batch 4: 0 rows collected
    '367787858',  # Batch 6: possibly truncated (last)
    '367781264',  # Batch 7: possibly truncated (last)  
    '367869541',  # Batch 10: possibly truncated (last)
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
    
    sql_file = os.path.join(SQL_DIR, f'requery_{sid}.sql')
    with open(sql_file, 'w') as f:
        f.write(sql)
    
    print(f"\nQuerying session {sid}...")
    
    # Submit
    submit_cmd = [TALOS, 'query', 'submit', '--scene', 'SKILL', '--region', 'cn', '--sql-file', sql_file]
    result = subprocess.run(submit_cmd, capture_output=True, text=True, env=ENV)
    if result.returncode != 0:
        print(f"  ERROR submitting: {result.stderr}")
        continue
    qid = result.stdout.strip()
    
    # Wait for result
    result_cmd = [TALOS, 'query', 'result', '--qid', qid, '--wait', '--region', 'cn', '--timeout', '600']
    result = subprocess.run(result_cmd, capture_output=True, text=True, env=ENV)
    if result.returncode != 0:
        print(f"  ERROR getting result: {result.stderr}")
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
    print(f"  totalRows={batch_total}, collected={len(data_rows)}")

# Now merge with existing data
print("\n=== Merging results ===")
with open(os.path.join(SQL_DIR, 'sql2_all_results.jsonl')) as f:
    all_rows = [json.loads(l) for l in f]

print(f"Original rows: {len(all_rows)}")

# Remove old (possibly incomplete) rows for requeried sessions
requeried_sids = set(requery_results.keys())
all_rows = [r for r in all_rows if r['session_id'] not in requeried_sids]
print(f"After removing requeried sessions: {len(all_rows)}")

# Add new complete data
for sid, rows in requery_results.items():
    all_rows.extend(rows)
    print(f"  Added {len(rows)} rows for {sid}")

# Save merged
output = os.path.join(SQL_DIR, 'sql2_all_results_merged.jsonl')
with open(output, 'w') as f:
    for row in all_rows:
        f.write(json.dumps(row, ensure_ascii=False) + '\n')

print(f"\nFinal total: {len(all_rows)} rows")
print(f"Output: {output}")
