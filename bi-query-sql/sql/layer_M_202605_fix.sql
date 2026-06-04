WITH 
latest_settings AS (
    SELECT host_id, ics_switch, gmt_modify, dt
    FROM (
        SELECT host_id, ics_switch, gmt_modify, dt,
            ROW_NUMBER() OVER (PARTITION BY host_id ORDER BY id DESC) AS rn
        FROM ba_phx.phx_base_phx_osv_ics_host_setting_history
        WHERE dt = '20260508'
    ) t
    WHERE rn = 1
),
open_smart_reply_hosts AS (
    SELECT DISTINCT host_id
    FROM latest_settings
    WHERE ics_switch = 1
        AND (
            (host_id % 10000 < 2000)
            OR gmt_modify > '2025-10-29 09:30:00'
        )
)
SELECT '全部房东（注册）' AS segment,
    COUNT(DISTINCT h.phx_user_id) AS total_hosts,
    COUNT(DISTINCT s.host_id) AS open_smart_reply_hosts,
    ROUND(COUNT(DISTINCT s.host_id) * 100.0 / NULLIF(COUNT(DISTINCT h.phx_user_id), 0), 2) AS open_rate_pct
FROM ba_phx.phx_dim_supply_host h
LEFT JOIN open_smart_reply_hosts s ON h.phx_user_id = s.host_id
WHERE h.dt = '20260508'
UNION ALL
SELECT '有在线房源的房东',
    COUNT(DISTINCT c.host_id), COUNT(DISTINCT s.host_id),
    ROUND(COUNT(DISTINCT s.host_id) * 100.0 / NULLIF(COUNT(DISTINCT c.host_id), 0), 2)
FROM ba_phx.phx_dim_supply_host_extend c
LEFT JOIN open_smart_reply_hosts s ON c.host_id = s.host_id
WHERE c.dt = '20260508' AND c.online_product_cnt > 0
UNION ALL
SELECT '活跃房东',
    COUNT(DISTINCT a.host_id), COUNT(DISTINCT s.host_id),
    ROUND(COUNT(DISTINCT s.host_id) * 100.0 / NULLIF(COUNT(DISTINCT a.host_id), 0), 2)
FROM ba_phx.phx_dim_supply_product_active_derive a
LEFT JOIN open_smart_reply_hosts s ON a.host_id = s.host_id
WHERE a.dt = '20260508' AND a.product_operation_type = 1
ORDER BY 1
