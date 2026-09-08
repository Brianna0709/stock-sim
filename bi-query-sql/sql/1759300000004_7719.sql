select identification
from mart_horizon_analyze_mtplatform.fact_log_horizon_arena_module_info
where exp_key = 'shiyanzu1'
  and partition_date >= '2026-08-25'
  and strategy_type = 0
group by identification
