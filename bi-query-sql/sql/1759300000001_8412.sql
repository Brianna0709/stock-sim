select
  count(distinct s.from_user_id) as im_guest_users,
  count(distinct m.user_id) as match_minsu_id,
  count(distinct t.meituan_user_id) as match_mt_id
from (
  select from_user_id
  from ba_phx.phx_mdw_detail_message_session_reply_time_by_daily
  where dt = 20250901 and is_from_host = 0
  group by from_user_id
) s
left join (
  select user_id
  from ba_phx.phx_topic_magic_trade_order
  where dt = 20250901 and process_code = 'paid' and paid_order_status = 1
  group by user_id
) m on s.from_user_id = m.user_id
left join (
  select meituan_user_id
  from ba_phx.phx_topic_magic_trade_order
  where dt = 20250901 and process_code = 'paid' and paid_order_status = 1
  group by meituan_user_id
) t on s.from_user_id = t.meituan_user_id
