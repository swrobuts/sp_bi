-- Erfolgskontrolle nach dem Import.
-- Die Sollwerte stehen als Kommentar dahinter; weicht eine Zahl ab, ist
-- fast immer das Datumsformat oder das Encoding schuld.

SELECT count(*)                        AS zeilen           FROM orders;  -- 9800
SELECT count(DISTINCT order_id)        AS bestellungen     FROM orders;  -- 4922
SELECT round(sum(sales), 2)            AS gesamtumsatz     FROM orders;  -- 2261536.78
SELECT count(*)                        AS fehlende_plz     FROM orders WHERE postal_code IS NULL;  -- 11
SELECT min(order_date), max(order_date)                    FROM orders;  -- 2015-01-03 | 2018-12-30

-- Umsatz je Jahr: 2015 479856.21 | 2016 459436.01 | 2017 600192.55 | 2018 722052.02
SELECT extract(year FROM order_date) AS jahr,
       round(sum(sales), 2)          AS umsatz
FROM orders
GROUP BY 1
ORDER BY 1;

-- Umsatz je Kategorie: Technology 827455.87 | Furniture 728658.58 | Office Supplies 705422.33
SELECT category, round(sum(sales), 2) AS umsatz
FROM orders
GROUP BY 1
ORDER BY 2 DESC;
