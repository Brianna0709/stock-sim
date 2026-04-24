-- IM咨询平台下单率 分子：咨询后在平台任意房东下单的订单数（按周汇总）
-- 统计周期：04.03-04.09, 04.10-04.16, 04.17-04.23
SELECT
    CASE
        WHEN m.dt BETWEEN '20260403' AND '20260409' THEN '04.03-04.09'
        WHEN m.dt BETWEEN '20260410' AND '20260416' THEN '04.10-04.16'
        WHEN m.dt BETWEEN '20260417' AND '20260423' THEN '04.17-04.23'
    END AS week_period,
    COUNT(DISTINCT o.order_id) AS order_count
FROM
    ba_phx.phx_mdw_detail_message_session_reply_time_by_daily AS m
JOIN
    ba_phx.phx_topic_trade_order AS o
ON
    m.from_user_id = o.user_id
    AND DATE(o.gmt_create) = DATE(STR_TO_DATE(m.dt, '%Y%m%d'))
WHERE
    m.dt BETWEEN '20260403' AND '20260423'
    AND m.is_from_host = 0
    AND o.gmt_create > m.gmt_init
GROUP BY
    CASE
        WHEN m.dt BETWEEN '20260403' AND '20260409' THEN '04.03-04.09'
        WHEN m.dt BETWEEN '20260410' AND '20260416' THEN '04.10-04.16'
        WHEN m.dt BETWEEN '20260417' AND '20260423' THEN '04.17-04.23'
    END
ORDER BY
    week_period
