SELECT dt, COUNT(*) as cnt FROM origindb_ss.hotel_ia_phx_user__phx_auto_reply_msg_survey WHERE dt >= '20260801' AND dt <= '20260807' GROUP BY dt ORDER BY dt;
