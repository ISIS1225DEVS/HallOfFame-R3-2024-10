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
import datetime

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller():
    """
    Crea una instancia del modelo
    """
    """
    Crea una instancia del modelo
    """
    control = {'model': None}
    control['model'] = model.new_data_structs()
    return control

 #Funciones para la carga de datos

def load_data(control, memflag=True):
    """
    Carga los datos del reto
    """
    start_time = get_time()
    # inicializa el proceso para medir memoria
    if memflag is True:
        tracemalloc.start()
        start_memory = get_memory()
    
    catalog = control['model']
    load_jobs(catalog)
    load_skills(catalog)
    load_employment_types(catalog)
    load_multilocations(catalog)
    
    stop_time = get_time()
    time = delta_time(start_time, stop_time)

    if memflag is True:
        stop_memory = get_memory()
        tracemalloc.stop()
        memory = delta_memory(stop_memory, start_memory)
        return time, memory

    else:
        return time

    
t_archivos= '10-por' #Esto se cambia para probar los diferentes tamaños de archivos ej: '10-por' o 'large'

def load_jobs(control):
    file = cf.data_dir + t_archivos + '-jobs.csv'
    input_file = csv.DictReader(open(file, encoding='utf-8'), delimiter=';')
    for job in input_file:
        for i in job:   
            if job[i] == "":
                job[i] = "Unknown"
        model.addJob(control, job)
        model.addJobCity(control, job)

def load_skills(control):
    file = cf.data_dir + t_archivos + '-skills.csv'
    input_file_skills = csv.DictReader(open(file, encoding='utf-8'), delimiter=';')
    for skill in input_file_skills:
        for i in skill:
            if skill[i] == "":
                skill[i] = "Unknown"
        model.addSkill(control, skill)

def load_employment_types(control):
    file = cf.data_dir + t_archivos + '-employments_types.csv'
    input_file = csv.DictReader(open(file, encoding='utf-8'), delimiter=';')
    for e_type in input_file:
        for i in e_type:
            if e_type[i] == "":
                e_type[i] = "Unknown"
        model.addEmploymentType(control, e_type)
    model.crear_arbol_salarios(control)
    

def load_multilocations(control):
    file = cf.data_dir + t_archivos + '-multilocations.csv'
    input_file = csv.DictReader(open(file, encoding='utf-8'), delimiter=';')
    for multilocation in input_file:
        for i in multilocation:
            if multilocation[i] == "":
                multilocation[i] = "Unknown"
        model.addMultilocation(control, multilocation)
 
def size_control(control):
    catalog= control['model']
    j= model.data_size(catalog['jobs'])
    s= model.data_size(catalog['skills'])
    e= model.data_size(catalog['employments_types'])
    m= model.data_size(catalog['multilocation'])
    return j, s, e, m

def data_org(control):
    catalog= control['model']
    catalog = model.sortJobsFinal(catalog['jobs'])
    return catalog


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


def req_1(data_structs, initialDate, finalDate):
    """
    Retorna el resultado del requerimiento 1
    """
    initialDate = datetime.datetime.strptime(initialDate, '%Y-%m-%d')
    finalDate = datetime.datetime.strptime(finalDate, '%Y-%m-%d')
    valor = model.req_1(data_structs, initialDate, finalDate)
    contador = valor[0]
    info = valor[1]
    return contador, info


def req_2(control, salario_min, salario_max):
    """
    Retorna el resultado del requerimiento 2
    """
    valor = model.req_2(control, salario_min, salario_max)
    contador = valor[0]
    info = valor[1]
    return contador, info


def req_3(control, pais, experticia):
    """
    Retorna el resultado del requerimiento 3
    """
    valor = model.req_3(control, pais, experticia)
    contador = valor[0]
    info = valor[1]
    return contador, info


def req_4(control, ciudad, ubicacion):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    res = model.req_4(control, ciudad, ubicacion)
    tamaño = res[0]
    data = res [1]
    return tamaño, data


def req_5(data_structs,n,tamanio_low,tamanio_high,habilidad,nivel_low,nivel_high):
    """
    Retorna el resultado del requerimiento 5
    """
    r= model.req_5(data_structs,n,tamanio_low,tamanio_high,habilidad,nivel_low,nivel_high)
    return r

def req_6(data_structs, n, initialDate, finalDate, salMin, salMax):
    """
    Retorna el resultado del requerimiento 6
    """
    initialDate = datetime.datetime.strptime(initialDate, '%Y-%m-%d')
    finalDate = datetime.datetime.strptime(finalDate, '%Y-%m-%d')
    r = model.req_6(data_structs, n, initialDate, finalDate, salMin, salMax)
    return r

def req_7(data_structs,anio,pais,conteo):
    """
    Retorna el resultado del requerimiento 7
    """
    r= model.req_7(data_structs,anio,pais,conteo)
    return r

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
