SELECT DISTINCT session_id
FROM ba_phx.phx_mdw_detail_message_sync
WHERE dt BETWEEN '20260623' AND '20260629'
  AND is_from_phx_host = 0
  AND is_to_phx_host = 1
  AND is_auto_send_by_sys = 0
  AND session_id IS NOT NULL
  AND session_id IN (
    SELECT session_id
    FROM (
      SELECT
        session_id,
        get_json_object(msg_extension, '$.PHXExtensionOrderStatus') AS os,
        ROW_NUMBER() OVER (PARTITION BY session_id ORDER BY gmt_msg_gen) AS rn
      FROM ba_phx.phx_mdw_detail_message_sync
      WHERE dt BETWEEN '20260623' AND '20260629'
        AND is_from_phx_host = 0
        AND is_to_phx_host = 1
        AND is_auto_send_by_sys = 0
        AND session_id IS NOT NULL
        AND msg_extension IS NOT NULL
    ) t
    WHERE rn = 1 AND os = '0'
  )
  AND valid_payload RLIKE '入住|办理|登记|check in|Check in|Check In|CHECK IN'