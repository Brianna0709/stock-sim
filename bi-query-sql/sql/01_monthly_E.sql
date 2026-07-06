WITH host_survey AS (
    SELECT COUNT(id) AS host_survey
    FROM ba_phx.bas_phx_ai_reply_msg_host_survey
    WHERE gmt_create BETWEEN '2026-01-01 00:00:00' AND '2026-01-31 23:59:59'
),
ai_reply AS (
    SELECT COUNT(reply_id) AS reply_count
    FROM log.phx_hsop_osv_ai_reply_log
    WHERE dt BETWEEN '20260101' AND '20260131'
      AND _mt_datetime BETWEEN '2026-01-01 00:00:00' AND '2026-01-31 23:59:59'
      AND ai_msg_recommend_strategy > 0
)
SELECT
    host_survey.host_survey  AS host_survey_total,
    ai_reply.reply_count     AS ai_reply_total,
    ROUND(host_survey.host_survey * 100.0 / ai_reply.reply_count, 2) AS error_rate_pct
FROM host_survey, ai_reply;
