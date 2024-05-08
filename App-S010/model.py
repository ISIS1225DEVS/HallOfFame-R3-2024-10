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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from datetime import datetime
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.ADT import minpq as mpq
from DISClib.ADT import indexminpq as impq
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import selectionsort as se
from DISClib.Algorithms.Sorting import mergesort as merg
from DISClib.Algorithms.Sorting import quicksort as quk
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""

# Construccion de modelos


def new_data_structs():
    """
    Inicializa las estructuras de datos del modelo. Las crea de
    manera vacía para posteriormente almacenar la información.
    """
    #TODO: Inicializar las estructuras de datos
    data_structs = {'skills':None,
                    'multilocations':None,
                    'employment_types':None,
                    'jobs_fecha':None,
                    'jobs_salary':None,
                    'jobs_nivel_pais':None,
                    'jobs_ciudad':None,
                    'jobs_fecha_salary':None,
                    "mapa_pais" : None
                    }
    
    
    data_structs['jobs_fecha'] = om.newMap(omaptype='RBT')
    data_structs['jobs_salary'] = om.newMap(omaptype='RBT')
    
    data_structs['jobs_tamano'] = om.newMap(omaptype='RBT')
    data_structs['skills'] = mp.newMap(1160000,maptype="PROBING",loadfactor=0.5)
    data_structs['multilocations'] = mp.newMap(1160000,maptype="PROBING",loadfactor=0.5)
    data_structs['employment_types'] = mp.newMap(1160000,maptype="PROBING",loadfactor=0.5)
    data_structs['jobs_ciudad'] = mp.newMap(5000,maptype="PROBING",loadfactor=0.7)
    data_structs['jobs_pais'] = mp.newMap(10000,maptype="PROBING",loadfactor=0.7)
    data_structs['jobs_id'] = mp.newMap(10000,maptype="PROBING",loadfactor=0.7)
    
    data_structs['mapa_pais'] = mp.newMap(maptype="PROBING",loadfactor=0.5)

    

    return data_structs


# Funciones para agregar informacion al modelo
def add_id_skills(data_structs, data):
    if (mp.contains(data_structs['skills'], data['id']))==False:
        lista_nueva = lt.newList(datastructure = 'ARRAY_LIST')
        lt.addLast(lista_nueva,data)
        mp.put(data_structs['skills'], data['id'], lista_nueva)
    else:
        lista = me.getValue(mp.get(data_structs['skills'], data['id']))
        lt.addLast(lista, data)
        mp.put(data_structs['skills'], data['id'], lista)

def add_id_jobs(data_structs, data):
    if (mp.contains(data_structs['jobs_id'], data['id']))==False:
        lista_nueva = lt.newList(datastructure = 'ARRAY_LIST')
        lt.addLast(lista_nueva,data)
        mp.put(data_structs['jobs_id'], data['id'], lista_nueva)
    else:
        lista = me.getValue(mp.get(data_structs['jobs_id'], data['id']))
        lt.addLast(lista, data)
        mp.put(data_structs['jobs_id'], data['id'], lista)


def add_multilocation(data_structs,data):
    id = data['id']
    if mp.contains(data_structs['multilocations'],id):
        valor = mp.get(data_structs['multilocations'],id)
        list = me.getValue(valor)
        lt.addLast(list,data)
        mp.put(data_structs['multilocations'], id,list) 
    else:
        list_id = lt.newList("ARRAY_LIST")
        lt.addLast(list_id,data)
        mp.put(data_structs["multilocations"],id,list_id)
    

def add_employement_types(data_structs,data):
    id = data['id']
    if mp.contains(data_structs['employment_types'],id):
        valor = mp.get(data_structs['employment_types'],id)
        list = me.getValue(valor)
        lt.addLast(list,data)
        mp.put(data_structs['employment_types'], id,list) 
    else:
        list_id = lt.newList("ARRAY_LIST")
        lt.addLast(list_id,data)
        mp.put(data_structs["employment_types"],id,list_id)

def add_country_jobs(data_structs, data):
    """
    Función para agregar nuevos elementos a la lista
    """
    #TODO: Crear la función para agregar elementos a una lista
    if (mp.contains(data_structs['jobs_pais'], data['country_code']))==False:
        lista_nueva = lt.newList(datastructure = 'ARRAY_LIST')
        lt.addLast(lista_nueva,data)
        mp.put(data_structs['jobs_pais'], data['country_code'], lista_nueva)
    else:
        lista = me.getValue(mp.get(data_structs['jobs_pais'], data['country_code']))
        lt.addLast(lista, data)
        mp.put(data_structs['jobs_pais'], data['country_code'], lista)

def add_city_jobs(data_structs, data):
    """
    Función para agregar nuevos elementos a la lista
    """
    #TODO: Crear la función para agregar elementos a una lista
    if (mp.contains(data_structs['jobs_ciudad'], data['city']))==False:
        lista_nueva = lt.newList(datastructure = 'ARRAY_LIST')
        lt.addLast(lista_nueva,data)
        mp.put(data_structs['jobs_ciudad'], data['city'], lista_nueva)
    else:
        lista = me.getValue(mp.get(data_structs['jobs_ciudad'], data['city']))
        lt.addLast(lista, data)
        mp.put(data_structs['jobs_ciudad'], data['city'], lista)

def add_salarios(data_structs, data):
    data['salary_in_usd'] = convert_to_usd(data['salary_from'], data['currency_salary'])
    if not (om.contains(data_structs['jobs_salary'], data['salary_in_usd'])):
        lista_ofertas = lt.newList("ARRAY_LIST")
        lt.addLast(lista_ofertas, data)
        om.put(data_structs['jobs_salary'], data['salary_in_usd'], lista_ofertas)
    else:
        entrada_lista_ofertas = om.get(data_structs['jobs_salary'], data['salary_in_usd'])
        lista_ofertas = me.getValue(entrada_lista_ofertas)
        lt.addLast(lista_ofertas, data)
        om.put(data_structs['jobs_salary'], data['salary_in_usd'], lista_ofertas)

def add_jobs_fecha(data_structs, data):
    """
    Función para agregar nuevos elementos a la lista
    """

    fecha= datetime.strptime(data["published_at"],"%Y-%m-%dT%H:%M:%S.%fZ").date()
    mapa_fechas= data_structs["jobs_fecha"]
    entry= om.get(mapa_fechas,fecha)
    if entry== None:
        lista= lt.newList("ARRAY_LIST")
        om.put(mapa_fechas,fecha,lista)
    else:
        lista=me.getValue(entry)
    lt.addLast(lista,data)

def add_map_country_jobs(data_structs, data):
    hash_pais = data_structs["mapa_pais"]
    if mp.contains(data_structs["mapa_pais"], data["country_code"]) == False:
        mapa_codigo_pais_fecha = om.newMap(omaptype='RBT')
        fecha_en_datetime = datetime.strptime(data["published_at"],"%Y-%m-%dT%H:%M:%S.%fZ")
        lista_ofertas = lt.newList("ARRAY_LIST")
        lt.addLast(lista_ofertas, data)
        om.put(mapa_codigo_pais_fecha, fecha_en_datetime, lista_ofertas)
        mp.put(hash_pais, data["country_code"], mapa_codigo_pais_fecha)
    else:
        entrada_mapa_ya_existente = mp.get(data_structs["mapa_pais"], data["country_code"])
        mapa_ya_existente = me.getValue(entrada_mapa_ya_existente)
        fecha_en_datetime = datetime.strptime(data["published_at"],"%Y-%m-%dT%H:%M:%S.%fZ")

        if not(om.contains(mapa_ya_existente, fecha_en_datetime)):
            lista_ofertas = lt.newList("ARRAY_LIST")
            lt.addLast(lista_ofertas, data)
            om.put(mapa_ya_existente, fecha_en_datetime, lista_ofertas)
        else:
            entrada_lista_ofertas = om.get(mapa_ya_existente, fecha_en_datetime)
            lista_ofertas = me.getValue(entrada_lista_ofertas)
            lt.addLast(lista_ofertas, data)
            om.put(mapa_ya_existente, fecha_en_datetime, lista_ofertas)
        

def add_jobs_tamano(data_structs, data):
    """
    Función para agregar nuevos elementos a la lista
    """

    size = data['company_size']
    if size == "Undefined":
        size = 0
    else:
        size = int(size)
    mapa_size = data_structs["jobs_tamano"]
    entry= om.get(mapa_size,size)
    if entry== None:
        lista= lt.newList()
        om.put(mapa_size,size,lista)
    else:
        lista=me.getValue(entry)
    lt.addLast(lista,data)

     
def add_keys(data_structs, oferta):
    id = oferta['id']
    #print(data_structs['skills'])
    skills = me.getValue(mp.get(data_structs['skills'], id))
    employments = me.getValue(mp.get(data_structs['employment_types'], id))
    multilocations = me.getValue(mp.get(data_structs['multilocations'], id))
    oferta["name_skill"] = []
    oferta["level_skill"] = {}
    for skill in lt.iterator(skills):
        oferta["name_skill"].append(skill['name'])
        oferta["level_skill"][skill["name"]] = skill['level']
    for employment in lt.iterator(employments):
        oferta['salary_min'] = employment['salary_from']
        oferta['salary_max'] = employment['salary_to']
        oferta['type_empl'] = employment['type']
        oferta['currency_salary'] = employment['currency_salary']
        oferta['salary_in_usd'] = convert_to_usd(employment['salary_from'], employment['currency_salary'])
    for multilocation in lt.iterator(multilocations):
        oferta['city_mult'] = multilocation['city']
        oferta['street_mult'] = multilocation['street']

    return oferta

def add_keys_jobs(data_structs, employment):
    id = employment['id']
    jobs = me.getValue(mp.get(data_structs['jobs_id'], id))
    skills = me.getValue(mp.get(data_structs['skills'], id))
    employment["name_skill"] = []
    employment["level_skill"] = {}
    for skill in lt.iterator(skills):
        employment["name_skill"].append(skill['name'])
    for job in lt.iterator(jobs):
        employment['published_at'] = job['published_at']
        employment['titulo'] = job['title']
        employment['nombre_empresa'] = job['company_name']
        employment['experticia'] = job['experience_level']
        employment['pais'] = job['country_code']
        employment['ciudad'] = job['city']
        employment['tamanio_empresa'] = job['company_size']
        employment['ubicacion'] = job['workplace_type']



def info_carga_de_datos(data_structs):
    mapa_fechas= data_structs["jobs_fecha"]
    listas_ofertas= om.values(mapa_fechas,om.minKey(mapa_fechas),om.maxKey(mapa_fechas))
    ofertas= lt.newList()
    for lista in lt.iterator(listas_ofertas):
        for oferta in lt.iterator(lista):
            
            add_keys(data_structs, oferta)
            lt.addLast(ofertas,oferta)
            
    if lt.size(ofertas)>11:
        primeros= lt.subList(ofertas,1,5)
        ultimos=lt.subList(ofertas,lt.size(ofertas)-5,5)
        rta=lt.newList()
        for oferta in lt.iterator(ultimos):
            lt.addLast(rta,oferta)
        for oferta in lt.iterator(primeros):
            lt.addLast(rta,oferta)
        ofertas=rta
    return ofertas


# Funciones para creacion de datos

def new_data(id, info):
    """
    Crea una nueva estructura para modelar los datos
    """
    #TODO: Crear la función para estructurar los datos
    pass


# Funciones de consulta

def get_data(data_structs, id):
    """
    Retorna un dato a partir de su ID
    """
    #TODO: Crear la función para obtener un dato de una lista
    pass


def data_size(data_structs):
    """
    Retorna el tamaño de la lista de datos
    """
    #TODO: Crear la función para obtener el tamaño de una lista
    pass


def req1(data_structs,fecha_i,fecha_f):
    mapa_fechas= data_structs["jobs_fecha"]
    fecha_i= datetime.strptime(fecha_i,"%Y-%m-%d").date()
    fecha_f= datetime.strptime(fecha_f,"%Y-%m-%d").date()

    listas_ofertas= om.values(mapa_fechas,fecha_i,fecha_f)
    tamanio= 0
    ofertas= lt.newList()
    for lista in lt.iterator(listas_ofertas):
        tamanio+=lt.size(lista)
        for oferta in lt.iterator(lista):
            lt.addLast(ofertas,oferta)
    if lt.size(ofertas)>10:
        primeros= lt.subList(ofertas,1,5)
        ultimos=lt.subList(ofertas,lt.size(ofertas)-5,5)
        rta=lt.newList()
        for oferta in lt.iterator(ultimos):
            lt.addLast(rta,oferta)
        for oferta in lt.iterator(primeros):
            lt.addLast(rta,oferta)
        ofertas=rta
    quk.sort(ofertas, compare_Dates)
    return tamanio,ofertas


def convert_to_usd(amount, currency):
    cambio_monedas = {}
    cambio_monedas['eur'] = 1.07
    cambio_monedas['chf'] = 1.10
    cambio_monedas['pln'] = 0.25
    cambio_monedas['gbp'] = 1.35
    cambio_monedas['usd'] = 1.00

    if amount == '' or currency == '':
        amount = 0
        currency = 'usd'
    
    return float(amount) * cambio_monedas[currency]

def req2(data_structs, lim_inf_salary, lim_sup_salary):
    """
    Función que soluciona el requerimiento 2
    """
    mapa_fechas= data_structs["jobs_salary"]
    listas_salarios = om.values(mapa_fechas,lim_inf_salary,lim_sup_salary)
    tamanio= 0
    salarios = lt.newList()
    for lista in lt.iterator(listas_salarios):
        tamanio+=lt.size(lista)
        for salario in lt.iterator(lista):
            add_keys_jobs(data_structs, salario)
            lt.addLast(salarios, salario)
    
    if lt.size(salarios)>11:
        primeros= lt.subList(salarios,1,5)
        ultimos=lt.subList(salarios,lt.size(salarios)-5,5)
        rta=lt.newList()
        for salario in lt.iterator(primeros):
            lt.addLast(rta,salario)
        for salario in lt.iterator(ultimos):
            lt.addLast(rta,salario)
        salarios = rta
    quk.sort(salarios, compareMinSalary)
    return tamanio, salarios
    


def req_3(control,N, country_code, experience_level):
    """
    Función que soluciona el requerimiento 3
    """
    ans = lt.newList('ARRAY_LIST')
    country = control['jobs_pais']
    mapa_country = mp.get(country, country_code)
    if mapa_country:
        lista = me.getValue(mapa_country)      
        for job in lt.iterator(lista):
            add_keys(control,job)
            if job['experience_level'] == experience_level:
                
                dic_respuesta={"published_at":job["published_at"],
                          "título":job["title"],
                          'company_name': job['company_name'],
                          "nivel_experticia":job["experience_level"],
                          "ciudad":job["city"],
                          "pais":job["country_code"],
                          "tamanio":job["company_size"],
                          "tipo_lugar":job["workplace_type"],
                          "salary_in_usd":job["salary_in_usd"],
                          "habilidad": job['name_skill']
                          }
                lt.addLast(ans, dic_respuesta)
                
    quk.sort(ans, compare_Dates)
    if lt.size(ans) <= N:
        ofertas_final = ans
    else:
        ofertas_final = lt.subList(ans, 1, N)
    return ofertas_final
    # TODO: Realizar el requerimiento 3



def req_4(control, N, city, tipo_ubicacion):
    """
    Función que soluciona el requerimiento 4
    """
    ans = lt.newList('ARRAY_LIST')
    ciudad = control['jobs_ciudad']
    mapa_city = mp.get(ciudad, city)
    if mapa_city:
        lista = me.getValue(mapa_city)   
        for job in lt.iterator(lista):
            add_keys(control,job)
            if job['workplace_type'] == tipo_ubicacion:
                
                dic_respuesta={"published_at":job["published_at"],
                          "título":job["title"],
                          'company_name': job['company_name'],
                          "nivel_experticia":job["experience_level"],
                          "ciudad":job["city"],
                          "pais":job["country_code"],
                          "tamanio":job["company_size"],
                          "tipo_lugar":job["workplace_type"],
                          "salary_in_usd":job["salary_in_usd"],
                          "habilidad": job['name_skill']
                          }
                lt.addLast(ans, dic_respuesta)
    quk.sort(ans, compare_Dates)
    if lt.size(ans) <= N:
        ofertas_final = ans
    else:
        ofertas_final = lt.subList(ans, 1, N) 
    return ofertas_final


def req_5(control, N, lim_inf_tam, lim_sup_tam, skill, lim_inf_nh, lim_sup_nh):
    """
    Función que soluciona el requerimiento 5
    """
    mapa_tamano= control["jobs_tamano"]
    
    listas_ofertas= om.values(mapa_tamano,lim_inf_tam,lim_sup_tam)
    tamanio= 0
    ofertas= lt.newList()
    for lista in lt.iterator(listas_ofertas):
        tamanio+=lt.size(lista)
        for oferta in lt.iterator(lista):
            add_keys(control, oferta)
            if skill in oferta["name_skill"]:
                if(oferta['level_skill'][skill] >=lim_inf_nh) and (oferta['level_skill'][skill] <= lim_sup_nh):
                    lt.addLast(ofertas,oferta)
    quk.sort(ofertas, compare_dates)
    if lt.size(ofertas) <= N:
        ofertas_final = ofertas
    else:
        ofertas_final = lt.subList(ofertas, 0, N)
    """if lt.size(ofertas)>10:
        primeros= lt.subList(ofertas,1,5)
        ultimos=lt.subList(ofertas,lt.size(ofertas)-4,5)
        rta=lt.newList()
        for oferta in lt.iterator(primeros):
            lt.addLast(rta,oferta)
        for oferta in lt.iterator(ultimos):
            lt.addLast(rta,oferta)
        ofertas=rta"""
    return tamanio,ofertas_final


def req_6(data_structs,N_ciudades,fecha_i,fecha_f, lim_inf_sal, lim_sup_sal):
    """
    Función que soluciona el requerimiento 6
    """
    mapa_fechas= data_structs["jobs_fecha"]
    
    # TODO: Realizar el requerimiento 6
    fecha_i= datetime.strptime(fecha_i,"%Y-%m-%d").date()
    fecha_f= datetime.strptime(fecha_f,"%Y-%m-%d").date()
    listas_ofertas= om.values(mapa_fechas,fecha_i,fecha_f)
    tamanio= 0
    ofertas= lt.newList()
    for lista in lt.iterator(listas_ofertas):
        tamanio+=lt.size(lista)
        for oferta in lt.iterator(lista):
            add_keys(data_structs, oferta)
            if oferta["salary_in_usd"]>= lim_inf_sal and oferta["salary_in_usd"]<=lim_sup_sal:
                lt.addLast(ofertas,oferta)
    dic_ciudades, mayor_ciudad, numero_ciudades = encontrar_mayor_ciudad(ofertas)
    ciudades = list(dic_ciudades.items())
    ciudades_tad = lt.newList()
    for ciudad in ciudades:
        lt.addLast(ciudades_tad,ciudad)  
    quk.sort(ciudades_tad, compare_ciudades)
    ciudades_mayores = lt.newList("ARRAY_LIST")
    for ciudad in lt.iterator(ciudades_tad):
        N_ciudades-=1
        lt.addLast(ciudades_mayores,ciudad)
        if N_ciudades<=0:
            break
    ans = lt.newList("ARRAY_LIST")
    for oferta in lt.iterator(ofertas):
        if oferta['city'] == mayor_ciudad:
            lt.addLast(ans,oferta)
    if lt.size(ans)>11:
        primeros= lt.subList(ans,1,5)
        ultimos=lt.subList(ans,lt.size(ans)-5,5)
        rta=lt.newList()
        for oferta in lt.iterator(ultimos):
            lt.addLast(rta,oferta)
        for oferta in lt.iterator(primeros):
            lt.addLast(rta,oferta)
        ans=rta
    quk.sort(ans, compare_Dates)
    return tamanio,numero_ciudades,ciudades_mayores, ans

def encontrar_mayor_ciudad(ofertas):
    dic_ciudades = {}
    for job in lt.iterator(ofertas):
        ciudad = job['city']
        if ciudad not in dic_ciudades.keys():
            dic_ciudades[ciudad] = 1
        else:
            dic_ciudades[ciudad]+=1
    numero_ciudades = len(dic_ciudades)
    mayor = 0
    mayor_ciudad = ''
    for ciudad in dic_ciudades:
        if dic_ciudades[ciudad] > mayor:
            mayor = dic_ciudades[ciudad]
            mayor_ciudad = ciudad
    return dic_ciudades, mayor_ciudad, numero_ciudades


def req_7(data_structs, anio, codigo_pais, propiedad):
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Realizar el requerimiento 7
    tipo_propiedad = None
    if propiedad.lower() == "experticia":
        tipo_propiedad = "experticia"
    elif propiedad.lower() == "ubicacion":
        tipo_propiedad = "ubicacion"
    else:
        tipo_propiedad = "habilidad"
    
    entrada_mapa_pais = mp.get(data_structs["mapa_pais"], codigo_pais)
    arbol_pais = me.getValue(entrada_mapa_pais)
    empieza_el_rango = datetime(year=int(anio), month=1, day=1)
    termina_el_rango = datetime(year=int(anio), month=12, day=31)
    lista_ofertas_anio = om.values(arbol_pais, empieza_el_rango, termina_el_rango)
    dicc_ans = {}
    cantidad_ofertas = 0
    
    
    if tipo_propiedad == "experticia":
        dicc_ans["junior"] = lt.newList("ARRAY_LIST")
        dicc_ans["mid"] = lt.newList("ARRAY_LIST")
        dicc_ans["senior"] = lt.newList("ARRAY_LIST")
        lista_variable=lt.newList("ARRAY_LIST")
        for lista_por_fechas in lt.iterator(lista_ofertas_anio):
            for oferta in lt.iterator(lista_por_fechas):
                cantidad_ofertas += 1
                lt.addLast(dicc_ans[oferta["experience_level"]], oferta)
                lt.addLast(lista_variable,oferta)
    elif tipo_propiedad == "ubicacion":
        lista_variable=lt.newList("ARRAY_LIST")
        dicc_ans["remote"] = lt.newList("ARRAY_LIST")
        dicc_ans["partly_remote"] = lt.newList("ARRAY_LIST")
        dicc_ans["office"] = lt.newList("ARRAY_LIST")
        for lista_por_fechas in lt.iterator(lista_ofertas_anio):
            for oferta in lt.iterator(lista_por_fechas):
                cantidad_ofertas += 1
                lt.addLast(dicc_ans[oferta["workplace_type"]], oferta)
                lt.addLast(lista_variable,oferta)
    else:
        for lista_por_fechas in lt.iterator(lista_ofertas_anio):
            for oferta in lt.iterator(lista_por_fechas):
                cantidad_ofertas += 1
                add_keys(data_structs,oferta)
                for habilidad in oferta["name_skill"]:
                    if habilidad in dicc_ans:
                        lt.addLast(dicc_ans[habilidad], oferta)
                        lt.addLast(lista_variable,oferta)
                    else:
                        dicc_ans[habilidad] = lt.newList("ARRAY_LIST")
                        lt.addLast(dicc_ans[habilidad], oferta)
                        lista_variable=lt.newList("ARRAY_LIST")
                        lt.addLast(lista_variable,oferta)
    return dicc_ans, cantidad_ofertas,lista_variable


def req_8(data_structs):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    pass


# Funciones utilizadas para comparar elementos dentro de una lista

def compare(data_1, data_2):
    """
    Función encargada de comparar dos datos
    """
    #TODO: Crear función comparadora de la lista
    pass

def compare_Dates(dicc1,dicc2):
    fecha1 = dicc1["published_at"]
    fecha2 = dicc2["published_at"]
    if fecha1 < fecha2:
        return 0
    elif fecha1 > fecha2:
        return 1
    else:
        if dicc1["salary_in_usd"] != dicc2["salary_in_usd"]:
            return dicc1["salary_in_usd"] > dicc2["salary_in_usd"]

    
def compare_dates(dicc1,dicc2):
    fecha1 = dicc1["published_at"]
    fecha2 = dicc2["published_at"]
    if fecha1 > fecha2:
        return 0
    elif fecha1 < fecha2:
        return 1

def compareDates(fecha1,fecha2):

    if fecha1 < fecha2:
        return 0
    elif fecha1 > fecha2:
        return 1
    return -1

def compare_ciudades(ciudad1,ciudad2):
    ciudad1 = ciudad1[0]
    ciudad2 = ciudad2[0]
    if ciudad1 > ciudad2:
        return 0
    elif ciudad1 < ciudad2:
        return 1
    

def compareMinSalary(dicc1,dicc2):
    if dicc1["salary_in_usd"] != dicc2["salary_in_usd"]:
        return dicc1["salary_in_usd"] < dicc2["salary_in_usd"]
    else:
        fecha1 = dicc1['published_at']
        fecha2 = dicc2['published_at']
        if fecha1 < fecha2:
            return 0
        elif fecha1 > fecha2:
            return 1
# Funciones de ordenamiento


def sort_criteria(data_1, data_2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        data1 (_type_): _description_
        data2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    #TODO: Crear función comparadora para ordenar
    pass


def sort(data_structs):
    """
    Función encargada de ordenar la lista con los datos
    """
    #TODO: Crear función de ordenamiento
    pass
