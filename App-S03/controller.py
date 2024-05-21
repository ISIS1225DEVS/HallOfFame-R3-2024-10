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
from currency_converter import CurrencyConverter
from DISClib.ADT import map as mp
from DISClib.ADT import minpq as mpq
from DISClib.ADT import indexminpq as impq
from DISClib.ADT import orderedmap as om
from DISClib.ADT import list as lt
from DISClib.DataStructures import mapentry as me


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

globalSufijo = "20-por"
prueba = "Rapidez"

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

def cambiar_pruebas(respuesta):
    global prueba
    prueba = respuesta
    return prueba

def cambiarTamañoMuestra(sufijo):
    global globalSufijo
    globalSufijo = sufijo

def load_data(control):
    """
    Carga los datos del reto
    """
    catalog = control['model']
    if prueba == "Rapidez":
        start_time = get_time()
    else:
        tracemalloc.start()
        start_memory = get_memory()

    c = CurrencyConverter()
    # TODO: Realizar la carga de datos
    loadEmployments_types(control["model"])
    loadMultilocations(control["model"])
    loadSkills(control["model"])
    loadJobs(control["model"], c)
    
    
    catalog = control
    sorted_jobs = model.getSortedList(control)
    if prueba == "Rapidez":
        end_time = get_time()
        return control, delta_time(start_time, end_time), prueba, sorted_jobs
    else:
        stop_memory = get_memory()
        tracemalloc.stop()
        A_memory = delta_memory(stop_memory, start_memory)
        return control, A_memory, prueba, sorted_jobs
    #model.add_data_major_structure(control["model"])
    
    
    
def loadEmployments_types(catalog):
    file = cf.data_dir + 'data/'+globalSufijo+'-employments_types.csv'
    
    input_file = csv.DictReader(open(file, encoding='utf-8'), delimiter=";")
    
    for employment_type in input_file:
        fijo = False
        if employment_type["salary_from"] == "" or employment_type["salary_to"] == "":
            promedio_salarial = 0
            fijo = None
        else:
            if float(employment_type["salary_from"]) ==  float(employment_type["salary_to"]):
                fijo = True
            promedio_salarial = (float(employment_type["salary_from"]) + float(employment_type["salary_to"]))/2
        employment_type["fijo"] = fijo
        employment_type["promedio_salarial"] = promedio_salarial
        model.add_data(catalog,"employments_types", employment_type, None)
    return catalog

def loadJobs(catalog,c):
    file = cf.data_dir + 'data/'+globalSufijo+'-jobs.csv'
    input_file = csv.DictReader(open(file, encoding='utf-8'), delimiter=";")
    conteo = 0
    conteo_salario = 0
    for job in input_file:
        #conteo += 1
        if job["city"] == "Poznan" and job["workplace_type"] == "partly_remote":
            conteo +=1 
        
        salario_minimo = 0
        salario_promedio_oferta= 0
        for employment_type in lt.iterator(me.getValue(mp.get(catalog["employments_types"], job["id"]))):
            divisa_oferta = employment_type["currency_salary"]
            promedio_salarial = convertir_divisas(employment_type["promedio_salarial"], employment_type["currency_salary"],c)
            salary_from =  convertir_divisas(employment_type["salary_from"], employment_type["currency_salary"], c)
            salario_promedio_oferta +=  promedio_salarial/lt.size(me.getValue(mp.get(catalog["employments_types"], job["id"])))
            if salary_from != "":
                if salario_minimo == 0:
                    salario_minimo = salary_from
                if salary_from < salario_minimo:
                    salario_minimo = salary_from
        if salario_minimo >= 6900 and salario_minimo <= 7000:
            conteo_salario +=1
        
        model.add_data(catalog,"jobs", job, c)
    #print(f"CONTEOOOOOOOO {conteo}")
    #print(f"CONTEOOOOOOOO SALARIOS {conteo_salario}")
    #    if conteo == 200:
    #        break
    return catalog

def convertir_divisas(salario_a_convertir, divisa, c):
   
    if divisa == "usd":
        return int(salario_a_convertir)
    else:
        if divisa == "":
            return 0
        else:   
            divisa = str.upper(divisa)
            #c= CurrencyConverter()
            #print(c.currencies)
            salario_convertido = c.convert(int(salario_a_convertir), divisa,  'USD')
            #print(salario_a_convertir)
            return salario_convertido

def loadMultilocations(catalog):
    file = cf.data_dir + 'data/'+globalSufijo+'-multilocations.csv'
    input_file = csv.DictReader(open(file, encoding='utf-8'),delimiter=";")
    for multilocation in input_file:
        model.add_data(catalog,"multilocations", multilocation, None)
    return catalog

def loadSkills(catalog):
    file = cf.data_dir + 'data/'+globalSufijo+'-skills.csv'
    input_file = csv.DictReader(open(file, encoding='utf-8'), delimiter=";")
    for skill in input_file:
        model.add_data(catalog,"skills", skill, None)
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


def req_1(control, fecha_inicial, fecha_final):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    global prueba
    prueba=prueba

    if prueba == "Rapidez":
        start_time = get_time()
    else:
        tracemalloc.start()
        start_memory = get_memory()
        
    cantidad_ofertas, total_ofertas , cinco= model.req_1(control["model"]["jobs"], fecha_inicial, fecha_final)
    if prueba == "Almacenamiento":

        stop_memory = get_memory()
        tracemalloc.stop()
        A_memory = delta_memory(stop_memory, start_memory)
        return cantidad_ofertas, total_ofertas , cinco,A_memory,prueba
       
    else:
        
        end_time = get_time()
        return cantidad_ofertas, total_ofertas , cinco , delta_time(start_time, end_time),prueba
    

   


def req_2(control, salario_minimo, salario_maximo):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    start_time = get_time()
    cantidad_ofertas, final, total_ofertas = model.req_2(control["model"]["salaries_offers"], salario_minimo, salario_maximo)
    end_time = get_time()
    time= delta_time(start_time, end_time)
    return cantidad_ofertas, final , time, total_ofertas


def req_3(control,pais,experticia,N):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    start_time = get_time()
    ordenada,size=model.req_3(control["model"],pais,experticia,N)
    end_time = get_time()
    time= delta_time(start_time, end_time)
    return ordenada,size,time


def req_4(control,N, ciudad, ubicacion):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    global prueba
    prueba=prueba

    if prueba == "Rapidez":
        start_time = get_time()
    else:
        tracemalloc.start()
        start_memory = get_memory()
        
    cantidad_ofertas, total_ofertas, cinco = model.req_4(control["model"], N, ciudad, ubicacion)
    if prueba == "Almacenamiento":

        stop_memory = get_memory()
        tracemalloc.stop()
        A_memory = delta_memory(stop_memory, start_memory)
        return cantidad_ofertas, total_ofertas, cinco,A_memory,prueba
       
    else:
        
        end_time = get_time()
        return cantidad_ofertas, total_ofertas, cinco , delta_time(start_time, end_time),prueba
    
        
    #return cantidad_ofertas, ofertas_resultantes, cinco


def req_5(control, numero_ofertas, tamano_minimo_compania,
          tamano_maximo_compania, skill, limite_inferior_skill, limite_superior_skill):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    start_time = get_time()
    cantidad_ofertas, final = model.req_5(control["model"], numero_ofertas, tamano_minimo_compania,
          tamano_maximo_compania, skill, limite_inferior_skill, limite_superior_skill)
    end_time = get_time()
    time= delta_time(start_time, end_time)
    return cantidad_ofertas, final, time

def req_6(control,N,fecha1,fecha2,salario1,salario2):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    start_time = get_time()
    tamaño,lista,ordenada,size=model.req_6(control["model"],N,fecha1,fecha2,salario1,salario2)
    end_time = get_time()
    time= delta_time(start_time, end_time)
    return tamaño,lista,ordenada,size, time
 


def req_7(control, año, codigo_pais, propiedad_conteo, bins):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7
    global prueba
    prueba=prueba

    if prueba == "Rapidez":
        start_time = get_time()
    else:
        tracemalloc.start()
        start_memory = get_memory()
    data_experticia, data_ubicacion, data_habilidad, ofertas_totales, maximo, minimo = model.req_7(control["model"], año, codigo_pais, propiedad_conteo, bins)
    if prueba == "Almacenamiento":

        stop_memory = get_memory()
        tracemalloc.stop()
        A_memory = delta_memory(stop_memory, start_memory)
        
        return data_experticia, data_ubicacion, data_habilidad, ofertas_totales, maximo, minimo,A_memory,prueba
       
    else:
        
        end_time = get_time()
        return data_experticia, data_ubicacion, data_habilidad, ofertas_totales, maximo, minimo, delta_time(start_time, end_time),prueba
    
    
    


def req_8(control,req):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    model.req_8(control["model"] , req)


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
