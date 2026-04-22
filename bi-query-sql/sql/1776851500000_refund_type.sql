SELECT
    dt,
    -- 区分协商退和非协商退
    CASE 
        WHEN msg_payload RLIKE '(协商退)' THEN '协商退'
        ELSE '非协商退'
    END AS refund_type,
    COUNT(DISTINCT from_dx_uid) AS refund_inquiry_guest_cnt
FROM
    ba_phx.phx_mdw_detail_message_sync
WHERE
    dt BETWEEN '20251215' AND '20260115'
    -- 1. 限定方向：房客发给房东
    AND is_from_phx_host = 0 
    AND is_to_phx_host = 1
    -- 2. 核心：模糊匹配退款意图关键词
    AND msg_payload RLIKE '(退款|退费|退钱|全额退|申请退|协商退|补差价|赔偿|取消订单|取消预订)'
GROUP BY
    dt,
    CASE 
        WHEN msg_payload RLIKE '(协商退)' THEN '协商退'
        ELSE '非协商退'
    END
ORDER BY 
    dt, refund_type
