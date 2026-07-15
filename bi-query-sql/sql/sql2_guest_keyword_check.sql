SELECT session_id, gmt_msg_gen, valid_payload
FROM ba_phx.phx_mdw_detail_message_sync
WHERE dt BETWEEN '20260623' AND '20260629'
  AND session_id = '367848530'
  AND is_from_phx_host = 0
  AND is_to_phx_host = 1
  AND is_auto_send_by_sys = 0
  AND valid_payload RLIKE '入住|办理|登记|check in|Check in|Check In|CHECK IN'