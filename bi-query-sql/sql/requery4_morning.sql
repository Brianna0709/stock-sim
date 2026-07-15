SELECT 
  session_id, 
  gmt_msg_gen, 
  is_from_phx_host, 
  valid_payload,
  get_json_object(msg_extension, '$.PHXExtensionOrderStatus') AS order_status
FROM ba_phx.phx_mdw_detail_message_sync
WHERE dt = '20260624'
  AND session_id = '367929496'
  AND gmt_msg_gen >= '2026-06-24 00:00:00'
  AND gmt_msg_gen < '2026-06-24 14:00:00'
ORDER BY gmt_msg_gen