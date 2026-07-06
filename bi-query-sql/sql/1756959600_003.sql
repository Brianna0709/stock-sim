SELECT
    s.dt AS dt,
    COUNT(DISTINCT s.host_id) AS online_active_hosts,
    COUNT(DISTINCT CASE WHEN s.ics_switch = 0 AND DATE_FORMAT(s.gmt_modify, 'yyyyMMdd') = s.dt THEN s.host_id END) AS daily_opened_closed_hosts,
    COUNT(DISTINCT CASE WHEN s.ics_switch = 0 THEN s.host_id END) AS daily_closed_hosts,
    ROUND(
        COUNT(DISTINCT CASE WHEN s.ics_switch = 0 AND DATE_FORMAT(s.gmt_modify, 'yyyyMMdd') = s.dt THEN s.host_id END) * 1.0
        / COUNT(DISTINCT s.host_id), 4
    ) AS daily_operate_close_rate,
    ROUND(
        COUNT(DISTINCT CASE WHEN s.ics_switch = 0 THEN s.host_id END) * 1.0
        / COUNT(DISTINCT s.host_id), 4
    ) AS daily_status_close_rate
FROM ba_phx.phx_base_phx_osv_ics_host_setting_history s
INNER JOIN ba_phx.phx_dim_supply_host_extend e
    ON s.host_id = e.host_id AND s.dt = e.dt
WHERE s.dt BETWEEN '20260529' AND '20260604'
  AND s.status = 1
  AND e.is_online_host = 1
GROUP BY s.dt
ORDER BY s.dt;
