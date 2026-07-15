SELECT 
    COUNT(*) AS total_rows,
    SUM(CASE WHEN result = '0' THEN 1 ELSE 0 END) AS unresolved_count
FROM origindb_ss.hotel_ia_phx_user__phx_auto_reply_msg_survey
WHERE dt = '20260709'
  AND gmt_create >= '2026-07-03 00:00:00'
  AND gmt_create <  '2026-07-10 00:00:00'
  AND msg_type = 2
