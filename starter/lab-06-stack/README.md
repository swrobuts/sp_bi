# Lab 06 – Self-Hosted BI-Stack

Metabase, seine Metadatenbank und eine getrennte Analysedatenbank mit den
Superstore-Daten. Der Import läuft beim ersten Start von selbst und prüft
sich selbst; du musst keine Tabelle von Hand anlegen.

**Zeitbedarf:** 10–20 Minuten bis der Stack steht (davon der größte Teil
Image-Download), danach 45–90 Minuten für Metabase-Onboarding und Dashboards.

**Voraussetzung:** Docker Desktop läuft. Prüfen mit `docker info`.

## 1. Vorbereiten

```bash
cp .env.example .env          # danach beide Passwörter ändern
cp ../../data/train.csv .     # der Datensatz muss neben der Compose-Datei liegen
```

`.env` gehört nicht ins Git-Repo. Ohne die Datei bricht `docker compose` mit
einer Warnung über leere Variablen ab.

## 2. Starten

```bash
docker compose up -d
docker compose ps
```

Der Dienst `warehouse` legt beim allerersten Start die Tabelle `orders` an
und importiert `train.csv`. Alles unter `init/` läuft genau einmal – nämlich
solange das Volume leer ist. Ein zweites `docker compose up` importiert also
nicht doppelt.

Ob es geklappt hat:

```bash
docker compose logs warehouse | grep "Import ok"
# -> NOTICE:  Import ok: 9800 Zeilen
```

## 3. Erfolgskontrolle

```bash
docker compose exec -T warehouse psql -U superstore -d superstore -f - < verify.sql
```

**Sollausgabe:** 9800 Zeilen · 4922 Bestellungen · Gesamtumsatz 2261536.78 ·
11 fehlende Postleitzahlen · Zeitraum 2015-01-03 bis 2018-12-30.

Dieselben Zahlen liefern der pandas-Block aus Lab 05 und die DAX-Measures in
Power BI. Weichen sie ab, liegt es fast immer am Datumsformat (TT/MM/JJJJ)
oder am Encoding (LATIN1).

## 4. Datenbank in Metabase eintragen

`http://localhost:3000` öffnen, Einrichtungsassistent durchlaufen, dann
Einstellungen → Datenbanken → Datenbank hinzufügen:

| Feld | Wert |
|---|---|
| Datenbanktyp | PostgreSQL |
| Host | `warehouse` |
| Port | `5432` |
| Datenbankname | `superstore` |
| Benutzer | `superstore` |
| Passwort | dein `WAREHOUSE_PASSWORD` aus `.env` |

**Host ist `warehouse`, nicht `localhost`.** Metabase läuft in einem eigenen
Container; `localhost` wäre dort Metabase selbst. Innerhalb des Compose-
Netzwerks erreichen sich die Dienste über ihren Dienstnamen, und dort gilt
der Container-Port 5432 – nicht der nach außen veröffentlichte 5433.

Von deinem Rechner aus (psql, DBeaver, pgAdmin) gilt dagegen
`localhost:5433`:

```bash
psql postgresql://superstore:DEIN_PASSWORT@localhost:5433/superstore
```

## 5. Aufräumen

```bash
docker compose down          # Container weg, Daten bleiben
docker compose down -v       # auch die Volumes - der Import läuft dann neu
```

## Wenn etwas klemmt

| Symptom | Ursache | Abhilfe |
|---|---|---|
| `Import fehlgeschlagen: 0 Zeilen statt 9800` | `train.csv` fehlt neben der Compose-Datei | Datei kopieren, `docker compose down -v`, neu starten |
| `date/time field value out of range` | `SET datestyle` wurde entfernt | `02_import.sql` unverändert lassen – die Datei ist TT/MM/JJJJ |
| Metabase findet die Datenbank nicht | Host steht auf `localhost` | Host auf `warehouse`, Port auf `5432` ändern |
| Port 5433 belegt | lokales Postgres läuft | in `docker-compose.yml` linke Portseite ändern, z. B. `5434:5432` |
| Änderung in `init/` wirkt nicht | Skripte laufen nur bei leerem Volume | `docker compose down -v`, dann neu starten |
