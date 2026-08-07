SELECT 
    COUNT(*) as total_rows,
    SUM(CASE WHEN result = '0' THEN 1 ELSE 0 END) as result_0_count,
    SUM(CASE WHEN result = 0 THEN 1 ELSE 0 END) as result_int_0_count,
    COUNT(DISTINCT result) as distinct_results,
    COLLECT_SET(result) as result_values
FROM origindb_ss.hotel_ia_phx_user__phx_auto_reply_msg_survey
WHERE dt >= '20260801' AND dt <= '20260807'
  AND gmt_create >= '2026-08-01 00:00:00'
  AND gmt_create <  '2026-08-08 00:00:00'
  AND msg_type = 2;
