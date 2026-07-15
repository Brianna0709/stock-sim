import json
from collections import defaultdict

sessions = defaultdict(list)

with open('/root/.openclaw/workspace/sql2_result.jsonl', 'r') as f:
    lines = f.readlines()

# Skip meta and columns (lines 0 and 1)
for line in lines[2:]:
    line = line.strip()
    if not line:
        continue
    try:
        row = json.loads(line)
        sid = row.get('session_id', '')
        sessions[sid].append(row)
    except:
        continue

# Write to markdown
with open('/root/.openclaw/workspace/session_content_result.md', 'w') as out:
    out.write('# Session 会话内容查询结果\n\n')
    out.write('## 查询概要\n\n')
    out.write('- **SQL1 查询结果**：原始查询匹配到 **112,531** 个符合条件的 session_id（数据量超大，取前50个用于第二步查询）\n')
    out.write('- **SQL2 查询结果**：50个 session 共产生 **1,029** 条消息记录\n')
    out.write('- **预览数据**：以下展示预览中的 **{}** 条记录（预览样本，非全量），按 session_id 分组\n'.format(len(lines)-2))
    out.write('- **完整数据下载**：\n')
    out.write('  - 文枢链接：https://wenshu-s3.sankuai.com/v2/wsjr_898/T20260715_143737_06311_z2y5w.csv?AWSAccessKeyId=SRV_STkYgII727423zKqISimZLlxREvY4nQL&Expires=1784101101&Signature=bbFY3eGcdCOFobhqD0spw0uWFpo%3D\n')
    out.write('  - materialKey：352730345763254272\n\n')
    out.write('- **查询时间范围**：2026-06-23 至 2026-06-29\n')
    out.write('- **筛选条件**：\n')
    out.write('  - 首条消息的 PHXExtensionOrderStatus = 0（订单状态为0）\n')
    out.write('  - 客人发送的消息中包含"入住|办理|登记|check in"等关键词\n\n')
    out.write('---\n\n')
    out.write('## 会话内容（按 session_id 分组）\n\n')
    out.write('> 说明：`is_from_phx_host=0` 表示**客人**发送，`is_from_phx_host=1` 表示**房东/系统**发送\n\n')
    
    for sid in sorted(sessions.keys()):
        msgs = sessions[sid]
        out.write('### Session ID: {}\n\n'.format(sid))
        out.write('| 时间 | 发送方 | 消息内容 |\n')
        out.write('|------|--------|----------|\n')
        for m in msgs:
            time_str = m.get('gmt_msg_gen', '')
            sender = '房东' if m.get('is_from_phx_host') == '1' else '客人'
            payload = m.get('valid_payload', '').replace('|', '\\|').replace('\n', ' ')
            if len(payload) > 200:
                payload = payload[:200] + '...'
            out.write('| {} | {} | {} |\n'.format(time_str, sender, payload))
        out.write('\n')
    
    out.write('---\n\n')
    out.write('## SQL1（获取 session_id）\n\n')
    out.write('```sql\n')
    with open('/root/.openclaw/workspace/bi-query-sql/sql/1752561240000_sql1_limited.sql', 'r') as sf:
        out.write(sf.read())
    out.write('\n```\n\n')
    out.write('## SQL2（获取完整会话内容）\n\n')
    out.write('```sql\n')
    with open('/root/.openclaw/workspace/bi-query-sql/sql/1752561240000_sql2.sql', 'r') as sf:
        out.write(sf.read())
    out.write('\n```\n')

print('Total sessions in preview: {}'.format(len(sessions)))
print('Total message rows in preview: {}'.format(len(lines)-2))
for sid in sorted(sessions.keys()):
    print('  Session {}: {} messages'.format(sid, len(sessions[sid])))
