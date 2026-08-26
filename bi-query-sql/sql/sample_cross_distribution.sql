select 
  is_manual_valid_reply_with1min,
  is_valid_reply_with10min,
  is_valid_reply_with1h,
  is_manual_valid_reply,
  is_valid_reply,
  is_pure_manual_valid_reply,
  reply_type_new,
  count(*) as cnt
from ba_phx.phx_dim_message_session
where dt = '20260816'
and is_check_session = 1
group by 1, 2, 3, 4, 5, 6, 7
order by 1, 2, 3, 4, 5, 6, 7
