SELECT * FROM (
    SELECT '0501-0507' AS period, COUNT(DISTINCT c.host_id) AS total_hosts, COUNT(DISTINCT s.host_id) AS smart_reply_hosts, ROUND(COUNT(DISTINCT s.host_id) * 100.0 / COUNT(DISTINCT c.host_id), 2) AS usage_rate_pct
    FROM ba_phx.phx_dim_supply_host_extend c
    LEFT JOIN (SELECT DISTINCT host_id FROM log.phx_hsop_osv_ai_reply_log WHERE dt BETWEEN '20260501' AND '20260507' AND ai_msg_recommend_strategy > 0 AND HOUR(_mt_datetime) >= 7) s ON c.host_id = s.host_id
    WHERE c.dt = '20260507' AND c.online_product_cnt > 0
    UNION ALL
    SELECT '0501-0514' AS period, COUNT(DISTINCT c.host_id) AS total_hosts, COUNT(DISTINCT s.host_id) AS smart_reply_hosts, ROUND(COUNT(DISTINCT s.host_id) * 100.0 / COUNT(DISTINCT c.host_id), 2) AS usage_rate_pct
    FROM ba_phx.phx_dim_supply_host_extend c
    LEFT JOIN (SELECT DISTINCT host_id FROM log.phx_hsop_osv_ai_reply_log WHERE dt BETWEEN '20260501' AND '20260514' AND ai_msg_recommend_strategy > 0 AND HOUR(_mt_datetime) >= 7) s ON c.host_id = s.host_id
    WHERE c.dt = '20260514' AND c.online_product_cnt > 0
    UNION ALL
    SELECT '0501-0521' AS period, COUNT(DISTINCT c.host_id) AS total_hosts, COUNT(DISTINCT s.host_id) AS smart_reply_hosts, ROUND(COUNT(DISTINCT s.host_id) * 100.0 / COUNT(DISTINCT c.host_id), 2) AS usage_rate_pct
    FROM ba_phx.phx_dim_supply_host_extend c
    LEFT JOIN (SELECT DISTINCT host_id FROM log.phx_hsop_osv_ai_reply_log WHERE dt BETWEEN '20260501' AND '20260521' AND ai_msg_recommend_strategy > 0 AND HOUR(_mt_datetime) >= 7) s ON c.host_id = s.host_id
    WHERE c.dt = '20260521' AND c.online_product_cnt > 0
    UNION ALL
    SELECT '0501-0528' AS period, COUNT(DISTINCT c.host_id) AS total_hosts, COUNT(DISTINCT s.host_id) AS smart_reply_hosts, ROUND(COUNT(DISTINCT s.host_id) * 100.0 / COUNT(DISTINCT c.host_id), 2) AS usage_rate_pct
    FROM ba_phx.phx_dim_supply_host_extend c
    LEFT JOIN (SELECT DISTINCT host_id FROM log.phx_hsop_osv_ai_reply_log WHERE dt BETWEEN '20260501' AND '20260528' AND ai_msg_recommend_strategy > 0 AND HOUR(_mt_datetime) >= 7) s ON c.host_id = s.host_id
    WHERE c.dt = '20260528' AND c.online_product_cnt > 0
    UNION ALL
    SELECT '0501-0531' AS period, COUNT(DISTINCT c.host_id) AS total_hosts, COUNT(DISTINCT s.host_id) AS smart_reply_hosts, ROUND(COUNT(DISTINCT s.host_id) * 100.0 / COUNT(DISTINCT c.host_id), 2) AS usage_rate_pct
    FROM ba_phx.phx_dim_supply_host_extend c
    LEFT JOIN (SELECT DISTINCT host_id FROM log.phx_hsop_osv_ai_reply_log WHERE dt BETWEEN '20260501' AND '20260531' AND ai_msg_recommend_strategy > 0 AND HOUR(_mt_datetime) >= 7) s ON c.host_id = s.host_id
    WHERE c.dt = '20260531' AND c.online_product_cnt > 0
) t ORDER BY period;
