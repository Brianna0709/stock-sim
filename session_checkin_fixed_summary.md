# Session Checkin Fixed - 查询结果摘要

## 执行时间
2026-07-15 15:12 ~ 15:25 (CST)

## 查询条件
- 日期范围：2026-06-23 ~ 2026-06-29 (`dt BETWEEN '20260623' AND '20260629'`)
- 数据表：`ba_phx.phx_mdw_detail_message_sync`
- 筛选条件：
  - 客人发给房东的消息（`is_from_phx_host = 0`, `is_to_phx_host = 1`）
  - 非系统自动发送（`is_auto_send_by_sys = 0`）
  - Session 首条消息的订单状态为"未下单"（`order_status = '0'`）
  - 消息内容包含入住相关关键词（入住|办理|登记|check in 等）
  - **修正点**：命中关键词的消息本身也要求 `order_status = '0'`（确保是订前阶段发的）

## 第一步：获取符合条件的 session_id
- **SQL 结果**：50 个 session_id（LIMIT 50）
- **说明**：实际符合条件的 session 数量可能超过 50 个，此处仅取前 50 个

## 第二步：查询完整会话内容
- **查询总行数**：907 条消息（talos 报告值）
- **实际收集行数**：906 条消息（1 条为重复消息，去重后为 906）
- **涵盖 session 数**：50 个 session 全部覆盖

### 按 session 消息数分布
- 最多消息的 session：367929496（136 条消息，横跨 6/24 和 6/27 两天）
- 最少消息的 session：367111328（3 条消息）
- 平均每个 session：约 18 条消息

## 第三步：Excel 文件
- **输出路径**：`/root/.openclaw/workspace/session_checkin_fixed.xlsx`
- **Sheet 名**：会话内容
- **数据行数**：906 行（+ 49 个分隔空行 + 1 行表头 = 956 行）
- **列**：session_id | 时间 | 发送方 | 消息内容 | 订单状态
- **格式**：
  - 表头加粗、浅蓝色背景 (RGB: 180,210,255)
  - 发送方：客人/房东
  - 订单状态：未下单/待确认/已确认/已入住/-
  - Arial 字体、大小 11
  - 文本自动换行
  - 首行冻结
  - 不同 session 之间用空行分隔

## 文枢链接
- SQL1 materialKey: `352739171830566912`
- SQL2 materialKey: `352739350245568512`
