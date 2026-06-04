WITH daily AS (
    SELECT
        dt,
        COUNT(DISTINCT CASE WHEN is_from_phx_host = 0 AND is_auto_send_by_sys = 0 AND is_im_block_each_today = 0 THEN session_id END) AS total_session,
        COUNT(DISTINCT CASE WHEN auto_reply_msg_type = 'IntelligentResponse' THEN session_id END) AS intelligent_session
    FROM ba_phx.phx_mdw_detail_message_sync
    WHERE dt BETWEEN '20260425' AND '20260501'
        AND is_im_block_each_today = 0
    GROUP BY dt
),
ics_daily AS (
    SELECT host_id, ics_switch, dt
    FROM (
        SELECT
            host_id,
            ics_switch,
            dt,
            ROW_NUMBER() OVER (PARTITION BY host_id, dt ORDER BY id DESC) AS rn
        FROM ba_phx.phx_base_phx_osv_ics_host_setting_history
        WHERE dt BETWEEN '20260425' AND '20260501'
    ) t
    WHERE rn = 1
),
session_host AS (
    SELECT dt, session_id, to_phx_user_id AS host_id
    FROM (
        SELECT
            dt,
            session_id,
            to_phx_user_id,
            ROW_NUMBER() OVER (PARTITION BY dt, session_id ORDER BY gmt_msg_gen) AS rn
        FROM ba_phx.phx_mdw_detail_message_sync
        WHERE dt BETWEEN '20260425' AND '20260501'
            AND is_from_phx_host = 0
            AND is_auto_send_by_sys = 0
            AND is_im_block_each_today = 0
    ) t
    WHERE rn = 1
),
ics_session_daily AS (
    SELECT
        s.dt,
        COUNT(DISTINCT CASE WHEN COALESCE(i.ics_switch,0)=1 THEN s.session_id END) AS ics_on_session
    FROM session_host s
    LEFT JOIN ics_daily i ON s.host_id=i.host_id AND s.dt=i.dt
    GROUP BY s.dt
)
SELECT
    ROUND(AVG(d.total_session), 0) AS avg_total_session,
    ROUND(AVG(i.ics_on_session), 0) AS avg_ics_on_session,
    ROUND(AVG(d.intelligent_session), 0) AS avg_intelligent_session,
    ROUND(AVG(i.ics_on_session)*100.0 / AVG(d.total_session), 2) AS ics_on_pct,
    ROUND(AVG(d.intelligent_session)*100.0 / AVG(d.total_session), 2) AS intelligent_pct
FROM daily d
JOIN ics_session_daily i ON d.dt = i.dt
