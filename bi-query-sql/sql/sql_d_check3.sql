SELECT dt, COUNT(*) AS cnt
FROM origindb_ss.hotel_ia_phx_user__phx_auto_reply_msg_survey
WHERE dt BETWEEN '20260611' AND '20260613'
GROUP BY dt
ORDER BY dt;
