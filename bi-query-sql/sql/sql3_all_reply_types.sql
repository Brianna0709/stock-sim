-- 全部考核会话的 reply_type_new 分布，确认枚举值范围
select 
  coalesce(cast(t5.reply_type_new as string), 'null') as reply_type_new,
  count(distinct t4.session_id) as session_cnt
from ba_phx.phx_mdw_detail_message_session_reply_time_by_daily as t4
join ba_phx.phx_dim_message_session as t5
  on t4.dt = t5.dt
  and t4.session_id = t5.session_id
where t4.dt = '20260816'
  and t5.is_check_session = 1
group by 1
order by 2 desc
