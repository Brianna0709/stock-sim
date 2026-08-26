select
  t1.host_id,
  coalesce(t1.im_numer, 0) as im_round_1min_reply,
  coalesce(t1.im_denom, 0) as im_round_total,
  0 as virtual_call_answered,
  0 as virtual_call_total,
  case when coalesce(t1.im_denom,0) = 0 then 0
  else round(coalesce(t1.im_numer,0)/coalesce(t1.im_denom,0),2)
  end as reply_1min_rate
from (
  select
    t4.to_user_id as host_id,
    count(distinct case when t5.is_check_session=1 then t4.session_id end) as im_denom,
    count(distinct case when t5.is_check_session=1 and t5.is_reply=1 and t5.is_manual_valid_reply_with1min=1 then t4.session_id end) as im_numer
  from ba_phx.phx_mdw_detail_message_session_reply_time_by_daily as t4
  join ba_phx.phx_dim_message_session as t5
    on t4.dt = t5.dt
    and t4.session_id = t5.session_id
  where t4.dt between '20260701' and '20260731'
    and ((t5.is_check_session=1 and t5.is_reply=1 and t5.is_manual_valid_reply_with1min=1)
     or (t5.is_check_session=1 and t4.is_to_host=1))
  group by t4.to_user_id
) as t1
