SELECT session_id, gmt_msg_gen, is_from_phx_host, is_to_phx_host, is_auto_send_by_sys, valid_payload,
  get_json_object(msg_extension, '$.PHXExtensionOrderStatus') AS order_status
FROM ba_phx.phx_mdw_detail_message_sync
WHERE dt BETWEEN '20260623' AND '20260629'
  AND session_id = '367848530'
ORDER BY gmt_msg_gen