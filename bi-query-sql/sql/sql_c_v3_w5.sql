-- 关闭率 = 当天在历史表中有记录且最新记录为关闭(0)的房东数 / 当天最新记录为开启(1)的房东数
-- 注意：分子只统计"当天有记录"且状态为关闭的，代表当天主动操作过关闭的房东
-- 分母是当天快照最新状态为开启的房东
WITH daily_latest AS (
    SELECT host_id, ics_switch, dt
    FROM (
        SELECT host_id, ics_switch, dt,
               ROW_NUMBER() OVER (PARTITION BY host_id, dt ORDER BY id DESC) AS rn
        FROM ba_phx.phx_base_phx_osv_ics_host_setting_history
        WHERE dt BETWEEN '20260515' AND '20260521'
    ) t WHERE rn=1
),
-- 当天有操作记录且操作为关闭的房东
daily_close_action AS (
    SELECT dt,
           COUNT(DISTINCT CASE WHEN ics_switch=0 THEN host_id END) AS action_close_host
    FROM (
        SELECT host_id, ics_switch, dt, gmt_modified,
               LAG(ics_switch) OVER (PARTITION BY host_id ORDER BY gmt_modified) AS prev_switch
        FROM ba_phx.phx_base_phx_osv_ics_host_setting_history
        WHERE dt BETWEEN '20260515' AND '20260521'
    ) t
    WHERE ics_switch = 0 AND prev_switch = 1
    GROUP BY dt
),
daily_open AS (
    SELECT dt, COUNT(DISTINCT host_id) AS open_host
    FROM daily_latest
    WHERE ics_switch = 1
    GROUP BY dt
)
SELECT
    ROUND(AVG(a.action_close_host)*100.0/NULLIF(AVG(o.open_host),0), 4) AS daily_close_rate_pct
FROM daily_close_action a
JOIN daily_open o ON a.dt = o.dt;
