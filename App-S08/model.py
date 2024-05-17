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
from DISClib.DataStructures import rbtnode as rbt
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import selectionsort as se
from DISClib.Algorithms.Sorting import mergesort as merg
from DISClib.Algorithms.Sorting import quicksort as quk
import folium
assert cf
from folium.plugins import MarkerCluster

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""
usd_usd=1
eur_usd=1.19
gbp_usd=1.26
pln_usd=0.25
chf_usd=1.11
# Construccion de modelos

def new_data_structs():
    """
    Inicializa las estructuras de datos del modelo. Las crea de
    manera vacía para posteriormente almacenar la información.
    """
    #TODO: Inicializar las estructuras de datos
    datos={
        "jobs": None,
        "skills": None,
        "employment": None,
        "multilocation": None
    }
    datos["jobs"]=mp.newMap(10, maptype='PROBING', loadfactor=0.5)
    datos["skills"]=mp.newMap(4, maptype='PROBING', loadfactor=0.5)
    datos["employment"]=mp.newMap(4, maptype='PROBING', loadfactor=0.5)
    datos["multilocation"]=mp.newMap(2, maptype='PROBING', loadfactor=0.5)
    mp.put(datos["jobs"], "jobs-lista", lt.newList("ARRAY_LIST"))
    mp.put(datos["jobs"], "jobs-mapa-id", mp.newMap(34000, maptype='PROBING', loadfactor=0.5))
    mp.put(datos["jobs"], "jobs-mapa-fecha", om.newMap(omaptype='RBT', cmpfunction=comparedate))
    mp.put(datos["jobs"], "jobs-mapa-ciudad", mp.newMap(34000, maptype='PROBING', loadfactor=0.5))
    mp.put(datos["jobs"], "jobs-mapa-pais", mp.newMap(34000, maptype='PROBING', loadfactor=0.5))
    mp.put(datos["jobs"], "jobs-mapa-req3", mp.newMap(100, maptype='PROBING', loadfactor=0.5))
    mp.put(datos["skills"], "skills-mapa-id", mp.newMap(34000, maptype='PROBING', loadfactor=0.5))
    mp.put(datos["skills"], "skills-mapa-skill", mp.newMap(34000, maptype='PROBING', loadfactor=0.5))
    mp.put(datos["employment"], "employment-mapa-ordenado", om.newMap(omaptype='RBT', cmpfunction=comparesalary))
    mp.put(datos["employment"], "employment-mapa-id", mp.newMap(34000, maptype='PROBING', loadfactor=0.5))
    mp.put(datos["multilocation"], "multilocation-mapa-id", mp.newMap(34000, maptype='PROBING', loadfactor=0.5))
    return datos
    
def add_jobs(datos, data):
    """
    Función para agregar nuevos elementos a la lista
    Args:
    lista_jobs_actual: lista de datos actual de los trabajos unicamente
    data: datos a agregar leidos del archivo csv
    Returns:
    lista_jobs_actual: lista de datos actual de los trabajos con los datos agregados
    """
    #TODO: Crear una funcion para arreglar esto mejor
    #Se añaden los datos a las listas que corresponden
    if data["company_size"]=="Undefined":
        tamanio=0
    else:
        tamanio=int(data["company_size"])
    resultado_jobs = new_job(data["title"],
                             data["street"],
                             data["city"],
                             data["country_code"],
                             data["address_text"],
                             data["marker_icon"],
                             data["workplace_type"],
                             data["company_name"],
                             data["company_url"],
                             tamanio,
                             data["experience_level"],
                             data["published_at"],
                             data["remote_interview"],
                             data["open_to_hire_ukrainians"],
                             data["id"], 
                             data["display_offer"],
                             data["latitude"],
                             data["longitude"]
                             )
    lt.addLast(obtener_datos(datos, "jobs-lista"), resultado_jobs)
    
    if mp.get(obtener_datos(datos, "jobs-mapa-id"), data["id"])==None:
        mp.put(obtener_datos(datos, "jobs-mapa-id"), data["id"], resultado_jobs)
    if om.contains(obtener_datos(datos, "jobs-mapa-fecha"), data["published_at"][:10])==False:
        om.put(obtener_datos(datos, "jobs-mapa-fecha"), data["published_at"][:10], lt.newList("ARRAY_LIST"))
    lt.addLast(rbt.getValue(om.get(obtener_datos(datos, "jobs-mapa-fecha"), data["published_at"][:10])), resultado_jobs)
    
    if mp.get(obtener_datos(datos, "jobs-mapa-ciudad"), data["city"])==None:
        mp.put(obtener_datos(datos, "jobs-mapa-ciudad"), data["city"], mp.newMap(6, maptype='PROBING', loadfactor=0.3))
    if mp.get(me.getValue(mp.get(obtener_datos(datos, "jobs-mapa-ciudad"), data["city"])), data["workplace_type"])==None:
        mp.put(me.getValue(mp.get(obtener_datos(datos, "jobs-mapa-ciudad"), data["city"])), data["workplace_type"], lt.newList("ARRAY_LIST"))
    lt.addLast(me.getValue(mp.get(me.getValue(mp.get(obtener_datos(datos, "jobs-mapa-ciudad"), data["city"])), data["workplace_type"])), resultado_jobs)
    
    if mp.get(obtener_datos(datos, "jobs-mapa-pais"), data["country_code"])==None:
        mp.put(obtener_datos(datos, "jobs-mapa-pais"), data["country_code"], lt.newList("ARRAY_LIST"))
        
    if mp.get(obtener_datos(datos, "jobs-mapa-req3"), data["country_code"])==None:
        mp.put(obtener_datos(datos, "jobs-mapa-req3"), data["country_code"], mp.newMap(6, maptype='PROBING', loadfactor=0.3))
    if mp.get(me.getValue(mp.get(obtener_datos(datos, "jobs-mapa-req3"), data["country_code"])), data["experience_level"])==None:
        mp.put(me.getValue(mp.get(obtener_datos(datos, "jobs-mapa-req3"), data["country_code"])), data["experience_level"],lt.newList("ARRAY_LIST"))
    lt.addLast(me.getValue(mp.get(me.getValue(mp.get(obtener_datos(datos, "jobs-mapa-req3"), data["country_code"])), data["experience_level"])), resultado_jobs)
    
    lt.addLast(me.getValue(mp.get(obtener_datos(datos, "jobs-mapa-pais"), data["country_code"])), resultado_jobs)
    
    return datos

def add_skills(datos, data):
    """
    Función para agregar nuevos elementos a la lista
    Args:
    mapa_skills_actual: lista de datos actual de las habilidades unicamente
    data: datos a agregar leidos del archivo csv
    Returns:
    mapa_skills_actual: lista de datos actual de las habilidades con los datos agregados
    """
    #Se añaden los datos a las listas que corresponden
    #Lo mismo anterior pero con otro formato de diccionario
    resultado_skills = new_skill(data["name"], int(data["level"]), data["id"])
    if mp.get(obtener_datos(datos, "skills-mapa-id"), data["id"])==None:
        mp.put(obtener_datos(datos, "skills-mapa-id"), data["id"], lt.newList("ARRAY_LIST"))
    lt.addLast(me.getValue(mp.get(obtener_datos(datos, "skills-mapa-id"), data["id"])), resultado_skills)
    if mp.get(obtener_datos(datos, "skills-mapa-skill"), data["name"])==None:
        mp.put(obtener_datos(datos, "skills-mapa-skill"), data["name"], lt.newList("ARRAY_LIST"))
    lt.addLast(me.getValue(mp.get(obtener_datos(datos, "skills-mapa-skill"), data["name"])), resultado_skills)
    return datos
def add_employments(datos, data):
    #Mismo proceso que skills
   
    if data["salary_from"]!="" or data["salary_to"]!="":
        if data["currency_salary"]!="USD":
            salary_from=conversor_divisas(float(data["salary_from"]), data["currency_salary"])
            salary_to=conversor_divisas(float(data["salary_to"]), data["currency_salary"])
        else:
            salary_from=float(data["salary_from"])
            salary_to=float(data["salary_to"])
    else:
        salary_from=0.0
        salary_to=0.0
    resultado_employments = new_employment_type(data["type"], data["id"], data["currency_salary"], salary_from, salary_to)
    hay_menor_v_1=False
    hay_menor_v_2=False
    if mp.get(obtener_datos(datos, "employment-mapa-id"), data["id"])==None:
        mp.put(obtener_datos(datos, "employment-mapa-id"), data["id"], resultado_employments)
    else:
        valor_mapa=me.getValue(mp.get(obtener_datos(datos, "employment-mapa-id"), data["id"]))
        if valor_mapa["salary_from"]>salary_from:
            hay_menor_v_1=True
        elif valor_mapa["salary_from"]<salary_from:
            hay_menor_v_2=True
    if hay_menor_v_1==True:
        mp.put(obtener_datos(datos, "employment-mapa-id"), data["id"], resultado_employments)
    if hay_menor_v_2==True:
        mp.put(obtener_datos(datos, "employment-mapa-id"), data["id"], valor_mapa)
    """
    hay_menor_v_1=False
    hay_menor_v_2=False
    if mp.get(obtener_datos(datos, "employment-mapa-id"), data["id"])==None:
        mp.put(obtener_datos(datos, "employment-mapa-id"), data["id"], resultado_employments)
    if om.contains(obtener_datos(datos, "employment-mapa-ordenado"), salary_from)==False:
        om.put(obtener_datos(datos, "employment-mapa-ordenado"), salary_from, mp.newMap(1000, maptype='PROBING', loadfactor=0.5))
    mp.put(rbt.getValue(om.get(obtener_datos(datos, "employment-mapa-ordenado"), salary_from)), data["id"],resultado_employments)
    if mp.get(obtener_datos(datos, "employment-mapa-id"), data["id"])!=None:
        valor_mapa=me.getValue(mp.get(obtener_datos(datos, "employment-mapa-id"), data["id"]))
        if valor_mapa["salary_from"]>salary_from:
            hay_menor_v_1=True
        elif valor_mapa["salary_from"]<salary_from:
            hay_menor_v_2=True
    if hay_menor_v_1==True:
        mp.remove(rbt.getValue(om.get(obtener_datos(datos, "employment-mapa-ordenado"), valor_mapa["salary_from"])), valor_mapa["id"])
        mp.put(rbt.getValue(om.get(obtener_datos(datos, "employment-mapa-ordenado"), salary_from)), data["id"], resultado_employments)
        mp.put(obtener_datos(datos, "employment-mapa-id"), data["id"], resultado_employments)
    if hay_menor_v_2==True:
        mp.remove(rbt.getValue(om.get(obtener_datos(datos, "employment-mapa-ordenado"), salary_from)), data["id"])
        mp.put(rbt.getValue(om.get(obtener_datos(datos, "employment-mapa-ordenado"), valor_mapa["salary_from"])), data["id"], valor_mapa)
        mp.put(obtener_datos(datos, "employment-mapa-id"), data["id"], valor_mapa) 
    """
    return datos
def load_employments_types2(datos):
    employments_id=obtener_datos(datos, "employment-mapa-id")
    employments_ordenado=obtener_datos(datos, "employment-mapa-ordenado")
    for i in lt.iterator(mp.keySet(employments_id)):
        salario=me.getValue(mp.get(employments_id, i))["salary_from"]
        if mp.get(employments_id, i)!=None:
            if om.get(employments_ordenado,salario)==None:
                om.put(employments_ordenado, salario, lt.newList("ARRAY_LIST"))
            lt.addLast(rbt.getValue(om.get(employments_ordenado, salario)), me.getValue(mp.get(employments_id, i)))
    return datos
def add_multilocation(datos, data):
    """
    Función para agregar nuevos elementos a la lista
    Args:
    lista_multilocation: lista de datos actual de las habilidades unicamente
    data: datos a agregar leídos del archivo csv
    Returns:
    lista_multilocation: lista de datos actual de las habilidades con los datos agregados
    """
    #Mismo proceso de skill
    #Se añaden los datos a las listas que corresponden
    resultado_multilocation = new_multilocation(data["city"], data["street"], data["id"])
    if mp.get(obtener_datos(datos,"multilocation-mapa-id"), data["id"])==None:
        mp.put(obtener_datos(datos,"multilocation-mapa-id"), data["id"], lt.newList("ARRAY_LIST"))
    lt.addLast(me.getValue(mp.get(obtener_datos(datos,"multilocation-mapa-id"), data["id"])), resultado_multilocation)   
    return datos
def sort_jobs(lista_jobs):
    """
    Función para ordenar los trabajos por fecha de publicación
    Args:
    lista_jobs: lista de trabajos a ordenar
    Returns:
    lista_jobs: lista de trabajos ordenada
    """
    merg.sort(lista_jobs, sort_dates)
    return lista_jobs
def new_job(title,street,city,country_code,address_text,marker_icon,workplace_type,company_name, company_url, company_size, experience_level, published_at, remote_interview, open_to_hire_ukranians, id_job, display_offer, latitude, longitude):
    """
    Crea una nueva estructura para modelar los datos
    """
    job = {
        "title": title,
        "street": street,
        "city": city,
        "country_code": country_code,
        "address_text": address_text,
        "marker_icon": marker_icon,
        "workplace_type": workplace_type,
        "company_name": company_name,
        "company_url": company_url,
        "company_size": company_size,
        "experience_level": experience_level,
        "published_at": published_at,
        "remote_interview": remote_interview,
        "open_to_hire_ukrainians": open_to_hire_ukranians,
        "id": id_job,
        "display_offer": display_offer,
        "latitude": latitude,
        "longitude": longitude
    }
    return job

def new_skill(name, level, id_job):
    """
    Crea una nueva estructura para modelar los datos
    """
    skill = {
        "name": name,
        "level": level,
        "id": id_job
    }
    return skill

def new_employment_type(type, id, currency_salary, salary_from, salary_to):
    employment = {
        "type": type,
        "id": id,
        "currency_salary": currency_salary,
        "salary_from": salary_from,
        "salary_to": salary_to
    }
    return employment

def new_multilocation(city, street, id):
    multilocation = {
        "city": city,
        "street": street,
        "id": id
    }
    return multilocation
def sort_dates(fecha_1:int, fecha_2:int):
    """
    Función encargada de comparar dos fechas
    """
    fechas1=fecha_1["published_at"]
    fechas2=fecha_2["published_at"]
    return fechas1>fechas2

def obtener_datos(datos:dict, seleccion:str):
    """Función para obtener los datos de la estructura de datos
    Posibles selecciones:
    - jobs-lista - Lista de trabajos en formato array
    - jobs-mapa-id - Mapa de trabajos por id en formato probing
    - jobs-mapa-fecha - Mapa de trabajos por fecha en formato rbt con llave %YYYY-%MM-%DD 
    - jobs-mapa-ciudad - Mapa de trabajos por ciudad en formato probing
    - jobs-mapa-pais - Mapa de trabajos por pais en formato probing
    - skills-mapa-id - Mapa de habilidades por id en formato probing
    - skills-mapa-skill - Mapa de habilidades por skill en formato probing
    - employment-mapa-ordenado - Mapa de empleos por salario en formato rbt
    - employment-mapa-id - Mapa de empleos por id en formato probing
    - multilocation-mapa-id - Mapa de multilocalizaciones por id en formato probing

    Args:
        datos (dict): _description_
        seleccion (str): _description_

    Returns:
        _type_: _description_
    """
    
    if seleccion == "jobs-lista":
        return me.getValue(mp.get(datos["jobs"], "jobs-lista"))
    elif seleccion == "jobs-mapa-id":
        return me.getValue(mp.get(datos["jobs"], "jobs-mapa-id"))
    elif seleccion == "jobs-mapa-fecha":
        return rbt.getValue(om.get(datos["jobs"], "jobs-mapa-fecha"))
    elif seleccion == "jobs-mapa-ciudad":
        return me.getValue(mp.get(datos["jobs"], "jobs-mapa-ciudad"))
    elif seleccion == "jobs-mapa-pais":
        return me.getValue(mp.get(datos["jobs"], "jobs-mapa-pais"))
    elif seleccion == "skills-mapa-id":
        return me.getValue(mp.get(datos["skills"], "skills-mapa-id"))
    elif seleccion == "skills-mapa-skill":
        return me.getValue(mp.get(datos["skills"], "skills-mapa-skill"))
    elif seleccion == "employment-mapa-ordenado":
        return rbt.getValue(om.get(datos["employment"], "employment-mapa-ordenado"))
    elif seleccion == "employment-mapa-id":
        return me.getValue(mp.get(datos["employment"], "employment-mapa-id"))
    elif seleccion == "multilocation-mapa-id":
        return me.getValue(mp.get(datos["multilocation"], "multilocation-mapa-id"))
    elif seleccion == "jobs-mapa-req3":
        return me.getValue(mp.get(datos["jobs"], "jobs-mapa-req3"))
    else:
        print("No se encontró la selección")
        return None
    
def comparedate(data1, data2):
    if data1 == data2:
        return 0
    elif data1 > data2:
        return 1
    else:
        return -1
def comparesalary(data1, data2):
    if data1 == data2:
        return 0
    elif data1 > data2:
        return 1
    else:
        return -1
# Funciones para agregar informacion al modelo
def conversor_divisas(salary, divisa):
    if divisa.lower() == "usd":
        return salary * usd_usd
    elif divisa.lower() == "eur":
        return salary * eur_usd
    elif divisa.lower() == "gbp":
        return salary * gbp_usd
    elif divisa.lower() == "pln":
        return salary * pln_usd
    elif divisa.lower() == "chf":
        return salary * chf_usd
    else:
        return None


def req_1(datos, fecha_inicio, fecha_fin):
    """
    Función que soluciona el requerimiento 1
    """
    lista_final=lt.newList("ARRAY_LIST")
    habilidades=obtener_datos(datos, "skills-mapa-id")
    valores=om.values(obtener_datos(datos, "jobs-mapa-fecha"), fecha_inicio, fecha_fin)
    salario=obtener_datos(datos, "employment-mapa-id")
    for i in lt.iterator(valores):
        for j in lt.iterator(i):
            lista_habilidades=me.getValue(mp.get(habilidades, j["id"]))
            habilidades_id=""
            for k in lt.iterator(lista_habilidades):
                if lt.size(lista_habilidades)==1:
                    habilidades_id+=k["name"]
                else:
                    habilidades_id+=k["name"]+", "
            lt.addLast(lista_final, (j["published_at"],
                                    j["title"],
                                    j["company_name"],
                                    j["experience_level"],
                                    j["country_code"],
                                    j["city"],
                                    j["company_size"],
                                    j["workplace_type"],
                                    habilidades_id,
                                    me.getValue(mp.get(salario, j["id"]))["salary_from"],
                                    float(j["latitude"]),
                                    float(j["longitude"])))
    merg.sort(lista_final, sort_date_req1)
    return lista_final, lt.size(lista_final)

def sort_date_req1(data_1, data_2):
    """
    Función encargada de comparar dos fechas
    """
    if data_1[0] == data_2[0]:
        if data_1[9]>data_2[9]:
            return True
        else:
            return False
    elif data_1[0] > data_2[0]:
        return True
    else:
        return False

def req_2(datos, minimo_salario, maximo_salario):
    """
    Función que soluciona el requerimiento 2
    """
    lista_final=lt.newList("ARRAY_LIST")
    empleos=obtener_datos(datos, "employment-mapa-ordenado")
    valores=om.values(empleos, minimo_salario, maximo_salario)
    for i in lt.iterator(valores):
        for j in lt.iterator(i):
            lista_habilidades=me.getValue(mp.get(obtener_datos(datos, "skills-mapa-id"), j["id"]))
            habilidades_id=""
            salarios=me.getValue(mp.get(obtener_datos(datos, "employment-mapa-id"), j["id"]))
            for k in lt.iterator(lista_habilidades):
                if lt.size(lista_habilidades)==1:
                    habilidades_id+=k["name"]
                else:
                    habilidades_id+=k["name"]+", "
            info_trabajo=me.getValue(mp.get(obtener_datos(datos, "jobs-mapa-id"), j["id"]))
            lt.addLast(lista_final, (info_trabajo["published_at"],
                                    info_trabajo["title"],
                                    info_trabajo["company_name"],
                                    info_trabajo["experience_level"],
                                    info_trabajo["country_code"],
                                    info_trabajo["city"],
                                    info_trabajo["company_size"],
                                    info_trabajo["workplace_type"],
                                    habilidades_id,
                                    salarios["salary_from"],
                                    float(info_trabajo["latitude"]),
                                    float(info_trabajo["longitude"])))
    merg.sort(lista_final, sort_date_req2)
    return lista_final, lt.size(lista_final)
def sort_date_req2(data_1, data_2):
    """
    Función encargada de comparar dos fechas
    """
    if data_1[9] > data_2[9]:
        return True
    elif data_1[9] ==data_2[9]:
        if data_1[0]>data_2[0]:
            return True
        else:
            return False
    else:
        return False


def req_3(datos, n, cod_pais, nivel_exp):
    """
    Función que soluciona el requerimiento 3
    """
    # Crea una nueva lista vacía 
    rta = lt.newList("ARRAY_LIST")
    # Obtiene el mapa de trabajos por país desde los datos
    mapa_trabajos = obtener_datos(datos, "jobs-mapa-req3")
    # Obtiene la lista de trabajos para el país especificado
    lista_trabajos = me.getValue(mp.get(me.getValue(mp.get(mapa_trabajos, cod_pais)), nivel_exp))
    # Obtiene el total de ofertas de trabajo para el país
    total_ofertas = lt.size(lista_trabajos)
    #se obtiene mapa de habilidades
    for i in lt.iterator(lista_trabajos):
            lista_habilidades=me.getValue(mp.get(obtener_datos(datos, "skills-mapa-id"), i["id"]))
            habilidades_id=""
            for k in lt.iterator(lista_habilidades):
                if lt.size(lista_habilidades)==1:
                    habilidades_id+=k["name"]
                else:
                    habilidades_id+=k["name"]+", "
            # Verifica si el nivel de experiencia del trabajo coincide con el nivel especificado
            if nivel_exp == i["experience_level"]:
                # Obtiene los datos de salario para el trabajo actual
                salarios = me.getValue(mp.get(obtener_datos(datos, "employment-mapa-id"), i["id"]))
                # Agrega una tupla con los datos del trabajo y el salario a la lista de respuesta
                lt.addLast(rta, (i["published_at"] if i["published_at"] else "Desconocido",
                                i["title"] if i["title"] else "Desconocido",
                                i["company_name"] if i["company_name"] else "Desconocido",
                                i["experience_level"] if i["experience_level"] else "Desconocido",
                                i["country_code"] if i["country_code"] else "Desconocido",
                                i["city"] if i["city"] else "Desconocido",
                                i["company_size"] if i["company_size"] else "Desconocido",
                                i["workplace_type"] if i["workplace_type"] else "Desconocido",
                                habilidades_id,
                                salarios["salary_from"] if salarios and salarios["salary_from"] else 0.0,
                                float(i["latitude"]),
                                float(i["longitude"])))


    # Ordena la lista de respuesta por fecha de publicación y salarios
    merg.sort(rta, sort_date_and_salary)

    # Crea una sublista de la lista de respuesta con los primeros n elementos
    lista_nueva = lt.subList(rta, 1, n)

    return lista_nueva, lt.size(lista_nueva), total_ofertas

def sort_date_and_salary(data_1, data_2):
    """
    Función encargada de comparar dos fechas y salarios
    """
    if data_1[0] == data_2[0]: 
        if data_1[9] > data_2[9]:  
            return True
        else:
            return False
    elif data_1[0] > data_2[0]:  
        return True
    else:
        return False


def req_4(data_structs, n_ofertas, ciudad, tipo):
    """
    Función que soluciona el requerimiento 4
    """
    #Se obtiene mapa de trabajos
    mapa_trabajos=obtener_datos(data_structs, "jobs-mapa-ciudad")
    if mp.get(mapa_trabajos,ciudad) == None:
        return None
    lista_trabajos=me.getValue(mp.get(me.getValue(mp.get(mapa_trabajos,ciudad)),tipo))
     #Se obtiene el mapa de salarios
    mapa_salarios=obtener_datos(data_structs, "employment-mapa-id")
    #se obtiene mapa de habilidades
    mapa_habilidades=obtener_datos(data_structs, "skills-mapa-id")
    lista_nueva=lt.newList('ARRAY_LIST')
    lista_reducida=lt.newList('ARRAY_LIST')
    for i in lt.iterator(lista_trabajos):
        if  i["workplace_type"] ==tipo:
            habilidades_id=""
            informacion_trabajo= i
            habilidades=me.getValue(mp.get(mapa_habilidades, i["id"]))
            for i in lt.iterator(habilidades):
                    #Si la habilidad es la única, se agrega sin coma
                    if lt.size(habilidades)==1:
                        habilidades_id+=i["name"]
                    else:
                        habilidades_id+=i["name"]+", "
            valor_salario=me.getValue(mp.get(mapa_salarios, i["id"]))["salary_from"]
            lt.addLast(lista_nueva, (informacion_trabajo["published_at"],
                                         informacion_trabajo["title"],
                                         informacion_trabajo["company_name"],
                                         informacion_trabajo["experience_level"],
                                         informacion_trabajo["country_code"],
                                         informacion_trabajo["city"],
                                         informacion_trabajo["company_size"],
                                         informacion_trabajo["workplace_type"],
                                         habilidades_id,
                                         valor_salario,
                                         informacion_trabajo["latitude"],
                                         informacion_trabajo["longitude"]))
    merg.sort(lista_nueva, cmp_ofertas_by_fecha_y_salario)
    if lt.size(lista_nueva) < n_ofertas:
        n_ofertas= lt.size(lista_nueva)
    lista_reducida= lt.subList(lista_nueva,1,n_ofertas)
    todo=lt.size(lista_trabajos)
    return lista_reducida,todo

def cmp_ofertas_by_fecha_y_salario(oferta1, oferta2):
    """
    Devuelve verdadero (True) si la fecha de la oferta 1 es menor que en la oferta ,
    en caso de que sean iguales se analiza el salario de la oferta laboral, de lo contrario devuelva Falso

    Args:
        oferta1: información de la primera oferta laboral que incluye "salary_from" y "published_at"
        oferta2: información de la segunda oferta laboral que incluye "salary_from" y "published_at"
    """
    salario1= oferta1[8]
    salario2= oferta2[8]
    fecha1= oferta1[0]
    fecha2= oferta2[0]
    return (fecha1>fecha2) or (fecha1 == fecha2 and salario1 > salario2)


def req_5(control, numero_ofertas, tamanio_minimo, tamanio_maximo, habilidades, nivel_habilidad_minimo, nivel_habilidad_maximo):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento
    #Se obtiene el mapa de habilidades 
    mapa_habilidades=obtener_datos(control, "skills-mapa-skill")
    #Se obtiene la lista de trabajos
    mapa_trabajos=obtener_datos(control, "jobs-mapa-id")
    #Se obtiene la lista de habilidades a partir de la habilidad ingresada
    lista_habilidad=me.getValue(mp.get(mapa_habilidades, habilidades))
    #Se obtiene el mapa de salarios
    mapa_salarios=obtener_datos(control, "employment-mapa-id")
    #Se crea una lista vacía para almacenar los trabajos que cumplen con los requisitos
    lista_final=lt.newList("ARRAY_LIST")
    #Se recorre la lista de habilidades
    for i in lt.iterator(lista_habilidad):
        #Si el nivel de habilidad está en el rango ingresado, continua
        if i["level"]>=nivel_habilidad_minimo and i["level"]<=nivel_habilidad_maximo:
            #Se obtiene la información del trabajo a partir del id de la habilidad
            informacion_trabajo=me.getValue(mp.get(mapa_trabajos, i["id"]))
            #Si el tamaño de la empresa está en el rango ingresado, continua
            if informacion_trabajo["company_size"]>=tamanio_minimo and informacion_trabajo["company_size"]<=tamanio_maximo:
                #Se obtiene la lista de los posibles salarios del trabajo
                valor_salario=me.getValue(mp.get(mapa_salarios, i["id"]))["salary_from"]
                #Se inicializa el valor del salario en un número muy grande
                
                mapa_habilidades_id=obtener_datos(control, "skills-mapa-id")
                #Se obtiene la lista de habilidades a partir del id del trabajo
                lista_habilidades_id=me.getValue(mp.get(mapa_habilidades_id, i["id"]))
                #Se inicializa un string vacío para almacenar las habilidades
                habilidades_id=""
                #Se recorre la lista de habilidades de dicho trabajo
                for i in lt.iterator(lista_habilidades_id):
                    #Si la habilidad es la única, se agrega sin coma
                    if lt.size(lista_habilidades_id)==1:
                        habilidades_id+=i["name"]
                    else:
                        habilidades_id+=i["name"]+", "
                #Se añade la información del trabajo a la lista final
                lt.addLast(lista_final, (informacion_trabajo["published_at"],
                                         informacion_trabajo["title"],
                                         informacion_trabajo["company_name"],
                                         informacion_trabajo["experience_level"],
                                         informacion_trabajo["country_code"],
                                         informacion_trabajo["city"],
                                         informacion_trabajo["company_size"],
                                         informacion_trabajo["workplace_type"],
                                         habilidades_id,
                                         valor_salario,
                                         informacion_trabajo["latitude"],
                                         informacion_trabajo["longitude"]))
    #Se ordena la lista final por fecha de publicación
    merg.sort(lista_final, sort_dates_desc)
    if numero_ofertas>lt.size(lista_final):
        numero_ofertas=lt.size(lista_final)   
    sublista=lt.subList(lista_final, 1, numero_ofertas)
    return sublista,lt.size(lista_final)


def req_6(data_structs, numero_ciudades, fecha_inicio, fecha_fin, salario_minimo, salario_maximo):
    """
    Función que soluciona el requerimiento 6
    """
    #Obtiene las estructuras por fecha, salario, id
    jobs_fecha=obtener_datos(data_structs, "jobs-mapa-fecha")
    salarios=obtener_datos(data_structs, "employment-mapa-ordenado")
    salarios_id=obtener_datos(data_structs, "employment-mapa-id")
    #Crea las estructuras de datos necesarias
    ciudades=om.newMap(omaptype='RBT', cmpfunction=compare_city_req6)
    ciudades_jobs=mp.newMap(200, maptype='PROBING', loadfactor=0.5)
    cantidad=0
    #Arreglar cantidades con filtros exagerados
    if lt.size(om.values(jobs_fecha, fecha_inicio, fecha_fin))<lt.size(om.values(salarios, salario_minimo, salario_maximo)):
        for i in lt.iterator(om.values(jobs_fecha, fecha_inicio, fecha_fin)):
            for j in lt.iterator(i):
                trabajo=me.getValue(mp.get(salarios_id, j["id"]))
                if trabajo["salary_from"]>=salario_minimo and trabajo["salary_from"]<=salario_maximo:
                    if om.contains(ciudades, j["city"])==False:
                        om.put(ciudades, j["city"], 0)
                    om.put(ciudades, j["city"], rbt.getValue(om.get(ciudades, j["city"]))+1)
                    if mp.get(ciudades_jobs, j["city"])==None:
                        mp.put(ciudades_jobs, j["city"], lt.newList("ARRAY_LIST"))
                    lt.addLast(me.getValue(mp.get(ciudades_jobs, j["city"])), j)
                    cantidad+=1
    else:
        for i in lt.iterator(om.values(salarios, float(salario_minimo), float(salario_maximo))):
            for j in lt.iterator(i):
                trabajo=me.getValue(mp.get(obtener_datos(data_structs, "jobs-mapa-id"),j["id"]))
                if trabajo["published_at"][:9]>=fecha_inicio and trabajo["published_at"][:9]<=fecha_fin:
                    if om.contains(ciudades, trabajo["city"])==False:
                        om.put(ciudades, trabajo["city"], 0)
                    om.put(ciudades, trabajo["city"], rbt.getValue(om.get(ciudades, trabajo["city"]))+1)
                    if mp.get(ciudades_jobs, trabajo["city"])==None:
                        mp.put(ciudades_jobs, trabajo["city"], lt.newList("ARRAY_LIST"))
                    lt.addLast(me.getValue(mp.get(ciudades_jobs, trabajo["city"])), trabajo)
                    cantidad+=1
    top_ciudades=lt.newList("ARRAY_LIST")
    for i in lt.iterator(om.keySet(ciudades)):
        lt.addLast(top_ciudades, (i, rbt.getValue(om.get(ciudades, i))))
    top_ciudad=None
    merg.sort(top_ciudades, compare_amount_req6)
    top_ciudad=lt.firstElement(top_ciudades)[0]
    if numero_ciudades>lt.size(top_ciudades):
        numero_ciudades=lt.size(top_ciudades)
    top_ciudades=lt.subList(top_ciudades, 1, numero_ciudades)
    merg.sort(top_ciudades, compare_alphabetical_req6)
    lista_final=lt.newList("ARRAY_LIST")
    for i in lt.iterator(me.getValue(mp.get(ciudades_jobs, top_ciudad))):
        habilidades_id=""
        lista_habilidades=me.getValue(mp.get(obtener_datos(data_structs, "skills-mapa-id"), i["id"]))
        for j in lt.iterator(lista_habilidades):
            if lt.size(lista_habilidades)==1:
                habilidades_id+=j["name"]
            else:
                habilidades_id+=j["name"]+", "   
        lt.addLast(lista_final, (i["published_at"],
                                 i["title"],
                                 i["company_name"],
                                 i["experience_level"],
                                 i["country_code"],
                                 i["city"],
                                 i["company_size"],
                                 i["workplace_type"],
                                 habilidades_id,
                                 me.getValue(mp.get(salarios_id, i["id"]))["salary_from"],
                                 i["latitude"],
                                 i["longitude"]))
    merg.sort(lista_final, sort_date_req6)
    return lista_final,cantidad, mp.size(ciudades_jobs), top_ciudades
    # TODO: Realizar el requerimiento 6
    pass
def sort_date_req6(data_1, data_2):
    """
    Función encargada de comparar dos fechas
    """
    if data_1[0] == data_2[0]:
        if data_1[8]>data_2[8]:
            return True
        else:
            return False
    elif data_1[0] > data_2[0]:
        return True
    else:
        return False
def compare_alphabetical_req6(data_1, data_2):
    if data_1[0] < data_2[0]:
        return True
    else:
        return False
def compare_amount_req6(data_1, data_2):
    if data_1[1] > data_2[1]:
        return True
    else:
        return False

def compare_city_req6(data_1, data_2):
    if data_1 == data_2:
        return 0
    elif data_1 > data_2:
        return 1
    else:
        return -1
    
def req_7(data_structs, anio, codigo_pais, propiedad_conteo):
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Realizar el requerimiento 7
    lista_codigo_pais=me.getValue(mp.get(obtener_datos(data_structs, "jobs-mapa-pais"), codigo_pais))
    cantidad_ofertas_pais=om.values(obtener_datos(data_structs,"jobs-mapa-fecha"),str(anio)+"-01-01",str(anio)+"-12-31")
    skills=obtener_datos(data_structs, "skills-mapa-id")
    salario=obtener_datos(data_structs, "employment-mapa-id")
    cantidad_ofertas=0
    for i in lt.iterator(cantidad_ofertas_pais):
        cantidad_ofertas+=lt.size(i)
    lista_final=lt.newList("ARRAY_LIST")
    cantidad_grafico=0
    mapa_criterio=None
    if propiedad_conteo=="experience_level":
        mapa_criterio=mp.newMap(6, maptype='PROBING', loadfactor=0.5)
    elif propiedad_conteo=="workplace_type":
        mapa_criterio=mp.newMap(6, maptype='PROBING', loadfactor=0.5)
    else:
        mapa_criterio=mp.newMap(100, maptype='PROBING', loadfactor=0.5)
    for i in lt.iterator(lista_codigo_pais):
        if i["published_at"][:4]==str(anio):
            propiedad=None
            if propiedad_conteo=="experience_level":
                if mp.get(mapa_criterio, i["experience_level"])==None:
                    mp.put(mapa_criterio, i["experience_level"], 0)
                mp.put(mapa_criterio, i["experience_level"], me.getValue(mp.get(mapa_criterio, i["experience_level"]))+1)
                cantidad_grafico+=1
                propiedad=i["experience_level"]
            elif propiedad_conteo=="workplace_type":
                if mp.get(mapa_criterio, i["workplace_type"])==None:
                    mp.put(mapa_criterio, i["workplace_type"], 0)
                mp.put(mapa_criterio, i["workplace_type"], me.getValue(mp.get(mapa_criterio, i["workplace_type"]))+1)
                cantidad_grafico+=1
                propiedad=i["workplace_type"]
            else:
                valor=me.getValue(mp.get(skills, i["id"]))
                propiedad=""
                for j in lt.iterator(valor):
                    if mp.get(mapa_criterio, j["name"])==None:
                        mp.put(mapa_criterio, j["name"], 0)
                    mp.put(mapa_criterio, j["name"], me.getValue(mp.get(mapa_criterio, j["name"]))+1)
                    propiedad+=j["name"]+", "
                cantidad_grafico+=1
            lt.addLast(lista_final,
                (i["published_at"],
                 i["title"],
                 i["company_name"],
                 i["country_code"],
                 i["city"],
                i["company_size"],
                me.getValue(mp.get(salario, i["id"]))["salary_from"],
                propiedad,
                float(i["latitude"]),
                float(i["longitude"])))
    lista_mayor=lt.newList("ARRAY_LIST")
    for i in lt.iterator(mp.keySet(mapa_criterio)):
        lt.addLast(lista_mayor, (i, me.getValue(mp.get(mapa_criterio, i))))
    merg.sort(lista_mayor, compare_mayor)
    mayor=lt.firstElement(lista_mayor)
    menor=lt.lastElement(lista_mayor)       
    lista_grafico1=[]
    lista_grafico2=[]
    for i in lt.iterator(mp.keySet(mapa_criterio)):
        lista_grafico1.append((i))
        lista_grafico2.append((me.getValue(mp.get(mapa_criterio, i))))
    return lista_final,cantidad_ofertas, cantidad_grafico,lista_grafico1,lista_grafico2, mayor,menor
def compare_mayor(data_1, data_2):
    if data_1[1] == data_2[1]:
        if data_1[0]>data_2[0]:
            return True
        else:
            return False
    elif data_1[1] > data_2[1]:
        return True
    else:
        return False 
def req_8(datos, mapa, eleccion, req7=None):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    marker_cluster=MarkerCluster().add_to(mapa)
    folium.plugins.Fullscreen(
    position="topright",
    title="Expandir",
    title_cancel="Salir ",
    force_separate_button=True,
        ).add_to(mapa)
    if eleccion!=7:
        for i in lt.iterator(datos):
            folium.Marker(
                location=[float(i[10]), float(i[11])],
                tooltip=i[1],
                popup="<b>Published At:</b>"+i[0]+"<br><b>Title:</b>"+i[1]+"<br><b>Company:</b>"+i[2]+"<br><b>Experience Level:</b>"+i[3]+"<br><b>Country:</b>"+i[4]+"<br><b>City:</b>"+i[5]+"<br><b>Company Size:</b>"+str(i[6])+"<br><b>Workplace Type:</b>"+i[7]+"<br><b>Habildades:</b>"+i[8]+"<br><b>Salary:</b>"+str(i[9]),
                icon=folium.Icon(color="blue")
            ).add_to(marker_cluster)
    else:
        texto=None
        if req7=="experience_level":
            texto="Nivel experiencia: "
        elif req7=="workplace_type":
            texto="Ubicación: "
        else:
            texto="Habilidades: "
        
        for i in lt.iterator(datos):
            folium.Marker(
                location=[float(i[8]), float(i[9])],
                tooltip=i[1],
                popup="<b>Published At:</b>"+i[0]+"<br><b>Title:</b>"+i[1]+"<br><b>Company:</b>"+i[2]+"<br><b>Country:</b>"+i[3]+"<br><b>City:</b>"+i[4]+"<br><b>Company Size:</b>"+str(i[5])+"<br><b>Salario:</b>"+str(i[6])+"<br><b>"+texto+"</b>"+str(i[7]),
                icon=folium.Icon(color="blue")
            ).add_to(marker_cluster)
    folium.LayerControl().add_to(mapa)
    return mapa
# Funciones utilizadas para comparar elementos dentro de una lista

def compare(data_1, data_2):
    """
    Función encargada de comparar dos datos
    """
    #TODO: Crear función comparadora de la lista
    pass

# Funciones de ordenamiento


def sort_dates_desc(data_1, data_2):
    """
    Función encargada de comparar dos fechas
    """
    if data_1[0] == data_2[0]:
        if data_1[8]<data_2[8]:
            return True
        else:
            return False
    elif data_1[0] < data_2[0]:
        return True
    else:
        return False
    
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