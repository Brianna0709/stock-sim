const fs = require('fs');
const lines = fs.readFileSync('/root/.openclaw/workspace/bi-query-sql/sql2_result.jsonl', 'utf-8').trim().split('\n');

// Parse meta
const meta = JSON.parse(lines[0]);
const columns = JSON.parse(lines[1]);

// Parse data rows
const rows = [];
for (let i = 2; i < lines.length; i++) {
  try {
    rows.push(JSON.parse(lines[i]));
  } catch(e) {}
}

// Group by session_id
const groups = {};
for (const row of rows) {
  const sid = row.session_id;
  if (!groups[sid]) groups[sid] = [];
  groups[sid].push(row);
}

// Check if order fields are all empty
let hasOrderId = false;
let hasOrderCreateTime = false;
for (const row of rows) {
  if (row.order_id && row.order_id !== '' && row.order_id !== 'null') hasOrderId = true;
  if (row.order_create_time && row.order_create_time !== '' && row.order_create_time !== 'null') hasOrderCreateTime = true;
}

// Build markdown
let md = `# Session 会话内容查询结果（含订单信息）\n\n`;
md += `## 查询概览\n\n`;
md += `- **第一步查询**：获取符合条件的 session_id，共找到 **50** 个 session_id\n`;
md += `- **第二步查询**：查询完整会话内容，共 **${meta.totalRows}** 条消息记录\n`;
md += `- **预览数据**：以下展示前 ${rows.length} 条记录（按 session_id 分组），完整数据请通过文枢链接下载\n`;
md += `- **查询时间范围**：2026-06-23 至 2026-06-29\n\n`;

// Order field note
md += `## 订单字段说明\n\n`;
if (!hasOrderId) {
  md += `> ⚠️ **注意**：在预览数据中，order_id 字段全部为空值。这可能是因为 msg_extension 中的 PHXExtensionOrderId 字段在这些消息中未被填充，或者该字段仅在特定类型的消息（如系统消息）中才有值。\n\n`;
}
if (!hasOrderCreateTime) {
  md += `> ⚠️ **注意**：在预览数据中，order_create_time 字段全部为空值。PHXExtensionOrderCreateTime 字段在这些消息中未被填充。\n\n`;
}
md += `- order_status 字段有值，常见值：0（未下单）、5（待确认）、6（已确认/已下单）等\n\n`;

md += `## 文枢下载链接\n\n`;
md += `完整数据（${meta.totalRows} 行）可通过文枢下载：\n`;
md += `${meta.url}\n\n`;
md += `materialKey：${meta.materialKey}\n\n`;

md += `---\n\n`;
md += `## 会话详情（按 session_id 分组）\n\n`;

const sessionIds = Object.keys(groups).sort();
for (const sid of sessionIds) {
  const msgs = groups[sid];
  md += `### Session: ${sid}\n\n`;
  md += `| 时间 | 发送方 | 消息内容 | 订单ID | 订单状态 | 下单时间 |\n`;
  md += `|------|--------|----------|--------|----------|----------|\n`;
  for (const m of msgs) {
    const sender = m.is_from_phx_host === '1' ? '🏠 房东' : '👤 客人';
    const payload = (m.valid_payload || '').replace(/\|/g, '\\|').replace(/\n/g, ' ').substring(0, 100);
    const orderId = m.order_id || '-';
    const orderStatus = m.order_status || '-';
    const statusLabel = {'0': '0(未下单)', '5': '5(待确认)', '6': '6(已确认)', '': '-'}[m.order_status] || m.order_status || '-';
    const orderCreateTime = m.order_create_time || '-';
    md += `| ${m.gmt_msg_gen} | ${sender} | ${payload || '(空)'} | ${orderId || '-'} | ${statusLabel} | ${orderCreateTime || '-'} |\n`;
  }
  md += `\n`;
}

md += `---\n\n`;
md += `## SQL 查询语句\n\n`;
md += `### SQL1 - 获取 session_id\n\n`;
md += '```sql\n' + fs.readFileSync('/root/.openclaw/workspace/bi-query-sql/sql/sql1_session_ids.sql', 'utf-8') + '\n```\n\n';
md += `### SQL2 - 获取完整会话内容\n\n`;
md += '```sql\n' + fs.readFileSync('/root/.openclaw/workspace/bi-query-sql/sql/sql2_session_content.sql', 'utf-8') + '\n```\n\n';

fs.writeFileSync('/root/.openclaw/workspace/session_content_with_order.md', md);
console.log(`Written ${md.length} chars, ${sessionIds.length} sessions, ${rows.length} messages`);
console.log(`Sessions in preview: ${sessionIds.join(', ')}`);
console.log(`Has order_id values: ${hasOrderId}`);
console.log(`Has order_create_time values: ${hasOrderCreateTime}`);
