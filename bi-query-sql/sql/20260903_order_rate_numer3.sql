SELECT
  o.create_order_date AS order_date,
  COUNT(DISTINCT CASE WHEN eu.uid IS NOT NULL THEN o.order_id END) AS exp_order_cnt,
  COUNT(DISTINCT CASE WHEN cu.uid IS NOT NULL THEN o.order_id END) AS ctrl_order_cnt
FROM
  ba_phx.phx_mdw_detail_message_session_reply_time_by_daily AS m
JOIN
  ba_phx.phx_topic_magic_trade_order AS o
ON
  m.from_user_id = o.user_id
  AND m.to_user_id = o.host_id
LEFT JOIN (select distinct cast(user_id as bigint) as uid from upload_table.im_guess_ab_0902) eu ON eu.uid = m.from_user_id
LEFT JOIN (select distinct cast(identification as bigint) as uid from upload_table.im_guess_ab_duizhaozu) cu ON cu.uid = m.from_user_id
WHERE
  m.dt BETWEEN '20260829' AND '20260903'
  AND m.is_from_host = 0
  AND o.create_order_time > m.gmt_init
  AND o.create_order_date = DATE(STR_TO_DATE(m.dt, '%Y%m%d'))
  AND o.process_code = 'create'
GROUP BY
  o.create_order_date
ORDER BY
  order_date
