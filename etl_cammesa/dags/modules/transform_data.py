#-----Funciones para la extraccion, transformacion y carga de datos de CAMMESA---
import requests
import json
import pandas as pd
from datetime import datetime


#---TRANSFORMACION

def transformar_datos_dem(path):

    '''
    Es una funcion que recibe la ubicacion de un diccionario y lo transforma.
    Se encarga de transformar los datos recibidos, asignarle unidades, corregir formato de fecha.
    '''

    json_path = (
        f"{path}/tablasinprocesar/data.json"
    )
    csv_path = (
        f"{path}/tablaprocesada/data.csv"
    )

    #Cargamos nuestro diccionario
    with open(json_path, "r") as json_file:
        dem_sitios = json.load(json_file)

    #Lista donde almacenaremos dataframes
    lista_dataframes = []

    print('Iniciando transformacion...')

    for id,data in dem_sitios.items():

        #Transformamos el json a dataframe    
        df = pd.DataFrame(data)

        #Seleccionamos algunas columnas de interes de todas las que devuelve
        columnas_interes = ['fecha','demHoy','demPrevista','tempHoy']

        df = df[columnas_interes] 

        #Agrego unidades al dataframe
        df.columns = ['Fecha','Demanda_Actual (MW)','Demanda_Prevista (MW)','Temperatura_Hoy (Celcius)']
       
        #Eliminamos si existen duplicados
        df.drop_duplicates(inplace=True)

        #Eliminamos filas con datos faltantes de demanda 
        df.dropna(subset=['Demanda_Actual (MW)','Demanda_Prevista (MW)'],inplace=True)

        #Transformar el formato de hora a Argentina Buenos Aires
        df['Fecha'] = pd.to_datetime(df['Fecha'], format='%Y-%m-%dT%H:%M:%S.%f%z').dt.tz_convert('America/Argentina/Buenos_Aires').dt.strftime('%Y-%m-%d %H:%M:%S')   

        df['Id_Region_SADI'] = id

        # Agregar columna de control de ingesta de datos
        df['Ingesta_de_datos_(Col_emporal)'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')     

        #Lo agregamos a la lista vacia
        lista_dataframes.append(df)

    #Concatenemos todos los dataframes uno debajo del otro
    df_completo = pd.concat(lista_dataframes,ignore_index=True)

    print('Transformacion Finalizada con exito!')

    df_completo.to_csv(csv_path,index=False)