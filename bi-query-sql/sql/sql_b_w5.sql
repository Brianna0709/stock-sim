SELECT
    COUNT(DISTINCT h.host_id) AS total_registered_host,
    COUNT(DISTINCT CASE WHEN h.ics_switch=1 THEN h.host_id END) AS ics_open_host,
    ROUND(COUNT(DISTINCT CASE WHEN h.ics_switch=1 THEN h.host_id END) * 100.0
          / COUNT(DISTINCT h.host_id), 2) AS usage_rate_pct
FROM (
    SELECT host_id, ics_switch,
           ROW_NUMBER() OVER (PARTITION BY host_id ORDER BY id DESC) AS rn
    FROM ba_phx.phx_base_phx_osv_ics_host_setting_history
    WHERE dt = '20260521'
) h
WHERE h.rn = 1;
