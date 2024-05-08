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

csv.field_size_limit(2147483647)

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller():
    """
    Crea una instancia del modelo
    """
    #TODO: Llamar la función del modelo que crea las estructuras de datos
    catalog = model.new_data_structs()
    return catalog


# Funciones para la carga de datos

def load_data(control, tamanio):
    """
    Carga los datos del reto
    """

    # TODO: Realizar la carga de datos
    memflag=True
    start_time= get_time()
    if memflag == True:
        tracemalloc.start()
        start_memory =get_memory()

#logica

    file =  cf.data_dir + str(tamanio) +'-jobs.csv'
    input_file = csv.DictReader(open(file, encoding="utf-8"), delimiter=';')
    i=0
    for job in input_file:
        i+=1
        model.add_jobs_fecha(control,job)
        model.add_jobs_tamano(control,job)
        model.add_map_country_jobs(control, job)


    ofertas=model.info_carga_de_datos(control)
              
#fin logica
    stop_time = get_time()
    delta_time_2 = stop_time- start_time
    if memflag is True:
        stop_memory = get_memory()
        tracemalloc.stop()
        delta__memory_2=delta_memory(stop_memory, start_memory)
    return i,ofertas, delta_time_2, delta__memory_2

def load_country_jobs(control, tamanho):
    """
    Carga los datos del reto
    """

    # TODO: Realizar la carga de datos
    memflag=True
    start_time = get_time()
    if memflag is True:
        tracemalloc.start()
        start_memory =get_memory()

#logica

    file =  cf.data_dir + str(tamanho) +'-jobs.csv'
    input_file = csv.DictReader(open(file, encoding="utf-8"), delimiter=';')
    for job in input_file:
        info = model.add_country_jobs(control,job)
        

#fin logica
    stop_time = get_time()
    delta_time_2 = stop_time- start_time
    if memflag is True:
        stop_memory = get_memory()
        tracemalloc.stop()
        delta__memory_2=delta_memory(stop_memory, start_memory)
    return info, delta_time_2, delta__memory_2

def load_city_jobs(control, tamanho):
    """
    Carga los datos del reto
    """

    # TODO: Realizar la carga de datos
    memflag=True
    start_time = get_time()
    if memflag is True:
        tracemalloc.start()
        start_memory =get_memory()

#logica

    file =  cf.data_dir + str(tamanho) +'-jobs.csv'
    input_file = csv.DictReader(open(file, encoding="utf-8"), delimiter=';')
    for job in input_file:
        info = model.add_city_jobs(control,job)
        

#fin logica
    stop_time = get_time()
    delta_time_2 = stop_time- start_time
    if memflag is True:
        stop_memory = get_memory()
        tracemalloc.stop()
        delta__memory_2=delta_memory(stop_memory, start_memory)
    return info, delta_time_2, delta__memory_2

def load_id_skills(control, tamanho):
    """
    Carga los datos del reto
    """

    # TODO: Realizar la carga de datos
    memflag=True
    start_time = get_time()
    if memflag is True:
        tracemalloc.start()
        start_memory =get_memory()

#logica

    file =  cf.data_dir + str(tamanho) +'-skills.csv'
    input_file = csv.DictReader(open(file, encoding="utf-8"), delimiter=';')
    for skill in input_file:
        
        info=model.add_id_skills(control,skill)
        

#fin logica
    stop_time = get_time()
    delta_time_2 = stop_time- start_time
    if memflag is True:
        stop_memory = get_memory()
        tracemalloc.stop()
        delta__memory_2=delta_memory(stop_memory, start_memory)
    return info, delta_time_2, delta__memory_2


def load_id_multilocations(control, tamanho):
    """
    Carga los datos del reto
    """

    # TODO: Realizar la carga de datos
    memflag=True
    start_time = get_time()
    if memflag is True:
        tracemalloc.start()
        start_memory =get_memory()

#logica

    file =  cf.data_dir + str(tamanho) +'-multilocations.csv'
    input_file = csv.DictReader(open(file, encoding="utf-8"), delimiter=';')
    for location in input_file:
        info = model.add_multilocation(control,location)
        

#fin logica
    stop_time = get_time()
    delta_time_2 = stop_time- start_time
    if memflag is True:
        stop_memory = get_memory()
        tracemalloc.stop()
        delta__memory_2=delta_memory(stop_memory, start_memory)
    return info, delta_time_2, delta__memory_2


def load_id_employments_types(control, tamanho):
    """
    Carga los datos del reto
    """
    # TODO: Realizar la carga de datos
    memflag=True
    start_time = get_time()
    if memflag is True:
        tracemalloc.start()
        start_memory =get_memory()
#logica
    file =  cf.data_dir + str(tamanho) +'-employments_types.csv'
    input_file = csv.DictReader(open(file, encoding="utf-8"), delimiter=';')
    for employment in input_file:
        model.add_salarios(control, employment)
        info = model.add_employement_types(control,employment)
        
#fin logica
    stop_time = get_time()
    delta_time_2 = stop_time- start_time
    if memflag is True:
        stop_memory = get_memory()
        tracemalloc.stop()
        delta__memory_2=delta_memory(stop_memory, start_memory)
    return info, delta_time_2, delta__memory_2


def load_id_jobs(control, tamanho):
    """
    Carga los datos del reto
    """

    # TODO: Realizar la carga de datos
    memflag=True
    start_time = get_time()
    if memflag is True:
        tracemalloc.start()
        start_memory =get_memory()

#logica

    file =  cf.data_dir + str(tamanho) +'-jobs.csv'
    input_file = csv.DictReader(open(file, encoding="utf-8"), delimiter=';')
    for job in input_file:
        info = model.add_id_jobs(control,job)
        

    #fin logica
    stop_time = get_time()
    delta_time_2 = stop_time- start_time
    if memflag is True:
        stop_memory = get_memory()
        tracemalloc.stop()
        delta__memory_2=delta_memory(stop_memory, start_memory)
    return info, delta_time_2, delta__memory_2
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


def req_1(control,fecha_i,fecha_f):
    """
    Retorna el resultado del requerimiento 1
    """
    start_time=get_time()
    tamanio,ofertas = model.req1(control,fecha_i,fecha_f)
    end_time = get_time()
    deltatime = delta_time(start_time,end_time)
    # TODO: Modificar el requerimiento 1
    return tamanio,ofertas,deltatime


def req2(control, lim_inf_salary, lim_sup_salary):
    """
    Retorna el resultado del requerimiento 2
    """
    start_time=get_time()
    tamanio,salarios = model.req2(control,lim_inf_salary, lim_sup_salary)
    end_time = get_time()
    deltatime = delta_time(start_time,end_time)
  
    return tamanio,salarios,deltatime


def req_3(control,N, country_code, experience_level):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    start_time = get_time()
    ans = model.req_3(control,N, country_code, experience_level)
    end_time = get_time()
    deltatime = delta_time(start_time, end_time)
    return ans, deltatime


def req_4(control,N, city, tipo_ubicacion):
    """
    Retorna el resultado del requerimiento 4
    """
    start_time = get_time()
    ans = model.req_4(control,N, city, tipo_ubicacion)
    end_time = get_time()
    deltatime = delta_time(start_time, end_time)
    return ans, deltatime


def req_5(control, N, lim_inf_tam, lim_sup_tam, skill, lim_inf_nh, lim_sup_nh):
    """
    Retorna el resultado del requerimiento 5
    """
    start_time = get_time()
    tamanio, ans = model.req_5(control, N, lim_inf_tam, lim_sup_tam, skill, lim_inf_nh, lim_sup_nh)
    end_time = get_time()
    deltatime = delta_time(start_time, end_time)
    return tamanio ,ans, deltatime

def req_6(control,N_ciudades,fecha_i,fecha_f, lim_inf_sal, lim_sup_sal):
    """
    Retorna el resultado del requerimiento 6
    """
    start_time = get_time()
    tamanio,numero_ciudades,ciudades_mayores,ofertas = model.req_6(control, N_ciudades,fecha_i,fecha_f, lim_inf_sal, lim_sup_sal)
    end_time = get_time()
    deltatime = delta_time(start_time, end_time)
    return tamanio ,numero_ciudades,ciudades_mayores ,ofertas, deltatime


def req_7(control, anio, codigo_pais, propiedad):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7
    start_time = get_time()
    dicc_ans, cantidad_ofertas,lista_variable = model.req_7(control, anio, codigo_pais, propiedad)
    end_time = get_time()
    deltatime = delta_time(start_time, end_time)
    return dicc_ans, cantidad_ofertas,lista_variable, deltatime



def req_8(control):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    pass


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
