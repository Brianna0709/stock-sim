#!/bin/bash
# 抢会议室脚本 - 互联T6 2026-03-30 17:00-18:00
# 运行直到 2026-03-30 17:00 为止

TARGET_DATE="2026-03-31"
START_TIME="11:00"
END_TIME="12:30"
BUILDING_ID="383"
DEADLINE="2026-03-31 11:00:00"
TITLE="会议"
LOG_FILE="$HOME/.openclaw/workspace/grab_room_log.txt"
RESULT_FILE="$HOME/.openclaw/workspace/grab_room_result.txt"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 开始监控互联T6 ${TARGET_DATE} ${START_TIME}-${END_TIME} 会议室..." | tee -a "$LOG_FILE"

while true; do
    NOW=$(date '+%Y-%m-%d %H:%M:%S')
    
    # 检查是否超过截止时间
    if [[ "$NOW" > "$DEADLINE" ]]; then
        echo "[$NOW] 已超过截止时间 $DEADLINE，停止监控。" | tee -a "$LOG_FILE"
        echo "TIMEOUT" > "$RESULT_FILE"
        exit 0
    fi
    
    echo "[$NOW] 查询可用会议室..." | tee -a "$LOG_FILE"
    
    # 查询可用会议室
    AVAILABLE=$(uv run mtroom -f json query "$BUILDING_ID" --date "$TARGET_DATE" 2>/dev/null | python3 -c "
import json, sys
rooms = json.load(sys.stdin)
available = []
for r in rooms:
    if r.get('status') == 'LOCKED':
        continue
    appts = r.get('appointments', [])
    conflict = False
    for a in appts:
        s = a.get('start_str', '')
        e = a.get('end_str', '')
        if s < '18:00' and e > '17:00':
            conflict = True
            break
    if not conflict:
        available.append({'name': r['room']['name'], 'room_id': r['room_id'], 'floor': r['room'].get('floor_name', ''), 'capacity': r['room'].get('capacity', 0)})
for a in available:
    print(f\"{a['room_id']}|{a['name']}|{a['floor']}|{a['capacity']}\")
" 2>/dev/null)
    
    # 周一当天高频（每10秒），其他时间60秒
    TODAY=$(date '+%Y-%m-%d')
    if [ "$TODAY" = "$TARGET_DATE" ]; then
        INTERVAL=10
    else
        INTERVAL=60
    fi

    if [ -n "$AVAILABLE" ]; then
        # 取第一个可用房间
        FIRST=$(echo "$AVAILABLE" | head -1)
        ROOM_ID=$(echo "$FIRST" | cut -d'|' -f1)
        ROOM_NAME=$(echo "$FIRST" | cut -d'|' -f2)
        FLOOR=$(echo "$FIRST" | cut -d'|' -f3)
        CAPACITY=$(echo "$FIRST" | cut -d'|' -f4)
        
        echo "[$NOW] 发现可用会议室: $ROOM_NAME ($FLOOR, 容纳${CAPACITY}人), room_id=$ROOM_ID，立即预订！" | tee -a "$LOG_FILE"
        
        # 立即预订
        BOOK_RESULT=$(uv run mtroom book --room-id "$ROOM_ID" --start "$START_TIME" --end "$END_TIME" --date "$TARGET_DATE" --title "$TITLE" 2>&1)
        echo "[$NOW] 预订结果: $BOOK_RESULT" | tee -a "$LOG_FILE"
        
        if echo "$BOOK_RESULT" | grep -qi "success\|成功\|schedule_id\|已预定\|预订成功\|booked"; then
            echo "[$NOW] 预订成功！$ROOM_NAME $FLOOR $TARGET_DATE $START_TIME-$END_TIME" | tee -a "$LOG_FILE"
            echo "SUCCESS|$ROOM_NAME|$FLOOR|$CAPACITY|$ROOM_ID|$BOOK_RESULT" > "$RESULT_FILE"
            exit 0
        else
            echo "[$NOW] 预订失败（可能被抢先），继续监控..." | tee -a "$LOG_FILE"
        fi
    else
        echo "[$NOW] 暂无可用会议室，${INTERVAL}秒后重试..." | tee -a "$LOG_FILE"
    fi
    
    sleep "$INTERVAL"
done
