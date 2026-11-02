// Usage: node scripts/render_pdf.js matchup-roast.html matchup-roast-weekN.pdf
// Needs Playwright (preinstalled in the cloud container; otherwise `npm i playwright && npx playwright install chromium`).
// Hides the on-page PDF download link (.noprint) via the HTML's print CSS. Dark theme is the default.
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [src, dst] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1500 } });
  await p.goto('file://' + path.resolve(src), { waitUntil: 'networkidle' }).catch(() => {});
  await p.emulateMedia({ media: 'print', colorScheme: 'dark' });
  await p.pdf({ path: dst, width: '1080px', height: '1500px', printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
  await b.close();
})();
