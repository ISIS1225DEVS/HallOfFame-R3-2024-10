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
import sys
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from datetime import datetime as dt
from DISClib.ADT import minpq as mpq
from DISClib.ADT import indexminpq as impq
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import selectionsort as se
from DISClib.Algorithms.Sorting import mergesort as merg
from DISClib.Algorithms.Sorting import quicksort as quk
assert cf
import folium
import webbrowser
import subprocess
from folium.plugins import MarkerCluster
from folium.features import CustomIcon
import requests
from PIL import Image
from io import BytesIO
from tqdm import tqdm
from tqdm.auto import tqdm
from colorama import Fore, Back, Style
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
    data_structs = {'jobs': None,
                    "jobs_time":None,
                    "jobs_compsize":None,
                    'employments': None,
                    'multilocations': None,
                    'skills': None}
    
    
    data_structs['jobs'] = om.newMap(omaptype='RBT')
    data_structs['jobs_time'] = om.newMap(omaptype='RBT')
    data_structs['jobs_compsize'] = om.newMap(omaptype='RBT')
    data_structs['employments'] = mp.newMap(numelements= 4, maptype="CHAINING", loadfactor=4)
    data_structs['multilocations'] = mp.newMap(numelements= 4, maptype="CHAINING", loadfactor=4)
    data_structs['skills'] = mp.newMap(numelements= 4, maptype="CHAINING", loadfactor=4)
   
    return data_structs
# Funciones para agregar informacion al modelo


def add_job(jobs,file_line):
    """
    Función para agregar nuevos elementos a la lista
    """
    check_empty = lambda value: value if(value is not None and value.strip() != "" and value.strip() != "-" and value.strip() != "NOT DEFINED" ) else "Unknown"
    time = dt.strptime(file_line['published_at'], "%Y-%m-%dT%H:%M:%S.%fZ")
    fecha = file_line['id']

    
    job_data = {'title': check_empty(file_line['title']),
                'street': check_empty(file_line['street']),
                'city': check_empty(file_line['city']),
                'country_code': check_empty(file_line['country_code']),
                'address_text': check_empty(file_line['address_text']),
                'marker_icon': check_empty(file_line['marker_icon']),
                'workplace_type': check_empty(file_line['workplace_type']),
                'company_name': check_empty(file_line['company_name']),
                'company_url': check_empty(file_line['company_url']),
                'company_size': check_empty(file_line['company_size']),
                'experience_level': check_empty(file_line['experience_level']),
                'published_at': time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                'remote_interview': check_empty(file_line['remote_interview']),
                'open_to_hire_ukrainians': check_empty(file_line['open_to_hire_ukrainians']),
                'id': check_empty(file_line['id']),
                'display_offer': check_empty(file_line['display_offer']),
                "longitude":check_empty(file_line["longitude"]),
                "latitude":check_empty(file_line["latitude"])}
   

    om.put(jobs, fecha,job_data)
      

def add_job_time(skill, file_line):
    """
    Función para agregar nuevos elementos a la lista
    """
    check_empty = lambda value: value if (value is not None and value.strip() != "" and value.strip() != "-"  and value.strip() != "NOT DEFINED") else "Unknown"
    key = file_line['published_at']
    time = dt.strptime(file_line['published_at'], "%Y-%m-%dT%H:%M:%S.%fZ")
    jobs_list_by_time = []

    job_data = {'title': check_empty(file_line['title']),
                'street': check_empty(file_line['street']),
                'city': check_empty(file_line['city']),
                'country_code': check_empty(file_line['country_code']),
                'address_text': check_empty(file_line['address_text']),
                'marker_icon': check_empty(file_line['marker_icon']),
                'workplace_type': check_empty(file_line['workplace_type']),
                'company_name': check_empty(file_line['company_name']),
                'company_url': check_empty(file_line['company_url']),
                'company_size': check_empty(file_line['company_size']),
                'experience_level': check_empty(file_line['experience_level']),
                'published_at': time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                'remote_interview': check_empty(file_line['remote_interview']),
                'open_to_hire_ukrainians': check_empty(file_line['open_to_hire_ukrainians']),
                'id': check_empty(file_line['id']),
                'display_offer': check_empty(file_line['display_offer']),
                "longitude":check_empty(file_line["longitude"]),
                "latitude":check_empty(file_line["latitude"])}
   
    
    if om.contains(skill, key) and key != None:
        jobs_list_by_time = om.get(skill, key)['value']
        jobs_list_by_time.append(job_data)
        om.put(skill, key, jobs_list_by_time)
    elif key != None:
        jobs_list_by_time.append(job_data)
        om.put(skill, key, jobs_list_by_time)


def add_jobs_compsize(control, file_line):
    """
    Función para agregar nuevos elementos a la lista
    """
    skill = control["jobs_compsize"]
    
    check_empty = lambda value: value if (value is not None and value.strip() != "" and value.strip() != "-"  and value.strip() != "NOT DEFINED") else "Unknown"
    key = file_line['company_size']
    time = dt.strptime(file_line['published_at'], "%Y-%m-%dT%H:%M:%S.%fZ")
    jobs_list_by_time = []

    habilidades = []
    
    job_data = {'title': check_empty(file_line['title']),
                'street': check_empty(file_line['street']),
                'city': check_empty(file_line['city']),
                'country_code': check_empty(file_line['country_code']),
                'address_text': check_empty(file_line['address_text']),
                'marker_icon': check_empty(file_line['marker_icon']),
                'workplace_type': check_empty(file_line['workplace_type']),
                'company_name': check_empty(file_line['company_name']),
                'company_url': check_empty(file_line['company_url']),
                'company_size': check_empty(file_line['company_size']),
                'experience_level': check_empty(file_line['experience_level']),
                'published_at': time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                'remote_interview': check_empty(file_line['remote_interview']),
                'open_to_hire_ukrainians': check_empty(file_line['open_to_hire_ukrainians']),
                'id': check_empty(file_line['id']),
                'display_offer': check_empty(file_line['display_offer']),
                "longitude":check_empty(file_line["longitude"]),
                "latitude":check_empty(file_line["latitude"])}
    
    list_skills = mp.get(control['skills'],file_line["id"])["value"]
    employment = mp.get(control['employments'],file_line["id"])["value"]
    for each in list_skills:
        x  = {"skill":each["name"],"level":each["level"]}
        habilidades.append(x)
    job_data["habilidades"] = habilidades        
    
  
    salarios = [dato["minimum_usd_salary"] for dato in employment if dato["minimum_usd_salary"] is not None]
    salario_minimo_actual = min(salarios) if salarios else None
    job_data["salario_minimo"] = salario_minimo_actual       
     
    if om.contains(skill, key) and key != None:
        jobs_list_by_time = om.get(skill, key)['value']
        jobs_list_by_time.append(job_data)
        om.put(skill, key, jobs_list_by_time)
    elif key != None:
        jobs_list_by_time.append(job_data)
        om.put(skill, key, jobs_list_by_time)        

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def universal_salary_def(currency_salary,money):
    if currency_salary.lower() == "usd":
        return money * 1
    elif currency_salary.lower() == "eur":
        return money * 1.19
    elif currency_salary.lower() == "gbp":
        return money * 1.27
    elif currency_salary.lower() == "pln":
        return money * 0.25
    elif currency_salary.lower() == "chf":
        return money * 1.11
    
def add_employment_type(employments, file_line):
    """
    Función para agregar nuevos elementos a la lista
    """
    check_empty = lambda value: value if (value is not None and value.strip() != "" and value.strip() != "-"  and value.strip() != "NOT DEFINED") else "Unknown"
    key = file_line['id']
    employment_list_by_id = []

    employment_data = {'type': check_empty(file_line['type']),
                        'currency_salary': check_empty(file_line['currency_salary']),
                        'salary_from': check_empty(file_line['salary_from']),
                        "salary_to" : check_empty(file_line['salary_to']),
                        "id" : check_empty(file_line['id'])
                        }
    
    salary_from =employment_data["salary_from"]
    salary_to = employment_data["salary_to"]
    salary_confirm = is_number(salary_to) and is_number(salary_from)
    currency_salary = employment_data["currency_salary"]
    
    if salary_confirm:
        salary = (float(salary_to) + float(salary_from))/2
        employment_data["average_salary"]= salary
        employment_data["minimum_usd_salary"]= int(universal_salary_def(currency_salary,float(salary_from)))
        
    else:
        employment_data["average_salary"]= None   
        employment_data["minimum_usd_salary"]= None
    average_salary = employment_data["average_salary"]
    
    if average_salary != None:
        universal_salary =  universal_salary_def(currency_salary,float(average_salary))
        employment_data["universal_salary"] = universal_salary
    else:
        employment_data["universal_salary"] = None 
        
        
    if mp.contains(employments, key) and key != None:
        employment_list_by_id = mp.get(employments, key)['value']
        employment_list_by_id.append(employment_data)
        mp.put(employments, key, employment_list_by_id)
    elif key != None:
        employment_list_by_id.append(employment_data)
        mp.put(employments, key, employment_list_by_id)


def add_multilocation(multilocation, file_line):
    """
    Función para agregar nuevos elementos a la lista
    """
    check_empty = lambda value: value if (value is not None and value.strip() != "" and value.strip() != "-"  and value.strip() != "NOT DEFINED") else "Unknown"
    key = file_line['id']
    multilocation_list_by_id = []

    multilocation_data = {'city': check_empty(file_line['city']),
                        'street': check_empty(file_line['street']),
                        "id" : check_empty(file_line['id'])
                        }
    
    if mp.contains(multilocation, key) and key != None:
        multilocation_list_by_id = mp.get(multilocation, key)['value']
        multilocation_list_by_id.append(multilocation_data)
        mp.put(multilocation, key, multilocation_list_by_id)
    elif key != None:
        multilocation_list_by_id.append(multilocation_data)
        mp.put(multilocation, key, multilocation_list_by_id)


def add_skill(skill, file_line):
    """
    Función para agregar nuevos elementos a la lista
    """
    check_empty = lambda value: value if (value is not None and value.strip() != "" and value.strip() != "-"  and value.strip() != "NOT DEFINED") else "Unknown"
    key = file_line['id']
    skill_list_by_id = []

    skill_data = {'name': check_empty(file_line['name']), 
                  'level': check_empty(file_line['level']),
                  "id" : check_empty(file_line['id'])}
    
    if mp.contains(skill, key) and key != None:
        skill_list_by_id = mp.get(skill, key)['value']
        skill_list_by_id.append(skill_data)
        mp.put(skill, key, skill_list_by_id)
    elif key != None:
        skill_list_by_id.append(skill_data)
        mp.put(skill, key, skill_list_by_id)

def generacion_respuesta_dict(titulos, data_list):
    respuesta = []
    for data in data_list:
       nuevo_diccionario = {i: None for i in titulos} 
       for key, value in data.items():
        
            if key in titulos:
                if key == "published_at":
                    try:
                        if len(value) == len('YYYY-MM-DD'):
                            job_date = dt.strptime(value, "%Y-%m-%d")  # Assuming date format without time
                        else:
                            job_date = dt.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")
                        nuevo_diccionario[key] = job_date    
                    except ValueError:
                        print(value)

                else:    
                    nuevo_diccionario[key] = value
    
       respuesta.append(nuevo_diccionario)
    return respuesta       
    
def generacion_respuesta(titulos, data_list):
    respuesta = lt.newList("ARRAY_LIST")
    
    for data in lt.iterator(data_list):
        nuevo_diccionario = {i: None for i in titulos}
        
        for key, value in data.items():
        
            if key in titulos:
                if key == "published_at":
                    try:
                        if len(value) == len('YYYY-MM-DD'):
                            job_date = dt.strptime(value, "%Y-%m-%d")  # Assuming date format without time
                        else:
                            job_date = dt.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")
                        nuevo_diccionario[key] = job_date    
                    except ValueError:
                        print(value)

                else:    
                    nuevo_diccionario[key] = value
        
        lt.addLast(respuesta, nuevo_diccionario)
        
    return respuesta


def req_1(control,fecha_inicial,fecha_final):
    """
    Función que soluciona el requerimiento 1
    """
    time_data = control["model"]["jobs_time"]
    data = om.values(time_data,fecha_inicial,fecha_final)
    lista = lt.newList("ARRAY_LIST")
    titulos = ["published_at","title","company_name","experience_level","country_code","city","company_size","workplace_type","Habilidades_solicitadas","longitude","latitude" ] 
    contador = 0
    skills = mp.valueSet(control["model"]["skills"])
    diccionario_habilidades = {}
    for id in lt.iterator(skills):
        for habilidad in id:
            nombre = habilidad["name"] 
            ids = habilidad["id"]
            if ids not in diccionario_habilidades:
                diccionario_habilidades[ids] =[nombre]
            else: 
                diccionario_habilidades[ids].append(nombre)
    
    
    for dato in lt.iterator(data):
        for trabajo in dato:
            id = trabajo["id"]
            skill = diccionario_habilidades[id]
            trabajo["Habilidades_solicitadas"] = skill
            lt.addLast(lista,trabajo)
            contador +=1
    
    sort_function_time(lista)
    respuesta = generacion_respuesta(titulos,lista)    
    return contador , respuesta
    
def req_2(control,salario_minimo,salario_maximo):
    """
    Función que soluciona el requerimiento 2
    """
    employment = mp.valueSet(control["model"]["employments"])
    skills = mp.valueSet(control["model"]["skills"])
    trabajo = om.valueSet(control["model"]["jobs"])
    diccionario_salario = {}
    diccionario_habilidades = {}
    lista = lt.newList("ARRAY_LIST")
    titulos = ["published_at","title","company_name","experience_level","country_code","city","company_size","workplace_type","salario_minimo","Habilidades_solicitadas", "longitude","latitude"] 
    contador = 0
    salario_minimo_anterior = 0
    for id in lt.iterator(employment):
        for dato in id:
            salario_minimo_actual = dato["minimum_usd_salary"] 
            ids = dato["id"] 
            # Si aún no se ha almacenado ningún salario mínimo para este id
            if ids not in diccionario_salario:
                diccionario_salario[ids] = salario_minimo_actual
            else:
                if  salario_minimo_actual != None and salario_minimo_anterior != None: 
                    salario_minimo_anterior = diccionario_salario[ids]
                    # Comparar el salario mínimo actual con el anterior y almacenar el mayor
                    if salario_minimo_actual < salario_minimo_anterior:
                        diccionario_salario[ids] = salario_minimo_actual
                    else:
                        diccionario_salario[ids] = salario_minimo_anterior
    
    for id in lt.iterator(skills):
        for habilidad in id:
            nombre = habilidad["name"] 
            ids = habilidad["id"]
            if ids not in diccionario_habilidades:
                diccionario_habilidades[ids] =[nombre]
            else: 
                diccionario_habilidades[ids].append(nombre)     
            
            
    for job in lt.iterator(trabajo):
        id = job["id"]
        salary = diccionario_salario[id]
        skill = diccionario_habilidades[id]
        if salary == "Unknown" or salary == None:
            puerta = False
        else: 
            puerta = int(salario_minimo) <= int(salary) <= int(salario_maximo)
        if puerta == True:
            contador +=1
            job["minimum_usd_salary"] = salary
            job["salario_minimo"]=job["minimum_usd_salary"]
            job["Habilidades_solicitadas"] = skill
            
            lt.addLast(lista,job) 
    
    
    
    
    sort_function(lista)
    respuesta = generacion_respuesta(titulos,lista)    
    return contador , respuesta
            
            
        


def req_3(control,n,codigo_pais,nivel_experticia):
    """
    Función que soluciona el requerimiento 3
    """
    employment = mp.valueSet(control["model"]["employments"])
    lista = lt.newList("ARRAY_LIST")
    titulos = ["published_at","title","company_name","experience_level","country_code","city","company_size","workplace_type","salario_minimo","Habilidades_solicitadas","longitude","latitude" ] 
    contador = 0    
    skills = mp.valueSet(control["model"]["skills"])
    trabajo = om.valueSet(control["model"]["jobs"])
    diccionario_salario = {}
    diccionario_habilidades = {}
    salario_minimo_anterior = 0
    
    for id in lt.iterator(employment):
        for dato in id:
            salario_minimo_actual = dato["minimum_usd_salary"] 
            ids = dato["id"] 
            # Si aún no se ha almacenado ningún salario mínimo para este id
            if ids not in diccionario_salario:
                diccionario_salario[ids] = salario_minimo_actual
            else:
                if  salario_minimo_actual != None and salario_minimo_anterior != None: 
                    salario_minimo_anterior = diccionario_salario[ids]
                    # Comparar el salario mínimo actual con el anterior y almacenar el mayor
                    if salario_minimo_actual < salario_minimo_anterior:
                        diccionario_salario[ids] = salario_minimo_actual
                    else:
                        diccionario_salario[ids] = salario_minimo_anterior
    
    for id in lt.iterator(skills):
        for habilidad in id:
            nombre = habilidad["name"] 
            ids = habilidad["id"]
            if ids not in diccionario_habilidades:
                diccionario_habilidades[ids] =[nombre]
            else: 
                diccionario_habilidades[ids].append(nombre)  
              
    for job in lt.iterator(trabajo):
        id = job["id"]
        pais = job["country_code"]
        experticia = job["experience_level"]
        salary = diccionario_salario[id]
        skill = diccionario_habilidades[id]
        
        if codigo_pais  == pais and nivel_experticia == experticia :
            
            job["minimum_usd_salary"] = salary
            job["salario_minimo"]=job["minimum_usd_salary"]
            job["Habilidades_solicitadas"] = skill
            
            lt.addLast(lista,job)
    
    sort_function_time(lista)
    
    lista = lt.subList(lista,0, n)
    respuesta = generacion_respuesta(titulos,lista)    
    return contador , respuesta


def req_4(control, n_offers, city_name, job_location):
    """
    Función que soluciona el requerimiento 4
    """
    jobs_values = om.valueSet(control["model"]["jobs"])
    employments_tuples = control["model"]["employments"]
    skills_tuples = control["model"]["skills"]
    ans = lt.newList("ARRAY_LIST")
    titles = ["published_at", "title", "company_name", "experience_level", "country_code", "city", "company_size", "workplace_type", "salary_from", "skills","longitude","latitude"]

    for each_job in lt.iterator(jobs_values):
        if each_job["city"] == city_name and each_job["workplace_type"] == job_location:
            job_id = each_job["id"]
            
            #Encuentra el salario mínimo ofrecido por trabajo
            employment = mp.get(employments_tuples, job_id)
            min_salary = int(lt.size(jobs_values))

            for i in employment["value"]:
                if i["salary_from"] != "Unknown" and int(i["salary_from"]) < min_salary:
                    min_salary = int(i["salary_from"])
            
            if min_salary == lt.size(jobs_values):
                min_salary = "Unknown"

            #Encuntra las habilidades solicitadas por trabajo
            skills = mp.get(skills_tuples, job_id)
            skills_ans = []

            for i in skills["value"]:
                skills_ans.append(i["name"])

            #Agrega el trabajo a la lista completa de respuesta
            each_job["salary_from"] = min_salary
            each_job["skills"] = skills_ans
            lt.addLast(ans, each_job)

    size = lt.size(ans)

    resultado_final = lt.newList('ARRAY_LIST')
    a = 0
    for sorted in lt.iterator(ans):
            if a < n_offers:
                lt.addLast(resultado_final,sorted)
                a += 1
                
    resultado_final = generacion_respuesta(titles,resultado_final)

    return resultado_final, size


def req_5(n,ls_companysize,li_companysize,skill,ls_companyskill,li_companyskill,control):
    """
    Función que soluciona el requerimiento 5
    """
    jobs = om.values(control['model']['jobs_compsize'],li_companysize,ls_companysize)
    employments = mp.valueSet(control['model']['employments'])
    titles = ["published_at", "title", "company_name", "experience_level", "country_code", "city", "company_size", "workplace_type", "salario_minimo", "habilidades","longitude","latitude"]
    result_list = lt.newList('ARRAY_LIST')
    contador = 0
    for lista in lt.iterator(jobs):
        for dato in lista:
            j = dato["habilidades"]
            for  i in j: 
                skill_d = i["skill"]
                level = i["level"]
                
                if is_number(level):                    
                    if str(skill_d) == str(skill) and (li_companyskill <= int(level) <= ls_companyskill):
                        lt.addLast(result_list, dato)
                        contador += 1
    
    size = lt.size(result_list)


    
    resultado_final = lt.newList('ARRAY_LIST')
    a = 0
    for sorted in lt.iterator(result_list):
            if a < n:
                lt.addLast(resultado_final,sorted)
                a += 1
                
    resultado_final = generacion_respuesta(titles,resultado_final)
    return contador, resultado_final


def req_6(control,n,fecha_inicial,fecha_final,salario_minimo,salario_maximo):
    """
    Función que soluciona el requerimiento 6
    """
    employment = mp.valueSet(control["model"]["employments"])
    lista = lt.newList("ARRAY_LIST")
    mapa= mp.newMap(numelements=17,
           prime=109345121,
           maptype='CHAINING',
           loadfactor=4)
    multilocation_list_by_id = []
    titulos = ["published_at", "title", "company_name","experience_level","country_code","city","company_size","workplace_type", "salario_minimo", "Habilidades_solicitadas","longitude","latitude"] #"published_at","title","company_name","salario_minimo","Habilidades_solicitadas" ,"experience_level","country_code","city","company_size","workplace_type","open_to_hire_ukrainians"]
    contador = 0    
    skills = mp.valueSet(control["model"]["skills"])
    time_data = control["model"]["jobs_time"]
    data = om.values(time_data,fecha_inicial,fecha_final)
    diccionario_salario = {}
    diccionario_habilidades = {}
    diccionario_ciudades = {}
    salario_minimo_anterior = 0
    
    for id in lt.iterator(employment):
        for dato in id:
            salario_minimo_actual = dato["minimum_usd_salary"] 
            ids = dato["id"] 
            # Si aún no se ha almacenado ningún salario mínimo para este id
            if ids not in diccionario_salario:
                diccionario_salario[ids] = salario_minimo_actual
            else:
                if  salario_minimo_actual != None and salario_minimo_anterior != None: 
                    salario_minimo_anterior = diccionario_salario[ids]
                    # Comparar el salario mínimo actual con el anterior y almacenar el mayor
                    if salario_minimo_actual < salario_minimo_anterior:
                        diccionario_salario[ids] = salario_minimo_actual
                    else:
                        diccionario_salario[ids] = salario_minimo_anterior
    
    for id in lt.iterator(skills):
        for habilidad in id:
            nombre = habilidad["name"] 
            ids = habilidad["id"]
            if ids not in diccionario_habilidades:
                diccionario_habilidades[ids] =[nombre]
            else: 
                diccionario_habilidades[ids].append(nombre)  
    
    for dato in lt.iterator(data):
        for job in dato:
            id = job["id"]
            ciudad = job["city"]
            salary = diccionario_salario[id]
            skill = diccionario_habilidades[id]
            if salary == "Unknown" or salary == None:
                puerta = False
            else: 
                puerta = int(salario_minimo) <= int(salary) <= int(salario_maximo)
            if puerta == True:
                contador +=1
                job["minimum_usd_salary"] = salary
                job["salario_minimo"]=job["minimum_usd_salary"]
                job["Habilidades_solicitadas"] = skill
                
                
                if ciudad  in diccionario_ciudades:
                    diccionario_ciudades[ciudad]+=1
                else: 
                    diccionario_ciudades[ciudad]=1
                    
                
                if mp.contains(mapa, ciudad) and ciudad != None:
                    multilocation_list_by_id = mp.get(mapa, ciudad)['value']
                    multilocation_list_by_id.append(job)
                    mp.put(mapa, ciudad, multilocation_list_by_id)
                elif ciudad != None:
                    multilocation_list_by_id.append(job)
                    mp.put(mapa, ciudad, multilocation_list_by_id)

    total_ciudades = len(diccionario_ciudades)
    diccionario_recortado = dict(sorted(diccionario_ciudades.items(), key=lambda item: item[1], reverse=True)[:n])
    n_ciudades_cumplen = []
    for ciudad_d in diccionario_recortado.keys():
        respuesta_d = {ciudad_d:None}
        n_ciudades_cumplen.append(ciudad_d)
        lista_tabajo = mp.get(mapa,ciudad_d)["value"]

        final = generacion_respuesta_dict(titulos, lista_tabajo)
        
        respuesta_d[ciudad_d] = final
        lt.addLast(lista,respuesta_d)
        
    n_ciudades_cumplen = sorted(n_ciudades_cumplen)                  
           

    return contador,total_ciudades,n_ciudades_cumplen,lista


def req_7(control, year, country_code, property_input):
    """
    Función que soluciona el requerimiento 7
    """
    employments_tuples = control["model"]["employments"]
    time_data = control["model"]["jobs_time"]
    fecha_inicial = year + "-01-01"
    fecha_final = year + "-12-31"
    data = om.values(time_data, fecha_inicial,fecha_final)
    skills_tuples = control["model"]["skills"]
    ans = lt.newList("ARRAY_LIST")
    general_size = 0
    graph_size = 0
    distribution = {}

    titles = ["published_at", "title", "company_name", "country_code", "city", "company_size", "salary_from", "property","longitude","latitude"]

    for i in lt.iterator(data):
        for each_job in i:
            general_size += 1
            if each_job["country_code"] == country_code:
                job_id = each_job["id"]
                skills = mp.get(skills_tuples, job_id)
                skills_ans = []

                #Encuentra el salario mínimo ofrecido por trabajo
                employment = mp.get(employments_tuples, job_id)
                min_salary = lt.size(data)

                for i in employment["value"]:
                    if i["salary_from"] != "Unknown":
                        if int(i["salary_from"]) < min_salary:
                            min_salary = int(i["salary_from"])
            
                if min_salary == lt.size(data):
                    min_salary = "Unknown"
                
                each_job["salary_from"] = min_salary

                if property_input == '1' and each_job["experience_level"] != "Unknown":
                    each_job["property"] = each_job["experience_level"]
                    lt.addLast(ans, each_job)

                    if each_job["experience_level"] in distribution:
                        distribution[each_job["experience_level"]] += 1
                    else:
                        distribution[each_job["experience_level"]] = 1

                if property_input == '2' and each_job["workplace_type"] != "Unknown":
                    each_job["property"] = each_job["workplace_type"]
                    lt.addLast(ans, each_job)

                    if each_job["workplace_type"] in distribution:
                        distribution[each_job["workplace_type"]] += 1
                    else:
                        distribution[each_job["workplace_type"]] = 1

                if property_input == '3':
                    for i in skills["value"]:
                        if i["name"] != "Unknown":
                            skills_ans.append(i["name"])
                            each_job["property"] = skills_ans
                            lt.addLast(ans, each_job)

                            if i["name"] in distribution:
                                distribution[i["name"]] += 1
                            else:
                                distribution[i["name"]] = 1

    graph_size = lt.size(ans)
    ans = generacion_respuesta(titles, ans)

    return ans, general_size, graph_size, distribution

def req_8(control,respuesta_req,type,req_name):
    """
    Función que soluciona el requerimiento 8
    """
    tqdm.pandas(ascii=True, bar_format='{l_bar}%s{bar}%s{r_bar}' % (Fore.GREEN, Fore.RESET))


    m = folium.Map(location=[0, 0], zoom_start=3)
    marker_cluster = MarkerCluster().add_to(m)
    
    if type == 1:
        for dato in tqdm(lt.iterator(respuesta_req), colour='green', ascii=True, bar_format='{l_bar}%s{bar}%s{r_bar}' % (Fore.GREEN, Fore.RESET)):
            folium.Marker([dato['latitude'], dato['longitude']], popup=dato,tooltip=dato['title'], icon=folium.Icon(color='lightblue', icon='star', prefix='fa', icon_color='darkred', angle=180, spin=True)).add_to(marker_cluster)
    elif type == 2:
        for city in tqdm(lt.iterator(respuesta_req),colour='red'): 
            for ciudad, trabajo in city.items():  
                for dato in trabajo:
                    folium.Marker([dato['latitude'], dato['longitude']], popup=dato,tooltip=dato['title'],icon=folium.Icon(color='lightblue', icon='star', prefix='fa', icon_color='darkred', angle=180, spin=True)).add_to(marker_cluster)
                
                
    titulo_mapa = f"{req_name}.html"
    m.save(titulo_mapa)    
    
    subprocess.Popen(['start', titulo_mapa], shell=True)
    webbrowser.open_new_tab(titulo_mapa)

def req_8_todos(respuesta_req1,respuesta_req2,respuesta_req3,respuesta_req4,respuesta_req5,respuesta_req6,respuesta_req7):  
    tqdm.pandas(ascii=True, bar_format='{l_bar}%s{bar}%s{r_bar}' % (Fore.GREEN, Fore.RESET))
    
    m = folium.Map(location=[0, 0], zoom_start=3)
    marker_cluster = MarkerCluster().add_to(m)
    
    for dato in lt.iterator(respuesta_req1):
        folium.Marker([dato['latitude'], dato['longitude']], popup=dato,tooltip=dato['title'], icon=folium.Icon(color='lightblue', icon='star', prefix='fa', icon_color='darkred', angle=180, spin=True)).add_to(marker_cluster)
    for dato in lt.iterator(respuesta_req2):
        folium.Marker([dato['latitude'], dato['longitude']], popup=dato,tooltip=dato['title'], icon=folium.Icon(color='darkpurple', icon='cloud', prefix='fa', icon_color='darkred', angle=180, spin=True)).add_to(marker_cluster)
    for dato in lt.iterator(respuesta_req3):
        folium.Marker([dato['latitude'], dato['longitude']], popup=dato,tooltip=dato['title'], icon=folium.Icon(color='lightgreen', icon='cog', prefix='fa', icon_color='darkred', angle=180, spin=True)).add_to(marker_cluster)
    for dato in lt.iterator(respuesta_req4):
        folium.Marker([dato['latitude'], dato['longitude']], popup=dato,tooltip=dato['title'], icon=folium.Icon(color='cadetblue', icon='diamond', prefix='fa', icon_color='darkred', angle=180, spin=True)).add_to(marker_cluster)
    for dato in lt.iterator(respuesta_req5):
        folium.Marker([dato['latitude'], dato['longitude']], popup=dato,tooltip=dato['title'], icon=folium.Icon(color='pink', icon='heart', prefix='fa', icon_color='darkred', angle=180, spin=True)).add_to(marker_cluster)
    for city in tqdm(lt.iterator(respuesta_req6),colour='red'): 
            for ciudad, trabajo in city.items():  
                for dato in trabajo:
                    folium.Marker([dato['latitude'], dato['longitude']], popup=dato,tooltip=dato['title'],icon=folium.Icon(color='green', icon='key', prefix='fa', icon_color='darkred', angle=180, spin=True)).add_to(marker_cluster)

    for dato in lt.iterator(respuesta_req7):
        folium.Marker([dato['latitude'], dato['longitude']], popup=dato,tooltip=dato['title'], icon=folium.Icon(color='red', icon='fa-life-ring', prefix='fa', icon_color='darkred', angle=180, spin=True)).add_to(marker_cluster)

    titulo_mapa = f"todos_los_requerimientos.html"
    m.save(titulo_mapa)    
    
    subprocess.Popen(['start', titulo_mapa], shell=True)
    webbrowser.open_new_tab(titulo_mapa)

      

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
    
    
    if data_1["minimum_usd_salary"] == data_2["minimum_usd_salary"]:
         if data_1["published_at"] > data_2["published_at"]:
            respuesta = True
         else:    
            respuesta = False
    elif data_1["minimum_usd_salary"] > data_2["minimum_usd_salary"]:
        respuesta = True
    else: 
         respuesta = False
    
    return respuesta     

def sort_function(data_structs):
    """
    Función encargada de ordenar la lista con los datos
    """
    merg.sort(data_structs, sort_criteria)


def sort_criteria_time(data_1, data_2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        data1 (_type_): _description_
        data2 (_type_): _description_

    Returns:
        _type_: _description_
    """
   
    if data_1["published_at"] < data_2["published_at"]:
        return True 
      
    else:    
        return False    


def sort_criteria_time_4(data_1, data_2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        data1 (_type_): _description_
        data2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    
    if data_1["published_at"] > data_2["published_at"]:
        return True 
    
    else:    
        return False
  


def sort_function_time_4(data_structs):
    """
    Función encargada de ordenar la lista con los datos
    """
    merg.sort(data_structs,sort_criteria_time_4)


def sort_function_time(data_structs):
    """
    Función encargada de ordenar la lista con los datos
    """
    merg.sort(data_structs,sort_criteria_time)


def ver_divisa(control):
    respuesta ={}
    datos = mp.valueSet(control["model"]["employments"])
    for data in lt.iterator(datos):
        
        for line in data:
            divisa = line["currency_salary"]
            if divisa in respuesta:
                respuesta[divisa] +=1
            else:
                respuesta[divisa] =1    
    
    return respuesta