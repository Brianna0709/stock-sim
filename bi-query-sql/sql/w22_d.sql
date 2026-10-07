SELECT COUNT(*) AS cnt
FROM origindb_ss.hotel_ia_phx_user__phx_auto_reply_msg_survey
WHERE dt = '20260924'
  AND msg_type = 2
  AND result = '0'
LIMIT 1;
