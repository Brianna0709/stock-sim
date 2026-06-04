SELECT 
    s.dt AS `统计日期`,
    COUNT(DISTINCT s.host_id) AS `在线活跃房东总数`,
    -- 当日实际关闭的房东（modify日期与dt同一天）
    COUNT(DISTINCT CASE 
        WHEN s.ics_switch = 0 
        AND DATE_FORMAT(s.gmt_modify, 'yyyyMMdd') = s.dt
        THEN s.host_id 
    END) AS `当日操作关闭的房东数`,
    -- 当日最终关闭状态（不考虑操作时间）
    COUNT(DISTINCT CASE WHEN s.ics_switch = 0 THEN s.host_id END) AS `当日关闭状态的房东数`,
    -- 当日操作关闭率
    ROUND(
        COUNT(DISTINCT CASE 
            WHEN s.ics_switch = 0 AND DATE_FORMAT(s.gmt_modify, 'yyyyMMdd') = s.dt
            THEN s.host_id 
        END) * 1.0 / 
        COUNT(DISTINCT s.host_id), 
        4
    ) AS `当日操作关闭率`,
    -- 当日最终关闭率
    ROUND(
        COUNT(DISTINCT CASE WHEN s.ics_switch = 0 THEN s.host_id END) * 1.0 / 
        COUNT(DISTINCT s.host_id), 
        4
    ) AS `当日状态关闭率`
FROM 
    ba_phx.phx_base_phx_osv_ics_host_setting_history s
INNER JOIN 
    ba_phx.phx_dim_supply_host_extend e
ON 
    s.host_id = e.host_id 
    AND s.dt = e.dt
WHERE 
    s.dt BETWEEN '20260509' AND '20260514'
    AND s.status = 1
    AND e.is_online_host = 1
GROUP BY 
    s.dt
ORDER BY 
    s.dt
