#!/usr/bin/env python3
"""Smoke- und Responsive-Test der Starter-Dash-Apps.

Der Re-Audit fand, dass die Lab-Seiten mobil sauber sind, das von den
Studierenden erzeugte Dashboard aber nicht: 673 px Dokumentbreite bei
390 px Viewport. Ein Ergebnis, das auf dem Handy kaputt aussieht,
entwertet die Uebung - deshalb wird es jetzt genauso geprueft wie die
Lernseiten selbst.

Was passiert:
  1. app.py und train.csv in ein leeres Verzeichnis kopieren
  2. App auf einem freien Port starten und auf HTTP 200 warten
  3. tools/check_responsive.js dagegen laufen lassen (320-1440 px)
  4. App beenden, Verzeichnis wegraeumen

Aufruf:  python3 tools/check_starter_apps.py
"""

import argparse
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV = ROOT / "data" / "train.csv"
APPS = ["lab-04-dash", "lab-05-fallstudie"]


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def wait_for(url, proc, timeout=90):
    deadline = time.time() + timeout
    while time.time() < deadline:
        if proc.poll() is not None:
            return False
        try:
            with urllib.request.urlopen(url, timeout=3) as r:
                if r.status == 200:
                    return True
        except (urllib.error.URLError, OSError):
            time.sleep(1)
    return False


def check(app_name):
    src = ROOT / "starter" / app_name / "app.py"
    if not src.exists():
        print(f"[FAIL] {app_name}: app.py fehlt")
        return False

    port = free_port()
    code = src.read_text(encoding="utf-8")
    # Port festlegen und den Debug-Reloader abschalten - er startet einen
    # zweiten Prozess, der sich nicht sauber beenden laesst.
    code = code.replace("app.run(debug=True)",
                        f"app.run(debug=False, port={port})")

    with tempfile.TemporaryDirectory() as td:
        work = Path(td)
        (work / "app.py").write_text(code, encoding="utf-8")
        shutil.copy(CSV, work / "train.csv")

        proc = subprocess.Popen([sys.executable, "app.py"], cwd=work,
                                stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        base = f"http://127.0.0.1:{port}"
        try:
            if not wait_for(base + "/", proc):
                err = (proc.stderr.read().decode(errors="replace")[-400:]
                       if proc.stderr else "")
                print(f"[FAIL] {app_name}: App startet nicht. {err.strip()}")
                return False
            print(f"[OK  ] {app_name}: startet und antwortet auf {base}")

            res = subprocess.run(
                ["node", str(ROOT / "tools" / "check_responsive.js"), base, "/", "--no-lang"],
                capture_output=True, text=True)
            print(res.stdout.strip())
            if res.returncode != 0:
                print(f"[FAIL] {app_name}: Responsive-Test fehlgeschlagen")
                return False
            print(f"[OK  ] {app_name}: keine Ueberbreite bei 320-1440 px")
            return True
        finally:
            proc.terminate()
            try:
                proc.wait(timeout=15)
            except subprocess.TimeoutExpired:
                proc.kill()


def main():
    argparse.ArgumentParser(description=__doc__).parse_args()
    ok = all([check(a) for a in APPS])
    print("\nAlle Starter-Apps bestanden" if ok else "\nMindestens eine Starter-App ist fehlerhaft")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
