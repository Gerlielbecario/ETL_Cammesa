DROP TABLE IF EXISTS fernando_huaranca99_coderhouse.mining_data ;

CREATE TABLE fernando_huaranca99_coderhouse.mining_data (
    fecha TIMESTAMP,
    demanda_actual_MW NUMERIC,
    demanda_prevista_MW NUMERIC,
    temperatura_hoy_celcius NUMERIC,
    id_region_sadi VARCHAR(50),
    ingesta_de_datos_columna TIMESTAMP
);
