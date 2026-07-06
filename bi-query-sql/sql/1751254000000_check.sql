SELECT
  host_id,
  ics_switch,
  gmt_modify,
  dt
FROM ba_phx.phx_base_phx_osv_ics_host_setting_history
WHERE dt = '20260629'
  AND host_id = 114444201
ORDER BY id DESC
LIMIT 1