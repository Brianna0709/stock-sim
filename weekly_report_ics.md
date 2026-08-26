# 客商IM智能化周报 · 固定取数文件

> 每周五执行一次，跑最新一周数据（周维度）。
> 月度数据：当月末（或月初）更新上月完整数据，不必每周更新。

---

## 📊 当前数据表（持续追加）

### 月度数据

| 指标 | 202602 | 202603 | 202604 | 202605 | 202606(0601-0617) |
|------|:---:|:---:|:---:|:---:|:---:|
| 智能回复使用率-有在线房源房东 | 25.09% | 25.79% | 26.89% | 47.59% | 38.71% |
| 智能客服关闭率-房东(操作关闭率日均) | 0.18% | 0.05% | 0.11% | 0.053% | 0.035% |
| 智能IM房客点击未解决率(SQL1) | 0.68% | 0.75% | 0.71% | 0.6999% | ⚠️待确认 |
| 智能IM房东反馈错误率(SQL2) | 0.14% | 0.12% | 0.17% | 0.17% | 0.18% |
| 智能回复消息覆盖率 | 20.76% | 21.97% | 22.94% | 22.48% | 22.85% |
| 智能回复会话覆盖率 | 68.11% | 69.55% | 71.69% | 72.29% | 73.89% |

### 周度数据

| 指标 | W2(0425-0501) | W3(0502-0508) | W4(0509-0514) | W5(0515-0521) | W6(0522-0528) | W7(0529-0604) | W8(0605-0611) | W9(0612-0618) | W10(0613-0619) | W11(0619-0625) | W12(0626-0702) | W13(0710-0716) | W14(0717-0723) | W15(0725-0731) | W16(0801-0807) | W17(0808-0814) | W18(0815-0821) |
|------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 智能回复使用率-有在线房源房东 | 49.86% | 51.37% | 52.25% | 29.71% | 30.02% | 30.98% | 31.04% | 31.61% | 32.2% | 31.77% | 33.88% | 36.47% | 37.69% | 38.24% | 41.22% | 41.17% | 40.11% |
| 智能客服关闭率-房东(操作关闭率日均) | 0.30% | 0.08% | 0.03% | 0.03% | 0.03% | 0.03% | 0.03% | 0.035% | 0.04% | 0.04% | 0.05% | 0.05% | 0.06% | 0.06% | 0.09% | 0.053% | 0.035% |
| 智能IM房客点击未解决率(SQL1) | 0.71% | 0.72% | 0.66% | 0.70% | ⚠️待确认 | 0.68% | ⚠️待跑(魔数) | 0.6962% | 0.7046% | 0.6753% | 0.6605% | ⚠️待确认 | ⚠️分区无数据(魔数) | 0.63% | ⚠️待确认(2.27%) | ⚠️无权限(魔数) | ⚠️无权限(魔数) |
| 智能IM房东反馈错误率(SQL2) | 0.19% | 0.17% | 0.16% | 0.16% | 0.16% | 0.17% | 0.17% | 0.18% | 0.17% | 0.17% | 0.19% | 0.24% | 0.27% | 0.26% | 0.27% | ⚠️无权限(魔数) | ⚠️无权限(魔数) |
| 智能回复消息覆盖率 | 22.92% | 22.45% | 22.30% | 22.36% | 22.50% | 22.70% | 22.77% | 23.00% | 23.04% | 23.35% | 23.52% | 23.98% | 23.63% | 23.78% | 22.83% | 23.73% | 23.28% |
| 智能回复会话覆盖率 | 71.45% | 71.85% | 72.78% | 72.40% | 72.98% | 73.29% | 73.78% | 74.02% | 74.01% | 74.79% | 74.98% | 75.26% | 75.59% | 75.73% | 72.53% | 75.07% | 75.46% |

---

## 🔧 SQL 代码

### ⚠️ 执行方式说明

- `ba_phx.phx_mdw_detail_message_sync`：CLI 有权限，可用 bi-query-sql skill 直接跑
- `ba_phx.phx_base_phx_osv_ics_host_setting_history`：CLI 有权限
- `origindb_ss.hotel_ia_phx_user__phx_auto_reply_msg_survey`：CLI 无权限，需魔数界面执行
- `ba_phx.phx_dim_supply_host_extend` / `log.phx_hsop_osv_ai_reply_log` / `ba_phx.bas_phx_ai_reply_msg_host_survey`：CLI 有权限（但 `bas_phx_ai_reply_msg_host_survey` 实际无权限，需魔数界面）
- 推荐队列：`root.zw06_2.hadoop-phx.query`

---

### SQL-A：智能回复会话覆盖率 + 消息覆盖率

> 对应指标：**智能回复会话覆盖率**（层级3/层级1）和 **智能回复消息覆盖率**（IntelligentResponse消息数/总房东消息数）

```sql
-- 修改 dt BETWEEN 的日期范围即可复用
-- 周维度：如 '20260815' AND '20260821'
-- 月维度：如 '20260801' AND '20260831'

WITH
daily AS (
    SELECT dt,
        COUNT(DISTINCT CASE WHEN is_from_phx_host=0 AND is_auto_send_by_sys=0 AND is_im_block_each_today=0 THEN session_id END) AS total_session,
        COUNT(DISTINCT CASE WHEN auto_reply_msg_type='IntelligentResponse' THEN session_id END) AS intelligent_session,
        -- 消息覆盖率分子/分母（房东侧消息）
        COUNT(CASE WHEN is_from_phx_host=1 AND auto_reply_msg_type='IntelligentResponse' THEN 1 END) AS ai_msg_cnt,
        COUNT(CASE WHEN is_from_phx_host=1 THEN 1 END) AS total_host_msg
    FROM ba_phx.phx_mdw_detail_message_sync
    WHERE dt BETWEEN '20260815' AND '20260821'
      AND is_im_block_each_today = 0
    GROUP BY dt
),
ics_daily AS (
    SELECT host_id, ics_switch, dt
    FROM (
        SELECT host_id, ics_switch, dt,
               ROW_NUMBER() OVER (PARTITION BY host_id, dt ORDER BY id DESC) AS rn
        FROM ba_phx.phx_base_phx_osv_ics_host_setting_history
        WHERE dt BETWEEN '20260815' AND '20260821'
    ) t WHERE rn=1
),
session_host AS (
    SELECT dt, session_id, to_phx_user_id AS host_id
    FROM (
        SELECT dt, session_id, to_phx_user_id,
               ROW_NUMBER() OVER (PARTITION BY dt, session_id ORDER BY gmt_msg_gen) AS rn
        FROM ba_phx.phx_mdw_detail_message_sync
        WHERE dt BETWEEN '20260815' AND '20260821'
          AND is_from_phx_host=0 AND is_auto_send_by_sys=0 AND is_im_block_each_today=0
    ) t WHERE rn=1
),
ics_session_daily AS (
    SELECT s.dt,
           COUNT(DISTINCT CASE WHEN COALESCE(i.ics_switch,0)=1 THEN s.session_id END) AS ics_on_session
    FROM session_host s
    LEFT JOIN ics_daily i ON s.host_id=i.host_id AND s.dt=i.dt
    GROUP BY s.dt
)
SELECT
    ROUND(AVG(d.total_session), 0)                                         AS avg_total_session,
    ROUND(AVG(d.intelligent_session), 0)                                   AS avg_ai_session,
    ROUND(AVG(d.intelligent_session)*100.0/AVG(d.total_session), 2)        AS session_coverage_pct,
    ROUND(AVG(d.ai_msg_cnt)*100.0/NULLIF(AVG(d.total_host_msg),0), 2)     AS msg_coverage_pct,
    ROUND(AVG(i.ics_on_session)*100.0/AVG(d.total_session), 2)            AS ics_open_session_pct
FROM daily d
JOIN ics_session_daily i ON d.dt=i.dt;
```

---

### SQL-B：智能回复使用率（有在线房源的房东）

> 对应指标：**智能回复使用率**（使用智能回复的房东 / 有在线房源的房东总数）
> 表：`log.phx_hsop_osv_ai_reply_log` + `ba_phx.phx_dim_supply_host_extend`
> ✅ 取结果中 segment='有在线房源的房东' 的 usage_rate_pct
> ⚠️ 注意：dt BETWEEN 用**周度范围**（如0815-0821），维度表快照用当周最后一天（若当天数据未就绪则用最新可用日）

```sql
-- 修改 dt BETWEEN（ai_reply_log）和 dt（维度表快照）即可复用
-- 周维度：ai_reply_log 用统计周范围，维度表用当周最后一天

WITH
smart_reply_hosts AS (
    SELECT DISTINCT host_id
    FROM log.phx_hsop_osv_ai_reply_log
    WHERE dt BETWEEN '20260815' AND '20260821'
      AND ai_msg_recommend_strategy > 0
      AND HOUR(_mt_datetime) >= 7  -- 排除0-7点数据
),
online_hosts_stats AS (
    SELECT
        COUNT(DISTINCT c.host_id) AS total_hosts,
        COUNT(DISTINCT s.host_id) AS smart_reply_hosts
    FROM ba_phx.phx_dim_supply_host_extend c
    LEFT JOIN smart_reply_hosts s ON c.host_id = s.host_id
    WHERE c.dt = '20260820'  -- 当周最后一天快照（若0821未就绪则用最新可用）
      AND c.online_product_cnt > 0  -- 有在线房源
)
SELECT
    '有在线房源的房东' AS segment,
    o.total_hosts, o.smart_reply_hosts,
    ROUND(o.smart_reply_hosts * 100.0 / o.total_hosts, 2) AS usage_rate_pct
FROM online_hosts_stats o;
```

---

### SQL-C：智能客服关闭率-房东（操作关闭率日均）

> 对应指标：**智能客服关闭率**（当日操作关闭的房东数 / 在线活跃房东总数）
> 表：`ba_phx.phx_base_phx_osv_ics_host_setting_history` + `ba_phx.phx_dim_supply_host_extend`
> 口径：当日操作关闭 = ics_switch=0 且 gmt_modify 与 dt 同一天；分母 = 在线活跃房东（is_online_host=1 且 status=1）

```sql
SELECT
    s.dt AS `统计日期`,
    COUNT(DISTINCT s.host_id) AS `在线活跃房东总数`,
    COUNT(DISTINCT CASE WHEN s.ics_switch = 0 AND DATE_FORMAT(s.gmt_modify, 'yyyyMMdd') = s.dt THEN s.host_id END) AS `当日操作关闭的房东数`,
    COUNT(DISTINCT CASE WHEN s.ics_switch = 0 THEN s.host_id END) AS `当日关闭状态的房东数`,
    ROUND(
        COUNT(DISTINCT CASE WHEN s.ics_switch = 0 AND DATE_FORMAT(s.gmt_modify, 'yyyyMMdd') = s.dt THEN s.host_id END) * 1.0
        / COUNT(DISTINCT s.host_id), 4
    ) AS `当日操作关闭率`,
    ROUND(
        COUNT(DISTINCT CASE WHEN s.ics_switch = 0 THEN s.host_id END) * 1.0
        / COUNT(DISTINCT s.host_id), 4
    ) AS `当日状态关闭率`
FROM ba_phx.phx_base_phx_osv_ics_host_setting_history s
INNER JOIN ba_phx.phx_dim_supply_host_extend e
    ON s.host_id = e.host_id AND s.dt = e.dt
WHERE s.dt BETWEEN '20260815' AND '20260821'  -- 改时间范围
  AND s.status = 1
  AND e.is_online_host = 1
GROUP BY s.dt
ORDER BY s.dt;
```

---

### SQL-D：智能IM房客点击未解决率（SQL1口径）

> 对应指标：**房客点击未解决率**（SQL1口径）
> 表：`origindb_ss.hotel_ia_phx_user__phx_auto_reply_msg_survey` + `ba_phx.phx_mdw_detail_message_sync`
> ⚠️ 注意：`dt` 用**所有实际日分区**（确保覆盖全部数据），`gmt_create` 用实际统计范围；`result='0'` 表示未解决；`msg_type=2` 表示智能回复
> 📌 规则：dt IN 实际日分区列表；gmt_create 范围 = 统计周实际日期
> ⚠️ CLI 无权限，需在魔数 BI 界面执行

```sql
-- 修改 dt（实际日分区列表）、gmt_create 的时间范围即可复用
-- dt IN 当周所有实际日分区（如 '20260815' 至 '20260821'）
-- gmt_create 范围 = 实际统计周（如 W18: 2026-08-15 ~ 2026-08-21）

WITH unsolved_stats AS (
    SELECT SUM(CASE WHEN result = '0' THEN 1 ELSE 0 END) AS unresolved_count
    FROM origindb_ss.hotel_ia_phx_user__phx_auto_reply_msg_survey
    WHERE dt IN ('20260815','20260816','20260817','20260818','20260819','20260820','20260821')
      AND gmt_create >= '2026-08-15 00:00:00'
      AND gmt_create <  '2026-08-22 00:00:00'
      AND msg_type = 2                             -- 1-自动回复、2-智能回复
),
intelligent_reply_stats AS (
    SELECT COUNT(DISTINCT msg_id) AS total_replies
    FROM ba_phx.phx_mdw_detail_message_sync
    WHERE dt BETWEEN '20260815' AND '20260821'
      AND gmt_create >= '2026-08-15 00:00:00'
      AND gmt_create <  '2026-08-22 00:00:00'
      AND is_from_phx_host = 1
      AND auto_reply_msg_type = 'IntelligentResponse'
)
SELECT
    (SELECT unresolved_count FROM unsolved_stats)      AS unsolved_feedbacks,
    (SELECT total_replies FROM intelligent_reply_stats) AS total_intelligent_replies,
    CASE WHEN (SELECT total_replies FROM intelligent_reply_stats) > 0
         THEN ROUND(
             (SELECT unresolved_count FROM unsolved_stats) * 100.0
             / (SELECT total_replies FROM intelligent_reply_stats), 4)
         ELSE 0
    END AS unsolved_rate_pct;
```

---

### SQL-E：智能IM房东反馈错误率（SQL2口径）

> 对应指标：**房东反馈错误率**（SQL2口径）
> 表：`ba_phx.bas_phx_ai_reply_msg_host_survey` + `log.phx_hsop_osv_ai_reply_log`
> ⚠️ `gmt_create` / `_mt_datetime` 用实际统计范围（含首尾）；`ai_msg_recommend_strategy > 0` 表示使用了智能回复
> ⚠️ CLI 无权限，需在魔数 BI 界面执行

```sql
-- 修改 gmt_create / _mt_datetime 的时间范围即可复用
-- W18 示例：2026-08-15 00:00:00 ~ 2026-08-21 23:59:59

WITH host_survey AS (
    SELECT COUNT(id) AS host_survey
    FROM ba_phx.bas_phx_ai_reply_msg_host_survey
    WHERE gmt_create BETWEEN '2026-08-15 00:00:00' AND '2026-08-21 23:59:59'
),
ai_reply AS (
    SELECT COUNT(reply_id) AS reply_count
    FROM log.phx_hsop_osv_ai_reply_log
    WHERE dt BETWEEN '20260815' AND '20260821'
      AND _mt_datetime BETWEEN '2026-08-15 00:00:00' AND '2026-08-21 23:59:59'
      AND ai_msg_recommend_strategy > 0
)
SELECT
    host_survey.host_survey  AS host_survey_total,
    ai_reply.reply_count     AS ai_reply_total,
    ROUND(host_survey.host_survey * 100.0 / ai_reply.reply_count, 2) AS error_rate_pct
FROM host_survey, ai_reply;
```

---

## 📅 执行节奏

| 任务 | 频率 | 说明 |
|------|------|------|
| 跑 SQL-A（会话覆盖率+消息覆盖率） | 每周五 | CLI可跑，直接执行 |
| 跑 SQL-B（使用率） | 每周五 | CLI可跑，取周末快照 |
| 跑 SQL-C（关闭率） | 每周五 | CLI可跑 |
| 跑 SQL-D（未解决率SQL1） | 每周五 | 需在魔数BI界面执行（CLI无权限） |
| 跑 SQL-E（错误率SQL2） | 每周五 | 需在魔数BI界面执行（CLI无权限） |
| 更新月度数据 | 每月初 | 更新上月完整数据 |

---

## ⚠️ 注意事项

1. **日期格式**：SQL 里日期用 `'YYYYMMDD'` 格式（如 `'20260821'`）
2. **关闭率口径**：分母是当日开启状态的房东，不是全部注册房东
3. **SQL1 vs SQL2**：未解决率两套口径数值差4-6倍，以主人确认的为准
4. **月度 vs 周度分母**：月度数据直接改 BETWEEN 日期范围即可，算法一致
5. **使用率口径**：指全部注册房东（不是活跃房东），分母更大，数值会偏低
6. **SQL-D 分区规则**：SQL-D 的 `dt` 使用当周所有实际日分区列表（确保覆盖全部数据），`gmt_create` 用实际统计周范围
7. **无权限表**：`origindb_ss.hotel_ia_phx_user__phx_auto_reply_msg_survey` 和 `ba_phx.bas_phx_ai_reply_msg_host_survey` CLI无权限，需通过魔数BI界面执行
