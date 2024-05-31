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
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
csv.field_size_limit(2147483647)
"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller():
    """
    Crea una instancia del modelo
    """
    control = {"model": None}
    control["model"] = model.new_data_structs()
    return control

# Funciones para la carga de datos

def load_data(control, file_size):
    
    data = control['model']
    employments_size = load_employments(data, file_size)
    multilocations_size = load_multilocations(data, file_size)
    skills_size = load_skills(data, file_size)
    jobs_size = load_jobs(data, file_size)


    return jobs_size, employments_size, multilocations_size, skills_size, 


def load_jobs(control, file_size):
    """
    Carga el archivo jobs.csv
    """
    jobs_file_location = cf.data_dir + f'{file_size}-jobs.csv'
    jobs_file = csv.DictReader(open(jobs_file_location, encoding='utf-8'), delimiter=';')



    for each_line in jobs_file:
        model.add_job(control['jobs'], each_line)
        model.add_job_time(control['jobs_time'], each_line)
        model.add_jobs_compsize(control,each_line)
    jobs_size = om.size(control['jobs'])
    
    return jobs_size


def load_employments(control, file_size):
    """
    Carga el archivo employments_types.csv
    """
    employment_file_location = cf.data_dir + f'{file_size}-employments_types.csv'
    employments_file = csv.DictReader(open(employment_file_location, encoding='utf-8'), delimiter=';')


    for each_line in employments_file:
        model.add_employment_type(control['employments'], each_line)
    
    employments_size = mp.size(control['employments'])
    
    return employments_size


def load_multilocations(control, file_size):
    """
    Carga el archivo employments_types.csv
    """
    multilocation_file_location = cf.data_dir + f'{file_size}-multilocations.csv'
    multilocations_file = csv.DictReader(open(multilocation_file_location, encoding='utf-8'), delimiter=';')

    for each_line in multilocations_file:
        model.add_multilocation(control['multilocations'], each_line)
    
    multilocation_size = mp.size(control['multilocations'])
    
    return multilocation_size


def load_skills(control, file_size):
    """
    Carga el archivo employments_types.csv
    """
    skills_file_location = cf.data_dir + f'{file_size}-skills.csv'
    skills_file = csv.DictReader(open(skills_file_location, encoding='utf-8'), delimiter=';')

    for each_line in skills_file:
        model.add_skill(control['skills'], each_line)
    
    skills_size = mp.size(control['skills'])
    
    return skills_size



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


def req_1(control,fecha_inicial,fecha_final):
    """
    Retorna el resultado del requerimiento 1
    """
    return model.req_1(control,fecha_inicial,fecha_final)


def req_2(control,salario_minimo,salario_maximo):
    """
    Retorna el resultado del requerimiento 2
    """
    return model.req_2(control,salario_minimo,salario_maximo)


def req_3(control,n,codigo_pais,nivel_experticia):
    """
    Retorna el resultado del requerimiento 3
    """
    return model.req_3(control,n,codigo_pais,nivel_experticia)


def req_4(control, n_offers, city_name, job_location):
    """
    Retorna el resultado del requerimiento 4
    """
    ans, size = model.req_4(control, n_offers, city_name, job_location)

    return ans, size


def req_5(n,ls_companysize,li_companysize,skill,ls_companyskill,li_companyskill,control):
    """
    Retorna el resultado del requerimiento 5
    """
    return model.req_5(n,ls_companysize,li_companysize,skill,ls_companyskill,li_companyskill,control)

def req_6(control,n,fecha_inicial,fecha_final,salario_minimo,salario_maximo):
    """
    Retorna el resultado del requerimiento 6
    """
    return model.req_6(control,n,fecha_inicial,fecha_final,salario_minimo,salario_maximo)


def req_7(control, year, country_code, property_input):
    """
    Retorna el resultado del requerimiento 7
    """
    ans, general_size, graph_size, distribution = model.req_7(control, year, country_code, property_input)

    return ans, general_size, graph_size, distribution


def req_8(control,respuesta_req,type,req_name):
    """
    Retorna el resultado del requerimiento 8
    """
    return model.req_8(control,respuesta_req,type,req_name)

def req_8_todos(respuesta_req1,respuesta_req2,respuesta_req3,respuesta_req4,respuesta_req5,respuesta_req6,respuesta_req7):
    return model.req_8_todos(respuesta_req1,respuesta_req2,respuesta_req3,respuesta_req4,respuesta_req5,respuesta_req6,respuesta_req7)

# Funciones para medir tiempos de ejecucion
def ver_divisa(control):
    return model.ver_divisa(control)


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
