select exp_key, layer_key, strategy_key, strategy_type, count(distinct identification) as user_cnt
from mart_horizon_analyze_mtplatform.dws_arena_exp_flow_info_hotel_travel_15_di_view
where partition_date = '2026-09-01'
  and (strategy_key like '%shiyanzu%' or exp_key like '%shiyanzu%')
group by 1,2,3,4
