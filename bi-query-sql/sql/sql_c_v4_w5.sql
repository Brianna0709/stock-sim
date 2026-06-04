-- 关闭率 = 当天操作从开启→关闭的房东数 / 当天快照最新状态为开启的房东数
-- 用 id 排序（id越大越新）来判断状态变化
WITH
-- 找出当天在表中有多条记录，且最新记录为0、倒数第二条为1的房东（即当天发生了1→0的变化）
daily_close_action AS (
    SELECT dt,
           COUNT(DISTINCT host_id) AS action_close_host
    FROM (
        SELECT host_id, dt, ics_switch,
               LAG(ics_switch) OVER (PARTITION BY host_id, dt ORDER BY id) AS prev_switch
        FROM ba_phx.phx_base_phx_osv_ics_host_setting_history
        WHERE dt BETWEEN '20260515' AND '20260521'
    ) t
    WHERE ics_switch = 0 AND prev_switch = 1
    GROUP BY dt
),
-- 当天快照最新状态
daily_latest AS (
    SELECT host_id, ics_switch, dt
    FROM (
        SELECT host_id, ics_switch, dt,
               ROW_NUMBER() OVER (PARTITION BY host_id, dt ORDER BY id DESC) AS rn
        FROM ba_phx.phx_base_phx_osv_ics_host_setting_history
        WHERE dt BETWEEN '20260515' AND '20260521'
    ) t WHERE rn=1
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
