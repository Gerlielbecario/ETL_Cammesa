import requests
import json
from datetime import datetime

#---EXTRACCION----
def get_dem_hoy(path_id_regiones:str,path_out:str) -> dict:

    '''
    Realiza la extraccion de demanda y temperatura de una region de Argentina.
    Las regiones son identificadas por un ID 
    '''

    #Ruta de nuestro archivo de salida
    json_path = (
        f"{path_out}/tablasinprocesar/data.json"
    )

    #Lectura de .json con los id de regiones de interes
    with open(path_id_regiones, 'r') as file:
        id_regiones = json.load(file)
        id_regiones = id_regiones['id_regiones']
    

    #La URL para realizar la consulta a la API
    url = 'https://api.cammesa.com/demanda-svc/demanda/ObtieneDemandaYTemperaturaRegion'
    
    dem_sitios = dict()

    for id in id_regiones:

        print(id)
        
        param = {'id_region':id}

        r = requests.get(url,params=param)
  
        r.raise_for_status()

        dem_sitios[id] = r.json()


    # Guardar el resultado en un archivo JSON
    with open(json_path, 'w') as json_file:
        json.dump(dem_sitios, json_file)



    
    print('Extraccion finalizada con exito')
