SELECT COUNT(*) AS cnt
FROM ba_phx.bas_phx_ai_reply_msg_host_survey
WHERE gmt_create BETWEEN '2026-09-24 00:00:00' AND '2026-09-24 23:59:59'
LIMIT 1;
