from datetime import datetime
import pandas as pd
import psycopg2
import os
from psycopg2.extras import execute_values
from .utils import get_credentials
from .utils import get_schema

def create_table_if_not_exists(conn):
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {get_schema()}.demanda_temperatura_cammesa (

        fecha TIMESTAMP,
        demanda_actual_MW NUMERIC,
        demanda_prevista_MW NUMERIC,
        temperatura_hoy_celcius NUMERIC,
        id_region_sadi VARCHAR(50),
        ingesta_de_datos_columna TIMESTAMP
    );
    """
    
    with conn.cursor() as cur:
        cur.execute(create_table_query)
        conn.commit()
    print(f"Table {get_schema()}.demanda_temperatura_cammesa is ready.")




def cargar_data(path):

    '''
    Es una funcion encargada de la carga y subida a redshift
    '''

    print(f"Cargando la data")
    csv_path = (
        f"{path}/tablaprocesada/data.csv"
    )

    df = pd.read_csv(csv_path)


    credentials = get_credentials()
   # print(credentials)
    conn = psycopg2.connect(**credentials)
    create_table_if_not_exists(conn)
    
    # Definir las columnas a insertar (deben coincidir con las columnas del CSV y la tabla SQL)
    columns = [
        "fecha",
        "demanda_actual_MW",
        "demanda_prevista_MW",
        "temperatura_hoy_celcius",
        "id_region_sadi",
        "ingesta_de_datos_columna"
    ]

    # Convertir el DataFrame en una lista de tuplas
    values = [tuple(x) for x in df.to_numpy()]

    # Preparar la consulta SQL
    table_name = "demanda_temperatura_cammesa"
    insert_sql = f"INSERT INTO {get_schema()}.{table_name} ({', '.join(columns)}) VALUES %s"

    # Ejecutar la inserción
    cur = conn.cursor()
    cur.execute("BEGIN")
    execute_values(cur, insert_sql, values)
    cur.execute("COMMIT")

    print("Datos cargados exitosamente.")