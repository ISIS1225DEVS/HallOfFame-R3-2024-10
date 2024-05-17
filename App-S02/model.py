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
from tabulate import tabulate
import pandas as pd
import folium
from folium.plugins import MarkerCluster
import matplotlib.pyplot as plt

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
    data_structs = {
        "jobs": None, #va a ser un arrarList con la información de los trabajos como siempre xd
        "fechasJobs": None, #va a ser un árbol binario RBT, donde sus llaves van a ser las fechas, y cada llave va a tener un valor que será un ARRARY_LIST con los id que tienen esa fecha correspondiente
        "jobsId": None, #va a ser una tabla de Hash, donde sus llaves son los IDs y los valores  la información de cada trabajo
        "skillsId": None,
        "employments": None,
        "employmentsId": None,
        "salariosFrom": None, #va a ser un RBT para filtrar los salarios mínimos. Las llaves serán los salarios, y sus valores un ARRAY_LIST con los id que tcumplen con ese salario
        "multilocationsId": None,
        'skills': None
    }
    
    data_structs["jobs"] = lt.newList("ARRAY_LIST")
    
    data_structs["jobsId"] = mp.newMap(
        numelements=375047,
        maptype="PROBING",
        loadfactor=0.6
    )
    
    data_structs["skillsId"] = mp.newMap(
        numelements=1064011,
        maptype="PROBING",
        loadfactor=0.6
    )
    data_structs["employments"] = lt.newList(datastructure="ARRAY_LIST")
    data_structs['skills'] = lt.newList(datastructure='ARRAY_LIST')
    
    data_structs["employmentsId"] = mp.newMap(
        numelements=479549,
        maptype="PROBING",
        loadfactor=0.6
    )
    
    data_structs["multilocationsId"] = mp.newMap(
        numelements=488479,
        maptype="PROBING",
        loadfactor=0.6
    )
    
    data_structs["fechasJobs"] = om.newMap(omaptype="RBT", cmpfunction= orden_fechas)
    data_structs["salariosFrom"] = om.newMap(omaptype="RBT", cmpfunction= orden_salarios)
    
    
    return data_structs

def orden_fechas(fecha1, fecha2):
    # print(fecha1)
    # print(fecha2)
    if fecha1<fecha2:
        # print(-1)
        return -1
    elif fecha1 == fecha2:
        # print(0)
        return 0
    else:
        # print(1)
        return 1
    
def orden_salarios(salario1, salario2):
    salario1= float(salario1)
    salario2=float(salario2)
    if(salario1 <salario2):
        return 1
    elif salario1 == salario2:
        return 0
    else:
        return -1

# Funciones para agregar informacion al modelo

def add_jobs(data_structs, data):
    """
    Función para agregar nuevos elementos a la lista
    """
    #TODO: Crear la función para agregar elementos a una lista
    lt.addLast(data_structs["jobs"], data)
    #voy a guardar adentro de cada mapa, una pareja llave valor, donde la llave es el ID y el valor es el dato total
    mp.put(data_structs["jobsId"], data["id"], data)
    fecha = data['published_at']
    update_published_at(data_structs["fechasJobs"], data)


def update_published_at(map, data): #notese que map es un arbol binario donde se van a guardar las fechas

    entry = om.get(map, data["published_at"][:16])
    if(entry is None):
        lista_con_id = lt.newList("ARRAY_LIST")
        lt.addLast(lista_con_id, data["id"])
        om.put(map, data["published_at"][:16], lista_con_id) #aqui se le está metiendo al arbol binario, con la llave de la fecha de publicacion, el primer id que tiene esa fecha
    else:
        lista_con_id = me.getValue(entry) #note que lista_con_id es el valor de la llave con dicha fecha de publicación
        lt.addLast(lista_con_id, data["id"])
        om.put(map, data["published_at"][:16], lista_con_id)
    

def jobs_size(data_structs):
    return lt.size(data_structs["jobs"])

def add_employments(data_structs, data, forma_de_carga):
    lt.addLast(data_structs["employments"], data)

    if (mp.contains(data_structs["employmentsId"], data["id"]) == False):
        tipo_divisa = data["currency_salary"]
        valor_insertar = data["salary_from"]
        salario_nuevo2 = data["salary_to"]
        if valor_insertar != "":
            if tipo_divisa == "pln":
                valor_insertar = float(convertir_pln(float(valor_insertar)))
                salario_nuevo2 = float(convertir_pln(float(salario_nuevo2)))
            elif tipo_divisa == "eur":
                valor_insertar = float(convertir_eur(float(valor_insertar)))
                salario_nuevo2 = float(convertir_eur(float(salario_nuevo2)))
            elif tipo_divisa == "gbp":
                valor_insertar = float(convertir_gbp(float(valor_insertar)))
                salario_nuevo2 = float(convertir_gbp(float(salario_nuevo2)))
            elif tipo_divisa == 'chf':
                valor_insertar = float(convertir_chf(float(valor_insertar)))
                salario_nuevo2 = float(convertir_chf(float(salario_nuevo2)))
        data["salary_from"] = valor_insertar
        data["salary_to"] = salario_nuevo2
        if forma_de_carga == True:
            data["currency_salary"] = data["currency_salary"] + "x"
        mp.put(data_structs["employmentsId"], data["id"], data)
    else:
        valor_antiguo = me.getValue(mp.get(data_structs["employmentsId"], data["id"]))
        if ((valor_antiguo["salary_from"] != "") and (data["salary_from"] != "")):
            salario_antiguo = float(valor_antiguo["salary_from"])
            
            
            salario_nuevo = data["salary_from"]
            salario_nuevo2 = data["salary_to"]
            tipo_divisa_nuevo = data["currency_salary"]
            if tipo_divisa_nuevo == "pln":
                salario_nuevo = float(convertir_pln(float(salario_nuevo)))
                salario_nuevo2 = float(convertir_pln(float(salario_nuevo2)))
            elif tipo_divisa_nuevo == "eur":
                salario_nuevo = float(convertir_eur(float(salario_nuevo)))
                salario_nuevo2 = float(convertir_eur(float(salario_nuevo2)))
            elif tipo_divisa_nuevo == "gbp":
                salario_nuevo = float(convertir_gbp(float(salario_nuevo)))
                salario_nuevo2 = float(convertir_gbp(float(salario_nuevo2)))
            elif tipo_divisa_nuevo == 'chf':
                salario_nuevo = float(convertir_chf(float(salario_nuevo)))
                salario_nuevo2 = float(convertir_chf(float(salario_nuevo2)))
            data["salary_from"] = salario_nuevo
            data["salary_to"] = salario_nuevo2
            if forma_de_carga == True:
                data["currency_salary"] = data["currency_salary"] + "x"
            if(float(salario_antiguo) > float(salario_nuevo)):
                mp.put(data_structs["employmentsId"], data["id"], data)
        elif valor_antiguo["salary_from"] == "":
            salario_nuevo = data["salary_from"]
            salario_nuevo2 = data["salary_to"]
            tipo_divisa_nuevo = data["currency_salary"]
            if tipo_divisa_nuevo == "pln":
                salario_nuevo = float(convertir_pln(float(salario_nuevo)))
                salario_nuevo2 = float(convertir_pln(float(salario_nuevo2)))
            elif tipo_divisa_nuevo == "eur":
                salario_nuevo = float(convertir_eur(float(salario_nuevo)))
                salario_nuevo2 = float(convertir_eur(float(salario_nuevo2)))
            elif tipo_divisa_nuevo == "gbp":
                salario_nuevo = float(convertir_gbp(float(salario_nuevo)))
                salario_nuevo2 = float(convertir_gbp(float(salario_nuevo2)))
            elif tipo_divisa_nuevo == 'chf':
                salario_nuevo = float(convertir_chf(float(salario_nuevo)))
                salario_nuevo2 = float(convertir_chf(float(salario_nuevo2)))
            data["salary_from"] = salario_nuevo
            data["salary_to"] = salario_nuevo2
            if forma_de_carga == True:
                data["currency_salary"] = data["currency_salary"] + "x"
            mp.put(data_structs["employmentsId"], data["id"], data)
         
    
    if(data["salary_from"] != ""):
        update_salaries(data_structs["salariosFrom"], data)
    
def update_salaries(map, data):
    tipo_divisa = data["currency_salary"]
    valor_insertar = data["salary_from"]
    if tipo_divisa == "pln":
        valor_insertar = float(convertir_pln(float(valor_insertar)))
    elif tipo_divisa == "eur":
        valor_insertar = float(convertir_eur(float(valor_insertar)))
    elif tipo_divisa == "gbp":
        valor_insertar = float(convertir_gbp(float(valor_insertar)))
    elif tipo_divisa == 'chf':
        valor_insertar = float(convertir_chf(float(valor_insertar)))
        
    entry = om.get(map, valor_insertar)
    
    if(entry is None):
        lista_con_id = lt.newList("ARRAY_LIST")
        lt.addLast(lista_con_id, data["id"])
        om.put(map, float(valor_insertar), lista_con_id)
    else:
        lista_con_id = me.getValue(entry)
        lt.addLast(lista_con_id, data["id"])
        om.put(map, float(valor_insertar), lista_con_id)
    return map

def employments_size(data_structs):
    return mp.size(data_structs["employmentsId"])


def add_multilocations(data_structs, data):
    """
    Función para agregar nuevos elementos a la lista
    """
    #TODO: Crear la función para agregar elementos a una lista
    mp.put(data_structs["multilocationsId"], data["id"], data)

def multilocations_size(data_structs):
    return mp.size(data_structs["multilocationsId"])

def add_skills(data_structs, data):
    """
    Función para agregar nuevos elementos a la lista
    """
    #TODO: Crear la función para agregar elementos a una lista
    
    #voy a guardar adentro de cada mapa, una pareja llave valor, donde la llave es el ID y el valor es el dato total
    
    
    
    mp.put(data_structs["skillsId"], data["id"], data) 
    lt.addLast(data_structs['skills'], data )   
    
def skills_size(data_structs):
    return mp.size(data_structs["skillsId"])


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
def convertir_fecha(fecha):
    año = fecha[:4]
    mes = fecha[5:7]
    dia = fecha[8:10]
    if len(fecha) >= 10:
        horas = fecha[11:13]
    else:
        horas = False
    if len(fecha) >= 13:
        minutos = fecha[14:16]
    else:
        minutos = False
    return año, mes, dia, horas, minutos

def cmp_ofertas_by_fecha_y_salario_promedio_descendentemente (oferta1, oferta2):
    """
    Devuelve False si la fecha de la primera oferta es menor.
    Si las ofertas son iguales entonces retorna False si el salario promedio [(salary_from + salary_true) / 2] de la primera oferta es menor.
    De lo contrario retorna True
    
    Es decir que ordena por fecha y salario descendentemente.
    """
    fecha_1 = oferta1["published_at"]
    fecha_2 = oferta2["published_at"]
    
    salario_promedio1 = oferta1["salary_promedio"]
    salario_promedio2 = oferta2["salary_promedio"]
    
    if(fecha_1 < fecha_2):
        return False
    elif fecha_1 == fecha_2:
        if salario_promedio1 < salario_promedio2:
            return False
        else: return True
    else: return True
    
def cmp_ofertas_by_fecha_y_salario_minimo_descendentemente (oferta1, oferta2):
    """
    Devuelve False si la fecha de la primera oferta es menor.
    Si las ofertas son iguales entonces retorna False si el salario minimo de la primera oferta es menor.
    De lo contrario retorna True
    
    Es decir que ordena por fecha y salario descendentemente.
    """
    fecha_1 = oferta1["published_at"]
    fecha_2 = oferta2["published_at"]
    
    salario_min1 = oferta1["salary_from"]
    salario_min2 = oferta2["salary_from"]
    
    if(fecha_1 < fecha_2):
        return False
    elif fecha_1 == fecha_2:
        if salario_min1 < salario_min2:
            return False
        else: return True
    else: return True
    

def cmp_ofertas_by_fecha_y_salario_minimo_descendentemente_req4 (oferta1, oferta2):
    """
    Devuelve False si la fecha de la primera oferta es menor.
    Si las ofertas son iguales entonces retorna False si el salario minimo de la primera oferta es menor.
    De lo contrario retorna True
    
    Es decir que ordena por fecha y salario descendentemente.
    """
    fecha_1 = oferta1["published_at"]
    fecha_2 = oferta2["published_at"]
    
    salario_min1 = oferta1["salary_from"]
    salario_min2 = oferta2["salary_from"]
    
    if(fecha_1 < fecha_2):
        return False
    elif ((fecha_1 == fecha_2) and (salario_min1 != "None") and (salario_min2!= "None")):
        if salario_min1 < salario_min2:
            return False
        else: return True
    else: return True

def req_1(data_structs,fecha_inicial, fecha_final, bono):
   
    jobs_rbt = data_structs["model"]["fechasJobs"]
    jobs_mp = data_structs["model"]["jobsId"]
    employments_mp = data_structs["model"]["employmentsId"]
    mp_skillsId = data_structs["model"]["skillsId"]
    ofertas_om = om.values(jobs_rbt, fecha_inicial, fecha_final)
    ofertas_lst = lt.newList('ARRAY_LIST')
    ofertas_lst2 = lt.newList('ARRAY_LIST')
    ofertas_lst3 = lt.newList('ARRAY_LIST')
    skll_lst = data_structs["model"]["skills"]
    hash_skills_totales = mp.newMap(numelements= 10, maptype= 'PROBING', loadfactor= 0.5)
    
    lst_id = lt.newList("ARRAY_LIST")
    
    ofertas_requisitos = lt.newList("ARRAY_LIST")
    ofertas_requisitos_primeras5 = lt.newList("ARRAY_LIST")
    ofertas_requisitos_ultimas5 = lt.newList("ARRAY_LIST")
    
    for skill in lt.iterator(skll_lst):
        if mp.contains(hash_skills_totales, skill['id']) != True:
            array_skill = lt.newList('ARRAY_LIST')
            lt.addLast(array_skill, skill['name'])
            mp.put(hash_skills_totales, skill['id'], array_skill)
        else:
            array= me.getValue(mp.get(hash_skills_totales, skill['id']))
            lt.addLast(array, skill['name'])
            mp.put(hash_skills_totales, skill['id'], array)
    
    for elem in lt.iterator(ofertas_om):
        for id in lt.iterator(elem):
            lt.addLast(ofertas_lst, id)
    for elem in lt.iterator(ofertas_lst):
        if mp.contains(jobs_mp, elem):
            job = me.getValue(mp.get(jobs_mp, elem))
            if mp.contains(employments_mp, elem):
                job["salary_from"] = me.getValue(mp.get(employments_mp, elem))["salary_from"]
                job["salary_to"] = me.getValue(mp.get(employments_mp, elem))["salary_to"]
                job["habilidades_solicitadas"] = me.getValue(mp.get(hash_skills_totales, id))["elements"]
                if (job["salary_from"] != None and job["salary_to"] != None) and (job["salary_from"] != "" and job["salary_to"] != ""):
                    job["salary_promedio"] = (float(job["salary_from"]) + float(job["salary_to"]))/2
                else: job["salary_promedio"] = 0.0
                if (job["salary_promedio"] == None) or (job["salary_promedio"] == ''):
                    job["salary_promedio"] = 0.0
            lt.addLast(ofertas_lst2, job)
            lt.addLast(lst_id, elem)
    ofertas_lst3 = sa.sort(ofertas_lst2, cmp_ofertas_by_fecha_y_salario_promedio_descendentemente)
    
    n_ofertas = lt.size(ofertas_lst3)
    
    if int(lt.size(ofertas_lst3)) >    10:
        primeras_5 = lt.subList(ofertas_lst3, int(lt.size(ofertas_lst3)) - 5, 5)

        ultimas_5 = lt.subList(ofertas_lst3, 1, 5)

        for oferta in lt.iterator(primeras_5):
            map_ofertas_requisitos_primeras5 = mp.newMap(numelements=19, maptype="PROBING", loadfactor=0.5)
            fecha = me.getValue(mp.get(jobs_mp, oferta["id"]))["published_at"]
            mp.put(map_ofertas_requisitos_primeras5, "fecha", fecha)
            titulo = me.getValue(mp.get(jobs_mp, oferta["id"]))["title"]
            mp.put(map_ofertas_requisitos_primeras5, "titulo", titulo)
            empresa = me.getValue(mp.get(jobs_mp, oferta["id"]))["company_name"]
            mp.put(map_ofertas_requisitos_primeras5, "empresa", empresa)
            experticia = me.getValue(mp.get(jobs_mp, oferta["id"]))["experience_level"]
            mp.put(map_ofertas_requisitos_primeras5, "experticia", experticia)
            pais = me.getValue(mp.get(jobs_mp, oferta["id"]))["country_code"]
            mp.put(map_ofertas_requisitos_primeras5, "pais", pais)
            ciudad = me.getValue(mp.get(jobs_mp, oferta["id"]))["city"]
            mp.put(map_ofertas_requisitos_primeras5, "ciudad", ciudad)
            tamanio = me.getValue(mp.get(jobs_mp, oferta["id"]))["company_size"]
            mp.put(map_ofertas_requisitos_primeras5, "tamanio", tamanio)
            ubicacion = me.getValue(mp.get(jobs_mp, oferta["id"]))["workplace_type"]
            mp.put(map_ofertas_requisitos_primeras5, "ubicacion", ubicacion)
            ucranianos = me.getValue(mp.get(jobs_mp, oferta["id"]))["open_to_hire_ukrainians"]
            mp.put(map_ofertas_requisitos_primeras5, "ucranianos", ucranianos)
            salario_promedio = oferta["salary_promedio"]
            mp.put(map_ofertas_requisitos_primeras5, "salario_promedio", salario_promedio)
            habilidades_solicitadas = oferta["habilidades_solicitadas"]
            mp.put(map_ofertas_requisitos_primeras5, "habilidades_solicitadas", habilidades_solicitadas)
            
            lt.addLast(ofertas_requisitos_primeras5,map_ofertas_requisitos_primeras5)

        for oferta in lt.iterator(ultimas_5):
            map_ofertas_requisitos_ultimas5 = mp.newMap(numelements=7, maptype="PROBING", loadfactor=0.5)
            fecha = me.getValue(mp.get(jobs_mp, oferta["id"]))["published_at"]
            mp.put(map_ofertas_requisitos_ultimas5, "fecha", fecha)
            titulo = me.getValue(mp.get(jobs_mp, oferta["id"]))["title"]
            mp.put(map_ofertas_requisitos_ultimas5, "titulo", titulo)
            empresa = me.getValue(mp.get(jobs_mp, oferta["id"]))["company_name"]
            mp.put(map_ofertas_requisitos_ultimas5, "empresa", empresa)
            experticia = me.getValue(mp.get(jobs_mp, oferta["id"]))["experience_level"]
            mp.put(map_ofertas_requisitos_ultimas5, "experticia", experticia)
            pais = me.getValue(mp.get(jobs_mp, oferta["id"]))["country_code"]
            mp.put(map_ofertas_requisitos_ultimas5, "pais", pais)
            ciudad = me.getValue(mp.get(jobs_mp, oferta["id"]))["city"]
            mp.put(map_ofertas_requisitos_ultimas5, "ciudad", ciudad)
            tamanio = me.getValue(mp.get(jobs_mp, oferta["id"]))["company_size"]
            mp.put(map_ofertas_requisitos_ultimas5, "tamanio", tamanio)
            ubicacion = me.getValue(mp.get(jobs_mp, oferta["id"]))["workplace_type"]
            mp.put(map_ofertas_requisitos_ultimas5, "ubicacion", ubicacion)
            ucranianos = me.getValue(mp.get(jobs_mp, oferta["id"]))["open_to_hire_ukrainians"]
            mp.put(map_ofertas_requisitos_ultimas5, "ucranianos", ucranianos)
            salario_promedio = oferta["salary_promedio"]
            mp.put(map_ofertas_requisitos_ultimas5, "salario_promedio", salario_promedio)
            habilidades_solicitadas = oferta["habilidades_solicitadas"]
            mp.put(map_ofertas_requisitos_ultimas5, "habilidades_solicitadas", habilidades_solicitadas)
            
            lt.addLast(ofertas_requisitos_ultimas5, map_ofertas_requisitos_ultimas5)
    
    else: 
        for oferta in lt.iterator(ofertas_lst3):
            map_ofertas_requisitos = mp.newMap(numelements=7, maptype="PROBING", loadfactor=0.5)
            fecha = me.getValue(mp.get(jobs_mp, oferta["id"]))["published_at"]
            mp.put(map_ofertas_requisitos, "fecha", fecha)
            titulo = me.getValue(mp.get(jobs_mp, oferta["id"]))["title"]
            mp.put(map_ofertas_requisitos, "titulo", titulo)
            empresa = me.getValue(mp.get(jobs_mp, oferta["id"]))["company_name"]
            mp.put(map_ofertas_requisitos, "empresa", empresa)
            experticia = me.getValue(mp.get(jobs_mp, oferta["id"]))["experience_level"]
            mp.put(map_ofertas_requisitos, "experticia", experticia)
            pais = me.getValue(mp.get(jobs_mp, oferta["id"]))["country_code"]
            mp.put(map_ofertas_requisitos, "pais", pais)
            ciudad = me.getValue(mp.get(jobs_mp, oferta["id"]))["city"]
            mp.put(map_ofertas_requisitos, "ciudad", ciudad)
            tamanio = me.getValue(mp.get(jobs_mp, oferta["id"]))["company_size"]
            mp.put(map_ofertas_requisitos, "tamanio", tamanio)
            ubicacion = me.getValue(mp.get(jobs_mp, oferta["id"]))["workplace_type"]
            mp.put(map_ofertas_requisitos, "ubicacion", ubicacion)
            ucranianos = me.getValue(mp.get(jobs_mp, oferta["id"]))["open_to_hire_ukrainians"]
            mp.put(map_ofertas_requisitos, "ucranianos", ucranianos)
            salario_promedio = oferta["salary_promedio"]
            mp.put(map_ofertas_requisitos, "salario_promedio", salario_promedio)
            habilidades_solicitadas = oferta["habilidades_solicitadas"]
            mp.put(map_ofertas_requisitos, "habilidades_solicitadas", habilidades_solicitadas)
            
            lt.addLast(ofertas_requisitos, map_ofertas_requisitos)
    if bono == "si":
        bono_req_1(lst_id, data_structs)        
    if int(lt.size(ofertas_lst3)) > 10:
        return 1 , ofertas_requisitos_primeras5, ofertas_requisitos_ultimas5, n_ofertas
    else: 
        return 2, ofertas_requisitos, 0, n_ofertas 

def bono_req_1(lst, data_structs):
    # lst_id = lt.newList("ARRAY_LIST")
    # for x in lt.iterator(lst):
    #     lt.addLast(lst_id, x["id"])
        
    lista_con_id = lst
    longitud_markers = lt.size(lista_con_id)
    jobs_id = data_structs["model"]["jobsId"]
    
    mapa = folium.Map(location=[19.9449799, 50.0646501], zoom_start=4)
    
    print("Como quiere ver la información? ")
    print("1. Quiere ver únicamente los marcadores \n")
    print("2. Quiere ver agrupadas las ofertas de trabajo \n")
    
    
    opt = int(input("Seleccione una opción: "))
    
    if opt == 1:
        for x in lt.iterator(lista_con_id):
            value = me.getValue(mp.get(jobs_id, x))
            longitude = float(value["longitude"])
            latitude = float(value["latitude"])
            
            folium.Marker([latitude, longitude], popup=value).add_to(mapa)
    elif opt == 2:
        mc = MarkerCluster()
        for y in lt.iterator(lista_con_id):
            value = me.getValue(mp.get(jobs_id, y))
            longitude = float(value["longitude"])
            latitude = float(value["latitude"])
            mc.add_child(folium.Marker([latitude, longitude], popup=value))
        mapa.add_child(mc)

    mapa.save("mapa.html")
 
    
def convertir_pln(salario):
    salario_usd = float(salario)*0.25
    return str(salario_usd)

def convertir_eur(salario):
    salario_usd = float(salario)*1.07
    return str(salario_usd)

def convertir_gbp(salario):
    salario_usd = float(salario)*1.25
    return str(salario_usd)

def convertir_chf(salario):
    salario_usd = float(salario)*1.11
    return str(salario_usd)


def cmp_ofertas_by_salario_minimo(oferta1, oferta2):
    
    if oferta1['salario_min'] == 'Desconocido' or oferta1['salario_min'] == '':
        salario_1 = 0
    else:
        salario_1 = float(oferta1["salario_min"])
    
    if oferta2['salario_min'] == '' or  oferta2['salario_min'] == 'Desconocido':
        salario_2 = 0
    else: 
        salario_2 = float(oferta2["salario_min"])
    
    fecha1 = oferta1["fecha"]
    fecha2 = oferta2["fecha"]
    
    if(salario_1 > salario_2):
        return False
    elif salario_1 == salario_2:
        if fecha1 < fecha2:
            return False
        else: return True
    else: return True

def req_2(data_structs, salario_inf, salario_sup, bono):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    jobs_lst = data_structs["model"]["jobs"]
    employments_mp = data_structs["model"]["employmentsId"]
    rbt_salarios = om.newMap(omaptype="RBT")
    skll_lst = data_structs["model"]["skills"]
    hash_skills_totales = mp.newMap(numelements= 10, maptype= 'PROBING', loadfactor= 0.5)
    rango = lt.newList('ARRAY_LIST')
    
    for skill in lt.iterator(skll_lst):
        if mp.contains(hash_skills_totales, skill['id']) != True:
            array_skill = lt.newList('ARRAY_LIST')
            lt.addLast(array_skill, skill['name'])
            mp.put(hash_skills_totales, skill['id'], array_skill)
        else:
            array= me.getValue(mp.get(hash_skills_totales, skill['id']))
            lt.addLast(array, skill['name'])
            mp.put(hash_skills_totales, skill['id'], array)
    
    for oferta in lt.iterator(jobs_lst):
        id_oferta = oferta['id']
        employments = me.getValue(mp.get(employments_mp, id_oferta))
        
        if employments['salary_from'] == '':
            salario_poner = float(0)
        else:
            salario_poner = float(employments['salary_from'])
        
        if om.contains(rbt_salarios, employments['id']) != True:
            om.put(rbt_salarios, employments['id'], float(salario_poner))
                
        if salario_inf <= float(salario_poner) and float(salario_poner) <= salario_sup:
            lt.addLast(rango, oferta)

    lst = lt.newList('ARRAY_LIST')
    lst_bonos = lt.newList("ARRAY_LIST")
    
    for x in lt.iterator(rango):
        dicc= {'salario_min': '', 'fecha': '', 'titulo': '', 'company': '', 'exp': '', 'pais': '', 'city': '', 'company_size':'', 'workplace': '', 'skill':''}
        idoferta= x['id']
        salary_info = me.getValue(mp.get(rbt_salarios, idoferta))
            
        if salary_info == float(0):
            dicc['salario_min'] = 'Desconocido'
        else:
            dicc['salario_min'] = salary_info

        dicc['fecha']=x["published_at"]
        dicc['titulo']=x["title"]          
        dicc['company']=x["company_name"]
        dicc['exp']=x["experience_level"]
        dicc['pais']=x["country_code"]
        dicc['city']=x["city"]
        dicc['company_size']=x["company_size"]
        dicc['workplace']=x["workplace_type"]
        dicc['skill']=me.getValue(mp.get(hash_skills_totales, idoferta))
        lt.addLast(lst, dicc)
        lt.addLast(lst_bonos, x["id"])
        
    total = lt.size(lst)
    lst_ordenada = sa.sort(lst, cmp_ofertas_by_salario_minimo)
    if bono == 'si':
        bono_req_2(lst_bonos, data_structs)
        return total, lst_ordenada
    else:
        return total, lst_ordenada

def bono_req_2(lst, data_structs):
    lista_con_id = lst
    longitud_markers = lt.size(lista_con_id)
    jobs_id = data_structs["model"]["jobsId"]
    
    mapa = folium.Map(location=[19.9449799, 50.0646501], zoom_start=4)
    
    print("Como quiere ver la información? ")
    print("1. Quiere ver únicamente los marcadores \n")
    print("2. Quiere ver agrupadas las ofertas de trabajo \n")
    
    
    opt = int(input("Seleccione una opción: "))
    
    if opt == 1:
        for x in lt.iterator(lista_con_id):
            value = me.getValue(mp.get(jobs_id, x))
            longitude = float(value["longitude"])
            latitude = float(value["latitude"])
            
            folium.Marker([latitude, longitude], popup=value).add_to(mapa)
    elif opt == 2:
        mc = MarkerCluster()
        for y in lt.iterator(lista_con_id):
            value = me.getValue(mp.get(jobs_id, y))
            longitude = float(value["longitude"])
            latitude = float(value["latitude"])
            mc.add_child(folium.Marker([latitude, longitude], popup=value))
        mapa.add_child(mc)
        
 
    

    
    mapa.save("mapa.html")
    

def req_3(data_structs, n_ofertas, pais, experticia, bono):
    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3
    lst_jobs = data_structs["model"]["jobs"]
    mp_employmentsId = data_structs["model"]["employmentsId"] #mapa con tablas de hash de los emplyments (id,oferta)
    mp_skillsId = data_structs["model"]["skillsId"]
    mp_ofertasId = data_structs["model"]["jobsId"] #mapa con tablas de hash con las ofertas (id,oferta)
    skll_lst = data_structs["model"]["skills"]
    hash_skills_totales = mp.newMap(numelements= 10, maptype= 'PROBING', loadfactor= 0.5)
    
    #Listas a retornar
    ofertas_requisitos = lt.newList("ARRAY_LIST")
    ofertas_requisitos_primeras5 = lt.newList("ARRAY_LIST")
    ofertas_requisitos_ultimas5 = lt.newList("ARRAY_LIST")
    
    for skill in lt.iterator(skll_lst):
        if mp.contains(hash_skills_totales, skill['id']) != True:
            array_skill = lt.newList('ARRAY_LIST')
            lt.addLast(array_skill, skill['name'])
            mp.put(hash_skills_totales, skill['id'], array_skill)
        else:
            array= me.getValue(mp.get(hash_skills_totales, skill['id']))
            lt.addLast(array, skill['name'])
            mp.put(hash_skills_totales, skill['id'], array)
    
    lst_ofertas = lt.newList('ARRAY_LIST')
    for oferta in lt.iterator(lst_jobs):
        if oferta["country_code"] == pais and oferta["experience_level"] == experticia:
            id = oferta["id"]
            job = me.getValue(mp.get(mp_ofertasId, id))
            if mp.contains(mp_employmentsId, id):
                job["salary_from"] = me.getValue(mp.get(mp_employmentsId, id))["salary_from"]
                job["habilidades_solicitadas"] = me.getValue(mp.get(hash_skills_totales, id))["elements"]
                if job["salary_from"] == None or job["salary_from"] == "":
                    job["salary_from"] = 0.0
                else:
                    job["salary_from"] = float(job["salary_from"])
                lt.addLast(lst_ofertas, job)
    
    
    lst_filtro = sa.sort(lst_ofertas, cmp_ofertas_by_fecha_y_salario_minimo_descendentemente)

    # • El número total de ofertas laborales publicadas para un país y que requieran un nivel de experiencia especifico.
    n_ofertas_tot = lt.size(lst_filtro)
    
    if n_ofertas > n_ofertas_tot:
        n_ofertas = n_ofertas_tot
    
    sublst_ofertas = lt.subList(lst_filtro, 1, n_ofertas)
    
    if int(lt.size(sublst_ofertas)) >    10:
        primeras_5 = lt.subList(sublst_ofertas, int(lt.size(sublst_ofertas)) - 5, 5)

        ultimas_5 = lt.subList(sublst_ofertas, 1, 5)

        for oferta in lt.iterator(primeras_5):
            map_ofertas_requisitos_primeras5 = mp.newMap(numelements=19, maptype="PROBING", loadfactor=0.5)
            fecha = me.getValue(mp.get(mp_ofertasId, oferta["id"]))["published_at"]
            mp.put(map_ofertas_requisitos_primeras5, "fecha", fecha)
            titulo = me.getValue(mp.get(mp_ofertasId, oferta["id"]))["title"]
            mp.put(map_ofertas_requisitos_primeras5, "titulo", titulo)
            empresa = me.getValue(mp.get(mp_ofertasId, oferta["id"]))["company_name"]
            mp.put(map_ofertas_requisitos_primeras5, "empresa", empresa)
            experticia = me.getValue(mp.get(mp_ofertasId, oferta["id"]))["experience_level"]
            mp.put(map_ofertas_requisitos_primeras5, "experticia", experticia)
            pais = me.getValue(mp.get(mp_ofertasId, oferta["id"]))["country_code"]
            mp.put(map_ofertas_requisitos_primeras5, "pais", pais)
            ciudad = me.getValue(mp.get(mp_ofertasId, oferta["id"]))["city"]
            mp.put(map_ofertas_requisitos_primeras5, "ciudad", ciudad)
            tamanio = me.getValue(mp.get(mp_ofertasId, oferta["id"]))["company_size"]
            mp.put(map_ofertas_requisitos_primeras5, "tamanio", tamanio)
            ubicacion = me.getValue(mp.get(mp_ofertasId, oferta["id"]))["workplace_type"]
            mp.put(map_ofertas_requisitos_primeras5, "ubicacion", ubicacion)
            salario_min = oferta["salary_from"]
            mp.put(map_ofertas_requisitos_primeras5, "salary_from", salario_min)
            habilidades_solicitadas = oferta["habilidades_solicitadas"]
            mp.put(map_ofertas_requisitos_primeras5, "habilidades_solicitadas", habilidades_solicitadas)
            
            lt.addLast(ofertas_requisitos_primeras5,map_ofertas_requisitos_primeras5)

        for oferta in lt.iterator(ultimas_5):
            map_ofertas_requisitos_ultimas5 = mp.newMap(numelements=7, maptype="PROBING", loadfactor=0.5)
            fecha = me.getValue(mp.get(mp_ofertasId, oferta["id"]))["published_at"]
            mp.put(map_ofertas_requisitos_ultimas5, "fecha", fecha)
            titulo = me.getValue(mp.get(mp_ofertasId, oferta["id"]))["title"]
            mp.put(map_ofertas_requisitos_ultimas5, "titulo", titulo)
            empresa = me.getValue(mp.get(mp_ofertasId, oferta["id"]))["company_name"]
            mp.put(map_ofertas_requisitos_ultimas5, "empresa", empresa)
            experticia = me.getValue(mp.get(mp_ofertasId, oferta["id"]))["experience_level"]
            mp.put(map_ofertas_requisitos_ultimas5, "experticia", experticia)
            pais = me.getValue(mp.get(mp_ofertasId, oferta["id"]))["country_code"]
            mp.put(map_ofertas_requisitos_ultimas5, "pais", pais)
            ciudad = me.getValue(mp.get(mp_ofertasId, oferta["id"]))["city"]
            mp.put(map_ofertas_requisitos_ultimas5, "ciudad", ciudad)
            tamanio = me.getValue(mp.get(mp_ofertasId, oferta["id"]))["company_size"]
            mp.put(map_ofertas_requisitos_ultimas5, "tamanio", tamanio)
            ubicacion = me.getValue(mp.get(mp_ofertasId, oferta["id"]))["workplace_type"]
            mp.put(map_ofertas_requisitos_ultimas5, "ubicacion", ubicacion)
            salario_min = oferta["salary_from"]
            mp.put(map_ofertas_requisitos_ultimas5, "salary_from", salario_min)
            habilidades_solicitadas = oferta["habilidades_solicitadas"]
            mp.put(map_ofertas_requisitos_ultimas5, "habilidades_solicitadas", habilidades_solicitadas)
            
            lt.addLast(ofertas_requisitos_ultimas5, map_ofertas_requisitos_ultimas5)
    
    else: 
        for oferta in lt.iterator(sublst_ofertas):
            map_ofertas_requisitos = mp.newMap(numelements=7, maptype="PROBING", loadfactor=0.5)
            fecha = me.getValue(mp.get(mp_ofertasId, oferta["id"]))["published_at"]
            mp.put(map_ofertas_requisitos, "fecha", fecha)
            titulo = me.getValue(mp.get(mp_ofertasId, oferta["id"]))["title"]
            mp.put(map_ofertas_requisitos, "titulo", titulo)
            empresa = me.getValue(mp.get(mp_ofertasId, oferta["id"]))["company_name"]
            mp.put(map_ofertas_requisitos, "empresa", empresa)
            experticia = me.getValue(mp.get(mp_ofertasId, oferta["id"]))["experience_level"]
            mp.put(map_ofertas_requisitos, "experticia", experticia)
            pais = me.getValue(mp.get(mp_ofertasId, oferta["id"]))["country_code"]
            mp.put(map_ofertas_requisitos, "pais", pais)
            ciudad = me.getValue(mp.get(mp_ofertasId, oferta["id"]))["city"]
            mp.put(map_ofertas_requisitos, "ciudad", ciudad)
            tamanio = me.getValue(mp.get(mp_ofertasId, oferta["id"]))["company_size"]
            mp.put(map_ofertas_requisitos, "tamanio", tamanio)
            ubicacion = me.getValue(mp.get(mp_ofertasId, oferta["id"]))["workplace_type"]
            mp.put(map_ofertas_requisitos, "ubicacion", ubicacion)
            salario_min = oferta["salary_from"]
            mp.put(map_ofertas_requisitos, "salary_from", salario_min)
            habilidades_solicitadas = oferta["habilidades_solicitadas"]
            mp.put(map_ofertas_requisitos, "habilidades_solicitadas", habilidades_solicitadas)
            
            lt.addLast(ofertas_requisitos, map_ofertas_requisitos)
    if bono == "si":
        bono_req3(sublst_ofertas, data_structs)
    if int(lt.size(sublst_ofertas)) > 10:
        return 1 , ofertas_requisitos_primeras5, ofertas_requisitos_ultimas5, n_ofertas_tot
    else: 
        return 2, ofertas_requisitos, 0, n_ofertas_tot
    
        
def bono_req3(lst, data_structs):            
    lista = lst
    lista_con_id = lt.newList("ARRAY_LIST")
    for z in lt.iterator(lista):
        lt.addLast(lista_con_id, z["id"])
    jobs_id = data_structs["model"]["jobsId"]
    
    mapa = folium.Map(location=[19.9449799, 50.0646501], zoom_start=4)
    
    print("Como quiere ver la información? ")
    print("1. Quiere ver únicamente los marcadores \n")
    print("2. Quiere ver agrupadas las ofertas de trabajo \n")
    
    
    opt = int(input("Seleccione una opción: "))
    
    if opt == 1:
        for x in lt.iterator(lista_con_id):
            value = me.getValue(mp.get(jobs_id, x))
            longitude = float(value["longitude"])
            latitude = float(value["latitude"])
            
            folium.Marker([latitude, longitude], popup=value).add_to(mapa)
    elif opt == 2:
        mc = MarkerCluster()
        for y in lt.iterator(lista_con_id):
            value = me.getValue(mp.get(jobs_id, y))
            longitude = float(value["longitude"])
            latitude = float(value["latitude"])
            mc.add_child(folium.Marker([latitude, longitude], popup=value))
        mapa.add_child(mc)
        
    mapa.save("mapa.html")


def req_4(data_structs, cantidad_n, ciudad, ubicacion, ans, ans_2):
    """
    Función que soluciona el requerimiento 4
    """
    # TODO: Realizar el requerimiento 4
    array_jobs = data_structs["model"]["jobs"]
    salarios = data_structs["model"]["employmentsId"]
    habilidades = data_structs["model"]["skillsId"]
    habilidades_extra = data_structs["model"]["skills"]
    
    hash_skills = mp.newMap(numelements=1000, maptype= 'PROBING', loadfactor= 0.5)
    for skill in lt.iterator(habilidades_extra):
        if mp.contains(hash_skills, skill['id']) != True:
            array_skill = lt.newList('ARRAY_LIST')
            lt.addLast(array_skill, skill['name'])
            mp.put(hash_skills, skill['id'], array_skill)
        else:
            array= me.getValue(mp.get(hash_skills, skill['id']))
            lt.addLast(array, skill['name'])
            mp.put(hash_skills, skill['id'], array)
    
    
    filtro = lt.newList("ARRAY_LIST")
    for x in lt.iterator(array_jobs):
        if ((x["city"] == ciudad) and (x["workplace_type"] == ubicacion)):
            id = x["id"]
            if ((me.getValue(mp.get(salarios, id))["salary_from"] == None) or (me.getValue(mp.get(salarios, id))["salary_from"] == "")):
                x["salary_from"] = 0
            else:
                x["salary_from"] = float(me.getValue(mp.get(salarios, id))["salary_from"])
            lt.addLast(filtro, x)
    
    if ans == True and ans_2 == True:
        filtro = sa.sort(filtro, cmp_ofertas_req4_caso1)
    elif ans == True and ans_2 == False:
        filtro = sa.sort(filtro, cmp_ofertas_req4_caso3)
    elif ans == False and ans_2 == True:
        filtro = sa.sort(filtro, cmp_ofertas_req4_caso2)
    elif ans == False and ans_2 == False:
        filtro = sa.sort(filtro, cmp_ofertas_req4_caso4)
        
    cantidad_total = lt.size(filtro)
    if cantidad_n > cantidad_total:
        cantidad_n = cantidad_total
        
    sublista = lt.subList(filtro, 1, cantidad_n)
    
    array_id = lt.newList("ARRAY_LIST")
    array_final = lt.newList("ARRAY_LIST")
    for y in lt.iterator(sublista):
        retorno = {}
        retorno["Fecha"] = y["published_at"]
        retorno["Título"] = y["title"]
        retorno["Empresa"] = y["company_name"]
        retorno["Experiencia"] = y["experience_level"]
        retorno["Ciudad"] = y["city"]
        retorno["Pais"] = y["country_code"]
        retorno["Tamaño"] = y["company_size"]
        retorno["Tipo Ubicacion"] = y["workplace_type"]
        retorno["Salario minimo"] = y["salary_from"]
        retorno["Habilidades solicitadas"] = me.getValue(mp.get(hash_skills, y["id"]))
        lt.addLast(array_final, retorno)
        lt.addLast(array_id, y["id"])
    bono_req4(array_id, data_structs)
    return cantidad_total, array_final

def bono_req4(lst, data_structs):            
    lista_con_id = lst

    jobs_id = data_structs["model"]["jobsId"]
    
    mapa = folium.Map(location=[19.9449799, 50.0646501], zoom_start=4)
    
    print("Como quiere ver la información? ")
    print("1. Quiere ver únicamente los marcadores \n")
    print("2. Quiere ver agrupadas las ofertas de trabajo \n")
    
    
    opt = int(input("Seleccione una opción: "))
    
    if opt == 1:
        for x in lt.iterator(lista_con_id):
            value = me.getValue(mp.get(jobs_id, x))
            longitude = float(value["longitude"])
            latitude = float(value["latitude"])
            
            folium.Marker([latitude, longitude], popup=value).add_to(mapa)
    elif opt == 2:
        mc = MarkerCluster()
        for y in lt.iterator(lista_con_id):
            value = me.getValue(mp.get(jobs_id, y))
            longitude = float(value["longitude"])
            latitude = float(value["latitude"])
            mc.add_child(folium.Marker([latitude, longitude], popup=value))
        mapa.add_child(mc)
        
    mapa.save("mapa.html")
    
    
def req_5(data_structs, n_ofertas, size_inf, size_sup, habilidad, skill_inf, skill_sup, bono):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5
    jobs_lst = data_structs["model"]["jobs"]
    skll_lst = data_structs['model']['skills']
    
    lst_bono = lt.newList("ARRAY_LIST")
    
    #aux skills respuesta
    hash_skill = mp.newMap(numelements=100, maptype= 'PROBING', loadfactor= 0.5)
    #aux total skills por id
    hash_skills_totales = mp.newMap(numelements=100, maptype= 'PROBING', loadfactor= 0.5)
    
    employments_mp = data_structs["model"]["employmentsId"]
    rbt_filtro = om.newMap(omaptype="RBT")
    
    for skill in lt.iterator(skll_lst):
        if mp.contains(hash_skills_totales, skill['id']) != True:
            array_skill = lt.newList('ARRAY_LIST')
            lt.addLast(array_skill, skill['name'])
            mp.put(hash_skills_totales, skill['id'], array_skill)
        else:
            array= me.getValue(mp.get(hash_skills_totales, skill['id']))
            lt.addLast(array, skill['name'])
            mp.put(hash_skills_totales, skill['id'], array)
        
        if skill['name'] == habilidad:
            if skill_inf <= float(skill['level']) and float(skill['level']) <= skill_sup:
                mp.put(hash_skill, skill['id'], 1)
                
    for job in lt.iterator(jobs_lst):
        if job['company_size'] != 'Undefined':
            if size_inf <= float(job['company_size']) and float(job['company_size']) <= size_sup:
                if mp.contains(hash_skill, job['id']) == True:
                    if om.contains(rbt_filtro, job['published_at']) != True:
                        aux = lt.newList('ARRAY_LIST')
                        lt.addLast(aux, job)
                        om.put(rbt_filtro, job['published_at'], aux)
                    else:
                        lt_aux = me.getValue(mp.get(rbt_filtro, job['published_at']))
                        lt.addLast(lt_aux, job)
                        om.put(rbt_filtro, job['published_at'], lt_aux)
    
    total = om.size(rbt_filtro) #Si es menor a la prueba, es porque solo cuenta las ofertas cuya habilidad este en el rango 
    rango = lt.newList('ARRAY_LIST')
    values_lt = om.valueSet(rbt_filtro)
    contador = 0
    
    while contador < int(n_ofertas):
        min = om.minKey(rbt_filtro)
        rec = me.getValue(mp.get(rbt_filtro, min))
        for y in lt.iterator(rec):
            if contador < n_ofertas:
                lt.addLast(rango, y)
                contador += 1
        om.deleteMin(rbt_filtro)
        
    lst  = lt.newList('ARRAY_LIST')
                    
    for oferta in lt.iterator(rango):
        dicc = {'fecha': '', 'titulo': '', 'empresa': '', 'experiencia': '', 'pais': '', 'ciudad': '', 'size_empresa': '', 'ubicacion': '', 'salario_min': '', 'skills': ''}
        dicc['fecha'] = oferta['published_at']
        dicc['titulo'] = oferta['title']
        dicc['empresa'] = oferta['company_name']     
        dicc['experiencia'] = oferta['experience_level']
        dicc['pais'] = oferta['country_code']
        dicc['ciudad'] = oferta['city']
        dicc['size_empresa'] = oferta['company_size']
        dicc['ubicacion'] = oferta['workplace_type']
        idoferta = oferta['id']
        
        salary_info = me.getValue(mp.get(employments_mp, idoferta))
        if salary_info['salary_from'] == '':
            dicc['salario_min'] = 'Desconocido'
        else:
            dicc['salario_min'] = salary_info['salary_from']
        
        dicc['skills'] = me.getValue(mp.get(hash_skills_totales, idoferta))
        lt.addLast(lst, dicc)
        lt.addLast(lst_bono, idoferta)
        
    lst_ordenada = sa.sort(lst, cmp_ofertas_by_fecha_y_salario_minimo_descendentemente_req5)
    if bono == 'si':
        bono_req_5(lst_bono, data_structs)
        return total, lst_ordenada
    else:
        return total, lst_ordenada

def bono_req_5(lst, data_structs):
    lista_con_id = lst
    longitud_markers = lt.size(lista_con_id)
    jobs_id = data_structs["model"]["jobsId"]
    
    mapa = folium.Map(location=[19.9449799, 50.0646501], zoom_start=4)
    
    print("Como quiere ver la información? ")
    print("1. Quiere ver únicamente los marcadores \n")
    print("2. Quiere ver agrupadas las ofertas de trabajo \n")
    
    
    opt = int(input("Seleccione una opción: "))
    
    if opt == 1:
        for x in lt.iterator(lista_con_id):
            value = me.getValue(mp.get(jobs_id, x))
            longitude = float(value["longitude"])
            latitude = float(value["latitude"])
            
            folium.Marker([latitude, longitude], popup=value).add_to(mapa)
    elif opt == 2:
        mc = MarkerCluster()
        for y in lt.iterator(lista_con_id):
            value = me.getValue(mp.get(jobs_id, y))
            longitude = float(value["longitude"])
            latitude = float(value["latitude"])
            mc.add_child(folium.Marker([latitude, longitude], popup=value))
        mapa.add_child(mc)
        
 
    

    
    mapa.save("mapa.html")

def cmp_ofertas_by_fecha_y_salario_minimo_descendentemente_req5 (oferta1, oferta2):
    """
    Devuelve False si la fecha de la primera oferta es menor.
    Si las ofertas son iguales entonces retorna False si el salario minimo de la primera oferta es menor.
    De lo contrario retorna True
    
    Es decir que ordena por fecha y salario descendentemente.
    """
    fecha_1 = oferta1["fecha"]
    fecha_2 = oferta2["fecha"]
    salario1 = oferta1['salario_min']
    if salario1 == '' or salario1 == 'Desconocido':
        salario1 = 0
    salario2 = oferta2['salario_min']
    if salario2 == '' or salario2 == 'Desconocido':
        salario2 = 0          
    
    if(fecha_1 > fecha_2):
        return False
    elif (fecha_1 == fecha_2):
        if float(salario1) < float(salario2):
            return False
        else: return True
    else: return True

def req_6(data_structs, n_ciudades, fecha_inicial, fecha_final, salario_inicial, salario_final, bono):
    """
    Función que soluciona el requerimiento 6
    Los parámetros de entrada de este requerimiento son:
• El número (N) de ciudades a consultar.
• La fecha inicial del periodo a consultar (con formato "%Y-%m-%d").
• La fecha final del periodo a consultar (con formato "%Y-%m-%d").
• El límite inferior del salario mínimo ofertado.
• El límite superior del salario mínimo ofertado.
    """
    # TODO: Realizar el requerimiento 6
    lst_bono = lt.newList("ARRAY_LIST")
    om_fechas = data_structs["model"]["fechasJobs"] #arbol por fechas
    om_salarios = data_structs["model"]["salariosFrom"] #arbol por salarios(minimos)
    mp_ofertasId = data_structs["model"]["jobsId"] #mapa con tablas de hash con las ofertas (id,oferta)
    mp_employmentsId = data_structs["model"]["employmentsId"] #mapa con tablas de hash de los emplyments (id,oferta)
    mp_skillsId = data_structs["model"]["skillsId"]
    mp_ciudades = mp.newMap(numelements=1499, maptype="PROBING") #este mapa va a tener las ciudades sin repetición con su cantidad específica
    lst_ciudades = lt.newList("ARRAY_LIST")
    values_fechas = om.values(om_fechas, fecha_inicial, fecha_final) #single linked list con ids dentro del rango de fechas
    values_salarios = om.values(om_salarios, salario_inicial, salario_final) #single linked list con ids dentro del rango de salarios_min
    skll_lst = data_structs["model"]["skills"]
    hash_skills_totales = mp.newMap(numelements= 10, maptype= 'PROBING', loadfactor= 0.5)
    #Listas a retornar
    ofertas_requisitos = lt.newList("ARRAY_LIST")
    ofertas_requisitos_primeras5 = lt.newList("ARRAY_LIST")
    ofertas_requisitos_ultimas5 = lt.newList("ARRAY_LIST")
    
    #Pasar a tablas de hash las fechas (id,oferta)
    mp_fechas_en_rango = mp.newMap(123457,109345121,'PROBING',0.5)
    
    for skill in lt.iterator(skll_lst):
        if mp.contains(hash_skills_totales, skill['id']) != True:
            array_skill = lt.newList('ARRAY_LIST')
            lt.addLast(array_skill, skill['name'])
            mp.put(hash_skills_totales, skill['id'], array_skill)
        else:
            array= me.getValue(mp.get(hash_skills_totales, skill['id']))
            lt.addLast(array, skill['name'])
            mp.put(hash_skills_totales, skill['id'], array)
    
    for elem in lt.iterator(values_fechas):
        for id in lt.iterator(elem):
            oferta = me.getValue(mp.get(mp_ofertasId, id))
            id = oferta["id"]
            job = me.getValue(mp.get(mp_ofertasId, id))
            if mp.contains(mp_employmentsId, id):
                job["salary_from"] = me.getValue(mp.get(mp_employmentsId, id))["salary_from"]
                job["habilidades_solicitadas"] = me.getValue(mp.get(hash_skills_totales, id))["elements"]
                if job["salary_from"] == None or job["salary_from"] == "":
                    job["salary_from"] = 0.0
                else:
                    job["salary_from"] = float(job["salary_from"])
            mp.put(mp_fechas_en_rango, id, job)
    

    mp_fechas_salarios = mp.newMap(123457,109345121,'PROBING',0.5)
    #Revisa si el id de la oferta en el sango de salarios está en el mapa de las fechas, si no está entonces se borra
    for elem in lt.iterator(values_salarios):
        for id in lt.iterator(elem):
            if mp.contains(mp_fechas_en_rango, id):
                ciudad = me.getValue(mp.get(mp_fechas_en_rango, id))["city"]
                if mp.contains(mp_ciudades, ciudad) == False:
                    mp.put(mp_ciudades,ciudad, 1)
                    lt.addLast(lst_ciudades, ciudad)
                else:
                    cantidad_previa = me.getValue(mp.get(mp_ciudades, ciudad))
                    cantidad_previa += 1
                    mp.put(mp_ciudades, ciudad, cantidad_previa)
                mp.put(mp_fechas_salarios,id,me.getValue(mp.get(mp_fechas_en_rango, id)))
    
    # • El número total de ofertas laborales publicadas entre un par de fechas y que estén en un rango de salario ofertado.
    n_ofertas = mp.size(mp_fechas_en_rango)
    # • Las N ciudades que cumplan las condiciones especificadas ordenadas alfabéticamente.
    ciudades_alfabeticamente = sa.sort(lst_ciudades, cmp_ciudades_alfabeticamente)
    
    array_ciudades_ofertas = lt.newList("ARRAY_LIST")
    for nombre_ciudades in lt.iterator(lst_ciudades):
        cantidad_de_la_ciudad = me.getValue(mp.get(mp_ciudades, nombre_ciudades))
        lt.addLast(array_ciudades_ofertas, {"ciudad": nombre_ciudades, "cantidad": cantidad_de_la_ciudad})
    
    
    ciudades_ordenadas = sa.sort(array_ciudades_ofertas, cmp_function_ordenar_ciudades_con_mas_ofertas_nombres)
    
    if n_ciudades > lt.size(ciudades_ordenadas):
         n_ciudades = lt.size(ciudades_ordenadas)
   # • Las N ciudades que cumplan las condiciones especificadas ordenadas alfabéticamente.
    sublista_de_las_N_ciudades = lt.subList(ciudades_ordenadas, 1, n_ciudades)
    # • El número total de ciudades que cumplan con las especificaciones.
    cantidad_ciudades_requisitos = lt.size(ciudades_ordenadas)
    #Ciudad con mas ofertas
    ciudad_con_mas_ofertas = lt.firstElement(ciudades_ordenadas)["ciudad"]
    
    lst_ofertas = mp.valueSet(mp_fechas_salarios)
    lst_ofertas_final = lt.newList('ARRAY_LIST')
    
    for oferta in lt.iterator(lst_ofertas):
        if oferta["city"] == ciudad_con_mas_ofertas:
            lt.addLast(lst_ofertas_final, oferta)
            lt.addLast(lst_bono, oferta["id"])
    lst_ofertas_final_final = sa.sort(lst_ofertas_final, cmp_ofertas_by_fecha_y_salario_minimo_descendentemente)
    if int(lt.size(lst_ofertas_final_final)) >    10:
        primeras_5 = lt.subList(lst_ofertas_final_final, int(lt.size(lst_ofertas_final_final)) - 5, 5)

        ultimas_5 = lt.subList(lst_ofertas_final_final, 1, 5)

        for oferta in lt.iterator(primeras_5):
            map_ofertas_requisitos_primeras5 = mp.newMap(numelements=19, maptype="PROBING", loadfactor=0.5)
            fecha = me.getValue(mp.get(mp_ofertasId, oferta["id"]))["published_at"]
            mp.put(map_ofertas_requisitos_primeras5, "fecha", fecha)
            titulo = me.getValue(mp.get(mp_ofertasId, oferta["id"]))["title"]
            mp.put(map_ofertas_requisitos_primeras5, "titulo", titulo)
            empresa = me.getValue(mp.get(mp_ofertasId, oferta["id"]))["company_name"]
            mp.put(map_ofertas_requisitos_primeras5, "empresa", empresa)
            experticia = me.getValue(mp.get(mp_ofertasId, oferta["id"]))["experience_level"]
            mp.put(map_ofertas_requisitos_primeras5, "experticia", experticia)
            pais = me.getValue(mp.get(mp_ofertasId, oferta["id"]))["country_code"]
            mp.put(map_ofertas_requisitos_primeras5, "pais", pais)
            ciudad = me.getValue(mp.get(mp_ofertasId, oferta["id"]))["city"]
            mp.put(map_ofertas_requisitos_primeras5, "ciudad", ciudad)
            tamanio = me.getValue(mp.get(mp_ofertasId, oferta["id"]))["company_size"]
            mp.put(map_ofertas_requisitos_primeras5, "tamanio", tamanio)
            ubicacion = me.getValue(mp.get(mp_ofertasId, oferta["id"]))["workplace_type"]
            mp.put(map_ofertas_requisitos_primeras5, "ubicacion", ubicacion)
            salario_min = oferta["salary_from"]
            mp.put(map_ofertas_requisitos_primeras5, "salary_from", salario_min)
            habilidades_solicitadas = oferta["habilidades_solicitadas"]
            mp.put(map_ofertas_requisitos_primeras5, "habilidades_solicitadas", habilidades_solicitadas)
            
            lt.addLast(ofertas_requisitos_primeras5,map_ofertas_requisitos_primeras5)

        for oferta in lt.iterator(ultimas_5):
            map_ofertas_requisitos_ultimas5 = mp.newMap(numelements=7, maptype="PROBING", loadfactor=0.5)
            fecha = me.getValue(mp.get(mp_ofertasId, oferta["id"]))["published_at"]
            mp.put(map_ofertas_requisitos_ultimas5, "fecha", fecha)
            titulo = me.getValue(mp.get(mp_ofertasId, oferta["id"]))["title"]
            mp.put(map_ofertas_requisitos_ultimas5, "titulo", titulo)
            empresa = me.getValue(mp.get(mp_ofertasId, oferta["id"]))["company_name"]
            mp.put(map_ofertas_requisitos_ultimas5, "empresa", empresa)
            experticia = me.getValue(mp.get(mp_ofertasId, oferta["id"]))["experience_level"]
            mp.put(map_ofertas_requisitos_ultimas5, "experticia", experticia)
            pais = me.getValue(mp.get(mp_ofertasId, oferta["id"]))["country_code"]
            mp.put(map_ofertas_requisitos_ultimas5, "pais", pais)
            ciudad = me.getValue(mp.get(mp_ofertasId, oferta["id"]))["city"]
            mp.put(map_ofertas_requisitos_ultimas5, "ciudad", ciudad)
            tamanio = me.getValue(mp.get(mp_ofertasId, oferta["id"]))["company_size"]
            mp.put(map_ofertas_requisitos_ultimas5, "tamanio", tamanio)
            ubicacion = me.getValue(mp.get(mp_ofertasId, oferta["id"]))["workplace_type"]
            mp.put(map_ofertas_requisitos_ultimas5, "ubicacion", ubicacion)
            salario_min = oferta["salary_from"]
            mp.put(map_ofertas_requisitos_ultimas5, "salary_from", salario_min)
            habilidades_solicitadas = oferta["habilidades_solicitadas"]
            mp.put(map_ofertas_requisitos_ultimas5, "habilidades_solicitadas", habilidades_solicitadas)
            
            lt.addLast(ofertas_requisitos_ultimas5, map_ofertas_requisitos_ultimas5)
    
    else: 
        for oferta in lt.iterator(lst_ofertas_final_final):
            map_ofertas_requisitos = mp.newMap(numelements=7, maptype="PROBING", loadfactor=0.5)
            fecha = me.getValue(mp.get(mp_ofertasId, oferta["id"]))["published_at"]
            mp.put(map_ofertas_requisitos, "fecha", fecha)
            titulo = me.getValue(mp.get(mp_ofertasId, oferta["id"]))["title"]
            mp.put(map_ofertas_requisitos, "titulo", titulo)
            empresa = me.getValue(mp.get(mp_ofertasId, oferta["id"]))["company_name"]
            mp.put(map_ofertas_requisitos, "empresa", empresa)
            experticia = me.getValue(mp.get(mp_ofertasId, oferta["id"]))["experience_level"]
            mp.put(map_ofertas_requisitos, "experticia", experticia)
            pais = me.getValue(mp.get(mp_ofertasId, oferta["id"]))["country_code"]
            mp.put(map_ofertas_requisitos, "pais", pais)
            ciudad = me.getValue(mp.get(mp_ofertasId, oferta["id"]))["city"]
            mp.put(map_ofertas_requisitos, "ciudad", ciudad)
            tamanio = me.getValue(mp.get(mp_ofertasId, oferta["id"]))["company_size"]
            mp.put(map_ofertas_requisitos, "tamanio", tamanio)
            ubicacion = me.getValue(mp.get(mp_ofertasId, oferta["id"]))["workplace_type"]
            mp.put(map_ofertas_requisitos, "ubicacion", ubicacion)
            salario_min = oferta["salary_from"]
            mp.put(map_ofertas_requisitos, "salary_from", salario_min)
            habilidades_solicitadas = oferta["habilidades_solicitadas"]
            mp.put(map_ofertas_requisitos, "habilidades_solicitadas", habilidades_solicitadas)
            
            lt.addLast(ofertas_requisitos, map_ofertas_requisitos)
    
    if bono == True:
        bono_req_6(lst_bono, data_structs)
    
    
    if int(lt.size(lst_ofertas_final_final)) > 10:
        return 1 , ofertas_requisitos_primeras5, ofertas_requisitos_ultimas5, n_ofertas, cantidad_ciudades_requisitos, sublista_de_las_N_ciudades
    else: 
        return 2, ofertas_requisitos, 0, n_ofertas, cantidad_ciudades_requisitos, sublista_de_las_N_ciudades
        
    
def bono_req_6(lst, data_structs):
    lista_con_id = lst
    longitud_markers = lt.size(lista_con_id)
    jobs_id = data_structs["model"]["jobsId"]
    
    mapa = folium.Map(location=[19.9449799, 50.0646501], zoom_start=4)
    
    print("Como quiere ver la información? ")
    print("1. Quiere ver únicamente los marcadores \n")
    print("2. Quiere ver agrupadas las ofertas de trabajo \n")
    
    
    opt = int(input("Seleccione una opción: "))
    
    if opt == 1:
        for x in lt.iterator(lista_con_id):
            value = me.getValue(mp.get(jobs_id, x))
            longitude = float(value["longitude"])
            latitude = float(value["latitude"])
            
            folium.Marker([latitude, longitude], popup=value).add_to(mapa)
    elif opt == 2:
        mc = MarkerCluster()
        for y in lt.iterator(lista_con_id):
            value = me.getValue(mp.get(jobs_id, y))
            longitude = float(value["longitude"])
            latitude = float(value["latitude"])
            mc.add_child(folium.Marker([latitude, longitude], popup=value))
        mapa.add_child(mc)
        
 
    

    
    mapa.save("mapa.html")    
    
    
    


def cmp_ciudades_alfabeticamente(ciudad1, ciudad2):
    if ciudad1 < ciudad2:
        return True
    else:
        return False

def cmp_function_ordenar_ciudades_con_mas_ofertas_nombres(dato1, dato2):
    cantidad_1 = dato1["cantidad"]
    cantidad_2 = dato2["cantidad"]
    
    ciudad_1 = dato1["ciudad"]
    ciudad_2 = dato2["ciudad"]
    
    if(cantidad_1 > cantidad_2):
        return True
    elif(cantidad_1 == cantidad_2):
        if(ciudad_1 < ciudad_2):
            return True
        else:
            return False
    else:
        return False
    
    
            


def req_7(data_structs, anio, pais, prop_conteo, bono):
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Realizar el requerimiento 7
    jobs = data_structs["model"]["fechasJobs"]
    jobsId = data_structs["model"]["jobsId"]
    skll_lst = data_structs['model']['skills']
    hash_skills_totales = mp.newMap(numelements= 100, maptype= 'PROBING', loadfactor= 0.5)
    employments_mp = data_structs['model']['employmentsId']
    jobs_anio = om.values(jobs, anio + "-01-01T00:00:00.000Z", anio + "12-31T23:59:59.999Z")
    num_ofertas = 0
    jobs_pais = lt.newList()
    
    for skill in lt.iterator(skll_lst):
        if mp.contains(hash_skills_totales, skill['id']) != True:
            array_skill = lt.newList('ARRAY_LIST')
            lt.addLast(array_skill, skill['name'])
            mp.put(hash_skills_totales, skill['id'], array_skill)
        else:
            array= me.getValue(mp.get(hash_skills_totales, skill['id']))
            lt.addLast(array, skill['name'])
            mp.put(hash_skills_totales, skill['id'], array)
    
    datos = mp.newMap(numelements=100, maptype='PROBING', loadfactor=0.5)
    
    for item in lt.iterator(jobs_anio):
        for job_id in lt.iterator(item):
            job = me.getValue(mp.get(jobsId, job_id))
            num_ofertas += 1
            if job["country_code"] == pais:
                if prop_conteo == 0: #experticia
                    if job["experience_level"] != "":
                        if mp.contains(datos, job['experience_level']) != True:
                            mp.put(datos, job['experience_level'], 1)
                        else:
                            valor = me.getValue(mp.get(datos, job['experience_level']))
                            mp.put(datos, job['experience_level'], valor +1)
                        lt.addLast(jobs_pais, job)
                        
                if prop_conteo == 1: #ubicacion
                    if job["city"] != "":
                        if mp.contains(datos, job['city']) != True:
                            mp.put(datos, job['city'], 1)
                        else:
                            valor = me.getValue(mp.get(datos, job['city']))
                            mp.put(datos, job['city'], valor+1)                            
                        lt.addLast(jobs_pais, job)  
                                        
                if prop_conteo == 2: #habilidad
                    skill_array = me.getValue(mp.get(hash_skills_totales, job["id"]))
                    for habilidad in lt.iterator(skill_array):
                        if mp.contains(datos, habilidad) != True:
                            mp.put(datos, habilidad, 1)
                        else:
                            valor = me.getValue(mp.get(datos, habilidad))
                            mp.put(datos, habilidad, valor +1) 
                    lt.addLast(jobs_pais, job)  
    
    if prop_conteo == 0:
        propiedad = 'Experticia'
        tamanio = 8
    elif prop_conteo == 1:
        propiedad = 'Ubicación'
        tamanio = 8
    elif prop_conteo == 2:
        propiedad = 'Habilidades'
        tamanio = 5
      
    keys_lt = mp.keySet(datos)
    keys = []
    values_lt = mp.valueSet(datos)
    values = []
    for k in lt.iterator(keys_lt):
        keys.append(k)
        
    for v in lt.iterator(values_lt):
        values.append(v)
    
    plt.bar(keys,values)
    
    for i, v in enumerate(values):
        plt.text(i, v + 0.5, str(v), ha='center', va='bottom', fontsize=8)
    
    plt.title('Gráfico de barras por ' + str(propiedad))
    plt.ylabel('Conteo')
    plt.tick_params(axis='x', rotation=90, labelsize=tamanio)
    plt.show()
    
    total_ofertas = lt.size(jobs_pais)
    total_grafico = mp.size(datos)
    ofertas = lt.newList('ARRAY_LIST')
    
    lst_bono = lt.newList("ARRAY_LIST")
    
    for x in lt.iterator(jobs_pais):
        dicc = {'fecha': '', 'titulo': '', 'empresa': '', 'experiencia': '', 'pais': '', 'ciudad': '', 'size_empresa': '', 'salario_min': '', 'propiedad': ''}
        
        idoferta = x['id']
        dicc['fecha'] = x['published_at']
        dicc['titulo'] = x['title']
        dicc['empresa'] = x['company_name']     
        dicc['experiencia'] = x['experience_level']
        dicc['pais'] = x['country_code']
        dicc['ciudad'] = x['city']
        dicc['size_empresa'] = x['company_size']
        salary_info = me.getValue(mp.get(employments_mp, idoferta))
        dicc['salario_min'] = salary_info['salary_from']
        dicc['propiedad'] = propiedad
        lt.addLast(ofertas, dicc)
        lt.addLast(lst_bono, idoferta)
        
    ofertas_ord = sa.sort(ofertas, cmp_ofertas_by_fecha_y_salario_minimo_descendentemente_req5)
    if bono == 'si':
        bono_req_7(lst_bono, data_structs)
        return total_ofertas, total_grafico, ofertas_ord
    else:   
        return total_ofertas, total_grafico, ofertas_ord

def bono_req_7(lst, data_structs):
    lista_con_id = lst
    longitud_markers = lt.size(lista_con_id)
    jobs_id = data_structs["model"]["jobsId"]
    
    mapa = folium.Map(location=[19.9449799, 50.0646501], zoom_start=4)
    
    print("Como quiere ver la información? ")
    print("1. Quiere ver únicamente los marcadores \n")
    print("2. Quiere ver agrupadas las ofertas de trabajo \n")
    
    
    opt = int(input("Seleccione una opción: "))
    
    if opt == 1:
        for x in lt.iterator(lista_con_id):
            value = me.getValue(mp.get(jobs_id, x))
            longitude = float(value["longitude"])
            latitude = float(value["latitude"])
            
            folium.Marker([latitude, longitude], popup=value).add_to(mapa)
    elif opt == 2:
        mc = MarkerCluster()
        for y in lt.iterator(lista_con_id):
            value = me.getValue(mp.get(jobs_id, y))
            longitude = float(value["longitude"])
            latitude = float(value["latitude"])
            mc.add_child(folium.Marker([latitude, longitude], popup=value))
        mapa.add_child(mc)
        
 
    

    
    mapa.save("mapa.html")

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

def imprimir_n(data_structs, pos_inicial, total):
    n = lt.subList(data_structs, pos_inicial, total)
    return n

def sort(data_structs):
    """
    Función encargada de ordenar la lista con los datos
    """
    #TODO: Crear función de ordenamiento
    pass

def cmp_ofertas_by_empresa_y_fecha (oferta1, oferta2):
    """
    Devuelve verdadero (True) si la empresa de la oferta1 es menor que en la
    oferta2,
    en caso de que sean iguales se analiza la fecha de publicación de la oferta
    laboral,
    de lo contrario devuelva falso (False).
    Args:
    oferta1: información de la primera oferta laboral que incluye
    "company_name" y "published_at"
    oferta1: información de la segunda oferta laboral que incluye
    "company_name" y "published_at"
    """
    company_name1 = oferta1["company_name"]
    company_name2 = oferta2["company_name"]
    
    fecha_1 = oferta1["published_at"]
    fecha_2 = oferta2["published_at"]
    

    if(fecha_1 < fecha_2):
        return True
    elif(fecha_1 == fecha_2):
        if(company_name1 < company_name2):
            return True
        else:
            return False
    else:
        return False

def cmp_ofertas_req4_caso1 (oferta1, oferta2):
    """
    Devuelve verdadero (True) si la empresa de la oferta1 es menor que en la
    oferta2,
    en caso de que sean iguales se analiza la fecha de publicación de la oferta
    laboral,
    de lo contrario devuelva falso (False).
    Args:
    oferta1: información de la primera oferta laboral que incluye
    "company_name" y "published_at"
    oferta1: información de la segunda oferta laboral que incluye
    "company_name" y "published_at"
    """
    salary_name1 = float(oferta1["salary_from"])
    salary_name2 = float(oferta2["salary_from"])
    
    fecha_1 = oferta1["published_at"]
    fecha_2 = oferta2["published_at"]
    

    if(fecha_1 < fecha_2):
        return True
    elif(fecha_1 == fecha_2):
        if(salary_name1 < salary_name2):
            return True
        else:
            return False
    else:
        return False

def cmp_ofertas_req4_caso3 (oferta1, oferta2):
    """
    Devuelve verdadero (True) si la empresa de la oferta1 es menor que en la
    oferta2,
    en caso de que sean iguales se analiza la fecha de publicación de la oferta
    laboral,
    de lo contrario devuelva falso (False).
    Args:
    oferta1: información de la primera oferta laboral que incluye
    "company_name" y "published_at"
    oferta1: información de la segunda oferta laboral que incluye
    "company_name" y "published_at"
    """
    salary_name1 = float(oferta1["salary_from"])
    salary_name2 = float(oferta2["salary_from"])
    
    fecha_1 = oferta1["published_at"]
    fecha_2 = oferta2["published_at"]
    

    if(fecha_1 < fecha_2):
        return True
    elif(fecha_1 == fecha_2):
        if(salary_name1 < salary_name2):
            return False
        else:
            return True
    else:
        return False

def cmp_ofertas_req4_caso2 (oferta1, oferta2):
    """
    Devuelve verdadero (True) si la empresa de la oferta1 es menor que en la
    oferta2,
    en caso de que sean iguales se analiza la fecha de publicación de la oferta
    laboral,
    de lo contrario devuelva falso (False).
    Args:
    oferta1: información de la primera oferta laboral que incluye
    "company_name" y "published_at"
    oferta1: información de la segunda oferta laboral que incluye
    "company_name" y "published_at"
    """
    salary_name1 = float(oferta1["salary_from"])
    salary_name2 = float(oferta2["salary_from"])
    
    fecha_1 = oferta1["published_at"]
    fecha_2 = oferta2["published_at"]
    

    if(fecha_1 < fecha_2):
        return False
    elif(fecha_1 == fecha_2):
        if(salary_name1 < salary_name2):
            return True
        else:
            return False
    else:
        return True
    
def cmp_ofertas_req4_caso4 (oferta1, oferta2):
    """
    Devuelve verdadero (True) si la empresa de la oferta1 es menor que en la
    oferta2,
    en caso de que sean iguales se analiza la fecha de publicación de la oferta
    laboral,
    de lo contrario devuelva falso (False).
    Args:
    oferta1: información de la primera oferta laboral que incluye
    "company_name" y "published_at"
    oferta1: información de la segunda oferta laboral que incluye
    "company_name" y "published_at"
    """
    salary_name1 = float(oferta1["salary_from"])
    salary_name2 = float(oferta2["salary_from"])
    
    fecha_1 = oferta1["published_at"]
    fecha_2 = oferta2["published_at"]
    

    if(fecha_1 < fecha_2):
        return False
    elif(fecha_1 == fecha_2):
        if(salary_name1 < salary_name2):
            return False
        else:
            return True
    else:
        return True

def ordenamiento(rta, control):
    if rta == 1:
        lista_ordenada = ins.sort(control, cmp_ofertas_by_empresa_y_fecha)
    elif rta == 2:
        lista_ordenada = merg.sort(control, cmp_ofertas_by_empresa_y_fecha)
    elif rta == 3:
        lista_ordenada = quk.sort(control, cmp_ofertas_by_empresa_y_fecha)
    elif rta == 4:
        lista_ordenada = se.sort(control, cmp_ofertas_by_empresa_y_fecha)
    elif rta == 5:
        lista_ordenada = sa.sort(control, cmp_ofertas_by_empresa_y_fecha)
    return lista_ordenada

def mostrar_en_pantalla(lst):
    
    resultado = []
    tabla = []
    for x in lt.iterator(lst):
        for y in x:
            if(y == "published_at"):
                resultado.append(x["city"])
            if(y == "title"):
                resultado.append(x["published_at"])
            if(y == "company_name"):
                resultado.append(x["experience_level"])
            if(y == "experience_level"):
                resultado.append(x["country_code"])
            if(y == "country_code"):
                resultado.append(x["company_name"])
            if(y == "city"):
                resultado.append(x["title"])
        tabla.append(resultado)
        #print("\n")
        resultado = []
    print(tabulate(tabla, headers=["Fecha", "Título", "Empresa", "Experiencia", "País", "Ciudad"], tablefmt="rounded_grid"))