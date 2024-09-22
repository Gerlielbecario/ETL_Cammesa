-- DROP DATABASE IF EXISTS etl_bitcoins;

-- CREATE DATABASE etl_bitcoins;

-- -- Connect to the database manually if needed in a script that is not run at init
-- --\c etl_bitcoins;

CREATE SCHEMA fernando_huaranca99_coderhouse;

CREATE TABLE fernando_huaranca99_coderhouse.mining_data (
    fecha TIMESTAMP,
    demanda_actual_MW NUMERIC,
    demanda_prevista_MW NUMERIC,
    temperatura_hoy_celcius NUMERIC,
    id_region_sadi VARCHAR(50),
    ingesta_de_datos_columna TIMESTAMP
);
