WITH close_daily AS (
    SELECT dt,
           COUNT(DISTINCT CASE WHEN ics_switch=0 THEN host_id END) AS close_host,
           COUNT(DISTINCT CASE WHEN ics_switch=1 THEN host_id END) AS open_host
    FROM (
        SELECT host_id, ics_switch, dt,
               ROW_NUMBER() OVER (PARTITION BY host_id, dt ORDER BY id DESC) AS rn
        FROM ba_phx.phx_base_phx_osv_ics_host_setting_history
        WHERE dt BETWEEN '20260515' AND '20260521'
    ) t WHERE rn=1
    GROUP BY dt
)
SELECT
    ROUND(AVG(close_host)*100.0/NULLIF(AVG(open_host),0), 4) AS daily_close_rate_pct
FROM close_daily;
