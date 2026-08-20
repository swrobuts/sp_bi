// Prueft die Abnahmekriterien, die einen echten Browser brauchen:
//
//   * scrollWidth <= innerWidth bei 320 / 390 / 768 / 1024 / 1440 px
//     (die Seite selbst darf nie horizontal scrollen; Tabellen und
//      Codebloecke duerfen es innerhalb ihres Containers)
//   * jede Seite rendert ueberhaupt - faengt Transpilierungsfehler ab
//   * kein "undefined" und keine CDN-Fehlermeldung im sichtbaren Text
//   * genau eine h1 je Seite, Sprunglink mit vorhandenem Ziel und
//     Sprachbuttons mit aria-label und aria-pressed
//
// Voraussetzung: ein lokaler Server laeuft (python3 -m http.server 8765) und
// Playwright ist erreichbar. Bewusst KEINE package.json im Repo - die Seite
// selbst bleibt build-frei. Wer das Skript braucht, installiert Playwright
// einmalig:  npx playwright install chromium
//
// Aufruf:  node tools/check_responsive.js [basis] [pfade] [--no-lang]
//   node tools/check_responsive.js http://localhost:8765
//   node tools/check_responsive.js http://127.0.0.1:8050 / --no-lang

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
// Ohne dritten Parameter werden die sieben Lernseiten geprueft. Mit einer
// kommagetrennten Pfadliste laesst sich stattdessen etwas anderes pruefen -
// zum Beispiel eine laufende Starter-Dash-App, die keine Sprachvarianten hat.
const PAGES = process.argv[3]
  ? process.argv[3].split(',').map((p) => p.trim()).filter(Boolean)
  : ['index.html', 'lab-01-grundlagen.html', 'lab-02-daten.html',
     'lab-03-kpis.html', 'lab-04-dashboards.html',
     'lab-05-fallstudie.html', 'lab-06-souveraenitaet.html'];
const WIDTHS = [320, 390, 768, 1024, 1440];
const LANGS = process.argv.includes('--no-lang') ? [null] : ['de', 'en'];
// Dash rendert die Diagramme erst nach dem ersten Callback - dann ist der
// Mindestinhalt deutlich kleiner als bei einer Lab-Seite.
const MIN_LEN = process.argv.includes('--no-lang') ? 40 : 1500;

(async () => {
  const browser = await launch();
  const fails = [];
  let checked = 0;

  for (const w of WIDTHS) {
    const ctx = await browser.newContext({ viewport: { width: w, height: 900 } });
    const page = await ctx.newPage();
    for (const p of PAGES) {
      for (const lang of LANGS) {
        const url = lang ? `${BASE}/${p}?lang=${lang}` : `${BASE}/${p}`;
        await page.goto(url, { waitUntil: 'networkidle' });
        // Babel transpiliert im Browser - kurz warten, bis gemountet ist.
        await page.waitForFunction(
          () => (document.getElementById('root') || {}).children?.length > 0,
          null, { timeout: 20000 }
        ).catch(() => {});
        if (MIN_LEN < 1500) await page.waitForTimeout(3500);  // Dash-Callbacks abwarten
        const r = await page.evaluate(() => ({
          sw: document.documentElement.scrollWidth,
          iw: window.innerWidth,
          len: (document.getElementById('root') || document.body).textContent.trim().length,
          bad: /undefined|\[object Object\]|konnte nicht geladen|could not load/.test(document.body.innerText),
          // Genau eine h1 je Seite: darunter haengt die Ueberschriftenhierarchie,
          // an der sich Screenreader-Nutzer durch die Seite bewegen.
          h1: document.querySelectorAll('h1').length,
          // Sprunglink und zugaengliche Sprachbuttons
          skip: !!document.querySelector('.skip-link'),
          skipTargetOk: (() => {
            const a = document.querySelector('.skip-link');
            if (!a) return false;
            try { return !!document.querySelector(a.getAttribute('href')); } catch (e) { return false; }
          })(),
          langLabelled: [...document.querySelectorAll('.lang-btn')]
            .every((b) => b.getAttribute('aria-label') && b.getAttribute('aria-pressed') !== null),
        }));
        checked++;
        const at = `${p}${lang ? ' ' + lang : ''} @${w}px`;
        if (r.sw > r.iw) fails.push(`${at}: scrollWidth ${r.sw} > innerWidth ${r.iw}`);
        if (r.len < MIN_LEN) fails.push(`${at}: nicht gerendert (${r.len} Zeichen)`);
        if (r.bad) fails.push(`${at}: Fehlertext im sichtbaren Inhalt`);
        // Semantik nur einmal je Seite pruefen, nicht bei jeder Breite
        if (w === WIDTHS[0] && MIN_LEN >= 1500) {
          if (r.h1 !== 1) fails.push(`${at}: ${r.h1} h1-Elemente statt genau einem`);
          if (!r.skip) fails.push(`${at}: kein Sprunglink zum Inhalt`);
          else if (!r.skipTargetOk) fails.push(`${at}: Sprunglink zeigt ins Leere`);
          if (!r.langLabelled) fails.push(`${at}: Sprachbutton ohne aria-label/aria-pressed`);
        }
      }
    }
    await ctx.close();
  }
  await browser.close();

  fails.forEach((f) => console.log('[FAIL]', f));
  console.log(`\n${checked - fails.length} von ${checked} Kombinationen bestanden`);
  process.exit(fails.length ? 1 : 0);
})();
