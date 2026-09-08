select `t45699_0_60036932`.`dt` as `dt`,
  count(distinct case when eu_session.uid is not null then `t45699_0_60036932`.`from_user_id` end) as exp_user_cnt,
  count(distinct case when cu_session.uid is not null then `t45699_0_60036932`.`from_user_id` end) as ctrl_user_cnt
from `ba_phx`.`phx_mdw_detail_message_session_reply_time_by_daily` as `t45699_0_60036932`
join `ba_phx`.`phx_dim_message_session` as `t3026286_1_60036932`
  on (`t45699_0_60036932`.`dt` = `t3026286_1_60036932`.`dt`
   and `t45699_0_60036932`.`session_id` = `t3026286_1_60036932`.`session_id`
   and `t3026286_1_60036932`.`dt` between 20260829 and 20260903)
join `ba_phx`.`phx_dim_message_session_trade` as `t3028836_3_60036932`
  on (`t45699_0_60036932`.`dt` = `t3028836_3_60036932`.`dt`
   and `t45699_0_60036932`.`session_id` = `t3028836_3_60036932`.`session_id`
   and `t3028836_3_60036932`.`dt` between 20260829 and 20260903)
left join (select distinct cast(user_id as bigint) as uid from upload_table.im_guess_ab_0902) eu_session on eu_session.uid = `t45699_0_60036932`.`from_user_id`
left join (select distinct cast(identification as bigint) as uid from upload_table.im_guess_ab_duizhaozu) cu_session on cu_session.uid = `t45699_0_60036932`.`from_user_id`
where (`t3026286_1_60036932`.`is_check_session` = 1
  and `t45699_0_60036932`.`dt` between 20260829 and 20260903
  and (t3028836_3_60036932.`session_paid_status` = 0 or t3028836_3_60036932.`session_paid_status` = 1))
group by 1
order by 1
