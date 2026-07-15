SET mapreduce.job.queuename=root.zw06_2.hadoop-phx.query;
SELECT 
  session_id, 
  gmt_msg_gen, 
  is_from_phx_host, 
  valid_payload,
  get_json_object(msg_extension, '$.PHXExtensionOrderStatus') AS order_status
FROM ba_phx.phx_mdw_detail_message_sync
WHERE dt BETWEEN '20260101' AND '20260630'
  AND session_id = '343234358'
  AND gmt_msg_gen > '2026-02-18 14:51:35'
ORDER BY gmt_msg_gen