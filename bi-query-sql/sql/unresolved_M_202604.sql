WITH host_survey AS (
    SELECT COUNT(id) AS host_survey
    FROM ba_phx.bas_phx_ai_reply_msg_host_survey
    WHERE gmt_create BETWEEN '2026-04-01 00:00:00' AND '2026-04-30 23:59:59'
),
ai_reply AS (
    SELECT COUNT(reply_id) AS reply_count
    FROM log.phx_hsop_osv_ai_reply_log
    WHERE _mt_datetime BETWEEN '2026-04-01 00:00:00' AND '2026-04-30 23:59:59'
        AND ai_msg_recommend_strategy > 0
)
SELECT
    host_survey.host_survey AS `未解决点击总数`,
    ai_reply.reply_count AS `智能回复总数`,
    ROUND(host_survey.host_survey * 100.0 / ai_reply.reply_count, 2) AS `未解决率(%)`
FROM host_survey, ai_reply
