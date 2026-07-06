WITH
smart_reply_hosts AS (
    SELECT DISTINCT host_id
    FROM log.phx_hsop_osv_ai_reply_log
    WHERE dt BETWEEN '20260529' AND '20260604'
      AND ai_msg_recommend_strategy > 0
      AND HOUR(_mt_datetime) >= 7
),
online_hosts_stats AS (
    SELECT
        COUNT(DISTINCT c.host_id) AS total_hosts,
        COUNT(DISTINCT s.host_id) AS smart_reply_hosts
    FROM ba_phx.phx_dim_supply_host_extend c
    LEFT JOIN smart_reply_hosts s ON c.host_id = s.host_id
    WHERE c.dt = '20260604'
      AND c.online_product_cnt > 0
)
SELECT
    '有在线房源的房东' AS segment,
    o.total_hosts, o.smart_reply_hosts,
    ROUND(o.smart_reply_hosts * 100.0 / o.total_hosts, 2) AS usage_rate_pct
FROM online_hosts_stats o;
