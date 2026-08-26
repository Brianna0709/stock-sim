select
  coalesce(t1.host_id, t3.host_id) as host_id,
  coalesce(t1.im_numer, 0) as im_round_1min_reply,
  coalesce(t1.im_denom, 0) as im_round_total,
  coalesce(t3.call_numer, 0) as virtual_call_answered,
  coalesce(t3.call_denom, 0) as virtual_call_total,
  case when (coalesce(t1.im_denom,0)+coalesce(t3.call_denom,0)) = 0 then 0
  else round((coalesce(t1.im_numer,0)+coalesce(t3.call_numer,0))/(coalesce(t1.im_denom,0)+coalesce(t3.call_denom,0)),2)
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
full outer join (
  select
    t7.host_id,
    count(distinct if(t7.is_operation_time=1, t7.record_id, NULL)) as call_denom,
    count(distinct if(t7.call_result='接通' and t7.is_operation_time=1, t7.record_id, NULL)) as call_numer
  from ba_phx.dwd_host_multi_channel_call_detail_di as t7
  where t7.dt between '20260701' and '20260731'
    and t7.call_source_type = 'axb_call'
  group by t7.host_id
) as t3
on t1.host_id = t3.host_id
