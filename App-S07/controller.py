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
import threading


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller():
    """
    Crea una instancia del modelo
    """
    control = {'model': None}
    control['model'] = model.newCatalog()
    
    return control


# Funciones para la carga de datos

def load_data(catalog):
    """
    Carga los datos del reto
    """
    catalog = catalog["model"]
    start_time = time.time() ##! QUITAR/DEBUG/REMOVER
    jobs = load_jobs(catalog) #ALL CSV LOADED
    
    stop_time = time.time() ##! QUITAR/DEBUG/REMOVER
    print("\033[1mTiempo proceso\033[0m") ##! QUITAR/DEBUG/REMOVER
    print("\033[1m"+str(delta_time(start_time,stop_time))+"\033[0m") ##! QUITAR/DEBUG/REMOVER
    return catalog["jobs"]

def load_jobs(catalog):
    tamaño = "large" # SIRVE PARA ALL DATA (ej: 10-por o small) #! DEJARLO COMO LARGE PARA LA ENTREGA
    jobsfile = cf.data_dir+tamaño+"-jobs.csv" 
    skillsfile = cf.data_dir+tamaño+"-skills.csv"
    EmpTypesfile = cf.data_dir+tamaño+"-employments_types.csv"
    multilocationfile = cf.data_dir+tamaño+"-multilocations.csv"
    
    model.Tempjobs(catalog,jobsfile) 
    
    SkillsDic = {}
    input_file_skills = csv.DictReader(open(skillsfile, encoding='utf-8'), delimiter=";")
    for oferta in input_file_skills:
        model.TempSkills(SkillsDic, oferta)
        
    EmpTypesDic = {}
    input_file_EmpTypes = csv.DictReader(open(EmpTypesfile, encoding='utf-8'), delimiter=";")
    for oferta in input_file_EmpTypes:
        model.TempEmpTypes(EmpTypesDic, oferta)
        
    multilocationDic = {}
    input_file_multilocation = csv.DictReader(open(multilocationfile, encoding='utf-8'), delimiter=";")
    for oferta in input_file_multilocation:
        model.Tempmultilocation(multilocationDic, oferta)
    
    model.addjobs(catalog, SkillsDic, EmpTypesDic, multilocationDic)
    return catalog["jobs"]

def tabulation3(data, head):
    res = model.declutterLoad3(data,head)
    return res

def tabulation5(data, head, keep):
    res = model.declutterLoad5(data,head,keep)
    return res

def tabulation_N(data, head, keep, N):
    res = model.declutterLoad_N(data, head, keep, N)
    return res

def Datesort(lista):
    listaord = model.Datesort(lista)
    return listaord


# Funciones de consulta sobre el catálogo

def req_1(control,fecha_inicial,fecha_final):
    """
    Retorna el resultado del requerimiento 1
    """
    tracemalloc.start() ##! QUITAR/DEBUG/REMOVER
    start_memory = get_memory() ##! QUITAR/DEBUG/REMOVER
    start_time = time.time() ##! QUITAR/DEBUG/REMOVER
    control = control["model"]
    res = model.req_1(control,fecha_inicial,fecha_final)
    stop_time = time.time() ##! QUITAR/DEBUG/REMOVER
    print("\033[1mTiempo proceso (s)\033[0m") ##! QUITAR/DEBUG/REMOVER
    print("\033[1m"+str(delta_time(start_time,stop_time))+"\033[0m") ##! QUITAR/DEBUG/REMOVER
    stop_memory = get_memory() ##! QUITAR/DEBUG/REMOVER
    tracemalloc.stop() ##! QUITAR/DEBUG/REMOVER
    print("\033[94mCantidad Memoria (kbps)\033[0m") ##! QUITAR/DEBUG/REMOVER
    print("\033[94m"+str(delta_memory(stop_memory, start_memory))+"\033[0m") ##! QUITAR/DEBUG/REMOVER
    return res


def req_2(control, salario_min, salario_max):
    """
    Retorna el resultado del requerimiento 2
    """
    tracemalloc.start() ##! QUITAR/DEBUG/REMOVER
    start_memory = get_memory() ##! QUITAR/DEBUG/REMOVER
    start_time = time.time() ##! QUITAR/DEBUG/REMOVER
    ofertas_cumplen, total_ofertas = model.req_2(control, salario_min, salario_max)
    stop_time = time.time() ##! QUITAR/DEBUG/REMOVER
    print("\033[1mTiempo proceso\033[0m") ##! QUITAR/DEBUG/REMOVER
    print("\033[1m"+str(delta_time(start_time,stop_time))+"\033[0m") ##! QUITAR/DEBUG/REMOVER
    stop_memory = get_memory() ##! QUITAR/DEBUG/REMOVER
    tracemalloc.stop() ##! QUITAR/DEBUG/REMOVER
    print("\033[94mCantidad Memoria (kbps)\033[0m") ##! QUITAR/DEBUG/REMOVER
    print("\033[94m"+str(delta_memory(stop_memory, start_memory))+"\033[0m") ##! QUITAR/DEBUG/REMOVER
    return ofertas_cumplen, total_ofertas



def req_3(control, n, CountryCode, ExpLvl):
    """
    Retorna el resultado del requerimiento 3
    """
    tracemalloc.start() ##! QUITAR/DEBUG/REMOVER
    start_memory = get_memory() ##! QUITAR/DEBUG/REMOVER
    start_time = time.time() ##! QUITAR/DEBUG/REMOVER
    control = control['model']
    ans = model.req_3(control, n, CountryCode, ExpLvl)
    stop_time = time.time() ##! QUITAR/DEBUG/REMOVER
    print("\033[1mTiempo proceso\033[0m") ##! QUITAR/DEBUG/REMOVER
    print("\033[1m"+str(delta_time(start_time,stop_time))+"\033[0m") ##! QUITAR/DEBUG/REMOVER
    stop_memory = get_memory() ##! QUITAR/DEBUG/REMOVER
    tracemalloc.stop() ##! QUITAR/DEBUG/REMOVER
    print("\033[94mCantidad Memoria (kbps)\033[0m") ##! QUITAR/DEBUG/REMOVER
    print("\033[94m"+str(delta_memory(stop_memory, start_memory))+"\033[0m") ##! QUITAR/DEBUG/REMOVER
    return ans


def req_4(control, n, ciudad, trabajo_ubicacion):
    """
    Retorna el resultado del requerimiento 4
    """
    control = control["model"]
    tracemalloc.start() ##! QUITAR/DEBUG/REMOVER
    start_memory = get_memory() ##! QUITAR/DEBUG/REMOVER
    start_time = time.time() ##! QUITAR/DEBUG/REMOVER
    res = model.req_4(control, n, ciudad, trabajo_ubicacion)
    stop_time = time.time() ##! QUITAR/DEBUG/REMOVER
    print("\033[1mTiempo proceso\033[0m") ##! QUITAR/DEBUG/REMOVER
    print("\033[1m"+str(delta_time(start_time,stop_time))+"\033[0m") ##! QUITAR/DEBUG/REMOVER
    stop_memory = get_memory() ##! QUITAR/DEBUG/REMOVER
    tracemalloc.stop() ##! QUITAR/DEBUG/REMOVER
    print("\033[94mCantidad Memoria (kbps)\033[0m") ##! QUITAR/DEBUG/REMOVER
    print("\033[94m"+str(delta_memory(stop_memory, start_memory))+"\033[0m") ##! QUITAR/DEBUG/REMOVER
    return res


def req_5(control, size_min, size_max, nombre_habilidad, skill_min, skill_max):
    """
    Retorna el resultado del requerimiento 5
    """
    tracemalloc.start() ##! QUITAR/DEBUG/REMOVER
    start_memory = get_memory() ##! QUITAR/DEBUG/REMOVER
    start_time = time.time() ##! QUITAR/DEBUG/REMOVER
    ofertas_cumplen, total_ofertas= model.req_5(control, size_min, size_max, nombre_habilidad, skill_min, skill_max)
    stop_time = time.time() ##! QUITAR/DEBUG/REMOVER
    print("\033[1mTiempo proceso\033[0m") ##! QUITAR/DEBUG/REMOVER
    print("\033[1m"+str(delta_time(start_time,stop_time))+"\033[0m") ##! QUITAR/DEBUG/REMOVER
    stop_memory = get_memory() ##! QUITAR/DEBUG/REMOVER
    tracemalloc.stop() ##! QUITAR/DEBUG/REMOVER
    print("\033[94mCantidad Memoria (kbps)\033[0m") ##! QUITAR/DEBUG/REMOVER
    print("\033[94m"+str(delta_memory(stop_memory, start_memory))+"\033[0m") ##! QUITAR/DEBUG/REMOVER
    return ofertas_cumplen, total_ofertas
    
def req_6(control, OldestDate, RecentDate, minSalary, maxSalary):
    """
    Retorna el resultado del requerimiento 6
    """
    catalog = control['model']
    tracemalloc.start() ##! QUITAR/DEBUG/REMOVER
    start_memory = get_memory() ##! QUITAR/DEBUG/REMOVER
    start_time = time.time() ##! QUITAR/DEBUG/REMOVER
    #poner acá llamado controller
    ans = model.req_6(catalog, OldestDate, RecentDate, minSalary, maxSalary)
    stop_time = time.time() ##! QUITAR/DEBUG/REMOVER
    print("\033[1mTiempo proceso\033[0m") ##! QUITAR/DEBUG/REMOVER
    print("\033[1m"+str(delta_time(start_time,stop_time))+"\033[0m") ##! QUITAR/DEBUG/REMOVER
    stop_memory = get_memory() ##! QUITAR/DEBUG/REMOVER
    tracemalloc.stop() ##! QUITAR/DEBUG/REMOVER
    print("\033[94mCantidad Memoria (kbps)\033[0m") ##! QUITAR/DEBUG/REMOVER
    print("\033[94m"+str(delta_memory(stop_memory, start_memory))+"\033[0m") ##! QUITAR/DEBUG/REMOVER
    

    return ans


def req_7(control, año, CODpais, propiedad_conteo):
    """
    Retorna el resultado del requerimiento 7
    """
    control = control["model"]
    tracemalloc.start() ##! QUITAR/DEBUG/REMOVER
    start_memory = get_memory() ##! QUITAR/DEBUG/REMOVER
    start_time = time.time() ##! QUITAR/DEBUG/REMOVER
    res = model.req_7(control, año, CODpais, propiedad_conteo)
    stop_time = time.time() ##! QUITAR/DEBUG/REMOVER
    print("\033[1mTiempo proceso\033[0m") ##! QUITAR/DEBUG/REMOVER
    print("\033[1m"+str(delta_time(start_time,stop_time))+"\033[0m") ##! QUITAR/DEBUG/REMOVER
    stop_memory = get_memory() ##! QUITAR/DEBUG/REMOVER
    tracemalloc.stop() ##! QUITAR/DEBUG/REMOVER
    print("\033[94mCantidad Memoria (kbps)\033[0m") ##! QUITAR/DEBUG/REMOVER
    print("\033[94m"+str(delta_memory(stop_memory, start_memory))+"\033[0m") ##! QUITAR/DEBUG/REMOVER
    return res


def req_8(control):
    """
    Retorna el resultado del requerimiento 8
    """
    tracemalloc.start() ##! QUITAR/DEBUG/REMOVER
    start_memory = get_memory() ##! QUITAR/DEBUG/REMOVER
    start_time = time.time() ##! QUITAR/DEBUG/REMOVER
    res=model.req_8(control)
    stop_time = time.time() ##! QUITAR/DEBUG/REMOVER
    print("\033[1mTiempo proceso\033[0m") ##! QUITAR/DEBUG/REMOVER
    print("\033[1m"+str(delta_time(start_time,stop_time))+"\033[0m") ##! QUITAR/DEBUG/REMOVER
    stop_memory = get_memory() ##! QUITAR/DEBUG/REMOVER
    tracemalloc.stop() ##! QUITAR/DEBUG/REMOVER
    print("\033[94mCantidad Memoria (kbps)\033[0m") ##! QUITAR/DEBUG/REMOVER
    print("\033[94m"+str(delta_memory(stop_memory, start_memory))+"\033[0m") ##! QUITAR/DEBUG/REMOVER
    return res


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