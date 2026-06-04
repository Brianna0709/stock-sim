-- 调试：查看每天 ics_switch=0 和 =1 各有多少房东
SELECT dt,
       COUNT(DISTINCT CASE WHEN ics_switch=0 THEN host_id END) AS close_host,
       COUNT(DISTINCT CASE WHEN ics_switch=1 THEN host_id END) AS open_host,
       ROUND(COUNT(DISTINCT CASE WHEN ics_switch=0 THEN host_id END)*100.0
             /NULLIF(COUNT(DISTINCT CASE WHEN ics_switch=1 THEN host_id END),0), 4) AS close_rate_pct
FROM (
    SELECT host_id, ics_switch, dt,
           ROW_NUMBER() OVER (PARTITION BY host_id, dt ORDER BY id DESC) AS rn
    FROM ba_phx.phx_base_phx_osv_ics_host_setting_history
    WHERE dt BETWEEN '20260515' AND '20260521'
) t WHERE rn=1
GROUP BY dt
ORDER BY dt;
