-- init/01_schema.sql - laeuft beim ersten Start automatisch
CREATE TABLE IF NOT EXISTS orders (
    row_id        integer PRIMARY KEY,
    order_id      text NOT NULL,
    order_date    date NOT NULL,
    ship_date     date NOT NULL,
    ship_mode     text NOT NULL,
    customer_id   text NOT NULL,
    customer_name text NOT NULL,
    segment       text NOT NULL,
    country       text NOT NULL,
    city          text NOT NULL,
    state         text NOT NULL,
    postal_code   text,            -- NULL-faehig: elf Werte fehlen
    region        text NOT NULL,
    product_id    text NOT NULL,
    category      text NOT NULL,
    sub_category  text NOT NULL,
    product_name  text NOT NULL,
    sales         numeric(12,4) NOT NULL
);

-- Zwei Entscheidungen, die man begruenden koennen sollte:
--   postal_code ist text, nicht integer. US-PLZ haben fuehrende Nullen
--   ("01013"); als Zahl gespeichert gingen sie verloren.
--   sales ist numeric(12,4), nicht float und nicht numeric(12,2). Die CSV
--   enthaelt Werte wie 957,5775. Mit zwei Nachkommastellen rundet Postgres
--   schon beim Import, und die Gesamtsumme weicht um rund 20 Cent von der
--   pandas- und der Power-BI-Zahl ab.

CREATE INDEX IF NOT EXISTS orders_order_date_idx   ON orders (order_date);
CREATE INDEX IF NOT EXISTS orders_category_idx     ON orders (category, sub_category);
CREATE INDEX IF NOT EXISTS orders_region_state_idx ON orders (region, state);
