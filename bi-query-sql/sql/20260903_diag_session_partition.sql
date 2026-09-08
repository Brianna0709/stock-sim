select t.dt as dt,
  count(distinct case when eu.uid is not null then t.session_id end) as exp_sess,
  count(distinct case when cu.uid is not null then t.session_id end) as ctrl_sess,
  count(distinct t.session_id) as total_sess,
  count(distinct case when eu.uid is not null then t.from_user_id end) as exp_users,
  count(distinct case when cu.uid is not null then t.from_user_id end) as ctrl_users,
  count(distinct t.from_user_id) as total_users
from ba_phx.phx_mdw_detail_message_session_reply_time_by_daily t
left join (select distinct cast(user_id as bigint) uid from upload_table.im_guess_ab_0902) eu on eu.uid = t.from_user_id
left join (select distinct cast(identification as bigint) uid from upload_table.im_guess_ab_duizhaozu) cu on cu.uid = t.from_user_id
where t.dt between 20260831 and 20260902
group by t.dt
order by t.dt
