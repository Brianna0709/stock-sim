SELECT dt, COUNT(*) AS cnt
FROM origindb_ss.hotel_ia_phx_user__phx_auto_reply_msg_survey
WHERE gmt_create >= '2026-06-05 00:00:00'
  AND gmt_create < '2026-06-12 00:00:00'
  AND msg_type = 2
GROUP BY dt
ORDER BY dt;
