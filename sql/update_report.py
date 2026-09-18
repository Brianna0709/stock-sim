p = '/root/.openclaw/workspace/weekly_report_ics.md'
lines = open(p, encoding='utf-8').read().split('\n')

sep_idx = 23
assert lines[sep_idx].startswith('|------|')
lines[sep_idx] = lines[sep_idx] + ':---:|'

rows = [
 ('| \u667a\u80fd\u56de\u590d\u4f7f\u7528\u7387', ' 31.67% |'),
 ('| \u667a能\u5ba2\u670d\u5173\u95ed\u7387', ' 0.035% |'),
 ('| \u667a能IM\u623f\u5ba2\u70b9\u51fb\u672a\u89e3\u51b3\u7387', ' \u26a0\ufe0f\u65e0\u6743\u9650(\u9b54\u6570) |'),
 ('| \u667a能IM\u623f\u4e1c\u53cd\u9988\u9519\u8bef率', ' ⚠️无\u6743限(\u9b54数) |'),
 ('| \u667a能\u56de\u590d\u6d88\u606f\u8986\u76d6\u7387', ' 23.25% |'),
 ('| \u667a能\u56de复会话覆\u76d6率', ' 75.56% |'),
]
count = 0
for i, ln in enumerate(lines):
    for prefix, val in rows:
        if ln.startswith(prefix) and i != sep_idx:
            lines[i] = ln.rstrip() + val
            count += 1
            break
print('rows updated:', count)

note = '8. **W22(0912-0918) \u5907\u6ce8**：\u4f7f用\u7387\u5206\u6bcd\u5feb\u7167\u7528 20260917\uff080918 \u5206\u533a\u672a\u5c31\u7eea\uff09\uff1b\u5173\u95ed\u7387\u4e3a 0912-0917 \u516d\u5929日均\uff080918 分区缺失）；SQL-D/E 因 CLI 无权限未跑，待\u9b54数界面执行；指定队列 root.zw06_2.hadoop-phx.query 无成员权限，已改用默认队列'
if not any('W22(0912-0918) 备注' in ln for ln in lines):
    while lines and lines[-1] == '':
        lines.pop()
    lines.append(note)

open(p, 'w', encoding='utf-8').write('\n'.join(lines))
print('done')
