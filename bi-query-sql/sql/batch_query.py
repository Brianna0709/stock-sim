#!/usr/bin/env python3
"""
Batch query: Split 50 session_ids into batches, submit each batch,
collect all results into a single JSONL file.
"""
import subprocess
import json
import os
import time

SESSION_IDS = [
    '367827473','367798336','367817280','367928108','367799650',
    '367812499','367837343','367885346','367848160','367779318',
    '367880409','367964502','367803573','367794261','367916339',
    '367794105','367820450','367929496','367780519','367964194',
    '366843494','367836910','367907655','367868297','367809980',
    '367849291','367901985','367916312','367801015','367787858',
    '367842139','367922438','367951926','367915376','367781264',
    '367791551','367917197','367848671','367844978','367849599',
    '367863957','367959530','367784524','367845871','366158923',
    '367798913','367799689','367111328','367799342','367869541'
]

BATCH_SIZE = 5
SQL_DIR = '/root/.openclaw/workspace/bi-query-sql/sql'
OUTPUT_FILE = os.path.join(SQL_DIR, 'sql2_all_results.jsonl')

ENV = dict(os.environ)
ENV['SKILL_NAME'] = 'bi-query-sql'
ENV['SKILL_ID'] = '2453'
ENV['SKILL_VERSION'] = 'V24'

TALOS = os.path.expanduser('~/.talos/bin/talos')

all_rows = []
total_reported = 0

batches = [SESSION_IDS[i:i+BATCH_SIZE] for i in range(0, len(SESSION_IDS), BATCH_SIZE)]
print(f"Total sessions: {len(SESSION_IDS)}, Batch size: {BATCH_SIZE}, Total batches: {len(batches)}")

for batch_idx, batch in enumerate(batches):
    in_clause = ",".join(f"'{sid}'" for sid in batch)
    sql = f"""SELECT 
  session_id, 
  gmt_msg_gen, 
  is_from_phx_host, 
  valid_payload,
  get_json_object(msg_extension, '$.PHXExtensionOrderStatus') AS order_status
FROM ba_phx.phx_mdw_detail_message_sync
WHERE dt BETWEEN '20260623' AND '20260629'
  AND session_id IN ({in_clause})
ORDER BY session_id, gmt_msg_gen"""
    
    sql_file = os.path.join(SQL_DIR, f'batch_{batch_idx}.sql')
    with open(sql_file, 'w') as f:
        f.write(sql)
    
    print(f"\n--- Batch {batch_idx+1}/{len(batches)}: sessions {batch[0]}..{batch[-1]} ---")
    
    # Submit
    submit_cmd = [TALOS, 'query', 'submit', '--scene', 'SKILL', '--region', 'cn', '--sql-file', sql_file]
    result = subprocess.run(submit_cmd, capture_output=True, text=True, env=ENV)
    if result.returncode != 0:
        print(f"  ERROR submitting: {result.stderr}")
        continue
    qid = result.stdout.strip()
    print(f"  Submitted qid: {qid}")
    
    # Wait for result
    result_cmd = [TALOS, 'query', 'result', '--qid', qid, '--wait', '--region', 'cn', '--timeout', '600']
    result = subprocess.run(result_cmd, capture_output=True, text=True, env=ENV)
    if result.returncode != 0:
        print(f"  ERROR getting result: {result.stderr}")
        continue
    
    lines = result.stdout.strip().split('\n')
    if len(lines) < 2:
        print(f"  ERROR: unexpected output format")
        continue
    
    meta = json.loads(lines[0])
    batch_total = meta.get('totalRows', 0)
    total_reported += batch_total
    
    data_rows = []
    for line in lines[2:]:  # skip meta and columns
        try:
            row = json.loads(line)
            if 'session_id' in row:
                data_rows.append(row)
        except:
            pass
    
    preview_count = len(data_rows)
    print(f"  totalRows={batch_total}, preview={preview_count}")
    
    if preview_count < batch_total:
        print(f"  WARNING: preview ({preview_count}) < totalRows ({batch_total}), some data may be missing!")
    
    all_rows.extend(data_rows)

# Write all results
with open(OUTPUT_FILE, 'w') as f:
    for row in all_rows:
        f.write(json.dumps(row, ensure_ascii=False) + '\n')

print(f"\n=== SUMMARY ===")
print(f"Total batches: {len(batches)}")
print(f"Total reported rows: {total_reported}")
print(f"Total collected rows: {len(all_rows)}")
print(f"Output: {OUTPUT_FILE}")
