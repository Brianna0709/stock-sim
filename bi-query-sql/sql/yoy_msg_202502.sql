WITH daily_stats AS (
    SELECT
        dt,
        auto_reply_msg_type,
        COUNT(*) AS message_count,
        SUM(COUNT(*)) OVER (PARTITION BY dt) AS total_daily_messages
    FROM ba_phx.phx_mdw_detail_message_sync
    WHERE dt BETWEEN '20250201' AND '20250228'
        AND is_from_phx_host = 1
    GROUP BY dt, auto_reply_msg_type
)
SELECT
    dt,
    auto_reply_msg_type,
    message_count,
    ROUND(message_count * 100.0 / total_daily_messages, 2) AS daily_percentage
FROM daily_stats
ORDER BY dt, auto_reply_msg_type
