const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  AlignmentType, HeadingLevel, BorderStyle, WidthType, ShadingType,
  VerticalAlign, LevelFormat
} = require('docx');
const fs = require('fs');

const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };
const cellMargins = { top: 100, bottom: 100, left: 140, right: 140 };

function headerCell(text, shade = "1F4E79") {
  return new TableCell({
    borders,
    margins: cellMargins,
    shading: { fill: shade, type: ShadingType.CLEAR },
    verticalAlign: VerticalAlign.CENTER,
    children: [new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new TextRun({ text, bold: true, color: "FFFFFF", size: 20, font: "Arial" })]
    })]
  });
}

function dataCell(text, shade = "FFFFFF", bold = false, align = AlignmentType.CENTER) {
  return new TableCell({
    borders,
    margins: cellMargins,
    shading: { fill: shade, type: ShadingType.CLEAR },
    children: [new Paragraph({
      alignment: align,
      children: [new TextRun({ text, bold, size: 20, font: "Arial" })]
    })]
  });
}

function sectionTitle(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 320, after: 160 },
    children: [new TextRun({ text, bold: true, size: 28, font: "Arial", color: "1F4E79" })]
  });
}

function bodyText(text, bold = false, color = "333333") {
  return new Paragraph({
    spacing: { before: 80, after: 80 },
    children: [new TextRun({ text, bold, size: 20, font: "Arial", color })]
  });
}

function highlight(text) {
  return new Paragraph({
    spacing: { before: 120, after: 120 },
    indent: { left: 360 },
    children: [new TextRun({ text, bold: true, size: 22, font: "Arial", color: "C00000" })]
  });
}

function gap() {
  return new Paragraph({ spacing: { before: 60, after: 60 }, children: [new TextRun("")] });
}

const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 20 } } },
    paragraphStyles: [
      {
        id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 36, bold: true, font: "Arial", color: "1F4E79" },
        paragraph: { spacing: { before: 360, after: 200 }, outlineLevel: 0 }
      },
      {
        id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: "Arial", color: "1F4E79" },
        paragraph: { spacing: { before: 280, after: 140 }, outlineLevel: 1 }
      }
    ]
  },
  numbering: {
    config: [
      {
        reference: "bullets",
        levels: [{
          level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } }
        }]
      }
    ]
  },
  sections: [{
    properties: {
      page: {
        size: { width: 11906, height: 16838 },
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
      }
    },
    children: [

      // ===== 标题 =====
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        alignment: AlignmentType.CENTER,
        spacing: { before: 0, after: 240 },
        children: [new TextRun({ text: "客商IM 智能回复覆盖率分析", bold: true, size: 40, font: "Arial", color: "1F4E79" })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 0, after: 480 },
        children: [new TextRun({ text: "数据口径：2026年1月4日 - 4月6日  |  制作：万能小汪分身", size: 18, font: "Arial", color: "777777" })]
      }),

      // ===== 一、核心指标汇总 =====
      sectionTitle("一、核心指标汇总（0104-0111 vs 0131-0406）"),
      gap(),

      new Table({
        width: { size: 100, type: WidthType.PERCENTAGE },
        columnWidths: [2400, 2200, 2200, 2200],
        rows: [
          new TableRow({
            tableHeader: true,
            children: [
              headerCell("覆盖维度"),
              headerCell("基准期（0104-0111）"),
              headerCell("对比期（0131-0406）"),
              headerCell("变化"),
            ]
          }),
          new TableRow({ children: [
            dataCell("会话覆盖率", "EBF3FB", true, AlignmentType.LEFT),
            dataCell("45.12%", "FFFFFF"),
            dataCell("49.61%", "E2EFDA"),
            dataCell("+4.49pp", "E2EFDA", true),
          ]}),
          new TableRow({ children: [
            dataCell("在线房东覆盖率", "EBF3FB", true, AlignmentType.LEFT),
            dataCell("23.83%", "FFFFFF"),
            dataCell("33.82%", "E2EFDA"),
            dataCell("+9.99pp", "E2EFDA", true),
          ]}),
          new TableRow({ children: [
            dataCell("活跃房东覆盖率", "EBF3FB", true, AlignmentType.LEFT),
            dataCell("37.27%", "FFFFFF"),
            dataCell("50.04%", "E2EFDA"),
            dataCell("+12.77pp", "E2EFDA", true),
          ]}),
        ]
      }),
      gap(),
      bodyText("注：两个维度口径不同——会话覆盖来自消息记录表，房东覆盖来自智能回复日志表（见第三节）。", false, "888888"),
      gap(),

      // ===== 二、两个维度的当前水位与上限 =====
      sectionTitle("二、当前水位 vs 理论上限"),
      gap(),

      // 2.1 会话维度
      bodyText("2.1  会话维度", true),
      gap(),
      new Table({
        width: { size: 100, type: WidthType.PERCENTAGE },
        columnWidths: [3000, 2500, 2500, 1906],
        rows: [
          new TableRow({ tableHeader: true, children: [
            headerCell("口径"),
            headerCell("总会话数"),
            headerCell("智能回复会话数"),
            headerCell("覆盖率"),
          ]}),
          new TableRow({ children: [
            dataCell("当前水位（0131-0406累计）", "EBF3FB", true, AlignmentType.LEFT),
            dataCell("1,230万", "FFFFFF"),
            dataCell("674万", "FFFFFF"),
            dataCell("54.8%", "E2EFDA", true),
          ]}),
          new TableRow({ children: [
            dataCell("理论上限", "FFF2CC", true, AlignmentType.LEFT),
            dataCell("1,230万", "FFFFFF"),
            dataCell("≈ 1,230万", "FFF2CC"),
            dataCell("~100%", "FFF2CC", true),
          ]}),
        ]
      }),
      gap(),
      new Paragraph({
        spacing: { before: 80, after: 80 },
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun({ text: "当前会话覆盖约55%，即每2个咨询会话中有1个完全没有智能回复介入。", size: 20, font: "Arial" })]
      }),
      new Paragraph({
        spacing: { before: 80, after: 80 },
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun({ text: "理论上限为100%（每个会话均有智能回复），实际天花板受制于：开关关闭的房东、问题类型超出模型覆盖范围。", size: 20, font: "Arial" })]
      }),
      gap(),

      // 2.2 活跃房东维度
      bodyText("2.2  活跃房东维度", true),
      gap(),
      new Table({
        width: { size: 100, type: WidthType.PERCENTAGE },
        columnWidths: [3000, 2500, 2500, 1906],
        rows: [
          new TableRow({ tableHeader: true, children: [
            headerCell("口径"),
            headerCell("分母（房东数）"),
            headerCell("有智能回复房东"),
            headerCell("覆盖率"),
          ]}),
          new TableRow({ children: [
            dataCell("当前水位（近3月区间）", "EBF3FB", true, AlignmentType.LEFT),
            dataCell("24.7万（全部活跃）", "FFFFFF"),
            dataCell("16.1万", "FFFFFF"),
            dataCell("65.3%", "E2EFDA", true),
          ]}),
          new TableRow({ children: [
            dataCell("日均水位", "EBF3FB", true, AlignmentType.LEFT),
            dataCell("6.2万（日均被咨询）", "FFFFFF"),
            dataCell("5.1万", "FFFFFF"),
            dataCell("82.5%", "E2EFDA", true),
          ]}),
          new TableRow({ children: [
            dataCell("理论上限（天花板）", "FFF2CC", true, AlignmentType.LEFT),
            dataCell("22.5万（有过咨询）", "FFF2CC"),
            dataCell("≈ 22.5万", "FFF2CC"),
            dataCell("~91%*", "FFF2CC", true),
          ]}),
        ]
      }),
      gap(),
      bodyText("*理论上限说明：全量24.7万活跃房东中，约2.2万从未收到过房客咨询，无法产生智能回复；有咨询的22.5万才是真实天花板，占比约91%。", false, "888888"),
      gap(),

      // ===== 三、活跃房东覆盖上不去的根因 =====
      sectionTitle("三、活跃房东覆盖率天花板分析（根因拆解）"),
      gap(),
      bodyText("数据口径：有IM咨询的活跃房东（~22.5万累计），按开关状态分布："),
      gap(),

      new Table({
        width: { size: 100, type: WidthType.PERCENTAGE },
        columnWidths: [4200, 2400, 2000, 1306],
        rows: [
          new TableRow({ tableHeader: true, children: [
            headerCell("开关状态"),
            headerCell("人数"),
            headerCell("占比"),
            headerCell("说明"),
          ]}),
          new TableRow({ children: [
            dataCell("实际使用智能回复", "E2EFDA", true, AlignmentType.LEFT),
            dataCell("16.1万", "E2EFDA"),
            dataCell("70.3%", "E2EFDA", true),
            dataCell("正常覆盖", "E2EFDA"),
          ]}),
          new TableRow({ children: [
            dataCell("开关开启但未触发", "FFFFFF", false, AlignmentType.LEFT),
            dataCell("0.4万", "FFFFFF"),
            dataCell("1.8%", "FFFFFF"),
            dataCell("场景缺失", "FFFFFF"),
          ]}),
          new TableRow({ children: [
            dataCell("主动关闭了开关", "FFC7CE", true, AlignmentType.LEFT),
            dataCell("5.9万", "FFC7CE"),
            dataCell("25.7%", "FFC7CE", true),
            dataCell("核心障碍", "FFC7CE", true),
          ]}),
          new TableRow({ children: [
            dataCell("从未设置过", "FFFFFF", false, AlignmentType.LEFT),
            dataCell("0.5万", "FFFFFF"),
            dataCell("2.2%", "FFFFFF"),
            dataCell("引导缺失", "FFFFFF"),
          ]}),
        ]
      }),
      gap(),
      highlight("核心结论：覆盖上不去的根因是「主动关闭」（占未覆盖的87%），而非认知/引导问题。"),
      gap(),
      new Paragraph({
        spacing: { before: 80, after: 80 },
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun({ text: "5.9万房东用过之后觉得不好用，主动关掉了开关 —— 这是满意度信号，不是触达问题。", size: 20, font: "Arial" })]
      }),
      new Paragraph({
        spacing: { before: 80, after: 80 },
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun({ text: "提升覆盖率的路径只有一条：提升准确率/体验 → 降低关闭率 → 覆盖率自然上升。", size: 20, font: "Arial" })]
      }),
      new Paragraph({
        spacing: { before: 80, after: 80 },
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun({ text: "活跃房东覆盖从37%升至50%（+12.77pp），大概率来自准确率提升后关闭的房东重新开启。", size: 20, font: "Arial" })]
      }),
      gap(),

      // ===== 四、日均绝对值趋势 =====
      sectionTitle("四、日均绝对值趋势（0131-0406）"),
      gap(),

      new Table({
        width: { size: 100, type: WidthType.PERCENTAGE },
        columnWidths: [2200, 2500, 2500, 2706],
        rows: [
          new TableRow({ tableHeader: true, children: [
            headerCell("月份"),
            headerCell("日均使用智能回复房东"),
            headerCell("日均被咨询活跃房东"),
            headerCell("日均介入率"),
          ]}),
          new TableRow({ children: [
            dataCell("1月（仅0131）", "EBF3FB", false, AlignmentType.LEFT),
            dataCell("4.3万", "FFFFFF"),
            dataCell("5.4万", "FFFFFF"),
            dataCell("80.4%", "FFFFFF"),
          ]}),
          new TableRow({ children: [
            dataCell("2月", "EBF3FB", false, AlignmentType.LEFT),
            dataCell("4.9万", "FFFFFF"),
            dataCell("6.2万", "FFFFFF"),
            dataCell("79.5%", "FFFFFF"),
          ]}),
          new TableRow({ children: [
            dataCell("3月", "EBF3FB", false, AlignmentType.LEFT),
            dataCell("5.0万", "FFFFFF"),
            dataCell("6.0万", "FFFFFF"),
            dataCell("83.8%", "FFFFFF"),
          ]}),
          new TableRow({ children: [
            dataCell("4月（01-06）", "EBF3FB", false, AlignmentType.LEFT),
            dataCell("6.1万", "E2EFDA", true),
            dataCell("7.1万", "E2EFDA"),
            dataCell("85.6%", "E2EFDA", true),
          ]}),
          new TableRow({ children: [
            dataCell("整体均值", "1F4E79", true, AlignmentType.LEFT),
            dataCell("5.1万", "1F4E79", true),
            dataCell("6.2万", "1F4E79", true),
            dataCell("82.5%", "1F4E79", true),
          ]}),
        ]
      }),
      gap(),
      new Paragraph({
        spacing: { before: 80, after: 80 },
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun({ text: "春节旺季（0218-0220）峰值：被咨询9.2万，介入率反降至76-78%（新房东涌入，未配置比例高）。", size: 20, font: "Arial" })]
      }),
      new Paragraph({
        spacing: { before: 80, after: 80 },
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun({ text: "3月起介入率稳步上升至84-87%，说明产品质量持续改善。", size: 20, font: "Arial" })]
      }),
      new Paragraph({
        spacing: { before: 80, after: 80 },
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun({ text: "清明假期（0403-0404）使用峰值7.2万，覆盖率86.2%，近期最高水位。", size: 20, font: "Arial" })]
      }),
      gap(),

      // ===== 五、口径说明 =====
      sectionTitle("五、数据口径说明"),
      gap(),

      new Table({
        width: { size: 100, type: WidthType.PERCENTAGE },
        columnWidths: [2400, 4000, 3506],
        rows: [
          new TableRow({ tableHeader: true, children: [
            headerCell("指标"),
            headerCell("数据表"),
            headerCell("关键字段"),
          ]}),
          new TableRow({ children: [
            dataCell("会话覆盖率", "EBF3FB", true, AlignmentType.LEFT),
            dataCell("ba_phx.phx_mdw_detail_message_sync", "FFFFFF", false, AlignmentType.LEFT),
            dataCell("is_from_phx_host=1，auto_reply_msg_type='IntelligentResponse'", "FFFFFF", false, AlignmentType.LEFT),
          ]}),
          new TableRow({ children: [
            dataCell("房东覆盖率（汇报口径）", "EBF3FB", true, AlignmentType.LEFT),
            dataCell("log.phx_hsop_osv_ai_reply_log", "FFFFFF", false, AlignmentType.LEFT),
            dataCell("ai_msg_recommend_strategy>0，HOUR>=7", "FFFFFF", false, AlignmentType.LEFT),
          ]}),
          new TableRow({ children: [
            dataCell("活跃房东分母", "EBF3FB", true, AlignmentType.LEFT),
            dataCell("ba_phx.phx_dim_supply_product_active_derive", "FFFFFF", false, AlignmentType.LEFT),
            dataCell("product_operation_type=1，dt=当日快照", "FFFFFF", false, AlignmentType.LEFT),
          ]}),
          new TableRow({ children: [
            dataCell("被咨询（天花板）", "EBF3FB", true, AlignmentType.LEFT),
            dataCell("ba_phx.phx_mdw_detail_message_session_reply_time_by_daily", "FFFFFF", false, AlignmentType.LEFT),
            dataCell("is_from_host=0（房客发起）", "FFFFFF", false, AlignmentType.LEFT),
          ]}),
        ]
      }),
      gap(),

      // ===== 结论 =====
      sectionTitle("六、结论与建议"),
      gap(),
      new Paragraph({
        spacing: { before: 100, after: 100 },
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun({ text: "活跃房东覆盖50%（全量口径）与日均介入率82.5%（有咨询时）并不矛盾，前者说「广度」，后者说「深度」。", size: 20, font: "Arial" })]
      }),
      new Paragraph({
        spacing: { before: 100, after: 100 },
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun({ text: "提升覆盖率的关键路径：准确率提升 → 减少「用了觉得不好用主动关闭」的5.9万房东 → 覆盖率自然增长。", size: 20, font: "Arial" })]
      }),
      new Paragraph({
        spacing: { before: 100, after: 100 },
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun({ text: "会话覆盖天花板仍有约45%空间（当前55%→理论100%），优先方向是未覆盖会话的场景拓展。", size: 20, font: "Arial" })]
      }),
      new Paragraph({
        spacing: { before: 100, after: 100 },
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun({ text: "旺季覆盖率下滑（新房东涌入）是正常现象，可考虑针对新房东的智能回复引导流程优化。", size: 20, font: "Arial" })]
      }),
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("/root/.openclaw/workspace/智能回复覆盖率分析.docx", buffer);
  console.log("Done");
});
