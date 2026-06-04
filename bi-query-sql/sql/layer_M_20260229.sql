WITH 
latest_settings AS (
    SELECT host_id, ics_switch, gmt_modify, dt
    FROM (
        SELECT host_id, ics_switch, gmt_modify, dt,
            ROW_NUMBER() OVER (PARTITION BY host_id ORDER BY id DESC) AS rn
        FROM ba_phx.phx_base_phx_osv_ics_host_setting_history
        WHERE dt = '20260229'
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
SELECT 
    '全部注册房东' AS segment,
    COUNT(DISTINCT h.phx_user_id) AS total_hosts,
    COUNT(DISTINCT s.host_id) AS open_smart_reply_hosts,
    ROUND(COUNT(DISTINCT s.host_id) * 100.0 / NULLIF(COUNT(DISTINCT h.phx_user_id), 0), 2) AS open_rate_pct
FROM ba_phx.phx_dim_supply_host h
LEFT JOIN open_smart_reply_hosts s ON h.phx_user_id = s.host_id
WHERE h.dt = '20260229'
