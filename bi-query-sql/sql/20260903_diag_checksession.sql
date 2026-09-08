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
  t.is_check_session,
  COUNT(DISTINCT s.session_id) AS session_cnt,
  COUNT(DISTINCT s.from_user_id) AS user_cnt
FROM ab_users ab
JOIN ba_phx.phx_mdw_detail_message_session_reply_time_by_daily s
  ON ab.user_id = s.from_user_id
JOIN ba_phx.phx_dim_message_session t
  ON s.dt = t.dt AND s.session_id = t.session_id
WHERE s.dt BETWEEN 20260831 AND 20260902
GROUP BY ab.strategy_key, s.dt, t.is_check_session
ORDER BY s.dt, ab.strategy_key, t.is_check_session
