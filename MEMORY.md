# MEMORY.md - Long-Term Memory

## 进行中的任务

### 📊 客商IM周报数据（每周五）
- **频率**：每周五跑
- **时间范围**：周维度（最新一周）+ 月度（当月末/月初更新上月）
- **6个指标**：智能回复使用率、关闭率、未解决率(SQL1)、错误率(SQL2)、消息覆盖率、会话覆盖率
- **固定取数文件**：`/root/.openclaw/workspace/weekly_report_ics.md`（含完整SQL代码+历史数据）
- **核心SQL表**：`ba_phx.phx_mdw_detail_message_sync` + `ba_phx.phx_base_phx_osv_ics_host_setting_history`（CLI有权限）
- **可能需要魔数界面跑**：未解决率SQL1（origindb_ss）、错误率SQL2（bas_phx+log）
- **口径**：已确认，后续统一使用（见 memory/2026-04-08.md 详细SQL）
- **历史数据参考**：主人曾引用过完整表格，可复用

### 📚 K线/股票学习计划
- **学城文档**：[📚 小白股票课堂 · 14天入门课](https://km.sankuai.com/collabpage/2760975410)
- **contentId**：2760975410
- **状态**：✅ 全部完成（2026-05-13 开始，2026-05-22 全部写完）
- **Day 1~14 全部写入学城文档** ✅
- **注意**：文档为高密级，使用 `updateDocumentByXml` 方式写入
- **待插入图片**：https://km.sankuai.com/api/file/2760975410/236631233269（已上传到学城，等待插入）
- **学习进度跟踪**：`stock_course_progress.md`（主人确认学完当前课后，更新+1，明天推下一课；未确认则明天继续推同一课）
- **主人实际进度**：从 Day 4 开始就没学了，当前卡在 Day 4

### 📝 个人周报生成规则
- **Skill文件**：`/root/.openclaw/workspace/weekly_report_skill.md`
- **触发词**：写周报、生成周报、周报模板
- **固定结构**：工作进展 → 关键数据 → 问题与解决 → 下周计划 → 认知迭代（必填，禁止空话）
- **行业动态**：生成前先搜索近一周相关行业/竞品动态，自然融入进展或认知迭代，不单独列段
- **推送方式**：每周按此模板生成，推送给主人

### 📊 客商IM周报SQL口径（已确认）
- **使用率**：取"有在线房源的房东"层，月度口径（当月1日至统计周末），SQL 见 weekly_report_ics.md SQL-B
- **关闭率**：在线活跃房东（is_online_host=1 + status=1）中，当日操作关闭（ics_switch=0 且 gmt_modify 与 dt 同一天）/ 在线活跃房东总数，SQL 见 weekly_report_ics.md SQL-C
- **未解决率(SQL-D)**：`dt` 用**跑数当天**（确保分区已存在），不用统计周最后一天+1天。gmt_create 范围覆盖完整统计周。
- **错误率(SQL-E)**：SQL-E 口径确认无变化


