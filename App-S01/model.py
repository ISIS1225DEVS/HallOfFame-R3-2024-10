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

import copy
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
import datetime
import matplotlib.pyplot as plt
import numpy as np

import matplotlib as mpl

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""

# Construccion de modelos


def new_data_structs():
    data_struct={
    "job_offers": None,
    "employment_types" : None,
    "multilocations" : None,
    "skills" : None,
    "dateIndex": None,
    'req5':None,
    'req6':None
    }
   
    # g
    data_struct['job_offers']= lt.newList('ARRAY_LIST')
    data_struct['dateIndex'] = om.newMap(omaptype='RBT',
                                      cmpfunction=compareDates) # paramtros
    data_struct['dateIndex_exp'] = om.newMap(omaptype='RBT',
                                      cmpfunction=compareDates) # paramtros
    data_struct['req5'] = om.newMap(omaptype='RBT',
                                      cmpfunction=compareDates)
    data_struct['req6'] = om.newMap(omaptype='RBT',
                                      cmpfunction=compareDates) # compare company size
    data_struct['job_offer_id'] = mp.newMap(101503,
                                   maptype='CHAINING',
                                   loadfactor=2)
    data_struct['employment_types_id'] =mp.newMap(101503,
                                   maptype='CHAINING',
                                   loadfactor=2)
                                  # cmpfunction=compareemployment)
    data_struct['multilocation_id'] = mp.newMap(101503,
                                   maptype='CHAINING',
                                   loadfactor=2)
                                  # cmpfunction=comparemultilocation)
    data_struct['skills_id'] = mp.newMap(101503,
                                   maptype='CHAINING',
                                   loadfactor=2)
    data_struct['req_4'] = mp.newMap(numelements=3,maptype='CHAINING')
    
    data_struct['req_7']= mp.newMap(numelements=194)
    data_struct['req_7_skills'] = mp.newMap(numelements=194,maptype='CHAINING') #Existen 194 paises
    """
    Inicializa las estructuras de datos del modelo. Las crea de
    manera vacía para posteriormente almacenar la información.
    """
    #TODO: Inicializar las estructuras de datos
    
    return data_struct


# Funciones para agregar informacion al modelo

def add_job(data_structs, data):   
    """
    Función para agregar nuevos elementos a la lista
    """
    #TODO: Crear la función para agregar elementos a una lista
    for i in data:
        if data[i] == "":
            data[i] = "Desconocido"
    carga_req4(data_structs,data)
    lt.addLast(data_structs['job_offers'],data)
    update_date_index(data_structs['dateIndex'], data)
    mp.put(data_structs['job_offer_id'], data['id'], data)
    if not mp.contains(data_structs['req_7'],data['country_code']):
        mapa=mp.newMap(numelements=2)
        mapaxp=mp.newMap(numelements=5)
        mapubi=mp.newMap(numelements=5)
        mp.put(mapa,'ubi',mapubi)
        mp.put(mapa,'exp',mapaxp)
        mapubi,mapaxp=carga_7(mapubi,mapaxp)
        mp.put(data_structs['req_7'],data['country_code'],mapa)
    else:
        mapapais=me.getValue(mp.get(data_structs['req_7'], data['country_code']))
        mapaxp = me.getValue(mp.get(mapapais,'exp'))
        mapubi = me.getValue(mp.get(mapapais,'ubi'))
    
    mapubi,mapaxp=map_sorter(mapubi,mapaxp,data)
    
    if not mp.contains(data_structs['req_7_skills'],data['country_code']):
        mapapais2=mp.newMap(numelements=9)
        mp.put(data_structs['req_7_skills'],data['country_code'],mapapais2)
    else: 
        mapapais2=me.getValue(mp.get(data_structs['req_7_skills'],data['country_code']))
        
    mapapais2=aniosorter(mapapais2,data)
        
    return data_structs
def add_employment_types(data_structs,data):
    for i in data:
        if data[i] == "":
            data[i] = "Desconocido"
    mp.put(data_structs['employment_types_id'],data['id'],data)


def add_multilocation(data_structs, data):
    for i in data:
        if data[i] == "-":
            data[i] = "Desconocido"
    mp.put(data_structs['multilocation_id'], data['id'],data )

def add_skills(data_structs,data):
    for i in data:
        if data[i] == "":
            data[i] = "Desconocido"
    if not mp.contains(data_structs['skills_id'],data['id']):
        lista=lt.newList(datastructure="ARRAY_LIST")
        mp.put(data_structs['skills_id'], data['id'], lista)
    else:
        lista=me.getValue(mp.get(data_structs['skills_id'],data['id']))
    lt.addLast(lista,data)
    
def carga_req4(data_structs,data):
    occurreddate = data['published_at']
    jobdate =occurreddate
    data['published_at']=jobdate
    
    if not mp.contains(data_structs['req_4'],data['workplace_type']):
        mapa=mp.newMap(numelements=150000)
        mp.put(data_structs['req_4'],data['workplace_type'],mapa)
    else:
        mapa=me.getValue(mp.get(data_structs['req_4'],data['workplace_type']))
    if not mp.contains(mapa,data['city']):
        heap=mpq.newMinPQ(compareDatesHeap)
        mp.put(mapa,data['city'],heap)
        
    else:
        heap=me.getValue(mp.get(mapa,data['city']))
    mpq.insert(heap,data)
    #Esta carga entra en req 4 que es un mapa y aca adentro busca si el workplace ya est como llave, si no esta crea una llave con el nombre de workplace type 
    #Una vez que ya esta en la llave de workplace type busca en un nuevo mapa que esta asociado a esta llave la ciudad, si no esta la crea
    #Asociada a cada llave esta asociado un heap, esto es para que la busqueda de N ofertas sea mucho mas rapida
    
    
    

def add_req5 (datastructs, data_skill):
    
    data = me.getValue(mp.get(datastructs['job_offer_id'],data_skill['id']))
    if 'skills' not in data:
        skills = data_skill['name']
        data['skills']= skills
    else: 
        data['skills'] += " , "
        data['skills'] += data_skill['name']
        
    req5 = datastructs['req5']
    if data['company_size'] == 'Undefined':
        data['company_size'] = 0
    if not om.contains(req5, int(data['company_size'])):
        lista = lt.newList()
        arbol_nivel = om.newMap(omaptype='RBT',
                                      cmpfunction=compareDates)
        skill = mp.newMap()
        om.put(arbol_nivel,data_skill['level'], lista)
        mp.put(skill, data_skill['name'],arbol_nivel)
        om.put(req5, int(data['company_size']), skill)
    else: 
        skill = me.getValue(om.get(req5, int(data['company_size'])))
        if not mp.contains(skill, data_skill['name']):
            
            lista = lt.newList()
            arbol_nivel = om.newMap(omaptype='RBT',
                                      cmpfunction=compareDates)
            om.put(arbol_nivel,data_skill['level'], lista )
            mp.put(skill, data_skill['name'],arbol_nivel)
        else:
            arbol_nivel = me.getValue(mp.get(skill, data_skill['name']))
            if not om.contains(arbol_nivel, data_skill['level']):
                lista = lt.newList()
                om.put(arbol_nivel, data_skill['level'], lista)
            else:
                arbol_nivel = me.getValue(mp.get(skill, data_skill['name']))
            if not om.contains(arbol_nivel, data_skill['level']):
                lista = lt.newList()
                om.put(arbol_nivel, data_skill['level'], lista)
            else:
                lista = me.getValue(om.get(arbol_nivel, data_skill['level']))
    lt.addLast(lista, data)


def add_req_6_nuevo(data_structs, data_emloy):
    ids = data_emloy['id']
    data = me.getValue(mp.get(data_structs['job_offer_id'], ids))
    if data_emloy['currency_salary'] == "Desconocido" or data_emloy['salary_from'] == 'Desconocido':
        salario_min = 0
    else:
        salario_min =salario(data_emloy['currency_salary'],data_emloy['salary_from'])
    data['salary'] = salario_min
    arbol_fechas = data_structs['req6']
    occurreddate = data['published_at']
    ciudad = data['city']
    fecha = datetime.datetime.strptime(occurreddate, "%Y-%m-%dT%H:%M:%S.%fZ")
    if not om.contains(arbol_fechas, fecha.date()):
        arbol_salario = om.newMap(omaptype='RBT',
                                       cmpfunction=compareDates)
        mapa_ciudades = mp.newMap()
        lista_ofertas = lt.newList()
        om.put(arbol_fechas, fecha.date(), arbol_salario)
        om.put(arbol_salario, salario_min, mapa_ciudades)
        mp.put(mapa_ciudades, ciudad, lista_ofertas)
    else:
        arbol_salario = me.getValue(om.get(arbol_fechas, fecha.date()))
        if not om.contains(arbol_salario, salario_min):
            lista_ofertas = lt.newList()
            mapa_ciudades = mp.newMap()
            mp.put(mapa_ciudades, ciudad, lista_ofertas )
            om.put(arbol_salario, salario_min, mapa_ciudades)
        else:
            mapa_ciudades = me.getValue(om.get(arbol_salario, salario_min))
            if not mp.contains(mapa_ciudades,ciudad):
                lista_ofertas = lt.newList()
                mp.put(mapa_ciudades, ciudad, lista_ofertas)
            else:
                lista_ofertas = me.getValue(mp.get(mapa_ciudades, ciudad))
            
    lt.addLast(lista_ofertas, data)
    
def salario(currency, money):
    plata = int(money)
    if currency == 'usd':
        plata = plata
    elif currency == 'eur':
        plata = plata*1.07
    elif currency == 'pln':
        plata = plata* 0.25
    else:
        plata =0
    return plata
        



def update_date_index(map, data):
    jobdate = data['published_at']
    
    if not om.contains(map, jobdate):
        date_entry = lt.newList()
        lt.addLast(date_entry, data)
        om.put(map,jobdate, date_entry )
    else:
        date_entry = me.getValue(om.get(map, jobdate))
        lt.addLast(date_entry,data)
    return map

def carga_7(ubi,xp):
    mp.put(xp,'junior', mp.newMap(numelements=10))
    mp.put(xp,'mid', mp.newMap(numelements=10))
    mp.put(xp,'senior', mp.newMap(numelements=10))
    mp.put(ubi,'office', mp.newMap(numelements=10))
    mp.put(ubi,'remote', mp.newMap(numelements=10))
    mp.put(ubi,'partly_remote', mp.newMap(numelements=10))
    return ubi,xp
def map_sorter(mapubi,mapaexp,data):
    ubica=me.getValue(mp.get(mapubi,data['workplace_type']))
    anio=data['published_at']
    exp=me.getValue(mp.get(mapaexp,data['experience_level']))
    if type(anio) != 'datetime.datetime':
        anio=datetime.datetime.strptime(anio, "%Y-%m-%dT%H:%M:%S.%fZ")
    anio=anio.year
    anio=str(anio)
    if not mp.contains(exp,anio):
        listaexp=lt.newList(datastructure="ARRAY_LIST")
        mp.put(exp,anio,listaexp)
    else:
        listaexp=me.getValue(mp.get(exp,anio))
    lt.addLast(listaexp,data)
    if not mp.contains(ubica,anio):
        listaubica=lt.newList(datastructure="ARRAY_LIST")
        mp.put(ubica,anio,listaubica)
    else:
        listaubica=me.getValue(mp.get(ubica,anio))
    lt.addLast(listaubica,data)
    return mapubi,mapaexp
def aniosorter(mapapais2,data):
    anio=data['published_at']
    if type(anio) != 'datetime.datetime':
        anio=datetime.datetime.strptime(anio, "%Y-%m-%dT%H:%M:%S.%fZ")
    anio=anio.year
    anio=str(anio)
    if not mp.contains(mapapais2,anio):
        lista=lt.newList(datastructure="ARRAY_LIST")
        mp.put(mapapais2,anio,lista)
    else:
        lista=me.getValue(mp.get(mapapais2,anio))
    lt.addLast(lista,data['id'])
    return mapapais2


def add_req6(map,data):
    pass

    

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


def req_1(data_structs, keylo, keyhi):
    """
    Función que soluciona el requerimiento 1
    """
    # TODO: Realizar el requerimiento 1
    keylo = datetime.strptime(keylo, "%Y-%m-%d").date()
    keyhi = datetime.strptime(keyhi, "%Y-%m-%d").date()
    mapa = data_structs['dateIndex']
    # comentario date time
    lista_return = lt.newList('ARRAY_LIST')
    lista_valores = om.values(mapa, keylo, keyhi)
    for valor in lt.iterator(lista_valores):
        for job in lt.iterator(valor):
            lt.addLast(lista_return, job)
            # tal vez sort
    return lt.size(lista_return), first_last(lista_return, ['published_at','city', 'country_code', 'title','workplace_type', 'experience_level', 'company_size', 'company_name', 'skills'])


def req_2(data_structs):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    pass


def req_3(data_structs):
    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3
    pass


def req_4(data,n,ciudad,ubi):
    info=data['req_4']
    info=me.getValue(mp.get(info,ubi))
    info=me.getValue(mp.get(info,ciudad))
    tamanio=mpq.size(info)
    retorno=lt.newList(datastructure='ARRAY_LIST')
    for i in range (0,int(n)):
        oferta=mpq.delMin(info)
        lt.addLast(retorno,oferta)
        id=oferta['id']
        salariomin=me.getValue(mp.get(data['employment_types_id'],id))['salary_from']
        oferta['salario']=salariomin
        skills=(me.getValue(mp.get(data['skills_id'],id)))
        skills=skills_to_str(skills)
        oferta['skills']=skills
    retorno=first_last(retorno,['published_at','title','company_name','experience_level','country_code','city','company_size','workplace_type','salario','skills'])
    return retorno,tamanio




    
    
    
def req_5(data_structs, mincomp,maxcomp, skill, minskill, maxskill):
    peso  = 0
    arbol = data_structs['req5']
    mincomp = int(mincomp)
    maxcomp = int(maxcomp)
    lista_return = lt.newList()
    lista_val = om.values(arbol, mincomp,maxcomp)
    for tablas in lt.iterator(lista_val):
        arbol_it = mp.get(tablas, skill)
        if not arbol_it is None:
            arbol_it = me.getValue(arbol_it)
            listas_datos = om.values(arbol_it,om.minKey(arbol_it), om.maxKey(arbol_it))
            for niveles in lt.iterator(listas_datos):
                peso += lt.size(niveles)
            lista_niveles = om.values(arbol_it,minskill,maxskill)
            for lista in lt.iterator(lista_niveles):
                for oferta in lt.iterator(lista):
                    lt.addLast(lista_return, oferta)
                
                
                
    return peso , first_last(lista_return,['published_at','city','title', 'country_code', 'skills','company_name','company_size','experience_level','salary']) , lt.size(lista_return,)
        

def req_6(data_structs, fechaInicial, fechaFinal, salarioMin, salarioMax):
   """
   Función que soluciona el requerimiento 6
   """
   # TODO: Realizar el requerimiento 6
   salarioMax = int(salarioMax)
   salarioMin = int(salarioMin)
   arbol_fechas=data_structs["req6"]
   diccionario_ciudades=om.newMap(omaptype="RBT", cmpfunction=compareDates)
   fechaInicial=datetime.strptime(fechaInicial, "%Y-%m-%d").date()
   fechaFinal=datetime.strptime(fechaFinal, "%Y-%m-%d").date()
   arboles_salario=om.values(arbol_fechas, fechaInicial, fechaFinal)
   max_ofertas=0
   max_ciudad=None
   cantidad_ofertas=0
   for arbol in lt.iterator(arboles_salario):
       mapas_ciudades=om.values(arbol,salarioMin,salarioMax)
       for mapa_ciudad in lt.iterator(mapas_ciudades):
           for ciudad in lt.iterator(mp.keySet(mapa_ciudad)):
               entry=om.get(diccionario_ciudades,ciudad)
               if entry==None:
                   lst=lt.newList()
                   om.put(diccionario_ciudades, ciudad, lst)
               else:
                   lst=me.getValue(entry)
               ofertas=me.getValue(mp.get(mapa_ciudad, ciudad))
               for oferta in lt.iterator(ofertas):
                   lt.addLast(lst,oferta)
               cantidad_ofertas+=lt.size(ofertas)
               if lt.size(lst)>max_ofertas:
                   max_ofertas=lt.size(lst)
                   max_ciudad=ciudad
   ciudades_ordenadas=om.keySet(diccionario_ciudades)
   lista_de_ciudades=lt.newList(datastructure="ARRAY_LIST")
   for ciudad in lt.iterator(ciudades_ordenadas):
       lt.addLast(lista_de_ciudades, ciudad)
   cantidad_ciudades=om.size(diccionario_ciudades)
   lista_ofertas_max_ciudad=me.getValue(om.get(diccionario_ciudades, max_ciudad))
   return cantidad_ofertas, cantidad_ciudades,lista_de_ciudades,first_last(lista_ofertas_max_ciudad, ['published_at','city','company_name','country_code','experience_level','title','skills','salary',]), max_ciudad



        
        


def req_7(data_structs):
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Realizar el requerimiento 7
    pass
def req7noskill(data_strcucts,anio,pais,crit):
    maxi=0
    mini=9999999999999
    ofertas=[]
    if crit=='workplace_type':
        key_word='ubi'
    else:
        key_word='exp'
    dicci=data_strcucts['model']['req_7']
    dicci=me.getValue(mp.get(dicci,pais))
    dicci=me.getValue(mp.get(dicci,key_word))
    tamanio=mp.size(dicci)
    headers=lt.newList(datastructure='ARRAY_LIST')
    for nombre in lt.iterator(mp.keySet(dicci)):
        encabezado=me.getKey(mp.get(dicci,nombre))
        lt.addLast(headers,encabezado)
    values=lt.newList(datastructure='ARRAY_LIST')
    for nombre in lt.iterator(mp.keySet(dicci)):
        valor=me.getValue(mp.get(dicci,nombre))
        valor=me.getValue(mp.get(valor,anio))
        valor=req7aux(valor,param=['published_at','title','company_name','country_code','city','company_size'],salario=True,data=data_strcucts)
        ofertas=ofertas+list(lt.iterator(valor))
        valor=lt.size(valor)
        if valor> maxi:
            maxi=valor
            maxim=me.getKey(mp.get(dicci,nombre))
        if valor<mini:
            mini=valor
            minim=me.getKey(mp.get(dicci,nombre))
        lt.addLast(values,valor)
    return headers,values,tamanio,maxi,maxim,mini,minim,ofertas
        
        
def req7skill(control,anio,pais):
    ofertas=[]
    data_structs=control['model']
    dicci0=data_structs['req_7']
    dicci0=me.getValue(mp.get(dicci0,pais))
    dicci0=me.getValue(mp.get(dicci0,'exp'))
    for oferta in lt.iterator(mp.keySet(dicci0)):
        valor=me.getValue(mp.get(dicci0,oferta))
        valor=me.getValue(mp.get(valor,anio))
        valor=req7aux(valor,param=['published_at','title','company_name','country_code','city','company_size'],salario=True,data=control)
        ofertas=ofertas+list(lt.iterator(valor))
    dicci=data_structs['req_7_skills']
    dicci=me.getValue(mp.get(dicci,pais))
    lista=me.getValue(mp.get(dicci,anio))
    tamanio=lt.size(lista)
    dictreto=mp.newMap(numelements=400)
    headers=lt.newList(datastructure="ARRAY_LIST")
    values=lt.newList(datastructure="ARRAY_LIST")
    maxi=0
    mini=9999999999999
    for i in range(1,lt.size(lista)):
        iD=lt.getElement(lista,i)
        lista_skill=me.getValue(mp.get(data_structs['skills_id'],iD))
        for j in range(1,lt.size(lista_skill)):
            skill=lt.getElement(lista_skill,j)
            skill=skill['id']
            if not mp.contains(dictreto,skill):
                mp.put(dictreto,skill,1)
            else:
                mp.put(dictreto,skill,(me.getValue(mp.get(dictreto,skill)))+1)
    for nombre in lt.iterator(mp.keySet(dictreto)):
        encabezado=me.getKey(mp.get(dictreto,nombre))
        lt.addLast(headers,encabezado)
    for nombre in lt.iterator(mp.keySet(dictreto)):
        valor=me.getValue(mp.get(dictreto,nombre))
        if valor> maxi:
            maxi=valor
            maxim=me.getKey(mp.get(dictreto,nombre))
        if valor<mini:
            mini=valor
            minim=me.getKey(mp.get(dictreto,nombre))
        lt.addLast(values,valor) 
    return headers,values,tamanio,maxi,maxim,mini,minim,ofertas
            
            
        
        

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


def sort(data_structs):
    """
    Función encargada de ordenar la lista con los datos
    """
    #TODO: Crear función de ordenamiento
    pass

def compareDates(date1, date2):
    """
    Compara dos fechas
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1
    
def tabulator(ultimos, i, primeros):
    # Esta parte le suma a primeros los primeros
    primeros_dict = mp.newMap(numelements=7,maptype="PROBING")
    ultimos_dict = mp.newMap(numelements=7,maptype="PROBING") 
    primeroc=copy.deepcopy(lt.getElement(primeros,i))
    ultimosc=copy.deepcopy(lt.getElement(ultimos,i))
    del primeroc['street']
    del primeroc['address_text']
    del primeroc['marker_icon']
    del primeroc['workplace_type']
    del primeroc['company_url']
    del primeroc['company_size']
    del primeroc['remote_interview']
    del primeroc['open_to_hire_ukrainians']
    del primeroc['display_offer']

    
    
    del ultimosc['street']
    del ultimosc['address_text']
    del ultimosc['marker_icon']
    del ultimosc['workplace_type']
    del ultimosc['company_url']
    del ultimosc['company_size']
    del ultimosc['remote_interview']
    del ultimosc['open_to_hire_ukrainians']
    del ultimosc['display_offer']
    
    lt.changeInfo(ultimos,i,ultimosc)
    lt.changeInfo(primeros,i,primeroc)



def first_last(lista,param=['published_at','city', 'country_code', 'title'],salario=False,data=None):
    res = lt.newList()
    if salario:
        data=data['model']
    if lt.size(lista)> 6:
        first = lt.subList(lista, 1, 3)
        last = lt.subList(lista, lt.size(lista)-2,3)
        for dato in lt.iterator(first):
            dic = {}
            for i in param:
                dic[i] = dato[i]
            if salario:
                salariomin=me.getValue(mp.get(data['employment_types_id'],dato['id']))['salary_from']
                dic['salario']=salariomin
            lt.addLast(res, dic)
        for dato in lt.iterator(last):
            dic = {}
            for i in param:
                dic[i] = dato[i]
            lt.addLast(res, dic)
    else:
        for dato in lt.iterator(lista):
            dic = {}
            for i in param:
                dic[i] = dato[i]
            if salario:
                data=data['model']
                salariomin=me.getValue(mp.get(data['employment_types_id'],dato['id']))['salary_from']
                dic['salario']=salariomin
            lt.addLast(res, dic)
    return res
        
    
def req7aux(lista,param=['published_at','city', 'country_code', 'title'],salario=False,data=None):
    res = lt.newList()
    if salario:
        data=data['model']
    if lt.size(lista)> 6:
        for dato in lt.iterator(lista):
            dic = {}
            for i in param:
                dic[i] = dato[i]
            if salario:
                salariomin=me.getValue(mp.get(data['employment_types_id'],dato['id']))['salary_from']
                dic['salario']=salariomin
            lt.addLast(res, dic) 
    return res      

def compareDatesHeap(date1, date2):
    """
    Compara dos fechas
    """
    date1=date1['published_at']
    date2=date2['published_at']
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1
def skills_to_str(lista):
    if lt.isEmpty(lista):
        return "Ninguno"
    else:
        retorno=""
        tamanio = lt.size(lista)
        for i in range(1,tamanio):
            retorno= retorno + " " + str(lt.getElement(lista,i)['name'])
        return retorno