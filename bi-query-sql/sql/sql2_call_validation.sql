-- 有虚拟电话接通的session，在is_manual_valid_reply_with1min中的分布
select 
  t5.is_manual_valid_reply_with1min,
  count(distinct t7.record_id) as call_cnt
from ba_phx.dwd_host_multi_channel_call_detail_di as t7
join ba_phx.phx_mdw_detail_message_session_reply_time_by_daily as t4
  on t7.host_id = t4.to_user_id
  and t7.dt = t4.dt
join ba_phx.phx_dim_message_session as t5
  on t4.dt = t5.dt
  and t4.session_id = t5.session_id
where t7.dt = '20260816'
  and t7.call_source_type = 'axb_call'
  and t7.call_result = '接通'
  and t7.is_operation_time = 1
  and t5.is_check_session = 1
group by 1
