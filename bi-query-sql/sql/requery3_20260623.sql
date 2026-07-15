SELECT 
  session_id, 
  gmt_msg_gen, 
  is_from_phx_host, 
  valid_payload,
  get_json_object(msg_extension, '$.PHXExtensionOrderStatus') AS order_status
FROM ba_phx.phx_mdw_detail_message_sync
WHERE dt = '20260623'
  AND session_id = '367929496'
ORDER BY gmt_msg_gen