select
  t4.dt,
  count(distinct case when t5.is_check_session=1 then t4.session_id end) as im_denom,
  count(distinct case when t5.is_check_session=1 and t5.is_reply=1 and t5.is_manual_valid_reply_with1min=1 then t4.session_id end) as im_numer,
  case when count(distinct case when t5.is_check_session=1 then t4.session_id end) = 0 then 0
  else round(count(distinct case when t5.is_check_session=1 and t5.is_reply=1 and t5.is_manual_valid_reply_with1min=1 then t4.session_id end)/count(distinct case when t5.is_check_session=1 then t4.session_id end),4)
  end as daily_im_1min_reply_rate
from ba_phx.phx_mdw_detail_message_session_reply_time_by_daily as t4
join ba_phx.phx_dim_message_session as t5
  on t4.dt = t5.dt
  and t4.session_id = t5.session_id
where t4.dt between '20260701' and '20260731'
  and ((t5.is_check_session=1 and t5.is_reply=1 and t5.is_manual_valid_reply_with1min=1)
   or (t5.is_check_session=1 and t4.is_to_host=1))
group by t4.dt
order by t4.dt
