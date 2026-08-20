# Starterpakete

Fertige Dateien zu den Labs 04, 05 und 06 – damit langer Code nicht aus der
Seite kopiert werden muss. Die Python- und SQL-Dateien werden aus den
Lab-Seiten erzeugt (`tools/build_starters.py`) und bleiben dadurch
automatisch synchron mit dem, was im Lab steht.

| Ordner | Inhalt | Lab |
|---|---|---|
| `lab-04-dash/` | `charts.py`, `app.py`, `requirements.txt`, `Dockerfile` | Lab 04 |
| `lab-05-fallstudie/` | `explore.py`, `app.py`, `measures.dax`, `requirements.txt` | Lab 05 |
| `lab-06-stack/` | `docker-compose.yml`, `init/`, `verify.sql`, `.env.example` | Lab 06 |

Der Datensatz `train.csv` liegt bewusst nicht in den Paketen, sondern einmal
unter `data/`. Jede README sagt, wohin er kopiert werden muss.

Zuletzt vollständig durchgespielt am 20.08.2026: alle Python-Dateien laufen
in einer frischen Umgebung durch, der Lab-06-Stack startet, importiert 9.800
Zeilen und liefert in `verify.sql` dieselben Zahlen wie pandas.
