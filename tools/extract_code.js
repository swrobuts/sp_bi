// Liest die Codebloecke aus den Lab-Seiten aus.
//
// Warum Node und nicht ein Regex in Python: die Bloecke stehen als JS-String-
// Literale in der Seite (einfache Quotes, doppelte Quotes, Template-Literale,
// \u-Escapes). Node kennt diese Regeln bereits; ein handgeschriebener Parser
// waere die naechste Fehlerquelle.
//
// Aufruf:  node tools/extract_code.js <lab.html>
// Ausgabe: JSON-Liste [{ name, kind, code }]

const fs = require('fs');
const vm = require('vm');

const file = process.argv[2];
const src = fs.readFileSync(file, 'utf8');

// 1. Welche Bezeichner werden mit welchem kind gerendert?
const kinds = new Map();
for (const m of src.matchAll(/<CodeBlock\s+code=\{([^}]+)\}[^>]*?kind="([a-z]+)"/g)) {
  kinds.set(m[1].trim(), m[2]);
}

const out = [];

// 2a. const NAME = "..." | '...' | `...`
for (const m of src.matchAll(/const\s+([A-Za-z_$][\w$]*)\s*=\s*(`(?:\\.|[^`\\])*`|"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')\s*;/g)) {
  const kind = kinds.get(m[1]);
  if (!kind) continue;
  out.push({ name: m[1], kind, code: vm.runInNewContext(m[2]) });
}

// 2b. const NAME = { de: "...", en: "..." };  -> zwei Eintraege NAME[de] / NAME[en]
const OBJ = /const\s+([A-Za-z_$][\w$]*)\s*=\s*\{\s*\n\s*de:\s*((?:`(?:\\.|[^`\\])*`|"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')),\s*\n\s*en:\s*((?:`(?:\\.|[^`\\])*`|"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')),\s*\n\s*\};/g;
for (const m of src.matchAll(OBJ)) {
  const kind = kinds.get(m[1] + '[lang]');
  if (!kind) continue;
  out.push({ name: `${m[1]}[de]`, kind, code: vm.runInNewContext(m[2]) });
  out.push({ name: `${m[1]}[en]`, kind, code: vm.runInNewContext(m[3]) });
}

// 3. tx.KEY / c.KEY -> Schluessel im translations-Objekt (je Sprache einmal)
for (const [ref, kind] of kinds) {
  const dot = ref.match(/^(?:tx|c)\.([\w$]+)$/);
  if (!dot) continue;
  const key = dot[1];
  const re = new RegExp(`^\\s*${key}:\\s*(\`(?:\\\\.|[^\`\\\\])*\`|"(?:\\\\.|[^"\\\\])*"|'(?:\\\\.|[^'\\\\])*')\\s*,`, 'gm');
  let i = 0;
  for (const m of src.matchAll(re)) {
    out.push({ name: `${key}[${i === 0 ? 'de' : 'en'}]`, kind, code: vm.runInNewContext(m[1]) });
    i++;
  }
}

process.stdout.write(JSON.stringify(out, null, 1));
