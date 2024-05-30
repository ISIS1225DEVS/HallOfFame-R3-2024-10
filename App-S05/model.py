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
from DISClib.Utils import error as error
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
    
    data_struct = {"arbolReq1": None,
                'arbolReq2': None,
                'tablaReq37': None,
                'tablaReq4': None,
                'tablaReq5': None,
                'tablaReq6': None,
               'tabla_skillsID': None,
               'tabla_employmentTypesID': None,
               "tabla_multilocationID":None,
               
               }
    
        
    data_struct['arbolReq1'] = om.newMap(omaptype='RBT', cmpfunction=defaultfunction_invertida)

    data_struct['arbolReq2'] = om.newMap(omaptype='RBT', cmpfunction=None)

    data_struct["tablaReq4"]=mp.newMap(100000,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   cmpfunction=compare_mapId)

    data_struct["tablaReq5"]=mp.newMap(100000,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   cmpfunction=compare_mapId)

    data_struct["tablaReq5"]=mp.newMap(100000,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   cmpfunction=compare_mapId)
    
    data_struct["tablaReq37"]=mp.newMap(2,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   cmpfunction=compare_mapId)

    data_struct['tablaReq6'] = mp.newMap(200000,
                                         maptype='PROBING',
                                         loadfactor=0.5,
                                         cmpfunction=compare_mapId)
    
    data_struct["tabla_skillsID"] = mp.newMap(400000,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   cmpfunction=compare_mapId)

    data_struct['tabla_multilocationID'] = mp.newMap(200937,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   cmpfunction=compare_mapId)
    
    data_struct['tabla_employmentTypesID'] = mp.newMap(244937,
                                   maptype='CHAINING',
                                   loadfactor=4,
                                   cmpfunction=compare_mapId)
    
    
    return data_struct




# Funciones para agregar informacion al modelo

def add_data(data_structs, data):
    """
    Función para agregar nuevos elementos a la lista
    """
    #TODO: Crear la función para agregar elementos a una lista
    pass

def add_arbolReq1(data_struct, job):
    mapa=data_struct["arbolReq1"]
    updateArbolDias(mapa, job)
    pass

def add_arbolReq2(data_struct, job):
    mapa=data_struct["arbolReq2"]
    updateArbolSalario(mapa, job)
    pass

def add_tablaReq4(data_struct, job):

    ciudad = job["city"]
    work_type  = job["workplace_type"]

    if ciudad == "":
        ciudad="Undefined"

    #Chequeo si existe la ciudad en la tabla 
    existPais=mp.contains(data_struct["tablaReq4"], ciudad)
    #Si ya existe el pais cojo el value de ese pais
    if existPais:
        entryCity = mp.get(data_struct["tablaReq4"], ciudad)
        cityValue = me.getValue(entryCity)
    #Si no existe creo un nuevo key, value pair 
    else:
        cityValue = newCityValueWorkType(ciudad)
        mp.put(data_struct["tablaReq4"], ciudad, cityValue)


    #Chequeo si el nivel que quiero añadir existe dentro de ese pais
    existWorkType = mp.contains(cityValue["workplace_type"], work_type)
    #Si si existe cojo ese experience level
    if existWorkType:
        entryWorkType = mp.get(cityValue["workplace_type"], work_type)
        #Cojo el value de ese entry
        workTypeValue = me.getValue(entryWorkType)
    #Si no existe creo un nuevo key, value pair
    else:
        workTypeValue = newWorkTypeValue(work_type)
        mp.put(cityValue["workplace_type"], work_type, workTypeValue)
    #Añado a la lista de trabajos de ese experience level 

    
    addJob_arbolFechaxSalario(workTypeValue["arbol"], job)
        
    pass


def newCityValueWorkType(ciudad):
    entry = {'city': "", "workplace_type": None}
    entry['city'] = ciudad
    entry['workplace_type'] = mp.newMap(numelements=3, maptype="PROBING", loadfactor=0.5, 
                            cmpfunction=compare_mapId)
    return entry

def newWorkTypeValue(work_type):
    entry = {"workplace_type": "", "arbol": None}
    entry["workplace_type"] = work_type
    entry["arbol"] = om.newMap(omaptype='RBT', cmpfunction=defaultfunction_invertida)
    
    return entry

def add_tablaReq5(data_struct, job):
    
    salaryKey=str(job["salary_from"])
    #Cambio el salario para que quede con 3 cifras para la llave
    while len(salaryKey)<6:
        salaryKey="0"+salaryKey
    jobKey=job["published_at"]+"X"+salaryKey+"X"+job["id"]
    
    #Cambio el company size para que tenga 7 cifras o ---- si es undefined
    if job["company_size"]=="Undefined":
        comp_size="------"
    else:
        comp_size=job["company_size"].zfill(7)
            
    empresaKey=comp_size
                    
    for skill in lt.iterator(job["skills"]):
        skillName=skill["name"]
        skill_level=skill["level"]
        
        if mp.contains(data_struct["tablaReq5"], skillName):
            parejaSkill = mp.get(data_struct["tablaReq5"], skillName)
            arbolNiveles = me.getValue(parejaSkill)
        else:
            arbolNiveles=om.newMap(omaptype="RBT")
            mp.put(data_struct["tablaReq5"], skillName, arbolNiveles)

        parejaArbolEmpresas=om.get(arbolNiveles, skill_level)

        if parejaArbolEmpresas is None:         
            arbolEmpresas=om.newMap(omaptype="RBT")
            om.put(arbolNiveles, skill_level, arbolEmpresas)
        else:
            arbolEmpresas=me.getValue(parejaArbolEmpresas)
        
        pareja_listaJobs=om.get(arbolEmpresas, empresaKey)
        
        if pareja_listaJobs is None: 
            listaJobs=lt.newList("ARRAY_LIST")
            om.put(arbolEmpresas, empresaKey, listaJobs)
        else:
            listaJobs=me.getValue(pareja_listaJobs)

        lt.addLast(listaJobs, (jobKey, job))

    pass        

def add_tablaReq37(data_struct, job):
    
    salaryKey=str(job["salary_from"])
    #Cambio el salario para que quede con 3 cifras para la llave
    while len(salaryKey)<6:
        salaryKey="0"+salaryKey
    jobKey=job["published_at"]+"X"+salaryKey+"X"+job["id"]
    
    fecha=job["published_at"].split("T")
    fecha2=fecha[0].split("-")
    yearKey=fecha2[0]
    countryKey=job["country_code"]
    #Para que no vaya a sacar error con los trabajos que no tienen nada en pais
    if countryKey == "":
        countryKey="Undefined"

    #Saco el valor del año
    entry = mp.get(data_struct["tablaReq37"], yearKey)
    #Si si existe cojo el value de ese año
    if entry is None:
        yearValue = newAnioValue(yearKey)
        mp.put(data_struct["tablaReq37"], yearKey, yearValue)
    #Si no existe creo una nueva key,value pair
    else:
        yearValue = me.getValue(entry)
    #Le sumo 1 a las ofertas totales del años
    yearValue["ofertas_totales"]+=1
    
    #Saco el valor del pais dentro de ese año
    tablaPaises=yearValue["paises"]
    paisPareja = mp.get(tablaPaises, countryKey)
    #Si si existe cojo el value de ese año
    if paisPareja is None:
        paisValue = newPaisValue(countryKey)
        mp.put(tablaPaises, countryKey, paisValue)
    #Si no existe creo una nueva key,value pair
    else:
        paisValue = me.getValue(paisPareja)
    #Le sumo 1 a las ofertas totales del país
    paisValue["ofertas_totales"]+=1
    
    if lt.size(job["skills"])>0:
        #Le sumo 1 a las ofertas totales que seran usadas para los skills
        paisValue["ofertas_totales_skills"]+=1
    
                    
    #Añado a la tabla de experiencia de ese país en ese año en el trabajo
    expPareja = mp.get(paisValue["tabla_experience_levels"], job["experience_level"])
    if expPareja is None:
        expValue = newExpValue(job["experience_level"])
        mp.put(paisValue["tabla_experience_levels"], job["experience_level"], expValue)
    else:
        expValue = me.getValue(expPareja)
    
    arbolJobs=expValue["jobs"]
    om.put(arbolJobs, jobKey, job)
    lt.addLast(expValue["jobs_lista"], (jobKey,job))

    
    #Añado a la tabla de habilidades
    for skill in lt.iterator(job["skills"]):
        skillName=skill["name"]
        
        skillPareja = mp.get(paisValue["tabla_skills"], skillName)
        if skillPareja is None:
            skillValue = newSkillValueReq7(skillName)
            mp.put(paisValue["tabla_skills"],skillName, skillValue)
        else:
            skillValue = me.getValue(skillPareja)
        
        lt.addLast(skillValue["jobs_lista"], (jobKey,job))
        
    if lt.size(job["skills"])>0:
        lt.addLast(paisValue["lista_jobs_skills"], (jobKey,job))
        
        
    #Añado a la tabla de ubicacion
    parejaUbicacion = mp.get(paisValue["tabla_workplace_type"], job["workplace_type"])
    if parejaUbicacion is None:
        ubicacionValue = newUbicacionValueReq7(job["workplace_type"])
        mp.put(paisValue["tabla_workplace_type"], job["workplace_type"], ubicacionValue)
    else:
        ubicacionValue = me.getValue(parejaUbicacion)
    
    lt.addLast(ubicacionValue["jobs_lista"], (jobKey,job))

    
    pass        

def add_tablaReq6(data_struct, job):
    """
    Agrega un trabajo al Requisito 6 con una estructura anidada que incluye una tabla de hash para 'Ciudad'
    con árboles rojo-negros para 'Salarios', 'Fecha Y-M-D', y 'Hora, Salario, id'.
    """
    city = job['city']
    salary = str(job['salary_from']).zfill(6)  # Aseguro que el salario tenga 6 dígitos
    date = job['published_at'].split('T')[0]
    time = job['published_at'].split('T')[1]
    job_id = job['id']


    # Obtener o inicializar el árbol de salarios para la ciudad dada
    salary_tree = get_or_create_rbt_MP(data_struct['tablaReq6'], city,  defaultfunction_invertida)

    # Obtener o inicializar el árbol de fechas para el salario dado
    date_tree = get_or_create_rbt_OM(salary_tree, salary, defaultfunction_invertida)

    # Obtener o inicializar el árbol de hora-salario-id para la fecha dada
    hour_salary_id_tree = get_or_create_rbt_OM(date_tree, date, defaultfunction_invertida)

    # Crear una clave única para hora-salario-id
    hour_salary_id_key = str(time) + "-" + str(salary) + "-" + str(job_id)

    # Insertar la información del trabajo
    om.put(hour_salary_id_tree, hour_salary_id_key, job)


def get_or_create_rbt_MP(map, key,cmpfunction):
    """
    Obtiene o crea un árbol rojo-negro para la clave dada en una tabla de hash.
    """
    entry = mp.get(map, key)
    if entry is None:
        # Si la entrada no existe, crea un nuevo árbol rojo-negro
        tree = om.newMap(omaptype='RBT', cmpfunction=cmpfunction)
        mp.put(map, key, tree)
    else:
        # Si la entrada existe, obtiene el árbol existente
        tree = me.getValue(entry)
    return tree

def get_or_create_rbt_OM(map, key,cmpfunction):
    """
    Obtiene o crea un árbol rojo-negro para la clave dada en un mapa ordenado.
    """
    #TODO Dani: tuve que copy pastear esta función porque cuando se creal el arbol de fechas, se está haciendo
        #el .get sobre el arbol de salarios, no sobre una tabla de hash. Lo mismo para el arbol de trabajos
    entry = om.get(map, key)
    if entry is None:
        # Si la entrada no existe, crea un nuevo árbol rojo-negro
        tree = om.newMap(omaptype='RBT', cmpfunction=cmpfunction)
        om.put(map, key, tree)
    else:
        # Si la entrada existe, obtiene el árbol existente
        tree = me.getValue(entry)
    return tree

def add_tabla_multilocationID(data_struct, job):
    mp.put(data_struct['tabla_multilocationID'], job['id'], job)


def add_tabla_employmentTypesID(data_struct, employType):
    #Cambio de divisa
        
    if  employType["currency_salary"] == "pln":
        employType["salary_from"] = round(float(employType["salary_from"]) * 0.25)
        employType["salary_to"] = round(float(employType["salary_to"]) * 0.25)

    elif  employType["currency_salary"] == "gbp":
        employType["salary_from"] = round(float(employType["salary_from"]) * 1.24)
        employType["salary_to"] = round(float(employType["salary_to"]) * 1.24)


    elif  employType["currency_salary"] == "eur":
        employType["salary_from"] =round(float(employType["salary_from"]) * 1.07)
        employType["salary_to"] = round(float(employType["salary_to"]) * 1.07)


    elif  employType["currency_salary"] == "chf":
        employType["salary_from"] =round(float(employType["salary_from"]) * 1.10)
        employType["salary_to"] = round(float(employType["salary_to"]) * 1.10)   
        
    mp.put(data_struct['tabla_employmentTypesID'], employType['id'], employType)
    
    
def add_tabla_skillsID(data_struct, skill):
    id = skill["id"]

    if mp.contains(data_struct["tabla_skillsID"], id):
        entrySkill = mp.get(data_struct["tabla_skillsID"], id)
        listSkills = me.getValue(entrySkill)
        lt.addLast(listSkills["skills"], skill)
    else:
        listSkills=newSkillsValue(id)
        mp.put(data_struct["tabla_skillsID"], id, listSkills)
        lt.addLast(listSkills["skills"], skill)


def add_arbolxHorarioxSalario():
    pass
    
def updateArbolDias(map, job):

    fechaHora = job["published_at"].split("T")
    fechaYMD=fechaHora[0]
    #Busco el día en el arbol
    entry = om.get(map, fechaYMD)
    
    if entry is None:
        #Si el día no existo añado el arbol del día
        arbolJobs = om.newMap(omaptype="RBT", cmpfunction=defaultfunction_invertida)
        om.put(map, fechaYMD, arbolJobs)
    else:
        arbolJobs = me.getValue(entry)
    
    #Le añado a ese arbol el trabajo
    addJobInd_arbolHoraxSalario(arbolJobs, job)
    
    return map

def updateArbolSalario (map, job):
    salarioKey=str(job["salary_from"])
    
    #Cambio el salario para que quede con 6 cifras para la llave

    salarioKey=salarioKey.zfill(6)

    entry = om.get(map, salarioKey)

    if entry is None: 
        #Si el árbol del salario existe
        arbolJobs = om.newMap(omaptype="RBT", cmpfunction=defaultfunction_invertida)
        om.put(map, salarioKey, arbolJobs)
    else:
        arbolJobs = me.getValue(entry)

    addSubArbol_fechas(arbolJobs, job)
    return map

def tablaToArbolReq7(mapa, arbol, jobInd):
            
    #Recorro cada uno de los valores de categoria del pais
    for pos2 in range(lt.size(mapa['table'])):
        
        entryCategoria = lt.getElement(mapa['table'], pos2+1)
        
        if (entryCategoria['key'] is not None and entryCategoria['key'] != '__EMPTY__'):
            
            size=str(lt.size(entryCategoria["value"]["jobs_lista"]))
            name=entryCategoria['key']
                
            #Cambio la cantidad de trabajos para que quede con 7 cifras para la llave
            size=size.zfill(8)
                
            size_name=size+"X"+name
            
            if jobInd:
                om.put(arbol, size_name, entryCategoria["value"])
            else:
                om.put(arbol, size_name, "Cuervo")
    
    pass

def loadArbolReq7(data_struct):
    for year in lt.iterator(mp.valueSet(data_struct["tablaReq37"])):
        for paisValue in lt.iterator(mp.valueSet(year["paises"])):
            tablaToArbolReq7(paisValue["tabla_experience_levels"], paisValue["arbol_experience_levels"], True)
            tablaToArbolReq7(paisValue["tabla_workplace_type"], paisValue["arbol_workplace_type"], True)
            tablaToArbolReq7(paisValue["tabla_skills"], paisValue["arbol_skills"], False)
    
#◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤
# Funciones para creacion de datos
#◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤


def new_data(id, info):
    """
    Crea una nueva estructura para modelar los datos
    """
    #TODO: Crear la función para estructurar los datos
    pass

def newEmpresaValue(empresa):
    entry = {'id': "", "skills": None, "ofertas_totales":0}
    entry['id'] = id
    
    entry['skills'] =  mp.newMap(numelements=500, maptype="PROBING", loadfactor=0.5)
    
    return entry
    
def newSkillsValue(id):
    entry = {'id': "", "skills": None}
    entry['id'] = id
    
    entry['skills'] = lt.newList('SINGLE_LINKED')
    
    return entry

def newExpValue(exp):
    entry = {'experience': exp, "jobs": None}
    entry['jobs'] = om.newMap(omaptype="RBT")
    entry["jobs_lista"]=lt.newList("ARRAY_LIST")
    
    return entry

def newSkillValueReq7(exp):
    entry = {'skill': exp, "jobs": None}
    entry['jobs_lista'] = lt.newList("ARRAY_LIST")
    
    return entry

def newUbicacionValueReq7(exp):
    entry = {'ubicacion': exp, "jobs": None}
    entry['jobs_lista'] =lt.newList("ARRAY_LIST")
    
    return entry

def newPaisValue(countryKey):
    entry = {'pais': countryKey, "ofertas_totales_skills":0, "ofertas_totales":0}
    
    entry['tabla_experience_levels'] = mp.newMap(numelements=3, maptype="PROBING", loadfactor=0.5)
    entry['arbol_experience_levels'] = om.newMap(omaptype="RBT")

    entry['tabla_workplace_type'] = mp.newMap(numelements=3, maptype="PROBING", loadfactor=0.5)
    entry['arbol_workplace_type'] = om.newMap(omaptype="RBT")

    entry['tabla_skills'] = mp.newMap(numelements=100, maptype="PROBING", loadfactor=0.5)
    entry['arbol_skills'] = om.newMap(omaptype="RBT")
    entry['lista_jobs_skills'] = lt.newList("ARRAY_LIST")

    return entry

def newAnioValue(anio):
    entry = {'anio': "", "paises": None, "ofertas_totales":0}
    entry['anio'] = anio
    
    entry['paises'] = mp.newMap(numelements=150, maptype="CHAINING", loadfactor=4)
    return entry

def addJobInd_arbolHoraxSalario(arbol, job):
    fecha=job["published_at"].split("T")
    hora=fecha[1]
    salarioKey=str(job["salary_from"])
    
    #Cambio el salario para que quede con 6 cifras para la llave
    while len(salarioKey)<6:
        salarioKey="0"+salarioKey
    
    #Creo la llave que primero tiene hora, después el salario, y por último el id del trabajo
    key=hora+"X"+salarioKey+"X"+job["id"]
    
    #Cada hoja tiene un solo trabajo
    om.put(arbol, key, job)
    
    pass 

def addJob_arbolFechaxSalario(arbol, job):
    fecha=job["published_at"]
    salarioKey=str(job["salary_from"])
    
    #Cambio el salario para que quede con 6 cifras para la llave
    
    salarioKey = salarioKey.zfill(6)
    
    #Creo la llave que primero tiene hora, después el salario, y por último el id del trabajo
    key = fecha+"X"+salarioKey+"X"+job["id"]
    
    #Cada hoja tiene un solo trabajo
    om.put(arbol, key, job)
    
    pass

def addSubArbol_fechas(arbol, job):
    fechaKey = job["published_at"]
    key = fechaKey + "X" + job["id"]

    om.put(arbol, key, job)
    pass

#◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤
# Funciones de consulta
#◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤

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



def req_1(data_structs, fechai, fechaf):
    """
    Función que soluciona el requerimiento 1
    """
    # TODO: Realizar el requerimiento 1
    fechas_rango = om.values(data_structs["arbolReq1"], fechaf, fechai)

    list_final = lt.newList("ARRAY_LIST")

    for subarbol in lt.iterator(fechas_rango):
        valueSetList(subarbol, list_final)
    
    return list_final


def req_2(data_structs, salarioi, salariof):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    salarioi = salarioi.zfill(6)
    salariof = salariof.zfill(6)
    salario_rango = om.values(data_structs["arbolReq2"], salarioi, salariof)

    list_final = lt.newList("ARRAY_LIST")
    
    for subarbol in lt.iterator(salario_rango):
        valueSetList(subarbol, list_final)
    
    return list_final


def req_3(data_struct, N, country_code, experience_level):
    year_keys = om.keySet(data_struct['tablaReq37'])
    recent_jobs = lt.newList('ARRAY_LIST')

    years_list = lt.newList()
    for year in lt.iterator(year_keys):
        lt.addLast(years_list, year)
    
    # Ordenamos la lista de años en orden descendente 
    sa.sort(years_list, sort_crit_years)

    for year in lt.iterator(years_list):
        year_value = me.getValue(om.get(data_struct['tablaReq37'], year))
        country_map = year_value['paises']
        country_value = me.getValue(mp.get(country_map, country_code))

        if country_value:
            exp_tree = country_value['tabla_experience_levels']
            exp_value = me.getValue(mp.get(exp_tree, experience_level))

            if exp_value:
                jobs_tree = exp_value['jobs']
                jobs_keys = om.keySet(jobs_tree)

                jobs_list = lt.newList()
                for job_key in lt.iterator(jobs_keys):
                    lt.addLast(jobs_list, job_key)
                
                

                for job_key in lt.iterator(jobs_list):
                    if lt.size(recent_jobs) < N:
                        offer = me.getValue(om.get(jobs_tree, job_key))
                        lt.addLast(recent_jobs, offer)
                    else:
                        break

                if lt.size(recent_jobs) >= N:
                    break

    return recent_jobs


def req_4(data_structs, n, city, work_type):
    """
    Función que soluciona el requerimiento 4
    """
    # TODO: Realizar el requerimiento 4

    entryCity =  mp.get(data_structs["tablaReq4"], city)
    cityValue = me.getValue(entryCity)

    entryWorkType = mp.get(cityValue["workplace_type"], work_type)
    worktypeValue = me.getValue(entryWorkType)
    

    ofertas = om.valueSet(worktypeValue["arbol"])

    ofertasN = lt.newList("ARRAY_LIST")

    size = lt.size(ofertas)

    if lt.size(ofertas)>int(n):
        ofertasN=lt.subList(ofertas,1,int(n))

    else:
        ofertasN = ofertas


    a = [ofertasN, size]
    return a


def req_5(data_structs, numOfertas, minCompSize, maxCompSize, skill, minSkillLev, maxSkillLev):
    """
    Función que soluciona el requerimiento 5
    Los parámetros de entrada de este requerimiento son:
        • El número (N) de ofertas laborales para consulta.
        • El límite inferior del tamaño de la compañía.
        • El límite superior del tamaño de la compañía.
        • Nombre de la habilidad solicitada.
        • El límite inferior del nivel de la habilidad.
        • El límite superior del nivel de la habilidad.
        
    Retorna:
        • El número total de ofertas laborales publicadas para las compañías que tengan un tamaño en un rango y que requieran una habilidad específica.
        • Las N ofertas laborales publicadas más antiguas que cumplan con las condiciones especificadas.

    """
  
    
    arbolFinalJobs=om.newMap(omaptype="RBT")
    ofertas_totales=0
    
    #Saco los arboles de la habilidad requerida
    skillPareja=mp.get(data_structs["tablaReq5"], skill)
    arbolNiveles=me.getValue(skillPareja)
    
    #Saco los valores del arbol que están en el rango de nivel de habilidades pedido
    niveles=om.values(arbolNiveles, minSkillLev, maxSkillLev)
    
    #Itero por los arboles de las empresas en cada nivel para buscar las ofertas con los 
    # tamaños de empresa correctos:
    for arbolEmpresa in lt.iterator(niveles):
        minCompKey=minCompSize.zfill(7)
        maxCompKey=maxCompSize.zfill(7)
        lista_listasJobs=om.values(arbolEmpresa, minCompKey, maxCompKey)
        
        #Recorro cada lista de trabajos
        for listaJobs in lt.iterator(lista_listasJobs):
            
            #Recorro cada trabajo
            for jobTuple in lt.iterator(listaJobs):
                ofertas_totales+=1
                om.put(arbolFinalJobs, jobTuple[0], jobTuple[1])
                
    listaFinal=om.valueSet(arbolFinalJobs)
    
    if lt.size(listaFinal)>int(numOfertas):
        listaFinal=lt.subList(listaFinal,1,int(numOfertas))
        
    return listaFinal, ofertas_totales
    



def req_6(data_struct, N, start_date, end_date, min_salary, max_salary):
    city_offers_count = mp.newMap(numelements=N, maptype='PROBING', loadfactor=0.5, cmpfunction=compare_mapId)
    total_offers = 0

    # Recorro las ciudades y cuento las ofertas que cumplen con las especificaciones
    for city in lt.iterator(mp.keySet(data_struct['tablaReq6'])):
        city_entry = mp.get(data_struct['tablaReq6'], city)

        if city_entry is not None:
            salary_tree = me.getValue(city_entry)
            min_salaryKey=min_salary.zfill(6)
            max_salaryKey=max_salary.zfill(6)
            count = count_city_offers(salary_tree, start_date, end_date, min_salaryKey, max_salaryKey)

            if count > 0:
                mp.put(city_offers_count, city, count)
                total_offers += count
                

    # Creo una lista de tuplas (ciudad, conteo) 
    city_count_list = lt.newList('ARRAY_LIST')

    keySet=mp.keySet(city_offers_count)
    for cityKey in lt.iterator(keySet):
        pareja=mp.get(city_offers_count, cityKey)
        count = me.getValue(pareja)
        if count > 0:
            lt.addLast(city_count_list, (cityKey, count))
            
   
    city_count_list = sa.sort(city_count_list, sort_crit_cityJobSize)
    
    num_ciudades=lt.size(city_count_list)

    # Selecciono las N primeras ciudades de la lista ordenada
    top_cities = lt.subList(city_count_list , 1, N) if lt.size(city_count_list ) >= N else city_count_list
    top_city_details = None
    city_with_most_offers = lt.firstElement(top_cities)
    top_city_details = get_city_offer_details(data_struct, city_with_most_offers[0],start_date, end_date,min_salaryKey, max_salaryKey)

    #Ordeno alfabeticamente
    sortedalf_city_count_list = sa.sort(top_cities, sort_critJobs_ciudad_MenorMayor)

    answer=[total_offers, sortedalf_city_count_list, top_city_details, num_ciudades]
    return answer

#///////////////////////////////Funciones aux Req6//////////////////////////////////////////////////////////

def count_city_offers(salary_tree, start_date, end_date, min_salary, max_salary):
    """
    Cuenta las ofertas de trabajo por ciudad que cumplen con las especificaciones de fecha y salario.
    Args:
        salary_tree (RBT): Árbol rojo-negro con la información de salarios y fechas.
        start_date (str): Fecha de inicio para filtrar ofertas.
        end_date (str): Fecha de finalización para filtrar ofertas.
        min_salary (int): Salario mínimo para filtrar ofertas.
        max_salary (int): Salario máximo para filtrar ofertas.
    
    Returns:
        int: Número total de ofertas que cumplen con las especificaciones.
    """
    offer_count = 0
   
    # Itera a través de los rangos de salario que cumplen con las especificaciones.
    salary_range = om.values(salary_tree, max_salary, min_salary)
        #TODO Dani: tocaba cambiar el orden de max salary y min salary cuando se invoca la función porque tiene como 
            #cmpfunction el defaultfunction_invertido
        #Ten cuidado entonces con eso cuando vayas hacer values en get_city_offer_details
    for date_tree in lt.iterator(salary_range):
        # Itera a través de las fechas que cumplen con las especificaciones dentro de cada rango de salario.
        date_range = om.values(date_tree, end_date, start_date)
        for job_list in lt.iterator(date_range):
            # Cada nodo de este árbol contiene una lista de trabajos, por lo que sumamos la longitud de cada lista al conteo.
            offer_count += lt.size(job_list)
    return offer_count


def get_city_offer_details(data_struct, city_name, start_date, end_date,min_salary, max_salary):
    """
    Esta función recupera los detalles de las ofertas laborales de la ciudad
    con el mayor número de ofertas publicadas.
    """
    city_entry = mp.get(data_struct['tablaReq6'], city_name)
    all_offers = lt.newList('ARRAY_LIST') 

    if city_entry:
        salary_tree = me.getValue(city_entry)
        salary_range = om.values(salary_tree, max_salary, min_salary)

        
    for date_tree in lt.iterator(salary_range):
        date_range = om.values(date_tree, end_date, start_date)

        for hour_salary_id_tree in lt.iterator(date_range):
                
                for job_key in lt.iterator(om.keySet(hour_salary_id_tree)):
                    job = om.get(hour_salary_id_tree, job_key)['value']
                    lt.addLast(all_offers, job)

    if lt.size(all_offers) > 10:
        first_five = lt.subList(all_offers, 1, 5)
        last_five = lt.subList(all_offers, lt.size(all_offers) - 4, 5)
        # nueva lista con ultimos y primeros 5 
        top_city_details = lt.newList('ARRAY_LIST')
        for offer in lt.iterator(first_five):
            lt.addLast(top_city_details, offer)
        for offer in lt.iterator(last_five):
            lt.addLast(top_city_details, offer)
    else:
        top_city_details = all_offers

    return top_city_details
    


    

def req_7(data_structs, year, pais, propiedad):
    """
    Función que soluciona el requerimiento 7
    
    Parámetros de entrada de este requerimiento son:
        • El año relevante (en formato “%Y”).
        • Código del país para la consulta (ej.: PL, CO, ES, etc).
        • La propiedad de conteo (experticia, ubicación, o habilidad).

    Respuesta:
        • Número de ofertas laborales publicadas dentro del periodo anual.
        • Número de ofertas laborales publicadas utilizados para crear el gráfico de barras de la
        propiedad.
        • Valor mínimo y valor máximo de la propiedad consultada en el gráfico de barras.
        • El gráfico de barras con la distribución de las ofertas laborales publicadas según la propiedad.
        • Listado de las ofertas laborales publicadas que cumplen las condiciones de conteo para el gráfico
        de barras. 
    """
   
    #Saco el año que pidio el usuario
    yearPareja=mp.get(data_structs["tablaReq37"], year)
    yearValue=me.getValue(yearPareja)
    #Consigo el número de ofertas totales del año
    numJobsYear=yearValue["ofertas_totales"]
    
    #Consigo la info de ese pais
    paisPareja=mp.get(yearValue["paises"], pais)
    paisValue=me.getValue(paisPareja)
    
    #Depende de la propiedad edito el título del gráfico y escojo los arboles que voy acceder
    if propiedad=="ubicacion": 
        xLabel="Tipos de ubicaciones"
        title="Cantidad de ofertas por ubicaciones en "+pais+" "+year
        nombre_arbolPropiedad="arbol_workplace_type"
        numJobsGrafica=paisValue["ofertas_totales"]
        skillTF=False
    
    elif propiedad=="experticia":
        xLabel="Niveles de experticia"
        title="Cantidad de ofertas por niveles de experticia en "+pais+" "+year
        nombre_arbolPropiedad="arbol_experience_levels"
        numJobsGrafica=paisValue["ofertas_totales"]
        skillTF=False

    else:
        xLabel="Habilidades"
        title="Cantidad de ofertas por habilidades en "+pais+" "+year
        nombre_arbolPropiedad="arbol_skills"
        numJobsGrafica=paisValue["ofertas_totales_skills"]
        skillTF=True

    arbolPropiedad=paisValue[nombre_arbolPropiedad]
    
    jobsArbol=om.newMap(omaptype="RBT")
    data={}
    
    #Saco el mayor y menor valor de la propiedad
    max_key=om.maxKey(arbolPropiedad)
    MaxSplitKey=max_key.split("X")
    jobsMax=int(MaxSplitKey[0])
    maxValue=MaxSplitKey[1]+" con "+ str(jobsMax)+" trabajos"
    
    min_key=om.minKey(arbolPropiedad)
    minSplitKey=min_key.split("X")
    jobsMin=int(minSplitKey[0])
    minValue=minSplitKey[1]+" con "+ str(jobsMin)+" trabajos"
    
    
    data, jobsArbol=valueKeySet_Req7(arbolPropiedad["root"], data, jobsArbol, skillTF)
    
    if skillTF:
        for job in lt.iterator(paisValue["lista_jobs_skills"]):
            om.put(jobsArbol, job[0], job[1])
    
    jobsList=lt.newList("ARRAY_LIST")
    valueSetList(jobsArbol, jobsList)
    
    #Saco los valores para el eje x y y del gráfico
    propiedades = list(data.keys())
    totales_propiedades = list(data.values())
    
    infoGrafica=[propiedades, totales_propiedades, xLabel, title]

    answer=[numJobsYear, numJobsGrafica, infoGrafica, maxValue, minValue, jobsList]
    
    return answer
    
def valueKeySet_Req7 (root, kDicc, vTree, skillTF):
    """
    Construye una lista con los valores de la tabla y un diccionario para hacer un grafíco con las llaves
    Args:
        root: El arbol con los elementos
        klist: La lista de respuesta
    Returns:
        Una lista con todos las llaves
    Raises:
        Exception
    """
    if (root is not None):
        valueKeySet_Req7(root['left'], kDicc, vTree, skillTF)
        
        #Descompongo el key para sacar la propiedad y la cantidad de ofertas
        xSplitKey=root["key"].split("X")
        jobs=int(xSplitKey[0])
        propiedad=xSplitKey[1]
        kDicc[propiedad]=jobs
        
        #Añado al arbol de trabajos
        if not skillTF:
            for job in lt.iterator( root['value']["jobs_lista"]):
                om.put(vTree, job[0], job[1])
        
        valueKeySet_Req7(root['right'], kDicc, vTree, skillTF)
    return kDicc, vTree


def req_8(data_structs):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    pass



#Funciones aux Req1


def valueSetList(rbt, list):
    """
    Construye una lista con los valores de la tabla
    Args:
        rbt: La tabla con los elementos
    Returns:
        Una lista con todos los valores
    Raises:
        Exception
    """
    try:
        vlist = valueSetTree(rbt['root'], list)
        return vlist
    except Exception as exp:
        error.reraise(exp, 'RBT:valueSet')

def valueSetTree(root, klist):
    """
    Construye una lista con los valorers de la tabla
    Args:
        root: El arbol con los elementos
        klist: La lista de respuesta
    Returns:
        Una lista con todos los valores
    Raises:
        Exception
    """
    try:
        if (root is not None):
            valueSetTree(root['left'], klist)
            lt.addLast(klist, root['value'])
            valueSetTree(root['right'], klist)
        return klist
    except Exception as exp:
        error.reraise(exp, 'RBT:valueSetTree')


        
# Funciones utilizadas para comparar elementos dentro de una lista

def compare(data_1, data_2):
    """
    Función encargada de comparar dos datos
    """
    #TODO: Crear función comparadora de la lista
    pass

def cmpfunction(key1, key2):
    # Si ambas key son del mismo tipo, se comparan directamente
    if type(key1) == type(key2):
        if key1 < key2:
            return -1
        elif key1 > key2:
            return 1
        else:
            return 0
    # Si una key int y la otra es str, convierte ambas a str para la comparación
    else:
        str_key1 = str(key1)
        str_key2 = str(key2)
        if str_key1 < str_key2:
            return -1
        elif str_key1 > str_key2:
            return 1
        else:
            return 0

def OGcmpFunction(key1, key2):
    if key1 == key2:
        return 0
    elif key1 < key2:
        return -1
    else:
        return 1

def defaultfunction_invertida(key1, key2):
    if key1 == key2:
        return 0
    elif key1 > key2:
        return -1
    else:
        return 1

#◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤
# Funciones de ordenamiento
#◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤

def sort_crit_cityJobSize(ciudad1, ciudad2):
    """
    ordena por numOfertas por ciudad
    """
    if ciudad1[1]>ciudad2[1]:
        return True
    elif ciudad1[1]<ciudad2[1]:
        return False
    
def sort_critJobs_ciudad_MenorMayor(city1, city2):
    """
    ordena alfabeticamente
    """
    if city1[0] < city2[0]:
        return True
    elif city1[0] > city2[0]:
        return False
    
def sort_crit_years(year1, year2):
   
    return int(year2) - int(year1)

def sort_crit_dates(date1, date2):
    
    if date1 > date2:
        return -1
    elif date1 < date2:
        return 1
    else:
        return 0
    

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

def compare_mapId(ID, entry):

    ID_key= me.getKey(entry)
    if (ID == ID_key):
        return 0
    elif (ID > ID_key):
        return 1
    else:
        return -1
    
def defaultfunction_invertida(key1, key2):
    if key1 == key2:
        return 0
    elif key1 > key2:
        return -1
    else:
        return 1
