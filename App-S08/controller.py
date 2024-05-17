"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import model
import time
import csv
import tracemalloc

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller():
    """
    Crea una instancia del modelo
    """
    control={
        "model":None
    }
    #Se llama la función model.new_data_structs (Para crear las estructuras de datos vacias) y se guarda en la llave "model" para reemplazar el None.
    control["model"]=model.new_data_structs()
    #Se devuelve el dict completo con las estructuras
    return control

def conversor_divisas(usd_usd,eur_usd,gbp_usd,pln_usd,chf_usd):
    model.usd_usd=usd_usd
    model.eur_usd=eur_usd
    model.gbp_usd=gbp_usd
    model.pln_usd=pln_usd
    model.chf_usd=chf_usd

# Funciones para la carga de datos

def load_data(control, tamanio, memoria):
    """
    Carga los datos del reto
    """
    if memoria==True:
        tracemalloc.start()
        start_memory=get_memory()
    start_time=get_time()
    
    datos=control["model"]
    #Se asignan variables que corresponden a cada tipo de dato que se va a cargar
    
    #Se llama la función load_jobs que carga los datos del reto
    #Jobs es el diccionario que se va a llenar con los datos
    load_jobs(datos, tamanio)
    load_multilocation(datos, tamanio)
    load_skills(datos, tamanio)
    load_employment_types(datos, tamanio)
    load_employment_types2(datos)
    print("Employments cargados en el modelo")

    model.sort_jobs(model.obtener_datos(datos,"jobs-lista"))
    end_time=get_time()
    if memoria==True:
        end_memory=get_memory()
        tracemalloc.stop()
        delta_mem=delta_memory(end_memory, start_memory)
    delta=delta_time(start_time, end_time)
    if memoria==True:
        return datos, delta, delta_mem
    else:
        return datos, delta

def load_jobs(datos, tamanio):
    """
    Carga los datos de los trabajos en el modelo    de un archivo csv
    Args:
    full_jobs: diccionario con las llaves del archivo Jobs vacias
    tamanio: tamaño del archivo que se va a cargar (10,20,30,40,50,60,70,80,90,small,medium,large)
    Returns:
    full_jobs: diccionario con las llaves del archivo Jobs llenas con los datos del archivo csv
    """
    #Si el tamaño del archivo es small, medium o large se carga el archivo -jobs.csv al ser diferente de -por-jobs.csv
    if tamanio=="small" or tamanio=="medium" or tamanio=="large":
        formato_archivo = "-jobs.csv"
    else:
        formato_archivo = "-por-jobs.csv"
        #Se abre el archivo csv y se lee
    with open(cf.data_dir+tamanio+formato_archivo, mode="r", encoding="utf-8") as csvfile:
        data=csv.DictReader(csvfile, delimiter=";")
            #job son los datos del archivo csv en formato de diccionario
        for job in data:
            retorno=model.add_jobs(datos, job)
    print("Trabajos cargados en el modelo")
    return retorno

def load_skills(datos, tamanio):
    """
    Carga los datos de las habilidades en el modelo de un archivo csv
    Args:
    full_skills: diccionario con las llaves del archivo Skills vacias
    tamanio: tamaño del archivo que se va a cargar (10,20,30,40,50,60,70,80,90,small,medium,large)
    Returns:
    full_skills: diccionario con las llaves del archivo Skills llenas con los datos del archivo csv
    """
    if tamanio=="small" or tamanio=="medium" or tamanio=="large":
        formato_archivo = "-skills.csv"
    else:
        formato_archivo = "-por-skills.csv"
        #Se abre el archivo csv y se lee
    with open(cf.data_dir+tamanio+formato_archivo, mode="r", encoding="utf-8") as csvfile:
        data=csv.DictReader(csvfile, delimiter=";")
        for skill in data:
            retorno=model.add_skills(datos, skill)
    print("Skills cargadas en el modelo")
    return retorno
def load_employment_types(datos,tamanio):
    """
    Carga los datos de los empleos por sus tipos del archivo csv
    Args:
        full_employment: diccionario con las llaves del archivo Employment_types vacias
        tamanio: tamaño del archivo que se va a cargar (10,20,30,40,50,60,70,80,90,small,medium,large)

    Returns:
        diccionario con las llaves del archivo Employments_types llenas con los datos del archivo csv
    """
    if tamanio=="small" or tamanio=="medium" or tamanio=="large":
        formato_archivo = "-employments_types.csv"
    else:
        formato_archivo = "-por-employments_types.csv"
        #Se abre el archivo csv y se lee
    with open(cf.data_dir+tamanio+formato_archivo, mode="r", encoding="utf-8") as csvfile:
        data = csv.DictReader(csvfile, delimiter=";")
        for employment in data:
            rta = model.add_employments(datos, employment)
    return rta

def load_multilocation(datos, tamanio):
    """
    Carga los datos de multilocation en el modelo de un archivo csv
    Args:
    multilocation: diccionario con las llaves del archivo Multilocation vacias
    tamanio: tamaño del archivo que se va a cargar (10,20,30,40,50,60,70,80,90,small,medium,large)
    Returns:
    multilocation: diccionario con las llaves del archivo multilocation llenas con los datos del archivo csv
    """
    #Si el tamaño del archivo es small, medium o large se carga el archivo -multilocation.csv al ser diferente de -por-multilocation.csv
    #Se abre el archivo csv y se lee
    if tamanio=="small" or tamanio=="medium" or tamanio=="large":
        formato_archivo = "-multilocations.csv"
    else:
        formato_archivo = "-por-multilocations.csv"
        #Se abre el archivo csv y se lee
    with open(cf.data_dir+tamanio+formato_archivo, mode="r", encoding="utf-8") as csvfile:

        data=csv.DictReader(csvfile, delimiter=";")
        #multi son los datos del archivo csv en formato de diccionario
        for multi in data:
            retorno=model.add_multilocation(datos, multi)
    print("Multilocation cargados en el modelo")
    return retorno
def load_employment_types2(datos):
    return model.load_employments_types2(datos)
def obtener_datos(control, llave):
    """Función para obtener los datos de la estructura de datos
    Posibles selecciones:
    - jobs-lista - Lista de trabajos en formato array
    - jobs-mapa-id - Mapa de trabajos por id en formato probing
    - jobs-mapa-fecha - Mapa de trabajos por fecha en formato rbt
    - jobs-mapa-ciudad - Mapa de trabajos por ciudad en formato chaining
    - jobs-mapa-pais - Mapa de trabajos por pais en formato chaining
    - skills-mapa-id - Mapa de habilidades por id en formato chaining
    - skills-mapa-skill - Mapa de habilidades por skill en formato chaining
    - employment-mapa-ordenado - Mapa de empleos por salario en formato rbt
    - employment-mapa-id - Mapa de empleos por id en formato chaining
    - multilocation-mapa-id - Mapa de multilocalizaciones por id en formato chaining

    Args:
        datos (dict): _description_
        seleccion (str): _description_

    Returns:
        _type_: _description_
    """
    return model.obtener_datos(control["model"], llave)
# Funciones de ordenamiento

def sort(control):
    """
    Ordena los datos del modelo
    """
    #TODO: Llamar la función del modelo para ordenar los datos
    pass


# Funciones de consulta sobre el catálogo

def get_data(control, id):
    """
    Retorna un dato por su ID.
    """
    #TODO: Llamar la función del modelo para obtener un dato
    pass


def req_1(control, fecha_inicio, fecha_fin, memoria):
    """
    Retorna el resultado del requerimiento 1
    """
    if memoria==True:
        tracemalloc.start()
        start_memory=get_memory()
    start_time=get_time()
    datos=control["model"]
    retorno=model.req_1(datos, fecha_inicio, fecha_fin)
    end_time=get_time()
    if memoria==True:
        end_memory=get_memory()
        tracemalloc.stop()
        delta_mem=delta_memory(end_memory, start_memory)
    delta=delta_time(start_time, end_time)
    if memoria==True:
        return retorno, delta, delta_mem
    else:
        return retorno, delta


def req_2(control, minimo_salario, maximo_salario, memoria):
    """
    Retorna el resultado del requerimiento 2
    """
    if memoria==True:
        tracemalloc.start()
        start_memory=get_memory()
    start_time=get_time()
    datos=control["model"]
    retorno=model.req_2(datos, minimo_salario, maximo_salario)
    end_time=get_time()
    if memoria==True:
        end_memory=get_memory()
        tracemalloc.stop()
        delta_mem=delta_memory(end_memory, start_memory)
    delta=delta_time(start_time, end_time)
    if memoria==True:
        return retorno, delta, delta_mem
    else:
        return retorno, delta
    
    pass


def req_3(control, n, cod_pais, nivel_exp, memoria):
    """
    Retorna el resultado del requerimiento 3
    """
    if memoria==True:
        tracemalloc.start()
        start_memory=get_memory()
    start_time=get_time()
    datos=control["model"]
    retorno=model.req_3(datos, n, cod_pais, nivel_exp)
    end_time=get_time()
    if memoria==True:
        end_memory=get_memory()
        tracemalloc.stop()
        delta_mem=delta_memory(end_memory, start_memory)
    delta=delta_time(start_time, end_time)
    if memoria==True:
        return retorno, delta,delta_mem
    else:
        return retorno, delta,


def req_4(control, n_ofertas, ciudad, tipo, memoria):
    """
    Retorna el resultado del requerimiento 4
    """
    if memoria==True:
        tracemalloc.start()
        start_memory=get_memory()
    start_time=get_time()
    datos=control["model"]
    retorno=model.req_4(datos, n_ofertas, ciudad, tipo)
    end_time=get_time()
    if memoria==True:
        end_memory=get_memory()
        tracemalloc.stop()
        delta_mem=delta_memory(end_memory, start_memory)
    delta=delta_time(start_time, end_time)
    if memoria==True:
        return retorno, delta, delta_mem
    else:
        return retorno, delta


def req_5(control, numero_ofertas, tamanio_minimo, tamanio_maximo, habilidades, nivel_habilidad_minimo, nivel_habilidad_maximo, memoria):
    """
    Retorna el resultado del requerimiento 5
    """
    if memoria==True:
        tracemalloc.start()
        start_memory=get_memory()
    start_time=get_time()
    datos=control["model"]
    retorno=model.req_5(datos, numero_ofertas, tamanio_minimo, tamanio_maximo, habilidades, nivel_habilidad_minimo, nivel_habilidad_maximo)
    end_time=get_time()
    if memoria==True:
        end_memory=get_memory()
        tracemalloc.stop()
        delta_mem=delta_memory(end_memory, start_memory)
    delta=delta_time(start_time, end_time)
    if memoria==True:
        return retorno, delta, delta_mem
    else:
        return retorno, delta
    # TODO: Modificar el requerimiento 
    pass

def req_6(control, numero_ciudades, fecha_inicio, fecha_fin, salario_minimo, salario_maximo, memoria):
    """
    Retorna el resultado del requerimiento 6
    """
    if memoria==True:
        tracemalloc.start()
        start_memory=get_memory()
    start_time=get_time()
    datos=control["model"]
    retorno=model.req_6(datos, numero_ciudades, fecha_inicio, fecha_fin, salario_minimo, salario_maximo)
    end_time=get_time()
    if memoria==True:
        end_memory=get_memory()
        tracemalloc.stop()
        delta_mem=delta_memory(end_memory, start_memory)
    delta=delta_time(start_time, end_time)
    if memoria==True:
        return retorno, delta, delta_mem
    else:
        return retorno, delta
    pass


def req_7(control,anio, codigo_pais, propiedad_conteo, memoria):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7
    if memoria==True:
        tracemalloc.start()
        start_memory=get_memory()
    start_time=get_time()
    datos=control["model"]
    retorno=model.req_7(datos, anio, codigo_pais, propiedad_conteo)
    end_time=get_time()
    if memoria==True:
        end_memory=get_memory()
        tracemalloc.stop()
        delta_mem=delta_memory(end_memory, start_memory)
    delta=delta_time(start_time, end_time)
    if memoria==True:
        return retorno, delta, delta_mem
    else:
        return retorno, delta
    pass


def req_8(datos, mapa, eleccion, req7, memoria):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    if memoria==True:
        tracemalloc.start()
        start_memory=get_memory()
    start_time=get_time()
    retorno=model.req_8(datos, mapa, eleccion,req7)
    end_time=get_time()
    if memoria==True:
        end_memory=get_memory()
        tracemalloc.stop()
        delta_mem=delta_memory(end_memory, start_memory)
    delta=delta_time(start_time, end_time)
    if memoria==True:
        return retorno, delta, delta_mem
    else:
        return retorno, delta


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed

def get_memory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def delta_memory(stop_memory, start_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory
