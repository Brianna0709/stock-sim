WITH unsolved_stats AS (
    SELECT SUM(CASE WHEN result = '0' THEN 1 ELSE 0 END) AS unresolved_count
    FROM origindb_ss.hotel_ia_phx_user__phx_auto_reply_msg_survey
    WHERE dt = '20260401'
        AND gmt_create >= '2026-03-01 00:00:00'
        AND gmt_create < '2026-04-01 00:00:00'
        AND msg_type = 2
),
intelligent_reply_stats AS (
    SELECT COUNT(DISTINCT msg_id) AS total_replies
    FROM ba_phx.phx_mdw_detail_message_sync
    WHERE dt BETWEEN '20260301' AND '20260331'
        AND gmt_create >= '2026-03-01 00:00:00'
        AND gmt_create < '2026-04-01 00:00:00'
        AND is_from_phx_host = 1
        AND auto_reply_msg_type = 'IntelligentResponse'
)
SELECT
    'sql1_202603_fix' AS period,
    (SELECT unresolved_count FROM unsolved_stats) AS unsolved_feedbacks,
    (SELECT total_replies FROM intelligent_reply_stats) AS total_intelligent_replies,
    CASE
        WHEN (SELECT total_replies FROM intelligent_reply_stats) > 0
        THEN ROUND((SELECT unresolved_count FROM unsolved_stats) * 100.0 / (SELECT total_replies FROM intelligent_reply_stats), 4)
        ELSE 0
    END AS unresolved_rate_percent
