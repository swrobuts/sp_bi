#!/usr/bin/env python3
"""Abnahmekriterien fuer das BI-Lab.

Prueft, was beim Selbststudium tatsaechlich weh tut, wenn es kaputt ist:

  1. Schema     - jede Spalte, die eine Aufgabe verwendet, existiert in train.csv
  2. Python     - jeder als "run" gekennzeichnete Python-Block laeuft in einer
                  frischen Umgebung ohne manuelle Aenderung durch
  3. Compose    - docker compose config besteht; das Image-Tag ist gepinnt
  4. Sprache    - die englische Fassung enthaelt keine deutschen UI-Texte
  5. Kennzeichen- jeder kopierbare Block ist als run / concept / diagram markiert
  6. Daten     - jede Datei, die ein lauffaehiger Block oeffnet, liegt im Repo
                 und wird auf derselben Seite zum Download angeboten

Aufruf:
    python3 tools/check_labs.py            # alles
    python3 tools/check_labs.py --quick    # ohne Python-Ausfuehrung

Voraussetzung fuer Schritt 2: pandas, numpy, plotly, dash im aktiven Interpreter.
Fehlt eine Bibliothek, wird der Block uebersprungen und als SKIP gemeldet -
nicht als Fehler, damit der Lauf auch ohne volle Umgebung nutzbar bleibt.
"""

import argparse
import csv
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "data" / "train.csv"
LABS = sorted(ROOT.glob("lab-0*.html"))

# Die Spalten, auf die sich Aufgabentexte und lauffaehige Bloecke beziehen.
# Konzeptsnippets nutzen bewusst Platzhalternamen und stehen nicht in dieser Liste.
REQUIRED_COLUMNS = [
    "Order ID", "Order Date", "Ship Date", "Ship Mode", "Customer ID",
    "Segment", "Country", "City", "State", "Postal Code", "Region",
    "Category", "Sub-Category", "Product Name", "Sales",
]

# Spalten, die es in der Forecasting-Variante NICHT gibt. Taucht eine davon
# in einer Aufgabe auf, ist die Aufgabe nicht loesbar - genau der Blocker,
# den der Usability-Test gefunden hat.
FORBIDDEN_COLUMNS = ["Profit", "Quantity", "Discount"]

results = []


def record(ok, area, msg):
    results.append((ok, area, msg))
    mark = "OK  " if ok is True else ("SKIP" if ok is None else "FAIL")
    print(f"[{mark}] {area}: {msg}")


def extract(lab: Path):
    out = subprocess.run(
        ["node", str(ROOT / "tools" / "extract_code.js"), str(lab)],
        capture_output=True, text=True, check=True,
    )
    return json.loads(out.stdout)


# ── 1. Schema ────────────────────────────────────────────────────────────────
def check_schema():
    with CSV_PATH.open(newline="", encoding="latin-1") as fh:
        header = next(csv.reader(fh))
    missing = [c for c in REQUIRED_COLUMNS if c not in header]
    record(not missing, "Schema",
           "alle benoetigten Spalten vorhanden" if not missing else f"fehlend: {missing}")

    # Verlangt eine Aufgabe eine Spalte, die es nicht gibt?
    for lab in LABS:
        text = lab.read_text(encoding="utf-8")
        for block in extract(lab):
            if block["kind"] != "run":
                continue
            hits = [c for c in FORBIDDEN_COLUMNS
                    if re.search(rf"\[['\"]?{c}['\"]?\]", block["code"])]
            if hits:
                record(False, "Schema",
                       f"{lab.name}/{block['name']} nutzt nicht vorhandene Spalte(n) {hits}")
    record(True, "Schema", "kein lauffaehiger Block greift auf Profit/Quantity/Discount zu")


# ── 2. Python-Bloecke ────────────────────────────────────────────────────────
def looks_like_python(code):
    """Erkennt Python auch ohne import-Zeile.

    Wichtig, weil ein Block ohne eigene Importe genau der Fall ist, der beim
    Kopieren scheitert: er setzt stillschweigend einen vorherigen Block voraus.
    Solche Bloecke sollen auffallen, nicht uebersprungen werden.
    """
    return bool(re.search(r"^\s*(import|from)\s+\w", code, re.M)
                or re.search(r"\b(df\[|px\.|pd\.|print\()", code))


def check_python(quick=False):
    if quick:
        record(None, "Python", "uebersprungen (--quick)")
        return
    for lab in LABS:
        for block in extract(lab):
            if block["kind"] != "run" or not looks_like_python(block["code"]):
                continue
            code = block["code"]
            # Dash-Apps starten einen Server - wir pruefen sie ohne app.run().
            headless = re.sub(r"^\s*app\.run\(.*$", "    pass", code, flags=re.M)
            with tempfile.TemporaryDirectory() as td:
                # Genau die Dateien bereitstellen, die der Lernende ueber die
                # Seite herunterladen kann - nicht mehr und nicht weniger.
                for fname, repo_path in DATA_FILES.items():
                    src = ROOT / repo_path
                    if src.exists():
                        shutil.copy(src, Path(td) / fname)
                script = Path(td) / "block.py"
                script.write_text(headless, encoding="utf-8")
                proc = subprocess.run([sys.executable, "block.py"], cwd=td,
                                      capture_output=True, text=True, timeout=180)
            name = f"{lab.name}/{block['name']}"
            if proc.returncode == 0:
                record(True, "Python", f"{name} laeuft durch")
            elif "ModuleNotFoundError" in proc.stderr:
                mod = re.search(r"No module named '([^']+)'", proc.stderr)
                record(None, "Python", f"{name} uebersprungen ({mod.group(1) if mod else '?'} fehlt)")
            else:
                record(False, "Python", f"{name} bricht ab: {proc.stderr.strip().splitlines()[-1][:160]}")


# ── 3. Docker Compose ────────────────────────────────────────────────────────
def check_compose():
    if not shutil.which("docker"):
        record(None, "Compose", "docker nicht installiert")
        return
    for lab in LABS:
        for block in extract(lab):
            if "services:" not in block["code"]:
                continue
            with tempfile.TemporaryDirectory() as td:
                (Path(td) / "compose.yaml").write_text(block["code"], encoding="utf-8")
                (Path(td) / ".env").write_text("POSTGRES_PASSWORD=pruefwert\n", encoding="utf-8")
                proc = subprocess.run(["docker", "compose", "config"], cwd=td,
                                      capture_output=True, text=True)
            name = f"{lab.name}/{block['name']}"
            record(proc.returncode == 0, "Compose",
                   f"{name} ist gueltig" if proc.returncode == 0
                   else f"{name}: {proc.stderr.strip()[:200]}")
            pinned = re.findall(r"image:\s*(\S+)", block["code"])
            unpinned = [i for i in pinned if ":" not in i or i.endswith(":latest")]
            record(not unpinned, "Compose",
                   "alle Images gepinnt" if not unpinned else f"ungepinnt: {unpinned}")


# ── 4. Sprachtrennung ────────────────────────────────────────────────────────
GERMAN_MARKERS = re.compile(
    r"\b(werden|wird|muessen|müssen|können|nicht|oder|für|"
    r"eine|einen|einer|dieser|diese|Datei|Spalte|Zeile|Verzeichnis|Passwort|"
    r"anlegen|erstellen|pruefen|prüfen|starten|anzeigen|Lösung|Versuche)\b")


def check_language():
    for lab in LABS:
        for block in extract(lab):
            if not block["name"].endswith("[en]"):
                continue
            hits = set(GERMAN_MARKERS.findall(block["code"]))
            record(not hits, "Sprache",
                   f"{lab.name}/{block['name']} ohne deutsche Reste" if not hits
                   else f"{lab.name}/{block['name']} enthaelt {sorted(hits)}")
        # Bloecke ohne Sprachvariante (gemeinsame Konstanten) separat pruefen
        for block in extract(lab):
            if "[" in block["name"]:
                continue
            hits = set(GERMAN_MARKERS.findall(block["code"]))
            if hits:
                record(False, "Sprache",
                       f"{lab.name}/{block['name']} ist sprachneutral eingebunden, "
                       f"enthaelt aber deutsche Woerter {sorted(hits)}")


# ── 5. Kennzeichnung ─────────────────────────────────────────────────────────
def check_tagging():
    for lab in LABS:
        text = lab.read_text(encoding="utf-8")
        total = len(re.findall(r"<CodeBlock\s", text))
        tagged = len(re.findall(r'<CodeBlock\s[^>]*kind="(?:run|concept|diagram)"', text))
        record(total == tagged, "Kennzeichnung",
               f"{lab.name}: {tagged}/{total} Bloecke gekennzeichnet")


# ── 6. Datenverfuegbarkeit ───────────────────────────────────────────────────
# Jede Datei, die ein lauffaehiger Block oeffnet, muss im Repo liegen und ueber
# die Seite herunterladbar sein. Sonst steht der Lernende vor einem Block, der
# "Laeuft unveraendert" verspricht und an einem FileNotFoundError scheitert -
# genau die Frustration, die diese Pruefung verhindern soll.

# Dateiname im Code -> Pfad im Repo
DATA_FILES = {
    "train.csv": "data/train.csv",
    "umsatz.csv": "data/beispiel/umsatz.csv",
    "bericht.xlsx": "data/beispiel/bericht.xlsx",
    "sales_api.json": "data/beispiel/sales_api.json",
}

# Diese Namen tauchen in Beispielen auf, sind aber Ausgabe- oder Projektdateien,
# die der Lernende selbst anlegt - keine Eingabedaten.
DATA_IGNORE = {"requirements.txt", "app.py", "charts.py", "explore.py",
               "docker-compose.yml", "compose.yaml", ".env"}

READ_CALL = re.compile(r"""(?:read_csv|read_excel|read_json|open)\(\s*['"]([^'"]+)['"]""")
# SQL: COPY ... FROM '/data/train.csv'
SQL_COPY = re.compile(r"""FROM\s+'([^']+\.[a-z]+)'""", re.I)
# Compose: - ./train.csv:/data/train.csv:ro
MOUNT = re.compile(r"""^\s*-\s+\./([\w./-]+\.[a-z]+):""", re.M)
# Eigene Pages-URL in lauffaehigem Code
OWN_URL = re.compile(r"""https://swrobuts\.github\.io/sp_bi/([\w./-]+)""")


def check_data_availability():
    referenced = set()
    for lab in LABS:
        for block in extract(lab):
            if block["kind"] != "run":
                continue
            code = block["code"]
            for hit in (READ_CALL.findall(code) + SQL_COPY.findall(code)
                        + MOUNT.findall(code)):
                name = hit.split("/")[-1]
                if name in DATA_IGNORE:
                    continue
                referenced.add((lab.name, block["name"], name))

    for lab_name, block_name, fname in sorted(referenced):
        where = f"{lab_name}/{block_name} -> {fname}"
        repo_path = DATA_FILES.get(fname)
        if repo_path is None:
            record(False, "Daten", f"{where}: unbekannte Datei, nicht im Repo hinterlegt")
        elif not (ROOT / repo_path).exists():
            record(False, "Daten", f"{where}: {repo_path} fehlt im Repo")
        else:
            record(True, "Daten", f"{where} liegt als {repo_path} bei")

    # Wird jede bereitgestellte Datei auch zum Download angeboten?
    for fname, repo_path in sorted(DATA_FILES.items()):
        used_in = {l for l, _, n in referenced if n == fname}
        for lab_name in sorted(used_in):
            html = (ROOT / lab_name).read_text(encoding="utf-8")
            if f'href="{repo_path}"' in html:
                record(True, "Daten", f"{lab_name} bietet {repo_path} zum Download an")
            else:
                record(False, "Daten", f"{lab_name} nutzt {fname}, verlinkt aber {repo_path} nicht")

    # Ueber HTTP geladene Daten muessen aus dem eigenen Repo kommen und dort liegen
    for lab in LABS:
        for block in extract(lab):
            if block["kind"] != "run":
                continue
            if "example.com" in block["code"]:
                record(False, "Daten",
                       f"{lab.name}/{block['name']} nutzt den fiktiven Host example.com")
            for path in OWN_URL.findall(block["code"]):
                target = ROOT / path
                record(target.exists(), "Daten",
                       f"{lab.name}/{block['name']} laedt {path} per HTTP \u2013 Datei liegt im Repo"
                       if target.exists() else
                       f"{lab.name}/{block['name']} laedt {path} per HTTP, aber die Datei fehlt im Repo")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true", help="Python-Bloecke nicht ausfuehren")
    args = ap.parse_args()

    check_schema()
    check_tagging()
    check_language()
    check_compose()
    check_data_availability()
    check_python(args.quick)

    failed = [r for r in results if r[0] is False]
    skipped = [r for r in results if r[0] is None]
    print(f"\n{len(results) - len(failed) - len(skipped)} bestanden, "
          f"{len(failed)} fehlgeschlagen, {len(skipped)} uebersprungen")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
