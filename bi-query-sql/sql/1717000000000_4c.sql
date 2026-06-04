SELECT dt, COUNT(*) as cnt FROM origindb_ss.hotel_ia_phx_user__phx_auto_reply_msg_survey WHERE dt >= '20260528' AND dt <= '20260530' GROUP BY dt ORDER BY dt;
