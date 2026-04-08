const pptxgen = require("pptxgenjs");
const { html2pptx } = require("./html2pptx");

async function main() {
  const pptx = new pptxgen();
  pptx.layout = "LAYOUT_16x9";
  pptx.author = "万能小汪分身";
  pptx.title = "AI+美股每日早报 2026-03-13";

  console.log("Creating slide 1 - Cover...");
  await html2pptx("slide1.html", pptx);

  console.log("Creating slide 2 - AI News...");
  await html2pptx("slide2.html", pptx);

  console.log("Creating slide 3 - Market Indices...");
  await html2pptx("slide3.html", pptx);

  console.log("Creating slide 4 - Hot Stocks...");
  await html2pptx("slide4.html", pptx);

  console.log("Creating slide 5 - Investment Advice...");
  await html2pptx("slide5.html", pptx);

  console.log("Creating slide 6 - Risk & Sources...");
  await html2pptx("slide6.html", pptx);

  await pptx.writeFile({ fileName: "daily-briefing.pptx" });
  console.log("Done! daily-briefing.pptx created.");
}

main().catch(e => { console.error(e); process.exit(1); });
