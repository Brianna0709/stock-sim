SELECT
    s.dt AS stat_dt,
    COUNT(DISTINCT s.host_id) AS online_active_hosts,
    COUNT(DISTINCT CASE WHEN s.ics_switch = 0 AND DATE_FORMAT(s.gmt_modify, 'yyyyMMdd') = s.dt THEN s.host_id END) AS closed_today_hosts,
    ROUND(
        COUNT(DISTINCT CASE WHEN s.ics_switch = 0 AND DATE_FORMAT(s.gmt_modify, 'yyyyMMdd') = s.dt THEN s.host_id END) * 1.0
        / COUNT(DISTINCT s.host_id), 4
    ) AS close_rate
FROM ba_phx.phx_base_phx_osv_ics_host_setting_history s
INNER JOIN ba_phx.phx_dim_supply_host_extend e
    ON s.host_id = e.host_id AND s.dt = e.dt
WHERE s.dt BETWEEN '20261017' AND '20261023'
  AND s.status = 1
  AND e.is_online_host = 1
GROUP BY s.dt
ORDER BY s.dt;
