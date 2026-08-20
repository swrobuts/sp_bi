-- init/02_import.sql - laeuft direkt nach dem Schema
--
-- COPY liest serverseitig, die Datei muss also IM Container liegen. Dafuer
-- ist der Mount ./train.csv -> /data/train.csv in der Compose-Datei da.
-- Wer keine Datei in den Container legen kann, nimmt \copy in psql; dann
-- liest der Client.
--
-- Das Datumsformat ist TT/MM/JJJJ. Ohne DateStyle bricht Postgres bei jedem
-- Tag > 12 ab - dieselbe Falle wie dayfirst=True in pandas.
SET datestyle = 'ISO, DMY';

COPY orders (
    row_id, order_id, order_date, ship_date, ship_mode,
    customer_id, customer_name, segment, country, city, state,
    postal_code, region, product_id, category, sub_category,
    product_name, sales
)
FROM '/data/train.csv'
WITH (FORMAT csv, HEADER true, ENCODING 'LATIN1');

-- Erfolgskontrolle: bricht ab, wenn die Zeilenzahl nicht stimmt.
DO $$
DECLARE n bigint;
BEGIN
    SELECT count(*) INTO n FROM orders;
    IF n <> 9800 THEN
        RAISE EXCEPTION 'Import fehlgeschlagen: % Zeilen statt 9800', n;
    END IF;
    RAISE NOTICE 'Import ok: % Zeilen', n;
END $$;
