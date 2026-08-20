#!/usr/bin/env python3
"""Erzeugt die Starterdateien aus den Lab-Seiten und packt sie als ZIP.

Der Sinn: der Code steht genau einmal - in der Lab-Seite. Wer dort etwas
aendert und dieses Skript laufen laesst, hat automatisch dieselbe Fassung im
Starterpaket. Handgepflegte Kopien waeren nach dem zweiten Semester
auseinandergelaufen.

Handgeschrieben und damit NICHT ueberschrieben werden: die READMEs, die
docker-compose.yml, init/*.sql, verify.sql und .env.example.

Aufruf:  python3 tools/build_starters.py
"""

import json
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STARTER = ROOT / "starter"

# Ziel -> (Lab-Datei, Blockname, optionaler Zeilen-Offset)
# Der Offset schneidet bei den Plotly-Folgebloecken die wiederholte Praeambel
# weg, damit charts.py nicht dreimal dasselbe importiert.
GENERATED = {
    "lab-04-dash/app.py":            ("lab-04-dashboards.html", "CODE_DASH_APP[de]", 0),
    "lab-04-dash/requirements.txt":  ("lab-04-dashboards.html", "CODE_REQUIREMENTS", 0),
    "lab-04-dash/Dockerfile":        ("lab-04-dashboards.html", "CODE_DOCKERFILE", 0),
    "lab-05-fallstudie/explore.py":  ("lab-05-fallstudie.html", "CODE_EXPLORE[de]", 0),
    "lab-05-fallstudie/app.py":      ("lab-05-fallstudie.html", "CODE_DASH[de]", 0),
    "lab-05-fallstudie/measures.dax": ("lab-05-fallstudie.html", "CODE_MEASURES[de]", 0),
    "lab-06-stack/docker-compose.yml": ("lab-06-souveraenitaet.html", "codeDockerCompose[de]", 0),
    "lab-06-stack/init/01_schema.sql": ("lab-06-souveraenitaet.html", "codeSchemaSql[de]", 0),
    "lab-06-stack/init/02_import.sql": ("lab-06-souveraenitaet.html", "codeImportSql[de]", 0),
}

CHARTS = ("lab-04-dashboards.html",
          ["CODE_PX_BAR[de]", "CODE_PX_LINE[de]", "CODE_PX_SCATTER[de]"])

PACKAGES = ["lab-04-dash", "lab-05-fallstudie", "lab-06-stack"]


def blocks(lab):
    out = subprocess.run(["node", str(ROOT / "tools" / "extract_code.js"), str(ROOT / lab)],
                         capture_output=True, text=True, check=True)
    return {b["name"]: b["code"] for b in json.loads(out.stdout)}


def main():
    cache = {}
    for target, (lab, name, skip) in GENERATED.items():
        cache.setdefault(lab, blocks(lab))
        code = cache[lab][name]
        if skip:
            code = "\n".join(code.split("\n")[skip:])
        path = STARTER / target
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(code.rstrip("\n") + "\n", encoding="utf-8")
        print("erzeugt:", target)

    # charts.py: die drei Plotly-Bloecke hintereinander, Praeambel nur einmal
    lab, names = CHARTS
    cache.setdefault(lab, blocks(lab))
    parts = [cache[lab][names[0]]]
    for n in names[1:]:
        parts.append("\n".join(cache[lab][n].split("\n")[5:]))
    (STARTER / "lab-04-dash/charts.py").write_text("\n\n".join(parts).rstrip("\n") + "\n",
                                                   encoding="utf-8")
    print("erzeugt: lab-04-dash/charts.py")

    for pkg in PACKAGES:
        src = STARTER / pkg
        zip_path = STARTER / f"{pkg}.zip"
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
            for f in sorted(src.rglob("*")):
                if f.is_file():
                    z.write(f, f"{pkg}/{f.relative_to(src)}")
        print("gepackt: ", zip_path.relative_to(ROOT))


if __name__ == "__main__":
    main()
