WITH ab_users AS (
  SELECT DISTINCT
    CAST(identification AS BIGINT) AS user_id,
    strategy_key
  FROM mart_jiulv_flow.aggr_abtest_hotel_trip_minsu_info_view
  WHERE partition_date BETWEEN '2026-08-29' AND '2026-09-02'
    AND exp_key = 'ab_arena_wanglingyun04_im_guess'
    AND strategy_key IN ('shiyanzu1', 'duizhaozu')
),
daily AS (
  SELECT
    ab.strategy_key,
    s.dt,
    COUNT(DISTINCT s.from_user_id) AS session_user_cnt
  FROM ab_users ab
  JOIN ba_phx.phx_mdw_detail_message_session_reply_time_by_daily s
    ON ab.user_id = s.from_user_id
  JOIN ba_phx.phx_dim_message_session t
    ON s.dt = t.dt AND s.session_id = t.session_id
  WHERE s.dt BETWEEN 20260829 AND 20260902
    AND t.is_check_session = 1
  GROUP BY ab.strategy_key, s.dt
)
SELECT
  ab.strategy_key,
  o.dt AS dt,
  COUNT(DISTINCT o.user_id) AS order_user_cnt
FROM ab_users ab
JOIN ba_phx.phx_topic_magic_trade_order o
  ON ab.user_id = o.user_id
LEFT JOIN ba_phx.phx_mdw_aggr_trade_message_session_by_daily ts
  ON o.order_id = ts.order_id AND o.dt = ts.dt AND ts.dt BETWEEN 20260829 AND 20260902
WHERE o.dt BETWEEN 20260829 AND 20260902
  AND o.category <> 2
  AND o.process_code = 'paid'
  AND o.paid_order_status = 1
  AND COALESCE(ts.before_paid_session_id, 0) > 0
GROUP BY ab.strategy_key, o.dt
