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
    #TODO: Llamar la función del modelo que crea las estructuras de datos
    control = {
        "model": None
        }
    control["model"] = model.new_data_structs()
    return control


# Funciones para la carga de datos

def load_data(control, filename, memory_sign, forma_de_carga):
    """
    Carga los datos del reto
    """
    # TODO: Realizar la carga de datos
    data_structs = control["model"]
    tiempo_inicial = get_time()
    
    cambio_memoria = None
    if memory_sign:
        tracemalloc.start()
        memoria_inicial = get_memory()
    
    jobs = load_jobs(data_structs, filename[0])
    skills = load_skills(data_structs, filename[2])
    multilocations = load_multilocations(data_structs, filename[3])
    employments = load_employments(data_structs, filename[1], forma_de_carga)
    
    tiempo_final = get_time()
    tiempo_total = delta_time(tiempo_inicial, tiempo_final)
    
    if memory_sign:
        memoria_final= get_memory()
        tracemalloc.stop()

        cambio_memoria = delta_memory(memoria_final, memoria_inicial)
    
    return jobs, skills, multilocations, employments, tiempo_total, cambio_memoria
    
def load_jobs(data_structs, name_jobs):
    
    jobs_file = cf.data_dir + name_jobs
    input_file = csv.DictReader(open(jobs_file, encoding="utf-8"), delimiter=";")
    
    for jobs in input_file:
        model.add_jobs(data_structs, jobs)
    return model.jobs_size(data_structs)

def load_skills(data_structs, name_skills):
    skills_file = cf.data_dir + name_skills
    input_file = csv.DictReader(open(skills_file, encoding="utf-8"), delimiter=";")
    
    for skills in input_file:
        model.add_skills(data_structs, skills)
    return model.skills_size(data_structs)

def load_multilocations(data_structs, name_multilocations):
    multilocations_file = cf.data_dir + name_multilocations
    input_file = csv.DictReader(open(multilocations_file, encoding="utf-8"), delimiter=";")
    
    for multilocations in input_file:
        model.add_multilocations(data_structs, multilocations)
    return model.multilocations_size(data_structs)

def load_employments(data_structs, name_employments, forma_de_carga):
    employments_file = cf.data_dir + name_employments
    input_file = csv.DictReader(open(employments_file, encoding="utf-8"),delimiter=";")
    
    for employments in input_file:
        model.add_employments(data_structs, employments, forma_de_carga)
    return model.employments_size(data_structs)

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


def req_1(control, fecha_inicial, fecha_final, memory_sign, bono):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    tiempo_inicial = get_time()
    
    cambio_memoria = None
    if memory_sign:
        tracemalloc.start()
        memoria_inicial = get_memory()
        
    numero, primeras5 , ultimas5, n_ofertas = model.req_1(control, fecha_inicial, fecha_final, bono)
    
    tiempo_final = get_time()
    tiempo_total = delta_time(tiempo_inicial, tiempo_final)
    
    if memory_sign:
        memoria_final= get_memory()
        tracemalloc.stop()

        cambio_memoria = delta_memory(memoria_final, memoria_inicial)
    
    return numero, primeras5, ultimas5, n_ofertas, tiempo_total, cambio_memoria


def req_2(control, salario_inf, salario_sup, memory_sign, bono):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    tiempo_inicial = get_time()
    cambio_memoria = None
    if memory_sign:
        tracemalloc.start()
        memoria_inicial = get_memory()
        
    total, ofertas = model.req_2(control, salario_inf, salario_sup, bono)
    
    tiempo_final = get_time()
    tiempo_total = delta_time(tiempo_inicial, tiempo_final)
    
    if memory_sign:
        memoria_final= get_memory()
        tracemalloc.stop()

        cambio_memoria = delta_memory(memoria_final, memoria_inicial)
    
    return total, ofertas, tiempo_total, cambio_memoria

def decidir_metodo_sort(rta, control):
    lista_ordenada = model.ordenamiento(rta, control)
    return lista_ordenada

def req_3(control, n_ofertas, pais, experticia, memory_sign, bono):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    tiempo_inicial = get_time()
    
    cambio_memoria = None
    if memory_sign:
        tracemalloc.start()
        memoria_inicial = get_memory()
    
    numero, primeras5, ultimas5, n_ofertas_tot = model.req_3(control, n_ofertas, pais, experticia, bono)
    
    tiempo_final = get_time()
    tiempo_total = delta_time(tiempo_inicial, tiempo_final)
    
    if memory_sign:
        memoria_final= get_memory()
        tracemalloc.stop()

        cambio_memoria = delta_memory(memoria_final, memoria_inicial)
    
    return numero, primeras5, ultimas5, n_ofertas_tot, tiempo_total, cambio_memoria


def req_4(control, cantidad_n, ciudad, ubicacion, memory_sign, ans, ans_2):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    tiempo_inicial = get_time()
    cambio_memoria = None
    if memory_sign:
        tracemalloc.start()
        memoria_inicial = get_memory()
        
    total, ofertas = model.req_4(control, cantidad_n, ciudad, ubicacion, ans, ans_2)
    
    tiempo_final = get_time()
    tiempo_total = delta_time(tiempo_inicial, tiempo_final)
    
    if memory_sign:
        memoria_final= get_memory()
        tracemalloc.stop()

        cambio_memoria = delta_memory(memoria_final, memoria_inicial)
    return total, ofertas, tiempo_total, cambio_memoria

def req_5(control, n_ofertas, size_inf, size_sup, habilidad, skill_inf, skill_sup, memory_sign, bono):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    tiempo_inicial = get_time()
    cambio_memoria = None
    if memory_sign:
        tracemalloc.start()
        memoria_inicial = get_memory()
        
    total, ofertas = model.req_5(control, n_ofertas, size_inf, size_sup, habilidad, skill_inf, skill_sup, bono)
    
    tiempo_final = get_time()
    tiempo_total = delta_time(tiempo_inicial, tiempo_final)
    
    if memory_sign:
        memoria_final= get_memory()
        tracemalloc.stop()

        cambio_memoria = delta_memory(memoria_final, memoria_inicial)
    
    return total, ofertas, tiempo_total, cambio_memoria

def req_6(control, n_ciudades, fecha_inicial, fecha_final, salario_inicial, salario_final, memory_sign, bono):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    tiempo_inicial = get_time()
    
    cambio_memoria = None
    if memory_sign:
        tracemalloc.start()
        memoria_inicial = get_memory()
        
    numero, primeras5 , ultimas5, n_ofertas, cantidad_ciudades_requisitos, ciudades_ordenadas = model.req_6(control, n_ciudades, fecha_inicial, fecha_final, salario_inicial, salario_final, bono)
    
    tiempo_final = get_time()
    tiempo_total = delta_time(tiempo_inicial, tiempo_final)
    
    if memory_sign:
        memoria_final= get_memory()
        tracemalloc.stop()

        cambio_memoria = delta_memory(memoria_final, memoria_inicial)
    
    return numero, primeras5, ultimas5, n_ofertas, cantidad_ciudades_requisitos, ciudades_ordenadas, tiempo_total, cambio_memoria


def req_7(control, anio, pais, propiedad, memory_sign, bono):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7
    tiempo_inicial = get_time()
    cambio_memoria = None
    if memory_sign:
        tracemalloc.start()
        memoria_inicial = get_memory()
        
    total_ofertas, total_grafico, ofertas = model.req_7(control, anio, pais, propiedad, bono)
    
    tiempo_final = get_time()
    tiempo_total = delta_time(tiempo_inicial, tiempo_final)
    
    if memory_sign:
        memoria_final= get_memory()
        tracemalloc.stop()

        cambio_memoria = delta_memory(memoria_final, memoria_inicial)
    
    return total_ofertas, total_grafico, ofertas, tiempo_total, cambio_memoria

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

def imprimir_n(control, pos_inicial, total):
    jobs = control["model"]["jobs"]
    n = model.imprimir_n(jobs, pos_inicial, total)
    
    return n

def convertir_bool(valor):
    if valor == "True":
        return True
    else:
        return False
def mostrar_en_pantalla(lst):
    model.mostrar_en_pantalla(lst)

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