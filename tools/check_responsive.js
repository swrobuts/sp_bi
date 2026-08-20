// Prueft die Abnahmekriterien, die einen echten Browser brauchen:
//
//   * scrollWidth <= innerWidth bei 320 / 390 / 768 / 1024 / 1440 px
//     (die Seite selbst darf nie horizontal scrollen; Tabellen und
//      Codebloecke duerfen es innerhalb ihres Containers)
//   * jede Seite rendert ueberhaupt - faengt Transpilierungsfehler ab
//   * kein "undefined" und keine CDN-Fehlermeldung im sichtbaren Text
//
// Voraussetzung: ein lokaler Server laeuft (python3 -m http.server 8765) und
// Playwright ist erreichbar. Bewusst KEINE package.json im Repo - die Seite
// selbst bleibt build-frei. Wer das Skript braucht, installiert Playwright
// einmalig:  npx playwright install chromium
//
// Aufruf:  node tools/check_responsive.js [http://localhost:8765]

// Playwright aus dem Projekt, global oder aus dem npx-Cache aufloesen.
// Im npx-Cache liegen oft mehrere Versionen, und nicht zu jeder ist der
// passende Browser heruntergeladen - deshalb werden alle Kandidaten
// gesammelt und beim Start der Reihe nach probiert.
function playwrightCandidates() {
  const out = [];
  for (const name of ['playwright', 'playwright-core']) {
    try { out.push(require(name)); } catch (e) { /* weiter */ }
  }
  const fs = require('fs'), path = require('path'), os = require('os');
  const cache = path.join(os.homedir(), '.npm', '_npx');
  if (fs.existsSync(cache)) {
    for (const dir of fs.readdirSync(cache)) {
      for (const name of ['playwright', 'playwright-core']) {
        const cand = path.join(cache, dir, 'node_modules', name);
        if (fs.existsSync(cand)) {
          try { out.push(require(cand)); } catch (e) { /* weiter */ }
        }
      }
    }
  }
  if (!out.length) {
    console.error('Playwright nicht gefunden. Einmalig einrichten:\n' +
                  '  npx playwright install chromium');
    process.exit(2);
  }
  return out;
}

// Erst den mitgelieferten Chromium probieren, dann das System-Chrome.
async function launch() {
  const errors = [];
  for (const pw of playwrightCandidates()) {
    for (const opts of [{}, { channel: 'chrome' }]) {
      try { return await pw.chromium.launch(opts); }
      catch (e) { errors.push(e.message.split('\n')[0]); }
    }
  }
  console.error('Kein startbarer Browser gefunden:\n  ' + [...new Set(errors)].join('\n  ') +
                '\nAbhilfe:  npx playwright install chromium');
  process.exit(2);
}

const BASE = process.argv[2] || 'http://localhost:8765';
const PAGES = ['index.html', 'lab-01-grundlagen.html', 'lab-02-daten.html',
               'lab-03-kpis.html', 'lab-04-dashboards.html',
               'lab-05-fallstudie.html', 'lab-06-souveraenitaet.html'];
const WIDTHS = [320, 390, 768, 1024, 1440];
const LANGS = ['de', 'en'];

(async () => {
  const browser = await launch();
  const fails = [];
  let checked = 0;

  for (const w of WIDTHS) {
    const ctx = await browser.newContext({ viewport: { width: w, height: 900 } });
    const page = await ctx.newPage();
    for (const p of PAGES) {
      for (const lang of LANGS) {
        await page.goto(`${BASE}/${p}?lang=${lang}`, { waitUntil: 'networkidle' });
        // Babel transpiliert im Browser - kurz warten, bis gemountet ist.
        await page.waitForFunction(
          () => (document.getElementById('root') || {}).children?.length > 0,
          null, { timeout: 20000 }
        ).catch(() => {});
        const r = await page.evaluate(() => ({
          sw: document.documentElement.scrollWidth,
          iw: window.innerWidth,
          len: (document.getElementById('root') || document.body).textContent.trim().length,
          bad: /undefined|\[object Object\]|konnte nicht geladen|could not load/.test(document.body.innerText),
        }));
        checked++;
        const at = `${p} ${lang} @${w}px`;
        if (r.sw > r.iw) fails.push(`${at}: scrollWidth ${r.sw} > innerWidth ${r.iw}`);
        if (r.len < 1500) fails.push(`${at}: nicht gerendert (${r.len} Zeichen)`);
        if (r.bad) fails.push(`${at}: Fehlertext im sichtbaren Inhalt`);
      }
    }
    await ctx.close();
  }
  await browser.close();

  fails.forEach((f) => console.log('[FAIL]', f));
  console.log(`\n${checked - fails.length} von ${checked} Kombinationen bestanden`);
  process.exit(fails.length ? 1 : 0);
})();
