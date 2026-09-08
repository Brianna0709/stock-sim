WITH ab_users AS (
  SELECT DISTINCT
    CAST(identification AS BIGINT) AS user_id,
    strategy_key
  FROM mart_jiulv_flow.aggr_abtest_hotel_trip_minsu_info_view
  WHERE partition_date BETWEEN '2026-08-29' AND '2026-09-02'
    AND exp_key = 'ab_arena_wanglingyun04_im_guess'
    AND strategy_key IN ('shiyanzu1', 'duizhaozu')
)
SELECT
  ab.strategy_key,
  s.dt,
  COUNT(DISTINCT s.from_user_id) AS consult_user_cnt,
  COUNT(DISTINCT CASE WHEN ts.session_paid_status = 0 OR ts.session_paid_status = 1 THEN s.from_user_id END) AS consult_trade_user_cnt
FROM ab_users ab
JOIN ba_phx.phx_mdw_detail_message_session_reply_time_by_daily s
  ON ab.user_id = s.from_user_id
JOIN ba_phx.phx_dim_message_session t
  ON s.dt = t.dt AND s.session_id = t.session_id
LEFT JOIN ba_phx.phx_dim_message_session_trade ts
  ON s.dt = ts.dt AND s.session_id = ts.session_id
WHERE s.dt BETWEEN 20260829 AND 20260902
  AND t.is_check_session = 1
GROUP BY ab.strategy_key, s.dt
