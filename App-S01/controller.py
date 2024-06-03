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
import csv
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as queue
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from datetime import datetime
csv.field_size_limit(2147483647)
"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller():
    """
    Crea una instancia del modelo
    """
    #TODO: Llamar la función del modelo que crea las estructuras de datos
    control = {
        'model': None
    }
    control['model'] = model.new_data_structs()
    return control

# Funciones para la carga de datos

def load_data(control, size_file):
    """
    Carga los datos del reto
    """
    # TODO: Realizar la carga de datos
    jobs = load_job_offers(control['model'], size_file)
    load_skills(control['model'], size_file)
    load_employement_types(control['model'], size_file)
    return jobs

def load_job_offers(catalog, size_file):
    if len(size_file)==2:
        size_file= size_file+str("-por")
    job_file_name = f"{cf.data_dir}{size_file}-jobs.csv"
    input_file = csv.DictReader(open(job_file_name, encoding='utf-8'), delimiter=";")
    for job_offer in input_file:
        model.add_job(catalog, job_offer)
    return model.first_last(catalog['job_offers'], ['published_at','city', 'country_code' , 'title', 'experience_level', 'company_name'])
# Funciones de ordenamiento

def load_employement_types(catalog, size_file):
    if len(size_file)==2:
        size_file= size_file+str("-por")
    employment_file_name = f"{cf.data_dir}{size_file}-employments_types.csv"
    input_file = csv.DictReader(open(employment_file_name, encoding= "utf-8"), delimiter=";")
    for employment_type in input_file:
        model.add_employment_types(catalog, employment_type)
        model.add_req_6_nuevo(catalog, employment_type)
        
def load_multilocations(catalog, size_file):
    if len(size_file)==2:
        size_file= size_file+str("-por")
    multilocations_file_name = f"{cf.data_dir}{size_file}-multilocations.csv"
    input_file = csv.DictReader(open(multilocations_file_name, encoding= "utf-8"), delimiter=";")
    for employment_type in input_file:
        model.add_multilocation(catalog, employment_type)


def load_skills(catalog, size_file):
    if len(size_file)==2:
        size_file= size_file+str("-por")
    skills_file_name = f"{cf.data_dir}{size_file}-skills.csv"
    print(skills_file_name)
    input_file = csv.DictReader(open(skills_file_name, encoding= "utf-8"), delimiter=";")
    for employment_type in input_file:
        model.add_skills(catalog, employment_type)
        #model.add_req5(catalog, employment_type )
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


def req_1(control,keylo, keyhi):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    size, lista = model.req_1(control['model'], keylo, keyhi)
    return size, lista 


def req_2(control):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    pass


def req_3(control):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    pass

def req_4(control,n,ciudad,ubi):
    data=control['model']
    retorno,tamanio=model.req_4(data,n,ciudad,ubi)
    return retorno,tamanio
    


def req_5(control, mincomp,maxcomp, skill, minskill, maxskill):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    peso, lista , size = model.req_5(control['model'], mincomp,maxcomp, skill, minskill, maxskill)
    return peso, lista, size

def req_6(control,fecha1,fecha2,salmin, salmax):
    cantidad_ofertas, cantidad_ciudades,lista_de_ciudades,lista_ofertas_max_ciudad, max_ciudad  = model.req_6(control['model'],fecha1,fecha2,salmin, salmax)
    return cantidad_ofertas, cantidad_ciudades,lista_de_ciudades,lista_ofertas_max_ciudad, max_ciudad


def req7noskill(control,anio,pais,crit):
    headers,values,tamanio,maxi,maxim,mini,minim,ofertas=model.req7noskill(control,anio,pais,crit)
    return headers,values,tamanio,maxi,maxim,mini,minim,ofertas
def req7skill(control,anio,pais):
    headers,values,tamanio,maxi,maxim,mini,minim,ofertas=model.req7skill(control,anio,pais)
    return headers,values,tamanio,maxi,maxim,mini,minim,ofertas
    
    
def req_7(control):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7
    pass


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

def tabulator(data):
   
    primeros = lt.subList(data, 1 , 3)
    ultimos = lt.subList(data, lt.size(data)- 2, 3)
    for i in range(1,4):
        model.tabulator(ultimos, i, primeros)
    return primeros, ultimos

def tabulador_req5(data):
    primeros = 0
    pass
