SELECT 
  session_id, 
  gmt_msg_gen, 
  is_from_phx_host, 
  valid_payload,
  get_json_object(msg_extension, '$.PHXExtensionOrderStatus') AS order_status
FROM ba_phx.phx_mdw_detail_message_sync
WHERE dt BETWEEN '20260623' AND '20260629'
  AND session_id IN ('367849291','367901985','367916312','367801015','367787858')
ORDER BY session_id, gmt_msg_gen