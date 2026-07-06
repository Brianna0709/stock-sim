WITH
monthly_smart_reply AS (
    -- 按月聚合：每个房东在当月是否用过智能回复
    SELECT MONTH(_mt_datetime) AS m, host_id
    FROM log.phx_hsop_osv_ai_reply_log
    WHERE dt BETWEEN '20260401' AND '20260601'
      AND ai_msg_recommend_strategy > 0
      AND HOUR(_mt_datetime) >= 7
    GROUP BY MONTH(_mt_datetime), host_id
),
monthly_online AS (
    -- 按月+房东：当月最后一天快照
    SELECT
        MONTH(c.dt) AS m,
        MONTH(c.dt) * 100 + DAY(c.dt) AS md,
        COUNT(DISTINCT c.host_id) AS total_hosts,
        COUNT(DISTINCT s.host_id) AS smart_reply_hosts,
        ROUND(COUNT(DISTINCT s.host_id) * 100.0 / COUNT(DISTINCT c.host_id), 2) AS usage_rate_pct
    FROM ba_phx.phx_dim_supply_host_extend c
    LEFT JOIN monthly_smart_reply s ON c.host_id = s.host_id AND MONTH(c.dt) = s.m
    WHERE c.dt BETWEEN '20260401' AND '20260601'
      AND c.online_product_cnt > 0
      AND c.dt IN ('20260430', '20260531', '20260601')
    GROUP BY MONTH(c.dt), MONTH(c.dt) * 100 + DAY(c.dt), c.dt
)
SELECT
    dt,
    total_hosts,
    smart_reply_hosts,
    usage_rate_pct
FROM monthly_online
ORDER BY dt;
