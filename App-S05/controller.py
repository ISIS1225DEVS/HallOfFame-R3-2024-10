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
from DISClib.ADT import list as lt
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import orderedmap as om


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller():
    """
    Crea una instancia del modelo
    """
    control = {
        'model': None
    }
    control['model'] = model.new_data_structs()
    return control

#◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤
# Funciones para la carga de datos
#◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤


def load_data(control,muestra, memflag=True):
    """
    Carga los datos del reto
    """
    # TODO: Realizar la carga de datos
     # toma el tiempo al inicio del proceso
    start_time = getTime()

    # inicializa el proceso para medir memoria
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()

    data_struct = control['model']
    
    load_multilocations(data_struct,muestra)
    load_skills(data_struct, muestra)
    load_employmentTypes(data_struct, muestra)
    numjobs=load_jobs(data_struct, muestra)
    model.loadArbolReq7(data_struct)
    
    # toma el tiempo al final del proceso
    stop_time = getTime()
    # calculando la diferencia en tiempo
    delta_time = deltaTime(stop_time, start_time)

    arbol = om.valueSet(data_struct["arbolReq1"])
    final = lt.newList("ARRAY_LIST")
    for subarbol in lt.iterator(arbol):
        model.valueSetList(subarbol, final)

    # finaliza el proceso para medir memoria
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        delta_memory = deltaMemory(stop_memory, start_memory)
        # respuesta con los datos de tiempo y memoria
        return [[delta_time, delta_memory], final]

    else:
        # respuesta sin medir memoria
        return [ delta_time, final]
    
    
    
def load_jobs(data_struct, muestra):
    jobfile = cf.data_dir + muestra+'-jobs.csv'
    input_file = csv.DictReader(open(jobfile, encoding='utf-8'),delimiter=';')
    sumatoria=0
    
    for job in input_file:
        salarioJobPareja=mp.get(data_struct["tabla_employmentTypesID"], job["id"])
        salarioJobValue=me.getValue(salarioJobPareja)
        job["salary_from"]=salarioJobValue["salary_from"]
        job["salary_to"]=salarioJobValue["salary_to"]
        
        skillsJobPareja=mp.get(data_struct["tabla_skillsID"], job["id"])
        skillsJobValue=me.getValue(skillsJobPareja)
        job["skills"]=skillsJobValue["skills"]
        
        job["skills_required"] = []
        for skill in lt.iterator(job["skills"]):
            job["skills_required"].append(skill["name"])
        
        model.add_arbolReq1(data_struct, job)
        model.add_arbolReq2(data_struct, job)
        model.add_tablaReq4(data_struct, job)
        model.add_tablaReq5(data_struct, job)
        model.add_tablaReq6(data_struct, job)
        model.add_tablaReq37(data_struct,job)
        
    return sumatoria


def load_employmentTypes(data_struct, muestra):
    skillsFile = cf.data_dir + muestra + '-employments_types.csv'
    input_file = csv.DictReader(open(skillsFile, encoding='utf-8'),delimiter=';')
    prev=None
    
    for employmentType in input_file:
        current=employmentType
        if prev==None:
            model.add_tabla_employmentTypesID(data_struct, employmentType)
        elif prev["id"]==employmentType["id"]:
            NewEmploymentType=employmentType
            if prev["type"]=="b2b":
                NewEmploymentType["salary_to"]=prev["salary_to"]
            else:
                NewEmploymentType["salary_from"]=prev["salary_from"]
            model.add_tabla_employmentTypesID(data_struct, NewEmploymentType)
        else:
            model.add_tabla_employmentTypesID(data_struct, employmentType)
            
        prev=current

        
    return None


def load_multilocations(data_struct, muestra):
    skillsFile = cf.data_dir + muestra + '-multilocations.csv'
    input_file = csv.DictReader(open(skillsFile, encoding='utf-8'),delimiter=';')
    
    pre_prev={"id":None}
    prev={"id":None}
    
    for multilocation in input_file:
        current=multilocation
        
        #añado el elemento a multilocation si tiene más de una location y solo lo añado una vez
        if prev["id"]==pre_prev["id"] and current["id"]!=prev["id"] and prev["id"]!=None:
            model.add_tabla_multilocationID(data_struct, prev)
            
        pre_prev=prev
        prev=current
    
    return None


def load_skills(data_struct, muestra):
    skillsFile = cf.data_dir + muestra + '-skills.csv'
    input_file = csv.DictReader(open(skillsFile, encoding='utf-8'),delimiter=';')
    for skill in input_file:
        model.add_tabla_skillsID(data_struct, skill)
       
    return None


def primeros3_ultimos3(data_struct):
    #Saco las parejas de los años
    primeros3=None
    ultimos3=None
    return primeros3, ultimos3


#◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤
# Funciones de ordenamiento
#◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤

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


def req_1(control, memflag, fechai, fechaf):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1

    # toma el tiempo al inicio del proceso
    start_time = getTime()

    # inicializa el proceso para medir memoria
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()

    a = model.req_1(control["model"], fechai, fechaf)

        # toma el tiempo al final del proceso
    stop_time = getTime()
    # calculando la diferencia en tiempo
    delta_time = deltaTime(stop_time, start_time)

    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        delta_memory = deltaMemory(stop_memory, start_memory)
        # respuesta con los datos de tiempo y memoria
        return [a, [delta_time, delta_memory]]

    else:
        # respuesta sin medir memoria
        return [a, delta_time]


def req_2(control, memflag, salarioi, salariof):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2

    # toma el tiempo al inicio del proceso
    start_time = getTime()

    # inicializa el proceso para medir memoria
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()

    a = model.req_2(control["model"], salarioi, salariof)

        # toma el tiempo al final del proceso
    stop_time = getTime()
    # calculando la diferencia en tiempo
    delta_time = deltaTime(stop_time, start_time)

    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        delta_memory = deltaMemory(stop_memory, start_memory)
        # respuesta con los datos de tiempo y memoria
        return [a, [delta_time, delta_memory]]

    else:
        # respuesta sin medir memoria
        return [a, delta_time]


def req_3(control,memflag, N, country_code, experience_level):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3

    # toma el tiempo al inicio del proceso
    start_time = getTime()

    # inicializa el proceso para medir memoria
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()

    a = model.req_3(control["model"], N, country_code, experience_level)    
    # toma el tiempo al final del proceso
    stop_time = getTime()
    # calculando la diferencia en tiempo
    delta_time = deltaTime(stop_time, start_time)

    # finaliza el proceso para medir memoria
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        delta_memory = deltaMemory(stop_memory, start_memory)
        # respuesta con los datos de tiempo y memoria
        return [a, [delta_time, delta_memory]]

    else:
        # respuesta sin medir memoria
        return [a, delta_time]

    



def req_4(control, memflag, n, city, work_type):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4

    # toma el tiempo al inicio del proceso
    start_time = getTime()

    # inicializa el proceso para medir memoria
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()

    a = model.req_4(control["model"], n, city, work_type)

        # toma el tiempo al final del proceso
    stop_time = getTime()
    # calculando la diferencia en tiempo
    delta_time = deltaTime(stop_time, start_time)

    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        delta_memory = deltaMemory(stop_memory, start_memory)
        # respuesta con los datos de tiempo y memoria
        return [a, [delta_time, delta_memory]]

    else:
        # respuesta sin medir memoria
        return [a, delta_time]


def req_5(control, memflag, numOfertas, minCompSize, maxCompSize, skill, minSkillLev, maxSkillLev):
    """
    Retorna el resultado del requerimiento 5
    """
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7
    """
    Retorna el resultado del requerimiento 7
    """
    # toma el tiempo al inicio del proceso
    start_time = getTime()

    # inicializa el proceso para medir memoria
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()
        
    ans=model.req_5(control["model"], numOfertas, minCompSize, maxCompSize, skill, minSkillLev, maxSkillLev)

    # toma el tiempo al final del proceso
    stop_time = getTime()
    # calculando la diferencia en tiempo
    delta_time = deltaTime(stop_time, start_time)

    # finaliza el proceso para medir memoria
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        delta_memory = deltaMemory(stop_memory, start_memory)
        # respuesta con los datos de tiempo y memoria
        return [ans, [delta_time, delta_memory]]

    else:
        # respuesta sin medir memoria
        return [ans, delta_time]
    

def req_6(control,memflag, N, start_date, end_date, min_salary, max_salary):
    """
    Retorna el resultado del requerimiento 6
    """
    # toma el tiempo al inicio del proceso
    start_time = getTime()

    # inicializa el proceso para medir memoria
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()

    a = model.req_6(control["model"], N, start_date, end_date, min_salary, max_salary)

    # toma el tiempo al final del proceso
    stop_time = getTime()
    # calculando la diferencia en tiempo
    delta_time = deltaTime(stop_time, start_time)

    # finaliza el proceso para medir memoria
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        delta_memory = deltaMemory(stop_memory, start_memory)
        # respuesta con los datos de tiempo y memoria
        return [a, [delta_time, delta_memory]]

    else:
        # respuesta sin medir memoria
        return [a, delta_time]


   
    


def req_7(control, memflag, year, pais, propiedad):
    """
    Retorna el resultado del requerimiento 7
    """
    """
    Retorna el resultado del requerimiento 7
    """
    # toma el tiempo al inicio del proceso
    start_time = getTime()

    # inicializa el proceso para medir memoria
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()
        
    ans=model.req_7(control["model"], year, pais, propiedad)

    # toma el tiempo al final del proceso
    stop_time = getTime()
    # calculando la diferencia en tiempo
    delta_time = deltaTime(stop_time, start_time)

    # finaliza el proceso para medir memoria
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        delta_memory = deltaMemory(stop_memory, start_memory)
        # respuesta con los datos de tiempo y memoria
        return [ans, [delta_time, delta_memory]]

    else:
        # respuesta sin medir memoria
        return [ans, delta_time]
    


def req_8(control):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    pass

#◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤
# Funciones para medir tiempos de ejecucion
#◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤


def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def deltaTime(end, start):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed


#◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤
# Funciones para medir la memoria utilizada
#◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤


def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def deltaMemory(stop_memory, start_memory):
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
