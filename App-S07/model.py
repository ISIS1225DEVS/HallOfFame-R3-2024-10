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
#from forex_python.converter import CurrencyRates as CR
assert cf
import threading
import threading
from datetime import datetime as dt
from datetime import timezone
import folium
from datetime import timezone
import time
import json


"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""

# Construccion de modelos

def newCatalog():
    catalog={
        "jobs":None,
        "published_at": None,
        "country_Experience":None,
        "city_Workplace":None,
        "companysize_skill":None,
        "salary_min":None
    }
    
    catalog["jobs"] = lt.newList("ARRAY_LIST")
    catalog["published_at"] = om.newMap(omaptype="RBT", cmpfunction=dateCompare)
    catalog["country_Experience"] = mp.newMap(numelements= 211,
                                            maptype='PROBING',
                                            loadfactor=0.5)
    catalog["city_Workplace"] = mp.newMap(numelements= 477,
                                            maptype='PROBING',
                                            loadfactor=0.5)
    catalog["companysize_skill"] = om.newMap(omaptype="RBT")
    catalog["salary_min"]= om.newMap(omaptype= "RBT", cmpfunction=SalaryCompare2)
    
    return catalog

#* Criterios de comparacion
def dateCompare(date1, date2):
    date1, date2 = dt.fromisoformat(date1), dt.fromisoformat(date2)
    date1, date2 = dateMakeAware(date1), dateMakeAware(date2)
    if date1 == date2:
        return 0
    if date1 < date2:
        return -1
    else:
        return 1


#########################################
# Funciones para crear lista temporales
#########################################

def Tempjobs(catalog, nombrearchivo):
    catalog["jobs"] = lt.newList(datastructure="ARRAY_LIST",filename=nombrearchivo,delimiter=";")
    return catalog

def TempSkills(SkillsDic, dato):
    if dato["id"] in SkillsDic:
        SkillsDic[dato["id"]]["skill_name"].append(dato["name"])
        SkillsDic[dato["id"]]["skill_level"].append(dato["level"])
    else:
        SkillsDic[dato["id"]]={"skill_name":[dato["name"]],"skill_level":[dato["level"]]}
    return SkillsDic

def TempEmpTypes(EmpTypesDic, dato):
    if dato["id"] in EmpTypesDic:
        EmpTypesDic[dato["id"]]["type"].append(dato["type"])
        EmpTypesDic[dato["id"]]["currency_salary"].append(dato["currency_salary"])
        EmpTypesDic[dato["id"]]["salary_from"].append(dato["salary_from"])
        EmpTypesDic[dato["id"]]["salary_to"].append(dato["salary_to"])
    else:
        EmpTypesDic[dato["id"]]={"type":[dato["type"]],
                                 "currency_salary":[dato["currency_salary"]],
                                 "salary_from":[dato["salary_from"]],
                                 "salary_to":[dato["salary_to"]]}
    return EmpTypesDic

def Tempmultilocation(multilocationDic, dato):
    if dato["id"] in multilocationDic:
        multilocationDic[dato["id"]]["sedes_city"].append(dato["city"])
        multilocationDic[dato["id"]]["sedes_street"].append(dato["street"])
    else:
        multilocationDic[dato["id"]]={"sedes_city":[dato["city"]],
                                 "sedes_street":[dato["street"]]}
    return multilocationDic

#########################################
# Funciones para agregar informacion al modelo  
#########################################

def addjobs(catalog, SkillsDic, EmpTypesDic, multilocationDic):
    rates = {"USD":1,"PLN":0.25,"EUR":1.07,"GBP":1.24,"CHF":1.10}
    """
    rates = {"USD":1}
    getrates(rates,"PLN")
    getrates(rates,"EUR")
    getrates(rates,"GBP")
    getrates(rates,"CHF")
    """
    for i in range(1,lt.size(catalog["jobs"])+1):
        dato = lt.getElement(catalog["jobs"],i)
        ID = dato["id"]
        count = 0
        suma_from = 0
        suma_to = 0
        for j in range(0,len(EmpTypesDic[ID]["salary_from"])):
            count = count+1
            if EmpTypesDic[ID]["salary_from"][j] != "":
                suma_from = suma_from + int(EmpTypesDic[ID]["salary_from"][j])
                suma_to = suma_to + int(EmpTypesDic[ID]["salary_to"][j])
        if EmpTypesDic[ID]["salary_from"] != [""]:
            promedio_from = suma_from/count
            promedio_to = suma_to/count
            EmpTypesDic[ID]["currency_promedio"] = EmpTypesDic[ID]["currency_salary"][0]
            EmpTypesDic[ID]["promedio_from"] = promedio_from
            EmpTypesDic[ID]["promedio_to"] = promedio_to
            
            #CONVERSION MONEDAS
            #salary_from
            if isinstance(EmpTypesDic[ID]["salary_from"], list):
                for l in range(len(EmpTypesDic[ID]["salary_from"])):
                    EmpTypesDic[ID]["salary_from"][l] = convert_to_usd(rates, EmpTypesDic[ID]["salary_from"][l], ((EmpTypesDic[ID]["currency_salary"][l]).upper()))
            else:
                EmpTypesDic[ID]["salary_from"]= convert_to_usd(rates, EmpTypesDic[ID]["salary_from"], ((EmpTypesDic[ID]["currency_salary"]).upper()))
            #salary_to
            if isinstance(EmpTypesDic[ID]["salary_to"], list):
                for l in range(len(EmpTypesDic[ID]["salary_to"])):
                    EmpTypesDic[ID]["salary_to"][l] = convert_to_usd(rates, EmpTypesDic[ID]["salary_to"][l], ((EmpTypesDic[ID]["currency_salary"][l]).upper()))
            else:
                EmpTypesDic[ID]["salary_to"]= convert_to_usd(rates, EmpTypesDic[ID]["salary_to"], ((EmpTypesDic[ID]["currency_salary"]).upper()))
            #promedio_from
            EmpTypesDic[ID]["promedio_from"]= convert_to_usd(rates, EmpTypesDic[ID]["promedio_from"], ((EmpTypesDic[ID]["currency_promedio"]).upper()))
            #promedio_to
            EmpTypesDic[ID]["promedio_to"]= convert_to_usd(rates, EmpTypesDic[ID]["promedio_to"], ((EmpTypesDic[ID]["currency_promedio"]).upper()))
            
        else:
            EmpTypesDic[ID]["currency_promedio"] = "Unknown"
            EmpTypesDic[ID]["promedio_from"] = "Unknown"
            EmpTypesDic[ID]["promedio_to"] = "Unknown"
        dato.update(SkillsDic[ID])
        dato.update(EmpTypesDic[ID])
        dato.update(multilocationDic[ID])
        for key in dato:
            if dato[key] == "":
                dato[key] = "Unknown"
            elif type(dato[key]) == list:
                for k in range(0,len(dato[key])):
                    if dato[key][k] == "":
                        dato[key][k] = "Unknown"
        lt.changeInfo(catalog["jobs"],i,dato)
        addcountry_Experience(catalog,dato["country_code"],dato)
        add_firstLevel_pubAt(catalog,dato["published_at"],dato) #* Esta vaina mete los tres niveles consecuentemente
        addcity_Workplace(catalog,dato["city"],dato)
        addcompanysize_skill(catalog,dato["company_size"],dato)
        addsalary(catalog, dato)
    return catalog

def addcountry_Experience(catalog,country,dato):
    country_Experience = catalog["country_Experience"]
    existcountry = mp.contains(country_Experience, country)
    if existcountry:
        entry = mp.get(country_Experience, country)
        Value = me.getValue(entry)
    else:
        Value = {"jobs":None,"Experience":None}
        Value["jobs"] = lt.newList(datastructure="ARRAY_LIST")
        Value["Experience"] = mp.newMap(numelements=11,
                                        maptype="PROBING",
                                        loadfactor=0.5)
        mp.put(country_Experience,country,Value)
    lt.addLast(Value["jobs"],dato)
    addExperience(Value,dato)
    
    
def addExperience(Value,dato):
    existExperience = mp.contains(Value["Experience"], dato["experience_level"])
    if existExperience:
        entry = mp.get(Value["Experience"], dato["experience_level"])
        lista = me.getValue(entry)
    else:
        lista = lt.newList(datastructure="ARRAY_LIST")
        mp.put(Value["Experience"],dato["experience_level"],lista)
    lt.addLast(lista,dato)
    
def add_firstLevel_pubAt(catalog,publishedAt,dato):
    pubAt = catalog["published_at"]
    ## Accedemos al RBT de fecha de publicación
    existsDate = om.contains(pubAt, publishedAt)
    ## Revisamos si ya existe la fecha
    if existsDate:
        # Si existe sacamos el valor correspodniente
        entry = om.get(pubAt, publishedAt)
        Value = me.getValue(entry)
    else:
        # Si no, creamos el "Valor"
        Value = {"jobs":None,"salary":None,"country":None}
        
        # El valor es un diccionario con la lista de jobs interna a esa fecha
        ## y se crea el siguiente nivel con los diccionarios internos de salary y country
        
        Value["jobs"] = lt.newList(datastructure="ARRAY_LIST")
        # Poner el nuevo diccionario de valores en el mapa ordenado
        om.put(pubAt,publishedAt,Value)
        #* Crear los mapas dónde se pondrá información en el siguiente nivel:
        Value['salary'] = om.newMap(omaptype="RBT", cmpfunction= SalaryCompare)
        Value['salary'] = om.newMap(omaptype="RBT", cmpfunction= SalaryCompare)
        Value['country'] = mp.newMap(maptype="PROBING", loadfactor=0.5)
    lt.addLast(Value["jobs"],dato)
    # Agregar el dato a la lista correspondiente a ese valor
    #* Llamar a la función para agregar datos de segundo nivel
    add_secondLevel_pubAt(Value,dato)
    return None
def SalaryCompare(Salary1, Salary2):
    if isinstance(Salary1, list):
        try:
            for sal in Salary1:
                sal = float(sal)
            Salary1 = min(Salary1)
        except:
            Salary1 = Salary1[0]
    if isinstance(Salary2, list):
        try:
            for sal in Salary2:
                sal = float(sal)
            Salary2 = min(Salary2)
        except:
            Salary2 = Salary2[0]
    try: 
        Salary1, Salary2 = float(Salary1), float(Salary2)
        if Salary1 == Salary2:
            return 0
        if Salary1 < Salary2:
            return -1
        else:
            return 1
    except:
        return 1
#* Función de comparación Salarios

    
def SalaryCompare2(Salary1, Salary2):
    Salary1, Salary2 = float(Salary1), float(Salary2)
    if Salary1 == Salary2:
        return 0
    if Salary1 < Salary2:
        return -1
    else:
        return 1
    


def add_secondLevel_pubAt(Value,dato):
    # Dónde 'Value' es el diccionario del tipo {"jobs":None,"salary":[ORDERED MAP],"country":{'countryHM': None, 'experience': None, 'workplace_type': None, 'skill_name': None}}
    salaryMap = Value['salary'] ##* Sacamos el mapa de salarios
    #* Parte 1 del nivel : Agregar valores al mapa de Salary
    # Extraer valores del dato
    salary = dato['salary_from']
    ## Accedemos al mapa de salario
    existsSalary = om.contains(salaryMap, salary)
    ## Revisamos si ya existe la fecha
    if existsSalary:
        # Si existe sacamos el valor correspodniente
        entry = om.get(salaryMap, salary)
        Value_salary = me.getValue(entry) #Esto es una lista
    else:
        # Si no, creamos el "Valor"
        # Dentro de salary habrá solamente una lista de datos que corresponde al salario
        Value_salary = lt.newList(datastructure="ARRAY_LIST")
        om.put(salaryMap,salary,Value_salary)
    #Value_salary es una lista con los datos que cumplen con la fecha Y el salario.
    lt.addLast(Value_salary,dato) 
    
    #* Parte 2 del nivel : Agregar valores al mapa de Country
    countryMap = Value['country']
    # Extraer valores del dato
    country = dato['country_code']
    ## Accedemos al mapa de salario
    existCountry = mp.contains(countryMap, country)
    ## Revisamos si ya existe la fecha
    if existCountry:
        # Si existe sacamos el valor correspodniente
        entry = mp.get(countryMap, country)
        Value_country = me.getValue(entry) #Esto es una dic de mapas
    else:
        # Si no, creamos el "Valor"
        # Dentro de 
        Value_country = {'jobs':None,'experience': None, 'workplace_type': None, 'skill_name': None}
        Value_country["jobs"] = lt.newList(datastructure="ARRAY_LIST")
        Value_country["experience_level"] = mp.newMap(maptype="PROBING", loadfactor=0.5)
        Value_country["workplace_type"] = mp.newMap(maptype="PROBING", loadfactor=0.5)
        Value_country["skill_name"] = mp.newMap(maptype="PROBING", loadfactor=0.5)
        mp.put(countryMap,country,Value_country)
    #Value_country es una lista con todos los valores que cumplen la fecha Y el País
    lt.addLast(Value_country["jobs"],dato) 
    
    #* Crear los mapas del siguiente nivel

    #* Llamar a la función para agregar datos de tercer nivel
    add_ThirdLevel_pubAt(Value_country,dato)
    return None


def add_ThirdLevel_pubAt(Value,dato):
    experienceMap = Value["experience_level"]
    experienceMap = Value["experience_level"]
    wpTypeMap = Value["workplace_type"]
    skillNameMap = Value["skill_name"]
    
    #* Parte 1 del nivel : Agregar valores al mapa de experience
    # Extraer valores del dato
    experience = dato['experience_level']
    existsExperience = mp.contains(experienceMap, experience)
    ## Revisamos si ya existe la experiencia
    if existsExperience:
        # Si existe sacamos el valor correspodniente
        entry = mp.get(experienceMap, experience)
        Value_experience = me.getValue(entry) #Esto es una lista
    else:
        # Si no, creamos el "Valor"
        # Dentro del valor sólo habrá una array list con todos los que cumplan
        Value_experience = lt.newList(datastructure="ARRAY_LIST")
        mp.put(experienceMap,experience,Value_experience)
    #Value_experience es una lista con los datos que cumplen con la fecha Y el país Y el salario.
    lt.addLast(Value_experience,dato) 
    
    #* Parte 2 del nivel : Agregar valores al mapa de wpTypeMap
    # Extraer valores del dato
    WpType = dato['workplace_type']
    existsWpType = mp.contains(experienceMap, WpType)
    ## Revisamos si ya existe el tipo
    if existsWpType:
        # Si existe sacamos el valor correspodniente
        entry = mp.get(wpTypeMap, WpType)
        Value_WpType = me.getValue(entry) #Esto es una lista
    else:
        # Si no, creamos el "Valor"
        # Dentro del valor sólo habrá una array list con todos los que cumplan
        Value_WpType = lt.newList(datastructure="ARRAY_LIST")
        mp.put(wpTypeMap,WpType,Value_WpType)
    #WpType es una lista con los datos que cumplen con la fecha Y el país Y la experiencia.
    lt.addLast(Value_experience,dato) 
    #* Parte 3 del nivel : Agregar valores al mapa de skillNameMap
    # Extraer valores del dato

    skillName = dato['skill_name'] 
    for i in range(0,len(skillName)):
        dato2 = dato.copy() #se copia para que no se modifiquen los datos del for
        dato2["skill_name"]=skillName[i]
        dato2["skill_level"]=dato["skill_level"][i]
        existsSkillName = mp.contains(skillNameMap, dato2["skill_name"])
        ## Revisamos si ya existe el tipo
        if existsSkillName:
            # Si existe sacamos el valor correspodniente
            entry = mp.get(skillNameMap, dato2["skill_name"])
            Value_SkillName = me.getValue(entry)
        else:
            # Si no, creamos el "Valor"
            # Dentro del valor sólo habrá una array list con todos los que cumplan
            Value_SkillName = lt.newList(datastructure="ARRAY_LIST")
            mp.put(skillNameMap,skillName[i],Value_SkillName)
        #Value_SkillName es una lista con los datos que cumplen con la fecha Y el país Y la experiencia.
        lt.addLast(Value_SkillName,dato2)
    return None


def addcity_Workplace(catalog,city,dato):
    city_Workplace = catalog["city_Workplace"]
    existcity = mp.contains(city_Workplace, city)
    if existcity:
        entry = mp.get(city_Workplace, city)
        Value = me.getValue(entry)
    else:
        Value = {"jobs":None,"Workplace":None}
        Value["jobs"] = lt.newList(datastructure="ARRAY_LIST")
        Value["Workplace"] = mp.newMap(numelements=3,
                                        maptype="PROBING",
                                        loadfactor=0.5)
        mp.put(city_Workplace,city,Value)
    lt.addLast(Value["jobs"],dato)
    addWorkplace(Value,dato)
    
def addWorkplace(Value,dato):
    existWorkplace = mp.contains(Value["Workplace"], dato["workplace_type"])
    if existWorkplace:
        entry = mp.get(Value["Workplace"], dato["workplace_type"])
        lista = me.getValue(entry)
    else:
        lista = lt.newList(datastructure="ARRAY_LIST")
        mp.put(Value["Workplace"],dato["workplace_type"],lista)
    lt.addLast(lista,dato)
    
def addcompanysize_skill(catalog,companysize,dato):
    companysize_skill = catalog["companysize_skill"]
    existcompanysize = om.contains(companysize_skill,companysize)
    if existcompanysize:
        entry = om.get(companysize_skill,companysize)
        Value = me.getValue(entry)
    else:
        Value = {"jobs":None,"Skill_level":None}
        Value["jobs"] = lt.newList(datastructure="ARRAY_LIST")
        Value["Skill_level"] = mp.newMap(numelements=7,
                                maptype="CHAINING",
                                loadfactor=4)
        mp.put(companysize_skill,companysize,Value)
    for i in range(0,len(dato["skill_level"])):
        dato2 = dato.copy() #se copia para que no se modifiquen los datos del for
        dato2["skill_name"]=dato["skill_name"][i]
        dato2["skill_level"]=dato["skill_level"][i]
        lt.addLast(Value["jobs"],dato2)
        existskilllevel = mp.contains(Value["Skill_level"], dato2["skill_level"])
        if existskilllevel:
            entry = mp.get(Value["Skill_level"], dato2["skill_level"])
            lista = me.getValue(entry)
        else:
            lista = lt.newList(datastructure="ARRAY_LIST")
            mp.put(Value["Skill_level"],dato2["skill_level"],lista)
        lt.addLast(lista,dato2)
        

def addsalary(catalog, oferta):
    #Ignora los unknown
    if "Unknown" not in oferta["salary_from"]:

        minimo_valor = oferta["salary_from"][0]

        for minimo in oferta["salary_from"]: 
            if minimo < minimo_valor:
                minimo_valor = minimo
                    
        exist_salary = om.contains(catalog["salary_min"], minimo)
        if exist_salary:
            entry = om.get(catalog["salary_min"],minimo)
            lista = me.getValue(entry)
        else:
            lista = lt.newList(datastructure="ARRAY_LIST")
            om.put(catalog["salary_min"], minimo, lista)
        lt.addLast(lista, oferta)
        om.put(catalog["salary_min"], minimo, lista) 
   

#*########################################
#*######## Funciones de consulta
#*########################################

def req_1(control,fecha_inicial,fecha_final):
    """
    Función que soluciona el requerimiento 1
    """
    mapafechas=control["published_at"]
    print("Altura: " + str(om.height(mapafechas))) ##! I Did what needed to be done. TEMP / TEMPORAL / REMOVE / QUITAR.
    print("Número de nodos: " +str(om.height(mapafechas))) ##! TEMP / TEMPORAL / REMOVE / QUITAR.
    print("Número de nodos: " +str(om.size(mapafechas))) ##! TEMP / TEMPORAL / REMOVE / QUITAR.
    print("Número de elementos: " +str(lt.size(control["jobs"]))) ##! TEMP / TEMPORAL / REMOVE / QUITAR.
    listavalues = om.values(mapafechas,fecha_inicial,fecha_final)
    lista = lt.newList("ARRAY_LIST")
    for dato in lt.iterator(listavalues):
        for datoinside in lt.iterator(dato["jobs"]):
            lt.addLast(lista,datoinside)
    cantidad_ofertas = lt.size(lista)
    return cantidad_ofertas, lista


def req_2(control, salario_min, salario_max):
    """
    Función que soluciona el requerimiento 2
    """
    catalog= control["model"]
    valores = om.values(catalog["salary_min"], salario_min, salario_max)
    ofertas_listas = lt.newList("ARRAY_LIST")
    for lista in lt.iterator(valores):
        for dato in lt.iterator(lista):
            lt.addLast(ofertas_listas, dato)
    total_ofertas = lt.size(ofertas_listas)
    return ofertas_listas, total_ofertas


def req_3(control, n, CountryCode, ExpLvl):
    #* Sacar el mapa de País/Experiencia
    country = control['country_Experience']
    CountryVals = me.getValue(om.get(country, CountryCode))
    # Sacar además los que tienen la experiencia  requerida de esos
    experience = CountryVals['Experience']
    experienceVals = me.getValue(om.get(experience, ExpLvl))
    #El número total de ofertas laborales publicadas para un país y que requieran un nivel de experiencia especifico
    totNum = lt.size(experienceVals)
    #Las N ofertas laborales publicadas más recientes que cumplan con las condiciones especificadas.
    sortRecent = Datesort(experienceVals)
    #uptoN = lt.subList(sortRecent, 1, n) #* Esto no va
    #Cada una de ofertas laborales debe desplegar la siguiente información:
    return totNum, sortRecent


def req_4(catalog, n, ciudad, trabajo_ubicacion):
    """
    Función que soluciona el requerimiento 4
    """
    info_ciudad = mp.get(catalog["city_Workplace"],ciudad)
    info_ciudad_value = me.getValue(info_ciudad)
    exist_Workplace = mp.contains(info_ciudad_value["Workplace"],trabajo_ubicacion)
    if exist_Workplace:
        entry = mp.get(info_ciudad_value["Workplace"],trabajo_ubicacion)
        lista_Workplace = me.getValue(entry)
    else:
        lista_Workplace = lt.newList(datastructure="ARRAY_LIST")
    cantidad_ofertas = lt.size(lista_Workplace)
    Datesort(lista_Workplace)
    if lt.size(lista_Workplace) >= n:
        lista_Workplace_red = lt.subList(lista_Workplace,1,lt.size(lista_Workplace))
    else:
        lista_Workplace_red = lista_Workplace
    return cantidad_ofertas, lista_Workplace_red


def req_5(control, size_min, size_max, nombre_habilidad, skill_min, skill_max):
    """
    Función que soluciona el requerimiento 5
    """
    catalog= control["model"]
    #Accede al mapa de company size
    hashmap_rango= om.values(catalog["companysize_skill"], size_min, size_max)
    #Accede al mapa de skills adentro de cpmany size
    valores_filtrados= lt.newList("ARRAY_LIST")
    for dato_lista_size in lt.iterator(hashmap_rango):
        for level_skill in lt.iterator(mp.keySet(dato_lista_size["Skill_level"])):
            #retorna las llaves (niveles del skill level)
            if int(skill_min) <= int(level_skill) <= int(skill_max):
                dato= mp.get(dato_lista_size["Skill_level"] ,level_skill)
                dato= me.getValue(dato)
                lt.addLast(valores_filtrados, dato)
    
    #valores_filtrados= me.getValue(valores_filtrados)
    #Obtener habilidad deseada
    valores_re_filtrados= lt.newList("ARRAY_LIST")
    for lista in (valores_filtrados["elements"]):
        #lista= me.getValue(lista)
        for oferta in (lista["elements"]):
            if oferta["skill_name"] == nombre_habilidad:
                lt.addLast(valores_re_filtrados, oferta)
    
    #Tamaño de ofertas que cumplen
    total_ofertas= lt.size(valores_re_filtrados)
      
    ofertas_listas= Datesort(valores_re_filtrados)
    
    return ofertas_listas, total_ofertas

def req_6(catalog, OldestDate, RecentDate, minSalary, maxSalary):
    """
    Función que soluciona el requerimiento 6
    """
    OldestDate, RecentDate = dt.strptime(OldestDate, '%Y-%m-%d'), dt.strptime(RecentDate, '%Y-%m-%d') # Manejo de Dechas
    OldestDate, RecentDate = dateMakeAware(OldestDate), dateMakeAware(RecentDate) # Agregar una hora UTC para comp
    OldestDate, RecentDate = str(OldestDate), str(RecentDate) # Covnertir a str para func de comparación (que convierte a oBJs dt)
    dateMap = catalog['published_at'] # Acceder al mapa de fechas
    #* Grab Values
    eleInDateRange = om.values(dateMap,OldestDate, RecentDate) # Sacar todos los valores en el intervalo de fechas
    bothCriteria = lt.newList('ARRAY_LIST') # Inicialización de lista
    MapaBothCriteria = mp.newMap(maptype='PROBING', loadfactor=0.5) ## Mapa para las que cumplen ambos criterios
    
    for eachlist in lt.iterator(eleInDateRange): #Para cada sub-lista en la lista de rango
        salaryMap = eachlist['salary'] # Acceder al sub-mapa que está en cada lista
        salaryInRange = om.values(salaryMap, minSalary, maxSalary) #Sacar el salario en el rango
        for salaryJob in lt.iterator(salaryInRange): # Para cada job dentro de salarios en rango
            for subsubele in lt.iterator(salaryJob): #Para cada sub-elemento dentro del rango
                lt.addLast(bothCriteria, subsubele) # Agrégelo a la lista de que cumple ambos criterios
                existsCity = mp.contains(MapaBothCriteria, subsubele['city']) # MAnejo de mapas
                if existsCity:
                    #GrabCity Key
                    CiList = me.getValue(mp.get(MapaBothCriteria, subsubele['city']))
                    lt.addLast(CiList, subsubele)
                else:
                    CiList = lt.newList('ARRAY_LIST')
                    mp.put(MapaBothCriteria, subsubele['city'], CiList) # Meter al mapa
                    CiList = me.getValue(mp.get(MapaBothCriteria, subsubele['city']))
                    lt.addLast(CiList, subsubele)
    #* Both Criteria es entonces una lista con todos los Jobs que Cumplen Ambos Criterios
    NumberoOfCriteria = lt.size(bothCriteria) # Contar total de Jobs que cumplen ambos criterios
    MapCounts = ContadorMapasNOList(bothCriteria, 'city') # Contador de mapas crea un mapa com {NomCiudad: <#Menciones>}
    TotalCities = mp.size(MapCounts) # Total de ciudad = total llaves en mapam contador
    SortedCities = sortCounterMapAscii(MapCounts) #* Single Linked ordenada de llaves (de Ciudades Alfabéticamente)
    TopCity = me.getKey(getMapStats2(MapCounts, 'max')) # Sacar la ciudad con más menciones usando el mapa contador
    TopCityInfo = me.getValue(mp.get(MapaBothCriteria, TopCity)) ## Sacar del mapa las que estan bajo la misma ciudad
    TopCityInfo = Datesort(TopCityInfo) # Organziar de acuerdo a fecha
    return NumberoOfCriteria, TotalCities, SortedCities, TopCity, TopCityInfo #* Top cityInfo es ARRAY_LIST

def dateMakeAware(dt_obj):
    return dt_obj.replace(tzinfo=timezone.utc)

def req_7(control, año, CODpais, propiedad_conteo):
    """
    Función que soluciona el requerimiento 7
    """
    #Se accede a published at
    fechas = control["published_at"]
    #Se obtienen los valores utiles de fechas  
    fechas_util_Value = om.values(fechas, dt(int(año),1,1).isoformat(), dt(int(año),12,31,23,59,59).isoformat())
    #Se añaden los valores de los paises utiles y el tipo de propiedad de contero en una lista
    datosfinaleslist = lt.newList("ARRAY_LIST")
    Count = mp.newMap(numelements=6000,maptype="PROBING",loadfactor=0.5)
    sizebar = 0
    sizeaño = 0
    for values in lt.iterator(fechas_util_Value):
        countries = values["country"]
        existcountry = mp.contains(countries,CODpais)
        if existcountry:
            entry = mp.get(countries,CODpais)
            value = me.getValue(entry)
            if propiedad_conteo == "habilidad" or propiedad_conteo == "h":
                key = "skill_name"
                sizebar, sizeaño = listadder(datosfinaleslist, Count, value, key, sizebar, sizeaño)
            elif propiedad_conteo == "ubicación" or propiedad_conteo == "u":
                key = "workplace_type"
                sizebar, sizeaño = listadder(datosfinaleslist, Count, value, key, sizebar, sizeaño)
            elif propiedad_conteo == "experticia" or propiedad_conteo == "e":
                key = "experience_level"
                sizebar, sizeaño = listadder(datosfinaleslist, Count, value, key, sizebar, sizeaño)
    
    keysCount = mp.keySet(Count)
    valuesCount = mp.valueSet(Count)
    dicCount = {}
    for i in range(1,lt.size(keysCount)+1):
        dicCount[lt.getElement(keysCount,i)]=lt.getElement(valuesCount,i)
    
    mini, maxi = getMapStats(Count)
    
    return datosfinaleslist, sizeaño, sizebar, mini, maxi, dicCount, Count

def listadder(datosfinaleslist, Mapcontador, dato, key, sizebar, sizeaño):
    dato_parcial = dato[key]
    listinfo = dato["jobs"]
    for info in lt.iterator(listinfo):
        sizeaño = sizeaño + 1
        if key == "skill_name":
            lista = info[key]
            for i in range(0,len(lista)):
                llave = lista[i]
                entry = mp.get(dato_parcial,llave)
                VALUE = me.getValue(entry)
                for value in lt.iterator(VALUE):
                    lt.addLast(datosfinaleslist,value)
                    sizebar = sizebar + 1
                    existdato = mp.contains(Mapcontador,value[key])
                    if existdato:
                        entry = mp.get(Mapcontador, value[key])
                        dato = me.getValue(entry)
                    else:
                        dato = 0
                    dato = dato + 1
                    mp.put(Mapcontador,value[key],dato)
        else:
            lt.addLast(datosfinaleslist,info)
            sizebar = sizebar + 1
            existdato = mp.contains(Mapcontador,info[key])
            if existdato:
                entry = mp.get(Mapcontador, info[key])
                dato = me.getValue(entry)
            else:
                dato = 0
            dato = dato + 1
            mp.put(Mapcontador,info[key],dato)
    return sizebar, sizeaño

def req_8(catalogm):
    ##* Leer el Json
    filename = 'bono.json'
    with open(filename, 'r') as file:
        datos = json.load(file)
    catalog = catalogm["model"]
    ##* Lista de keep:
    keep = ["published_at","title","company_name","experience_level","country_code","city",
        "company_size","workplace_type","skill_name"]
    ##* Req 1 elementos
    req1 = req_1(catalog, datos['req_1_fecha1'], datos['req_1_fecha2'])
    req1 = req1[1]
    req1Pyli = req1['elements']
    mapReq1 = folium.Map(location=[0, 0], zoom_start=5)

    ##* Req 2 elememtnos
    req2= req_2(catalogm, datos['req_2_sal1'], datos['req_2sal2'])
    req2 = req2[0]
    req2Pyli = req2['elements']
    mapReq2 = folium.Map(location=[0, 0], zoom_start=5)

    ##* Req 3 elememtnos
    req3= req_3(catalog, 10 , datos['req_3_Country'], datos['req_3_experience'])
    req3 = req3[1]
    req3Pyli = req3['elements']
    mapReq3 = folium.Map(location=[0, 0], zoom_start=5)
    
    ##* Req 4 elememtnos
    req4= req_4(catalog, 10 , datos['req_4_city'], datos['req_4_loc'])
    req4 = req4[1]
    req4Pyli = req4['elements']
    mapReq4 = folium.Map(location=[0, 0], zoom_start=5)

    ##* Req 5 elememtnos
    req5= req_5(catalogm, datos['req_5_size1'], datos['req_5_size2'], datos['req_5_hab'], datos['req_5_lvl1'], datos['req_5_lvl2'])
    req5 = req5[0]
    req5Pyli = req5['elements']
    mapReq5 = folium.Map(location=[0, 0], zoom_start=5)
    
    ##* Req 6 elememtnos
    req6= req_6(catalog, datos['req_6_fecha1'], datos['req_6_fecha2'], datos['req_6_sal1'], datos['req_6_sal2'])
    req6 = req6[4]
    req6Pyli = req6['elements']
    mapReq6 = folium.Map(location=[0, 0], zoom_start=5)

    ##* Req 7 elememtnos
    req7 = req_7(catalog, datos['req_7_year'], datos['req_7_country'], datos['req_7_prop'])
    req7 = req7[0]
    req7Pyli = req7["elements"]
    mapReq7 = folium.Map(location=[0, 0], zoom_start=5)

    for item in req1Pyli:
        coords = (item['latitude'], item['longitude']) 
        popinf = FolKeepOnly(keep, item)
        folium.Marker(coords, popinf).add_to(mapReq1)
    mapReq1.save('output_req1.html')  

    for item in req2Pyli:
        coords = (item['latitude'], item['longitude']) 
        popinf = FolKeepOnly(keep, item)
        folium.Marker(coords, popinf).add_to(mapReq2)
    mapReq2.save('output_req2.html')  

    for item in req3Pyli:
        coords = (item['latitude'], item['longitude']) 
        popinf = FolKeepOnly(keep, item)
        folium.Marker(coords, popinf).add_to(mapReq3)
    mapReq3.save('output_req3.html') 
    
    for item in req4Pyli:
        coords = (item['latitude'], item['longitude']) 
        popinf = FolKeepOnly(keep, item)
        folium.Marker(coords, popinf).add_to(mapReq4)
    mapReq4.save('output_req4.html')    
    
    for item in req5Pyli:
        coords = (item['latitude'], item['longitude']) 
        popinf = FolKeepOnly(keep, item)
        folium.Marker(coords, popinf).add_to(mapReq5)
    mapReq5.save('output_req5.html') 
    
    for item in req6Pyli:
        coords = (item['latitude'], item['longitude']) 
        popinf = FolKeepOnly(keep, item)
        folium.Marker(coords, popinf).add_to(mapReq6)
    mapReq6.save('output_req6.html') 
    
    for item in req7Pyli:
        coords = (item['latitude'], item['longitude']) 
        popinf = FolKeepOnly(keep, item)
        folium.Marker(coords, popinf).add_to(mapReq7)
    mapReq7.save('output_req7.html') 
    

    return None

def FolKeepOnly(keep, dicti):
    ShapeShifterdic = {}
    retli = []
    for key in keep:
        ShapeShifterdic[key] =  dicti[key]

    return ShapeShifterdic

#*####################################################################################
#*##########################Funciones Contadores mapas
#*####################################################################################

def ContadorMapasNOList(lista,llave:str):
    Mapcontador = mp.newMap(numelements=2000,maptype="CHAINING",loadfactor=4)
    for i in lt.iterator(lista):
        sublist = i[llave]
        existdato = mp.contains(Mapcontador,sublist)
        if existdato:
            entry = mp.get(Mapcontador, sublist)
            dato = me.getValue(entry)
        else:
            dato = 0
        dato = dato + 1
        mp.put(Mapcontador,sublist,dato)
    return Mapcontador

def ContadorMapasList(lista,llave:str):
    Mapcontador = mp.newMap(numelements=11,maptype="PROBING",loadfactor=0.5)
    for i in lt.iterator(lista):
        sublist = i[llave]
        for j in lt.iterator(sublist):
            subsublist=j
            existdato = mp.contains(Mapcontador,subsublist)
            if existdato:
                entry = mp.get(Mapcontador,subsublist)
                dato = me.getValue(entry)
            else:
                dato = 0
            dato = dato + 1
            mp.put(Mapcontador,subsublist,dato)
    return Mapcontador
#*####################################################################################
#*##########################Funciones Contadores mapas
#*####################################################################################

def ContadorMapasNOList(lista,llave:str):
    Mapcontador = mp.newMap(numelements=2000,maptype="CHAINING",loadfactor=4)
    for i in lt.iterator(lista):
        sublist = i[llave]
        existdato = mp.contains(Mapcontador,sublist)
        if existdato:
            entry = mp.get(Mapcontador, sublist)
            dato = me.getValue(entry)
        else:
            dato = 0
        dato = dato + 1
        mp.put(Mapcontador,sublist,dato)
    return Mapcontador

def ContadorMapasList(lista,llave:str):
    Mapcontador = mp.newMap(numelements=11,maptype="PROBING",loadfactor=0.5)
    for i in lt.iterator(lista):
        sublist = i[llave]
        for j in lt.iterator(sublist):
            subsublist=j
            existdato = mp.contains(Mapcontador,subsublist)
            if existdato:
                entry = mp.get(Mapcontador,subsublist)
                dato = me.getValue(entry)
            else:
                dato = 0
            dato = dato + 1
            mp.put(Mapcontador,subsublist,dato)
    return Mapcontador

# Funciones utilizadas para comparar elementos dentro de una lista

def getMapStats(map):
    '''Basado en un mapa de conteo regresa la pareja llave valor con valor más alto y bajo
    IN: mapa OUT: tupla con pareja llave valor <k,v> correspondiente a min, max'''
    keySet = mp.keySet(map)
    mini = float('inf')
    minikv = None
    maxi = float('-inf')
    maxikv = None
    for key in lt.iterator(keySet):
        kvpair = mp.get(map, key)
        try:
            val = int(kvpair['value'])
        except ValueError:
            raise Exception("getMapStats - Solo compara valores numericos!")
        if val < mini:
            mini = val
            minikv = kvpair
        if val > maxi:
            maxi = val
            maxikv = kvpair
    return minikv, maxikv

def getMapStats2(map, stat='max'):
    '''Basado en un mapa de conteo regresa la pareja llave valor con valor más alto o bajo
    IN: mapa, stat ('min'o 'max') OUT: pareja llave valor <k,v> correspondiente a stat'''
    keySet = mp.keySet(map)
    mini = float('inf')
    minikv = None
    maxi = float('-inf')
    maxikv = None
    for key in lt.iterator(keySet):
        kvpair = mp.get(map, key)
        try:
            val = int(kvpair['value'])
        except ValueError:
            raise Exception("getMapStats - Solo compara valores numericos!")
        if stat == 'min':
            if val < mini:
                mini = val
                minikv = kvpair
        elif stat == 'max':
            if val > maxi:
                maxi = val
                maxikv = kvpair
        else:
            raise ValueError("getMapStats - stat debe ser 'min' o 'max'")
    if stat == 'min':
        return minikv
    elif stat == 'max':
        return maxikv

def keyCompare(Key1, Key2):
    Key1, Key2 = Key1.upper(), Key2.upper()
    return Key1 < Key2

    
def sortCounterMapAscii(map) -> dict:
    '''Recibe un mapa, regresa la lista de llaver ordenada alfabéticamente'''
    keySet = mp.keySet(map)
    SortedKeys = merg.sort(keySet, keyCompare)


    return SortedKeys
    
#*####################################################################################
#*##########################Funciones de ordenamiento
#*####################################################################################


def CompareDatesISO8601(Dic1, Dic2): 
    date1 = Dic1['published_at']
    date2 = Dic2['published_at']
    date1 = dt.fromisoformat(date1)
    date2 = dt.fromisoformat(date2)
    if date1 == date2:
        return None
    elif date1 > date2:
        return True
    elif date1 < date2  :
        return False

def CompareSalary(salary1, salary2):
    if salary1 > salary2:
        return False
    elif salary1 < salary2:
        return True
    else:
        None

def Datesort(lista):
    listaord = merg.sort(lista, CompareDatesISO8601)
    return listaord

def getrates(rates,currency):
    try:
        if currency not in rates.keys():
            #rates[currency]=CR().get_rate(currency,"USD")
            print('This functionality was removed for the Hall of Fame. Go to line 42 and line 979')
        return rates
    except:
        if currency == "PLN":
            rates[currency]=0.25
        elif currency == "EUR":
            rates[currency]=1.07
        elif currency == "GBP":
            rates[currency]=1.24
        elif currency == "CHF":
            rates[currency]=1.10

def convert_to_usd(rates, amount, currency):
    for current in rates:
        if currency == current:
            usd_amount = rates[current] * float(amount)
            break
        elif currency == "":
            usd_amount=""
    #c = CR()
    #usd_amount = c.convert(currency, 'USD', amount)
    return str(usd_amount)

#*####################################################################################
#*##########################Funciones Tabulate
#*####################################################################################
def declutterLoad3(sortedlist, Head):
    keep = ["published_at", "title", "company_name","experience_level", "country_code", "city"]
    if Head:
        HeadSublist = lt.subList(sortedlist, 1, 3)
        Heads = DicKeepOnly(keep, HeadSublist)
    elif not Head:
        Tmin = lt.size(sortedlist) - 2
        TailsSublist = lt.subList(sortedlist, Tmin, 3)
        Tails = DicKeepOnly(keep, TailsSublist)
    if Head:
        return Heads['elements']
    else:
        return Tails['elements']
    
def declutterLoad5(sortedlist, Head, keep):
    if Head:
        HeadSublist = lt.subList(sortedlist, 1, 5)
        Heads = DicKeepOnly(keep, HeadSublist)
    elif not Head:
        Tmin = lt.size(sortedlist) - 4
        TailsSublist = lt.subList(sortedlist, Tmin, 5)
        Tails = DicKeepOnly(keep, TailsSublist)
    if Head:
        return Heads['elements']
    else:
        return Tails['elements']

def declutterLoad_N(sortedlist, Head, keep, N):
    """
    Head=False -> Primeras N | Head=True -> Ultimas N
    """
    if Head:
        HeadSublist = lt.subList(sortedlist, 1, N)
        Heads = DicKeepOnly(keep, HeadSublist)
    elif not Head:
        Tmin = lt.size(sortedlist) - N
        TailsSublist = lt.subList(sortedlist, Tmin, N)
        Tails = DicKeepOnly(keep, TailsSublist)
    if Head:
        return Heads['elements']
    else:
        return Tails['elements']

def DicKeepOnly(keep, ARRAY_LIST):
    kept = lt.newList("ARRAY_LIST")
    for element in lt.iterator(ARRAY_LIST):
        dic = {}
        for key in keep:
            dic[key] =  element[key]
        lt.addLast(kept, dic)
    return kept

def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed