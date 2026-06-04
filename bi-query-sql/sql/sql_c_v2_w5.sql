-- 关闭率口径：当日最新记录为关闭(ics_switch=0)且当日之前最新记录为开启(ics_switch=1)的房东数 / 当日开启状态房东数
-- 即"当天发生了开→关动作"的房东比例

WITH
-- 每天每个房东的最新状态
daily_status AS (
    SELECT host_id, ics_switch, dt,
           ROW_NUMBER() OVER (PARTITION BY host_id, dt ORDER BY id DESC) AS rn
    FROM ba_phx.phx_base_phx_osv_ics_host_setting_history
    WHERE dt BETWEEN '20260514' AND '20260521'
),
daily_latest AS (
    SELECT host_id, ics_switch, dt
    FROM daily_status
    WHERE rn = 1
),
-- 计算每天相较前一天的状态变化
daily_change AS (
    SELECT
        t.dt,
        COUNT(DISTINCT CASE WHEN t.ics_switch=0 AND prev.ics_switch=1 THEN t.host_id END) AS close_host,
        COUNT(DISTINCT CASE WHEN prev.ics_switch=1 THEN prev.host_id END) AS open_host
    FROM daily_latest t
    LEFT JOIN daily_latest prev ON t.host_id=prev.host_id
        AND prev.dt = DATE_FORMAT(DATE_SUB(t.dt, 1), 'yyyyMMdd')
    WHERE t.dt BETWEEN '20260515' AND '20260521'
    GROUP BY t.dt
)
SELECT
    ROUND(AVG(close_host)*100.0/NULLIF(AVG(open_host),0), 4) AS daily_close_rate_pct
FROM daily_change;
