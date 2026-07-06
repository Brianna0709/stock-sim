SELECT
    ROUND(AVG(daily_count.close_cnt), 4) AS avg_daily_close_rate,
    ROUND(AVG(daily_count.close_cnt), 0) AS total_close_hosts,
    ROUND(AVG(daily_count.total_cnt), 0) AS avg_total_active_hosts
FROM (
    SELECT
        s.dt,
        COUNT(DISTINCT s.host_id) AS total_cnt,
        COUNT(DISTINCT CASE WHEN s.ics_switch = 0 AND DATE_FORMAT(s.gmt_modify, 'yyyyMMdd') = s.dt THEN s.host_id END) AS close_cnt
    FROM ba_phx.phx_base_phx_osv_ics_host_setting_history s
    INNER JOIN ba_phx.phx_dim_supply_host_extend e
        ON s.host_id = e.host_id AND s.dt = e.dt
    WHERE s.dt BETWEEN '20260601' AND '20260617'
      AND s.status = 1
      AND e.is_online_host = 1
    GROUP BY s.dt
) daily_count;
