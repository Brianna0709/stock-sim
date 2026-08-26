select
  t1.dt,
  sum(t1.im_denom) as im_denom,
  sum(t1.im_numer) as im_numer,
  sum(t1.call_denom) as call_denom,
  sum(t1.call_numer) as call_numer,
  case when (sum(t1.im_denom)+sum(t1.call_denom)) = 0 then 0
  else round((sum(t1.im_numer)+sum(t1.call_numer))/(sum(t1.im_denom)+sum(t1.call_denom)),4)
  end as daily_reply_1min_rate
from (
  select
    t4.dt,
    t4.to_user_id as host_id,
    count(distinct case when t5.is_check_session=1 then t4.session_id end) as im_denom,
    count(distinct case when t5.is_check_session=1 and t5.is_reply=1 and t5.is_manual_valid_reply_with1min=1 then t4.session_id end) as im_numer,
    0 as call_denom,
    0 as call_numer
  from ba_phx.phx_mdw_detail_message_session_reply_time_by_daily as t4
  join ba_phx.phx_dim_message_session as t5
    on t4.dt = t5.dt
    and t4.session_id = t5.session_id
  where t4.dt between '20260701' and '20260731'
    and t5.is_check_session=1
    and t4.is_to_host=1
  group by t4.dt, t4.to_user_id

  union all

  select
    t7.dt,
    t7.host_id,
    0 as im_denom,
    0 as im_numer,
    count(distinct if(t7.is_operation_time=1, t7.record_id, NULL)) as call_denom,
    count(distinct if(t7.call_result='接通' and t7.is_operation_time=1, t7.record_id, NULL)) as call_numer
  from ba_phx.dwd_host_multi_channel_call_detail_di as t7
  where t7.dt between '20260701' and '20260731'
    and t7.call_source_type = 'axb_call'
  group by t7.dt, t7.host_id
) t1
group by t1.dt
order by t1.dt
