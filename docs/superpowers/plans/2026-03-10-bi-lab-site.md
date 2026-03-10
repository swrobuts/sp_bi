# BI Lab Site Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a complete 7-page static bilingual companion website for the THWS Business Intelligence module, using the INME Lab design system with Navy/Blue colors.

**Architecture:** 7 standalone HTML files, each with embedded React+Babel+Tailwind via CDN. The index.html serves as the hub with lab cards; each lab-*.html has a sidebar+content layout. All files are self-contained, no build step, GitHub Pages compatible.

**Tech Stack:** React 18 (CDN), Babel standalone, Tailwind CSS 2 (CDN), Space Grotesk + EB Garamond fonts, all via CDN.

---

## Chunk 1: index.html

### Task 1: Build index.html

**Files:**
- Create: `/tmp/sp_bi-lab/index.html`

- [ ] Write complete index.html with:
  - CSS variables: `--primary: #1E3A8A`, `--accent: #2563EB`
  - EN mode: teal `#0D9488` / `#14B8A6`
  - Sticky navbar (56px, white, border-bottom)
  - Hero with geometric background shapes (Navy DE, Teal EN)
  - Stats bar (6 LABS | 1 FALLSTUDIE | Power BI & Python | Open Source BI)
  - Quote strip (Deming quote, EB Garamond)
  - Labs grid (3 columns, 6 lab cards + bonus card)
  - Footer (black, two-column)
  - Full DE/EN bilingual translations object
  - localStorage key: `bi-lang`
  - ?lang=en passthrough on lab links
  - React 18 + Babel + Tailwind CDN

- [ ] Verify no TomSelect, no `overflow:hidden` on SVGs, JSX Unicode escaped

---

## Chunk 2: Lab Pages (lab-01 through lab-06)

### Task 2: lab-01-grundlagen.html

**Files:**
- Create: `/tmp/sp_bi-lab/lab-01-grundlagen.html`

- [ ] Write lab-01 with:
  - Fixed header (56px), sidebar (260px), main content area
  - DE/EN nav, back link to index.html
  - Sections: Was ist BI?, BI-Architektur, KPI-Konzepte, Tool-Überblick, YouTube-Ressourcen, Quiz
  - Tool comparison table (Power BI, Tableau, Plotly Dash, Superset, Metabase)
  - 3 quiz questions with multiple choice (React state)
  - CodeBlock component with copy button
  - Nav bottom: → lab-02

### Task 3: lab-02-daten.html

**Files:**
- Create: `/tmp/sp_bi-lab/lab-02-daten.html`

- [ ] Write lab-02 with:
  - Same header/sidebar/layout pattern
  - Sections: Datenquellen, Star/Snowflake Schema (ASCII diagram), Datenqualität
  - Pandas code examples with copy buttons
  - Table: structured vs semi-structured vs cloud sources
  - Nav bottom: ← lab-01, → lab-03

### Task 4: lab-03-kpis.html

**Files:**
- Create: `/tmp/sp_bi-lab/lab-03-kpis.html`

- [ ] Write lab-03 with:
  - Sections: DAX Grundlagen, Measures vs Calculated Columns
  - DAX code blocks (all 6 examples from brief)
  - Python/Pandas equivalents side-by-side
  - KPI table (Umsatz, Marge%, YoY, Conversion, LTV)
  - Filter Context explanation
  - Nav bottom: ← lab-02, → lab-04

### Task 5: lab-04-dashboards.html

**Files:**
- Create: `/tmp/sp_bi-lab/lab-04-dashboards.html`

- [ ] Write lab-04 with:
  - Sections: Dashboard-Design-Prinzipien, Chart-Auswahl, Plotly Express, Dash Architektur, Power BI vs Dash
  - Full Plotly Express code examples (bar, line, scatter)
  - Full Dash app.py code block
  - Comparison table: Power BI vs Plotly Dash (8 rows)
  - Nav bottom: ← lab-03, → lab-05

### Task 6: lab-05-fallstudie.html

**Files:**
- Create: `/tmp/sp_bi-lab/lab-05-fallstudie.html`

- [ ] Write lab-05 with:
  - Sections: Superstore Dataset intro, 5-step workflow
  - Step 1: Python data exploration code
  - Step 2: KPI hierarchy definition
  - Step 3: Power BI step-by-step (DAX measures)
  - Step 4: Full Plotly Dash app.py (~100 lines)
  - Step 5: Reflexionsfragen
  - Nav bottom: ← lab-04, → lab-06

### Task 7: lab-06-souveraenitaet.html

**Files:**
- Create: `/tmp/sp_bi-lab/lab-06-souveraenitaet.html`

- [ ] Write lab-06 with:
  - Sections: Digitale Souveränität, Cloud Lock-in, Open-Source Tools table
  - Docker Compose code (Metabase + PostgreSQL)
  - DSGVO Compliance Checklist
  - Entscheidungsmatrix table
  - Abschlussprojekt-Idee
  - Nav bottom: ← lab-05

---

## Shared Patterns (apply to ALL files)

### CSS Variables (index.html)
```css
:root { --primary: #1E3A8A; --accent: #2563EB; --dark: #1A1A1A; --light-bg: #FAFAFA; --primary-light: rgba(30,58,138,0.08); }
h2 { color: #1E3A8A; font-weight: 800; font-family: 'Space Grotesk', sans-serif; }
h3 { color: #1E3A8A; font-weight: 700; font-family: 'Space Grotesk', sans-serif; }
.bauhaus-accent-line { background: #2563EB; }
.bauhaus-badge { background: #2563EB; }
```

### EN Mode (Teal)
```css
[data-lang="en"] h2, [data-lang="en"] h3 { color: #0D9488; }
[data-lang="en"] .bauhaus-accent-line { background: #14B8A6; }
[data-lang="en"] .bauhaus-badge { background: #0D9488; }
[data-lang="en"] .lab-card { border-left-color: #14B8A6; }
```

### CodeBlock Component
```jsx
function CodeBlock({ code }) {
  const [copied, setCopied] = React.useState(false);
  const copy = () => {
    navigator.clipboard.writeText(code).then(() => {
      setCopied(true); setTimeout(() => setCopied(false), 1500);
    }).catch(() => {
      const el = document.createElement('textarea'); el.value = code;
      document.body.appendChild(el); el.select(); document.execCommand('copy');
      document.body.removeChild(el); setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    });
  };
  return (
    <div style={{ position: 'relative', marginBottom: '1rem' }}>
      <pre className="code-block">{code}</pre>
      <button onClick={copy} style={{
        position: 'absolute', top: '0.5rem', right: '0.5rem',
        background: copied ? '#059669' : '#E5E7EB',
        color: copied ? 'white' : '#374151',
        border: 'none', borderRadius: '4px',
        padding: '0.2rem 0.5rem', fontSize: '0.75rem', cursor: 'pointer'
      }}>{copied ? '✓ Kopiert' : 'Kopieren'}</button>
    </div>
  );
}
```

### Lang Persistence (lab pages)
```js
const urlLang = new URLSearchParams(window.location.search).get('lang');
const [lang, setLang] = React.useState(() => localStorage.getItem('bi-lang') || urlLang || 'de');
const toggleLang = () => {
  const newLang = lang === 'de' ? 'en' : 'de';
  setLang(newLang); localStorage.setItem('bi-lang', newLang);
};
```
