#!/bin/bash
# 每周四 16:00 自动发送战役进展提醒邮件
# 持续到 2026年五一结束（2026-05-05）后停止

# 检查是否已过期（2026-05-06 后停止）
EXPIRE_DATE="2026-05-06"
TODAY=$(date +%Y-%m-%d)
if [ "$TODAY" \> "$EXPIRE_DATE" ] || [ "$TODAY" = "$EXPIRE_DATE" ]; then
    echo "[$TODAY] 任务已过期（五一结束），跳过发送。"
    exit 0
fi

LOG_FILE="/root/.openclaw/workspace/scripts/send_weekly_email.log"
echo "[$TODAY $(date +%H:%M)] 开始发送战役进展提醒邮件..." >> "$LOG_FILE"

# 使用 Python 通过 OWA 发送邮件
PYOUT=$(python3 << 'PYEOF'
import sys, os
sys.path.insert(0, '/root/.openclaw/skills/meituan-mail-exchange/scripts')

from owa_api import ensure_owa_session, send_message

if not ensure_owa_session():
    print("OWA session FAIL，请检查登录状态")
    sys.exit(1)

result = send_message(
    to=[
        'songzihan03@meituan.com',
        'wuxi20@meituan.com',
        'fujiewei@meituan.com',
        'zhaofujian@meituan.com',
        'nilongjie@meituan.com',
    ],
    cc=['daizhenyuan@meituan.com'],
    subject='请填写战役进展和五一策略规划',
    body='''<p>大家好，</p>
<p>请填写战役进展和五一策略规划，相关文档请查看：</p>
<p><a href="https://km.sankuai.com/collabpage/2748572993">2026春季战役-经营能力组</a></p>
<p>感谢大家！</p>''',
    body_type='HTML',
    importance='Normal',
)

if result.get('success'):
    print(f"发送成功，item_id: {result.get('item_id')}")
else:
    print(f"发送失败: {result.get('error')}")
    sys.exit(1)
PYEOF
)

STATUS=$?
if [ $STATUS -eq 0 ]; then
    echo "[$TODAY $(date +%H:%M)] ✅ 邮件发送成功" >> "$LOG_FILE"
    # 发送大象消息通知主人
    openclaw message send --channel daxiang --target 2897431976 \
        --message "✅ 战役进展提醒邮件已发送！
📅 发送时间：$(date '+%Y-%m-%d %H:%M')
👥 收件人：songzihan03、wuxi20、fujiewei、zhaofujian、nilongjie
📄 主题：请填写战役进展和五一策略规划"
else
    echo "[$TODAY $(date +%H:%M)] ❌ 邮件发送失败: $PYOUT" >> "$LOG_FILE"
    # 发送大象消息通知失败
    openclaw message send --channel daxiang --target 2897431976 \
        --message "❌ 战役进展提醒邮件发送失败！
📅 时间：$(date '+%Y-%m-%d %H:%M')
⚠️ 错误：$PYOUT
请手动检查邮件发送状态。"
fi
