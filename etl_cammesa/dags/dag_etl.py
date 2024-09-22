import os
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

from modules import get_defaultairflow_args, get_dem_hoy, transformar_datos_dem, cargar_data, send_email

with DAG(
    dag_id="demanda_y_temperatura_etl",
    default_args=get_defaultairflow_args(),
    description="Extrae, transforma y sube datos de demanda y temperatura de regiones del SADI",
    schedule_interval="@daily",
    catchup=False,
) as dag:

    # Tasks
    # 1. Extraction
    task_extract = PythonOperator(
        task_id="extract_data",
        python_callable=get_dem_hoy,
        op_args=['/opt/airflow/id_regiones.json',os.getcwd()],
    )

    # 2. Transformation
    task_transform = PythonOperator(
        task_id="transform_data",
        python_callable=transformar_datos_dem,
        op_args=[os.getcwd()],
    )

    # 3. Loading
    task_load_data = PythonOperator(
        task_id="load_data",
        python_callable=cargar_data,
        op_args=[os.getcwd()],
    )
    # 4. Mailing
    send_email = PythonOperator(
        task_id="send_email",
        python_callable=send_email,
    )

    # Task dependencies
    task_extract >> task_transform >> task_load_data >> send_email
