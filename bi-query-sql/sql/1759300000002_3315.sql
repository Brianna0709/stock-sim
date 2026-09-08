select identification
from mart_horizon_analyze_mtplatform.dws_arena_exp_flow_info_meituan_plat_4_di_view
where exp_key = 'shiyanzu1'
  and partition_date >= '2026-08-25'
  and strategy_type = 0
group by identification
