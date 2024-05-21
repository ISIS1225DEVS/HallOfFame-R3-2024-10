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
from collections import Counter
import matplotlib.pyplot as plt
from datetime import datetime
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
    catalog= { "major_structure"  : None,
              "size_empresas": None,
              "salaries_offers":None,
              "jobs_cd": None,
              "jobs":None,
              "employments_types" : None,
              "multilocations" : None,
              "skills" : None
              }

    #catalog['major_structure'] = om.newMap(omaptype="RBT", cmpfunction=cmpFunctionFechaRBT)
    catalog['major_structure'] = mp.newMap(numelements=500, maptype="CHAINING", loadfactor=0.5)
    catalog['size_empresas'] = om.newMap(omaptype="RBT", cmpfunction=cmpfunctionSizeEmpresas)
    catalog["salaries_offers"] = om.newMap(omaptype= "RBT", cmpfunction=cmpFunctionSalarioRBT)
    
    catalog["jobs_cd"] = lt.newList("ARRAY_LIST")
    
    catalog['jobs'] = om.newMap(omaptype="RBT", cmpfunction=cmpFunctionFechaRBT)
    catalog['multilocations'] = mp.newMap(numelements=67445, maptype="CHAINING", loadfactor= 4)
    catalog['employments_types'] = mp.newMap(numelements=64988, maptype="CHAINING", loadfactor= 4)
    catalog['skills'] = mp.newMap(numelements=144410, maptype="CHAINING", loadfactor= 4)
    
    
    return catalog

def cmpfunctionSizeEmpresas(size1, size2):
    if size1 == 'Undefined':
        size1 = 0
    if size2 == 'Undefined':
        size2 = 0
    size1 = int(size1)
    size2 = int(size2)
    if size1 == size2:
        return 0
    elif size1 > size2:
        return 1
    else:
        return -1
# Funciones para agregar informacion al modelo

def add_data(data_structs,part,  data, c):
    """
    Función para agregar nuevos elementos a la lista
    """
    #TODO: Crear la función para agregar elementos a una lista
    if part == "employments_types":
        
        key= f"{data['id']}"
       
    elif part == "jobs":
        lt.addLast(data_structs["jobs_cd"], data)
        offer = data
        offer['city'] = offer['city'].strip()
        if offer['city'][0] != offer['city'][0].upper():
            offer['city'] = f"{offer['city'][0].upper()}{offer['city'][1:]}"
        key = f"{data['id']}"
        
       
        
        exist_country = mp.contains(data_structs['major_structure'],offer["country_code"])
        if not exist_country:
            mp.put(data_structs["major_structure"], offer["country_code"], mp.newMap(numelements=1000, maptype="PROBING", loadfactor=0.5))
        exist_city = mp.contains(me.getValue(mp.get(data_structs["major_structure"], offer["country_code"])), offer["city"])
        if not exist_city:
            mp.put(me.getValue(mp.get(data_structs["major_structure"], offer["country_code"])), offer["city"], mp.newMap(numelements=1000, maptype="PROBING", loadfactor=0.5))

        exist_business = mp.contains(me.getValue(mp.get(me.getValue(mp.get(data_structs["major_structure"], offer["country_code"])), offer["city"])), offer["company_name"])
        if not exist_business:
            mp.put(me.getValue(mp.get(me.getValue(mp.get(data_structs["major_structure"], offer["country_code"])), offer["city"])), offer["company_name"], mp.newMap(numelements=7, maptype="PROBING", loadfactor=0-5))
            "cmpfunction pendiente"
            mp.put(me.getValue(mp.get(me.getValue(mp.get(me.getValue(mp.get(data_structs["major_structure"], offer["country_code"])),offer["city"])), offer["company_name"])),"senior", om.newMap(omaptype='RBT', cmpfunction=cmpFunctionFechaRBT))
            mp.put(me.getValue(mp.get(me.getValue(mp.get(me.getValue(mp.get(data_structs["major_structure"], offer["country_code"])),offer["city"])), offer["company_name"])),"mid", om.newMap(omaptype='RBT',cmpfunction=cmpFunctionFechaRBT))
            mp.put(me.getValue(mp.get(me.getValue(mp.get(me.getValue(mp.get(data_structs["major_structure"], offer["country_code"])),offer["city"])), offer["company_name"])),"junior", om.newMap(omaptype='RBT',cmpfunction=cmpFunctionFechaRBT))

            #Acceder al país
            #me.getValue(mp.get(data_structs["major_structure"],offer["country_code"]))
            #Acceder a ciudad
            #me.getValue(mp.get(me.getValue(mp.get(data_structs["major_structure"],offer["country_code"])),offer["city"]))
            #Acceder a una empresa
            #me.getValue(mp.get(me.getValue(mp.get(me.getValue(mp.get(data_structs["major_structure"],offer["country_code"])),offer["city"])),offer["company_name"]))
            #Acceder a nivel de experiencia
            #me.getValue(mp.get(me.getValue(mp.get(me.getValue(mp.get(me.getValue(mp.get(data_structs["major_structure"],offer["country_code"])),offer["city"])),offer["company_name"])),offer["experience_level"]))
        divisa_oferta = None
        salario_minimo = 0
        salario_promedio_oferta= 0
        for employment_type in lt.iterator(me.getValue(mp.get(data_structs["employments_types"], offer["id"]))):
            divisa_oferta = employment_type["currency_salary"]
            promedio_salarial = convertir_divisas(employment_type["promedio_salarial"], employment_type["currency_salary"],c)
            salary_from =  convertir_divisas(employment_type["salary_from"], employment_type["currency_salary"], c)
            salario_promedio_oferta +=  promedio_salarial/lt.size(me.getValue(mp.get(data_structs["employments_types"], offer["id"])))
            if salary_from != "":
                if salario_minimo == 0:
                    salario_minimo = salary_from
                if salary_from < salario_minimo:
                    salario_minimo = salary_from
        

            #if employment_type["promedio_salarial"] < salario_minimo:
            #    salario_minimo = employment_type["promedio_salarial"]
        data["salario_minimo"] = salario_minimo
        data["salario_promedio"] = salario_promedio_oferta
        habilidades_solicitadas = lt.newList("ARRAY_LIST")
        promedio_habilidades = 0
        for skill in lt.iterator(me.getValue(mp.get(data_structs["skills"], offer["id"]))):
            lt.addLast(habilidades_solicitadas, skill["name"])
            promedio_habilidades = int(skill["level"])/lt.size(me.getValue(mp.get(data_structs["skills"], offer["id"])))
        data["habilidades_solicitadas"] = habilidades_solicitadas
        data["promedio_habilidad"] = promedio_habilidades

        exist_salaryOffer = om.contains(data_structs["salaries_offers"], data["salario_minimo"])
        if not exist_salaryOffer:
            om.put(data_structs["salaries_offers"], data["salario_minimo"], lt.newList("ARRAY_LIST"))
        lt.addLast(me.getValue(om.get(data_structs["salaries_offers"], data["salario_minimo"])), offer)
        
            
        data["salario_minimo"] = salario_minimo
        data["salario_promedio"] = salario_promedio_oferta
        data["divisa_para_revertir"]  = divisa_oferta
        """
        if divisa_oferta != None:
            data["salario_minimo"] = revertir_divisas(salario_minimo, divisa_oferta, c)
            data["salario_promedio"] = revertir_divisas(salario_promedio_oferta, divisa_oferta, c)
        """
        
        exist_fecha = om.contains(me.getValue(mp.get(me.getValue(mp.get(me.getValue(mp.get(me.getValue(mp.get(data_structs["major_structure"],offer["country_code"]))
                                                                        ,offer["city"])),offer["company_name"])),offer["experience_level"])), offer["published_at"][:10])
        if not exist_fecha:
            om.put(me.getValue(mp.get(me.getValue(mp.get(me.getValue(mp.get(me.getValue(mp.get(data_structs["major_structure"],offer["country_code"]))
                                                                        ,offer["city"])),offer["company_name"])),offer["experience_level"])), offer["published_at"][:10], om.newMap(omaptype="RBT", cmpfunction=cmpFunctionSalarioRBT))

        exist_salary = om.contains(me.getValue(om.get(me.getValue(mp.get(me.getValue(mp.get(me.getValue(mp.get(me.getValue(mp.get(data_structs["major_structure"],offer["country_code"]))
                                                                        ,offer["city"])),offer["company_name"])),offer["experience_level"])), offer["published_at"][:10])),salario_minimo)
        if not exist_salary:
            om.put(me.getValue(om.get(me.getValue(mp.get(me.getValue(mp.get(me.getValue(mp.get(me.getValue(mp.get(data_structs["major_structure"],offer["country_code"]))
                                                                            ,offer["city"])),offer["company_name"])),offer["experience_level"])), offer["published_at"][:10])),salario_minimo, lt.newList("ARRAY_LIST"))
        
        lt.addLast(me.getValue(om.get(me.getValue(om.get(me.getValue(mp.get(me.getValue(mp.get(me.getValue(mp.get(me.getValue(mp.get(data_structs["major_structure"],offer["country_code"]))
                                                                        ,offer["city"])),offer["company_name"])),offer["experience_level"])), offer["published_at"][:10])),salario_minimo)), offer)
        

        
        exist_tamaño = om.contains(data_structs["size_empresas"], data["company_size"])
        if not exist_tamaño:
            om.put(data_structs["size_empresas"], data["company_size"], lt.newList("ARRAY_LIST"))
            
        ya_esta = lt.isPresent(me.getValue(om.get(data_structs["size_empresas"], data["company_size"])),offer["company_name"])
        if not ya_esta:
        
        
            lt.addLast(me.getValue(om.get(data_structs["size_empresas"], data["company_size"])),offer["company_name"])
        
        exists_jobdate= om.contains(data_structs["jobs"],data["published_at"][:10])
        if not exists_jobdate:
            om.put(data_structs["jobs"],data["published_at"][:10], lt.newList("ARRAY_LIST"))
        lt.addLast(me.getValue(om.get(data_structs["jobs"],data["published_at"][:10])),offer)
        
    elif part == "multilocations":
        
        key = f"{data['id']}"
    
        
    else:
        key = f"{data['id']}"
    
    
    
        
    
    if part != "size" and part != "jobs":
        existkey = mp.contains(data_structs[part],key)
        if not existkey:
            mp.put(data_structs[part], key, lt.newList("ARRAY_LIST"))
            
        entry = mp.get(data_structs[part], key)
        lt.addLast(me.getValue(entry), data)
    

def getSortedList(control):
    
    lista =  control["model"]["jobs_cd"]
    merg.sort(lista, sort_crit_reciente_a_antiguo)
    return lista
    
        
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
def revertir_divisas(salario_a_revertir, divisa, c):
   
    if divisa == "usd":
        return float(salario_a_revertir)
    else:
        if divisa == "":
            return 0
        else:   
            divisa = str.upper(divisa)
            #c= CurrencyConverter()
            #print(c.currencies)
            salario_convertido = c.convert(float(salario_a_revertir), 'USD',  divisa)
            #print(salario_a_convertir)
            return salario_convertido

# Funciones para creacion de datos

def cmpFunctionFechaRBT(fecha1, fecha2):
    fecha1 = datetime.strptime(fecha1, "%Y-%m-%d")
    fecha2 = datetime.strptime(fecha2, "%Y-%m-%d")
    if fecha1 > fecha2:
        return 1
    elif fecha1 == fecha2:
        return 0
    else:
        return -1
def cmpFunctionSalarioRBT(salario1, salario2):
    if salario1 > salario2:
        return 1
    elif salario1 == salario2:
        return 0
    else:
        return -1
""" 
def sort_crit_reciente_a_antiguo(oferta1, oferta2):
    fecha1 = datetime.strptime(oferta1["published_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
    fecha2 = datetime.strptime(oferta2["published_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
    if fecha1 > fecha2:
        return True
    elif fecha1 < fecha2:
        return False
    else:
        if oferta1["salario_promedio"] > oferta2["salario_promedio"]:
            return True
        elif oferta1["salario_promedio"] < oferta2["salario_promedio"]:
            return False
        else: 
            return True
"""
    
def sort_crit_salario_minimo(oferta1, oferta2):
    salario1 = int(oferta1["salario_minimo"])
    salario2 = int(oferta2["salario_minimo"])
    if salario1 > salario2:
        return True
    elif salario1 < salario2:
        return False
    else:
        sort_crit_reciente_a_antiguo(oferta1, oferta2)

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


def req_1(data_structs, fecha0, fecha1):
    """
    Función que soluciona el requerimiento 1
    """
    # TODO: Realizar el requerimiento 1
    #fecha0 = datetime.strptime(fecha0,"%Y-%m-%d")
    #fecha1 = datetime.strptime(fecha1,"%Y-%m-%d")
    cantidad_ofertas = 0
    
    total_ofertas = lt.newList("ARRAY_LIST")
    listas_ofertas = om.values(data_structs,fecha0, fecha1)
    for lista_oferta in lt.iterator(listas_ofertas):
        cantidad_ofertas += lt.size(lista_oferta)
        for offer in lt.iterator(lista_oferta):
            lt.addLast(total_ofertas, offer)
    
    cinco = False
    if lt.size(total_ofertas) > 10:
        cinco =True
    
    merg.sort(total_ofertas, sort_crit_reciente_a_antiguo)
    return cantidad_ofertas, total_ofertas, cinco
        
    
def sort_crit_reciente_a_antiguo(oferta1, oferta2):
    fecha1 = datetime.strptime(oferta1["published_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
    fecha2 = datetime.strptime(oferta2["published_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
    if fecha1 > fecha2:
        return True
    elif fecha1 < fecha2:
        return False
    else:
        if oferta1["salario_minimo"] > oferta2["salario_minimo"]:
            return True
        elif oferta1["salario_minimo"] < oferta2["salario_minimo"]:
            return False
        else: 
            return True
    """
    if fecha1.year > fecha2.year:
        return False
    elif fecha1.year < fecha2.year:
        return True
    else:
        if fecha1.month > fecha2.month:
            return False
        elif fecha1.month < fecha2.month:
            return True
        else:
            if fecha1.day > fecha2.month:
                return False
            elif fecha1.day < fecha2.month:
                return True
            else:
                if fecha1.hour > fecha2.hour:
                    return False
                elif fecha1.hour < fecha2.hour:
                    return True
                else:
                    if fecha1.minute > fecha2.minute:
                        return False
                    elif fecha1.minute < fecha2.minute:
                        return True
                    else:
                        if oferta1["salario_promedio"] > oferta2["salario_promedio"]:
                            return False
                        elif oferta1["salario_promedio"] < oferta2["salario_promedio"]:
                            return True
                        else: 
                            return False
    """ 
    
    
    


def req_2(data_structs, salario_minimo, salario_maximo):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    
    cantidad_ofertas = 0
    
    total_ofertas = lt.newList("ARRAY_LIST")
    final = lt.newList("ARRAY_LIST")
    listas_ofertas = om.values(data_structs,salario_minimo, salario_maximo)
    
    for lista_oferta in lt.iterator(listas_ofertas):
        cantidad_ofertas += lt.size(lista_oferta)
        for offer in lt.iterator(lista_oferta):
            lt.addLast(total_ofertas, offer)
    
    
    if total_ofertas !=None:
        merg.sort(total_ofertas, sort_crit_reciente_a_antiguo)
    else:
        return None, None, None
        
    if lt.size(total_ofertas) >= 10:
        sb1 = lt.subList(total_ofertas, 1, 5)
        for zc in lt.iterator(sb1):
            lt.addLast(final, zc)
           
        sb2 = lt.subList(total_ofertas, (lt.size(total_ofertas)-5), 5)
        for zt in lt.iterator(sb2):
            lt.addLast(final, zt )  
            
    elif lt.size(total_ofertas)<10 and lt.size(total_ofertas)>0:
        final = total_ofertas
    elif lt.size(total_ofertas)==0:
        final = None
    return cantidad_ofertas, final, total_ofertas
    
def sort_crit_reciente_a_antiguo(oferta1, oferta2):
    fecha1 = datetime.strptime(oferta1["published_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
    fecha2 = datetime.strptime(oferta2["published_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
    if fecha1 > fecha2:
        return True
    elif fecha1 < fecha2:
        return False
    else:
        if oferta1["salario_promedio"] > oferta2["salario_promedio"]:
            return True
        elif oferta1["salario_promedio"] < oferta2["salario_promedio"]:
            return False
        else: 
            return True

def req_3(data_structs,pais, experticia,N ):
    """
    Función que soluciona el requerimiento 3
    """
    catalogo=data_structs["major_structure"]    
    lista_arboles=lt.newList("ARRAY_LIST")
    ofertas=lt.newList("ARRAY_LIST")
    mapaciudades= me.getValue(mp.get(catalogo,pais))
    mapas_empresas=mp.valueSet(mapaciudades)
    for mapa in lt.iterator(mapas_empresas):
        mapas_experticia= mp.valueSet(mapa)
        for mapa_e in lt.iterator(mapas_experticia):
            if experticia != "indiferente":
                mapa_fechas= me.getValue(mp.get(mapa_e,experticia))
                lt.addLast(lista_arboles,mapa_fechas)
            else:
                valores=mp.valueSet(mapa_e)
                for element in lt.iterator(valores):
                    lt.addLast(lista_arboles,element)

    ofertas= get_ofertas(lista_arboles,N)  
    ordenada= merg.sort(ofertas,sort_crit_req3)
    return ordenada,lt.size(ordenada)
    
def get_ofertas(lista_arboles,N):
    respuesta=lt.newList("ARRAY_LIST")
    while lt.size(respuesta) < N:
        mas_reciente= "0000-00-00"
        d_interes= None
        i=0
        indice=0
        for arbol in lt.iterator(lista_arboles):
            if not om.isEmpty(arbol):
                reciente= om.maxKey(arbol)
                if reciente > mas_reciente:
                    indice=i
                    mas_reciente=reciente
                    d_interes=arbol
            i+=1
        arbol_salarios= me.getValue(om.get(d_interes,mas_reciente))
        lt.deleteElement(lista_arboles,indice)
        arbol_nuevo=om.deleteMax(d_interes)
        lt.addLast(lista_arboles,arbol_nuevo)
        for key in lt.iterator(om.keySet(arbol_salarios)):
            lista_ofertas=me.getValue(mp.get(arbol_salarios,key))
            for element in lt.iterator(lista_ofertas):
                lt.addLast(respuesta,element)
        if lt.size(respuesta)>= N:
            return lt.subList(respuesta,0,N)
        




def req_4(data_structs, N, nombre_ciudad, ubicacion):
    
    """
    Función que soluciona el requerimiento 4
    """
    ciudad = None
    lista_llavesp = mp.keySet(data_structs["major_structure"])
    for llave_pais in lt.iterator(lista_llavesp):
        
        exists_city = mp.contains(me.getValue(mp.get(data_structs["major_structure"],llave_pais)),nombre_ciudad)
        if exists_city and llave_pais != "":
            #print(f"|{llave_pais}|")
            #print(mp.keySet(me.getValue(mp.get(data_structs["major_structure"],llave_pais))))
            ciudad = me.getValue(mp.get(me.getValue(mp.get(data_structs["major_structure"],llave_pais)),nombre_ciudad))
            break
    if ciudad == None:
        return False, False, False
    
    empresas = mp.keySet(ciudad)
    ofertasSN = lt.newList("ARRAY_LIST")
    ofertas_MD = lt.newList("ARRAY_LIST")
    ofertas_JU =lt.newList("ARRAY_LIST")
    ofertas_totales = lt.newList("ARRAY_LIST")
    
    for llave_empresa in lt.iterator(empresas):
        ofertas_senior = me.getValue(mp.get(me.getValue(mp.get(ciudad, llave_empresa)),"senior"))
        ofertas_mid = me.getValue(mp.get(me.getValue(mp.get(ciudad, llave_empresa)),"mid"))
        ofertas_junior = me.getValue(mp.get(me.getValue(mp.get(ciudad, llave_empresa)),"junior"))
        
        lista_provisional1 = lt.newList("ARRAY_LIST")
        lista_provisional2 = lt.newList("ARRAY_LIST")
        lista_provisional3 = lt.newList("ARRAY_LIST")
        if not om.isEmpty(ofertas_senior):
            
            #senior = om.values(ofertas_senior, ofertas_senior["root"]["key"], "2025-12-24")
            senior = om.valueSet(ofertas_senior)
            for nivel in lt.iterator(senior):
                lt.addLast(lista_provisional1, om.valueSet(nivel))
            for lista in lt.iterator(lista_provisional1):
                lt.addLast(ofertasSN, lista)
                
        if not om.isEmpty(ofertas_mid):
            #mid = om.values(ofertas_mid, ofertas_mid["root"]["key"], "2025-12-24")
            mid = om.valueSet(ofertas_mid)
            for nivel in lt.iterator(mid):
                lt.addLast(lista_provisional2, om.valueSet(nivel))
            for lista in lt.iterator(lista_provisional2):
                lt.addLast(ofertas_MD, lista)
                
            
        if not om.isEmpty(ofertas_junior):
            #junior = om.values(ofertas_junior, ofertas_junior["root"]["key"], "2025-12-24")
            junior = om.valueSet(ofertas_junior)
            for nivel in lt.iterator(junior):
                lt.addLast(lista_provisional3, om.valueSet(nivel))
            for lista in lt.iterator(lista_provisional3):
                lt.addLast(ofertas_JU, lista)
    
    conteo = 0          
    for valueset in lt.iterator(ofertasSN):
        for list in lt.iterator(valueset):
            
            for offer in lt.iterator(list):
                conteo += 1
                if offer["workplace_type"] == ubicacion:
                    lt.addLast(ofertas_totales, offer)
                
    for valueset in lt.iterator(ofertas_MD):
        for list in lt.iterator(valueset):
            for offer in lt.iterator(list):
                conteo += 1
                if offer["workplace_type"] == ubicacion:
                    lt.addLast(ofertas_totales, offer)
                    
    for valueset in lt.iterator(ofertas_JU):
        for list in lt.iterator(valueset):
            for offer in lt.iterator(list):
                conteo +=1
                if offer["workplace_type"] == ubicacion:
                    lt.addLast(ofertas_totales, offer)
            
    #print(F"CONTEOOOOOO: {conteo} ACÁÁÁÁÁÁÁÁ")
    cantidad_ofertas = lt.size(ofertas_totales)
    merg.sort(ofertas_totales, sort_crit_reciente_a_antiguo)
    
    if N == None:
        return cantidad_ofertas , ofertas_totales, False
    if lt.size(ofertas_totales) >= N:
        ofertas_totales = lt.subList(ofertas_totales, 1, N)
           
    cinco = False
    if lt.size(ofertas_totales)>10:
        cinco = True
        
    
    
    return cantidad_ofertas , ofertas_totales, cinco

        
    #print(llaves_pais)
   
        
        
        
    
    # TODO: Realizar el requerimiento 4
def sort_critr4(oferta1,oferta2):
    if oferta1["salario_minimo"]> oferta2["salario_minimo"]:
        return True
    elif oferta1["salario_minimo"] < oferta2["salario_minimo"]:
        return False
    else:
        return sort_crit_reciente_a_antiguo(oferta1, oferta2)


def req_5(data_structs, numero_ofertas, tamano_minimo_compania,
          tamano_maximo_compania, skill, limite_inferior_skill, limite_superior_skill):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5
    
    ofertas_totales = lt.newList("ARRAY_LIST")
    final = lt.newList("ARRAY_LIST")
    cantidad_ofertas = 0
    
    #Compañias que estan entre el rango de tamaños
    lista_nombres_companias = om.values(data_structs["size_empresas"],tamano_minimo_compania,tamano_maximo_compania)
    
    #Lista de ciudades
    lista_ciudades = mp.valueSet(data_structs["major_structure"])
    lista_empresas_filtradas = lt.newList("ARRAY_LIST")
    lista_nueva =lt.newList("ARRAY_LIST")
    
    ofertasSN = lt.newList("ARRAY_LIST")
    ofertas_MD = lt.newList("ARRAY_LIST")
    ofertas_JU =lt.newList("ARRAY_LIST")
    
    
###############################################################################################
    for ciudad in lt.iterator(lista_ciudades):
        lista_ciudades_por_valueset = mp.valueSet(ciudad)
        lt.addLast(lista_nueva, lista_ciudades_por_valueset)
        
        
    lista_hi = lt.newList("ARRAY_LIST")
    for df in lt.iterator(lista_nueva):
        for hi in lt.iterator(df):
            
            lt.addLast(lista_hi, hi)
            
            
            
#################################################################################################################
    lista_empresas_para_usar = lt.newList("ARRAY_LIST") 
    
   
    #print(data_structs["size_empresas"])
    
    for companies in lt.iterator(lista_nombres_companias):
        for companies2 in lt.iterator(companies):
            lt.addLast(lista_empresas_para_usar, companies2) 
        
            
 #####################################################################################
          
    for ciudades_c in lt.iterator(lista_hi):
        #print(ciudades_c)
        
        for ofertas_que_son in lt.iterator(lista_empresas_para_usar):
          
            xt = mp.get(ciudades_c, ofertas_que_son)
            if xt !=None:
                off = me.getValue(mp.get(ciudades_c, ofertas_que_son))
                ofertas_senior = me.getValue(mp.get(off,"senior"))
                ofertas_mid = me.getValue(mp.get(off,"mid"))
                ofertas_junior = me.getValue(mp.get(off,"junior"))
                    
                lista_provisional1 = lt.newList("ARRAY_LIST")
                lista_provisional2 = lt.newList("ARRAY_LIST")
                lista_provisional3 = lt.newList("ARRAY_LIST")
                if not om.isEmpty(ofertas_senior):
                    #senior = om.values(ofertas_senior, om.maxKey(ofertas_senior), ofertas_senior["root"]["key"])
                    senior = om.valueSet(ofertas_senior)
                        
                    for nivel in lt.iterator(senior):
                        lt.addLast(lista_provisional1, om.valueSet(nivel))
                        for lista in lt.iterator(lista_provisional1):
                            lt.addLast(ofertasSN, lista)
                        
                        """
                        salaries = om.values(nivel, om.maxKey(nivel), nivel["root"]["key"] )
                        ubicaciones = om.values(salaries, mp.valueSet(salaries), salaries["root"]["key"])
                        offers = me.getValue(mp.get(ubicaciones))
                        for oferta in lt.iterator(offers):
                            if skill in oferta["habilidades solicitadas"]:
                                if tamano_minimo_compania <= oferta["promedio_habilidad"] and oferta["habilidades solicitadas"] <= tamano_maximo_compania:
                                    lt.addLast(ofertas_totales, oferta)
                                    cantidad_ofertas +=1
                        """
                                
                                
                if not om.isEmpty(ofertas_mid):
                    
                    mid = om.valueSet(ofertas_mid)
                    for nivel in lt.iterator(mid):
                        lt.addLast(lista_provisional2, om.valueSet(nivel))
                        for lista in lt.iterator(lista_provisional2):
                            lt.addLast(ofertas_MD, lista)
                            
                    """
                    mid = om.values(ofertas_senior, om.maxKey(ofertas_mid), ofertas_mid["root"]["key"])
                        
                    for nivel1 in lt.iterator(senior):
                        salaries1 = om.values(nivel1, om.maxKey(nivel1), nivel1["root"]["key"] )
                        ubicaciones1 = om.values(salaries1, mp.valueSet(salaries1), salaries1["root"]["key"])
                        offers1 = me.getValue(mp.get(ubicaciones1))
                        for oferta1 in lt.iterator(offers1):
                            if skill in oferta1["habilidades solicitadas"]:
                                if tamano_minimo_compania <= oferta1["promedio_habilidad"] and oferta1["habilidades solicitadas"] <= tamano_maximo_compania:
                                    lt.addLast(ofertas_totales, oferta1)
                                    cantidad_ofertas +=1
                    """         
                            
                if not om.isEmpty(ofertas_junior):
                    junior = om.valueSet(ofertas_junior)
                    for nivel in lt.iterator(junior):
                        lt.addLast(lista_provisional3, om.valueSet(nivel))
                        for lista in lt.iterator(lista_provisional3):
                            lt.addLast(ofertas_JU, lista)
                    
                    
                    
                    """
                    junior = om.values(ofertas_senior, om.maxKey(ofertas_mid), ofertas_junior["root"]["key"])
                        
                    for nivel2 in lt.iterator(senior):
                        salaries2 = om.values(nivel2, om.maxKey(nivel2), nivel2["root"]["key"] )
                        ubicaciones2 = om.values(salaries2, mp.valueSet(salaries2), salaries2["root"]["key"])
                        offers2 = me.getValue(mp.get(ubicaciones2))
                        for oferta2 in lt.iterator(offers2):
                            if skill in oferta2["habilidades solicitadas"]:
                                if tamano_minimo_compania <= oferta2["promedio_habilidad"] and oferta2["habilidades solicitadas"] <= tamano_maximo_compania:
                                    lt.addLast(ofertas_totales, oferta2)
                                    cantidad_ofertas +=1
                    """
                            
    for valueset in lt.iterator(ofertasSN):
        for list in lt.iterator(valueset):
            for offer in lt.iterator(list):
                
                if skill in offer["habilidades_solicitadas"]["elements"]:
                    
                    if limite_inferior_skill <= offer["promedio_habilidad"] and offer["promedio_habilidad"]<= limite_superior_skill:
                        lt.addLast(ofertas_totales, offer)
                
    for valueset1 in lt.iterator(ofertas_MD):
        for list1 in lt.iterator(valueset1):
            for offer1 in lt.iterator(list1):
                
                if skill in offer1["habilidades_solicitadas"]["elements"]:
                    
                    if limite_inferior_skill <= offer1["promedio_habilidad"] and offer1["promedio_habilidad"] <= limite_superior_skill:
                        lt.addLast(ofertas_totales, offer)
                    
    for valueset2 in lt.iterator(ofertas_JU):
        for list2 in lt.iterator(valueset2):
            for offer2 in lt.iterator(list2):
                
                if skill in offer2["habilidades_solicitadas"]["elements"]:
                    
                    
                    if limite_inferior_skill <= offer2["promedio_habilidad"] and offer2["promedio_habilidad"] <= limite_superior_skill:
                        lt.addLast(ofertas_totales, offer)
                        
                
                
                
                
                
                
                
    cantidad_ofertas = lt.size(ofertas_totales)           
              
    if ofertas_totales !=None:
        merg.sort(ofertas_totales, sort_crit_reciente_a_antiguo)
        
    if lt.size(ofertas_totales) >= 10:
        sb1 = lt.subList(ofertas_totales, 1, 5)
        for zc in lt.iterator(sb1):
            lt.addLast(final, zc)
           
        sb2 = lt.subList(ofertas_totales, (lt.size(ofertas_totales)-5), 5)
        for zt in lt.iterator(sb2):
            lt.addLast(final, zt )  
            
    elif lt.size(ofertas_totales)<10 and lt.size(ofertas_totales)>0:
        if lt.size(ofertas_totales)>= int(numero_ofertas):
            
            final = lt.subList(ofertas_totales, 1, int(numero_ofertas)) 
            
        else:
            final = ofertas_totales
            
    elif lt.size(ofertas_totales)==0:
        final = None
        
    
    return cantidad_ofertas, final


def req_6(data_structs,N,fecha1,fecha2,salario1,salario2):
    """
    Función que soluciona el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6
    lista_fechas=lt.newList("ARRAY_LIST")
    mapa_salarios=mp.newMap(numelements=203560,maptype="CHAINING", loadfactor= 4)
    lista_total= lt.newList("ARRAY_LIST")
    jobs= data_structs["jobs"]
    salarios=data_structs["salaries_offers"]
    listas_ofertas_fechas=om.values(jobs,fecha1,fecha2)
    listas_ofertas_salarios=om.values(salarios,salario1,salario2)
    for lista_offer in lt.iterator(listas_ofertas_fechas):
        for offer in lt.iterator(lista_offer):
            lt.addLast(lista_fechas,offer)
            
    for lista_ofertas in lt.iterator(listas_ofertas_salarios):
        for oferta in lt.iterator(lista_ofertas):
            salario= oferta["salario_minimo"]
            if mp.contains(mapa_salarios,salario) == False:
                valor=lt.newList("ARRAY_LIST")
                lt.addLast(valor,oferta)
                mp.put(mapa_salarios,salario,valor)
            else:
                pareja=mp.get(mapa_salarios,salario)
                valorC=me.getValue(pareja)
                lt.addLast(valorC,oferta)

    for element1 in lt.iterator(lista_fechas):
        salario_of= element1["salario_minimo"]
        ciudad= element1["city"]
        if mp.contains(mapa_salarios,salario_of):
            lt.addLast(lista_total,element1)
           
    tamaño_total= lt.size(lista_total)
    ciudad,tamaño,lista=mas_ciudades(lista_total,N)
    lista_ofertas_ciudad=lt.newList("ARRAY_LIST")
    for oferta in lt.iterator(lista_total):
        if oferta["city"]== ciudad:
            lt.addLast(lista_ofertas_ciudad,oferta)

    return tamaño,lista,merg.sort(lista_ofertas_ciudad,sort_crit_req3),tamaño_total
def mas_ciudades(lista,N):
    lista_ciudades=[]
    for oferta in lt.iterator(lista):
        lista_ciudades.append(oferta["city"])

    contador_ciudades=Counter(lista_ciudades)
    ciudades_mas_ofertas = contador_ciudades.most_common(N)
    ciudad_mas_ofertas = contador_ciudades.most_common(1)[0][0]
    size=len(contador_ciudades)


    return ciudad_mas_ofertas,size,ciudades_mas_ofertas


           






def req_7(data_structs, año, codigo_pais, propiedad_conteo, bins):
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Realizar el requerimiento 7
    pais = me.getValue(mp.get(data_structs["major_structure"], codigo_pais))
    
    ciudades = lt.newList("ARRAY_LIST")
    for llave_ciudad in lt.iterator(mp.keySet(pais)):
        lt.addLast(ciudades, me.getValue(mp.get(pais, llave_ciudad)))
    
    empresas = lt.newList("ARRAY_LIST")
    for ciudad in lt.iterator(ciudades):
        for empresa in lt.iterator(mp.valueSet(ciudad)):
            lt.addLast(empresas, empresa)
            #    ofertas = om.values(ofertas_senior, ofertas_senior["root"]["key"], "2023-12-24")
        
        
    valueSetsJN = lt.newList("ARRAY_LIST")    
    valueSetsMI = lt.newList("ARRAY_LIST")
    valueSetsSN = lt.newList("ARRAY_LIST")
    
    for empresa in lt.iterator(empresas):
        ofertas_senior = om.values(me.getValue(mp.get(empresa,"senior")), f"{año}-01-1", f"{año}-12-31")
        ofertas_mid = om.values(me.getValue(mp.get(empresa,"mid")), f"{año}-01-1", f"{año}-12-31")
        ofertas_junior = om.values(me.getValue(mp.get(empresa,"junior")), f"{año}-01-1", f"{año}-12-31")
        
        lista_provisional1 = lt.newList("ARRAY_LIST")
        lista_provisional2 = lt.newList("ARRAY_LIST")
        lista_provisional3 = lt.newList("ARRAY_LIST")
        if not om.isEmpty(ofertas_senior):
            
            for nivel in lt.iterator(ofertas_senior):
                lt.addLast(lista_provisional1, om.valueSet(nivel))
            for lista in lt.iterator(lista_provisional1):
                lt.addLast(valueSetsSN, lista)
                
        if not om.isEmpty(ofertas_mid):
            
            for nivel in lt.iterator(ofertas_mid):
                lt.addLast(lista_provisional2, om.valueSet(nivel))
            for lista in lt.iterator(lista_provisional2):
                lt.addLast(valueSetsMI, lista)
                
            
        if not om.isEmpty(ofertas_junior):
            
            for nivel in lt.iterator(ofertas_junior):
                lt.addLast(lista_provisional3, om.valueSet(nivel))
            for lista in lt.iterator(lista_provisional3):
                lt.addLast(valueSetsJN, lista)
                
    ofertas_totales = lt.newList("ARRAY_LIST")
    data_experticia = []
    data_ubicacion = []
    data_habilidad = []
    
    listsSN = lt.newList("ARRAY_LIST")
    listsMD = lt.newList("ARRAY_LIST")
    listsJN = lt.newList("ARRAY_LIST")
    

    overview = mp.newMap(numelements=13, maptype="PROBING", loadfactor=0.5)
    mp.put(overview, "senior", 0)
    mp.put(overview, "mid", 0)
    mp.put(overview, "junior", 0)
    mp.put(overview, "office", 0)
    mp.put(overview, "remote", 0)
    mp.put(overview, "partly_remote", 0)
    overview_skills = mp.newMap(numelements=100, maptype="PROBING", loadfactor=0.5)
    
    for valueset in lt.iterator(valueSetsSN):
        for list in lt.iterator(valueset):
            lt.addLast(listsSN, list)
    
    for list in lt.iterator(listsSN):
        for offer in lt.iterator(list):
            lt.addLast(ofertas_totales, offer)
            data_experticia.append("senior")
            data_ubicacion.append(offer["workplace_type"])
            mp.put(overview, "senior", me.getValue(mp.get(overview, "senior"))+1)
            mp.put(overview, offer["workplace_type"], me.getValue(mp.get(overview, offer["workplace_type"]))+1)      
                
    for valueset in lt.iterator(valueSetsMI):
        for list in lt.iterator(valueset):
            lt.addLast(listsMD, list)
    for list in lt.iterator(listsMD):
        for offer in lt.iterator(list):
            lt.addLast(ofertas_totales, offer)
            data_experticia.append("mid")
            data_ubicacion.append(offer["workplace_type"])
            mp.put(overview, "mid", me.getValue(mp.get(overview, "mid"))+1)
            mp.put(overview, offer["workplace_type"], me.getValue(mp.get(overview, offer["workplace_type"]))+1)    
                
                    
    for valueset in lt.iterator(valueSetsJN):
        for list in lt.iterator(valueset):
            lt.addLast(listsJN, list)
    for list in lt.iterator(listsJN):
        for offer in lt.iterator(list):
            lt.addLast(ofertas_totales, offer)   
            data_experticia.append("junior")   
            data_ubicacion.append(offer["workplace_type"])
            mp.put(overview, "junior", me.getValue(mp.get(overview, "junior"))+1)
            mp.put(overview, offer["workplace_type"], me.getValue(mp.get(overview, offer["workplace_type"]))+1)
    
    for offer in lt.iterator(ofertas_totales):
        for skill in lt.iterator(offer["habilidades_solicitadas"]):
            if not mp.contains(overview_skills, skill):
                mp.put(overview_skills, skill,-1)
            mp.put(overview_skills, skill, me.getValue(mp.get(overview_skills, skill))+1)
            data_habilidad.append(skill)
    
    minimo_experticia = me.getValue(mp.get(overview, "junior"))
    minimo_ubicacion =  me.getValue(mp.get(overview, "remote"))
    minimo_skill = None
    maximo_experticia = 0
    maximo_ubicacion = 0
    maximo_skill = 0
    for key_skill in lt.iterator(mp.keySet(overview_skills)):
        if me.getValue(mp.get(overview_skills, key_skill)) > maximo_skill:
            maximo_skill = me.getValue(mp.get(overview_skills, key_skill))
        if minimo_skill == None:
            minimo_skill = me.getValue(mp.get(overview_skills, key_skill))
        else:
            if me.getValue(mp.get(overview_skills, key_skill)) < minimo_skill:
                minimo_skill = me.getValue(mp.get(overview_skills, key_skill))
    
    for key in lt.iterator(mp.keySet(overview)):
        if (key == "senior") or (key == "junior") or (key == "mid"):
            if me.getValue(mp.get(overview, key)) > maximo_experticia:
                maximo_experticia = me.getValue(mp.get(overview, key))
            elif me.getValue(mp.get(overview, key)) < minimo_experticia:
                minimo_experticia = me.getValue(mp.get(overview, key))
                
        if (key == "office") or (key == "remote") or (key == "partly_remote"):
            if me.getValue(mp.get(overview, key)) > maximo_ubicacion:
                maximo_ubicacion = me.getValue(mp.get(overview, key))
            elif me.getValue(mp.get(overview, key)) < minimo_ubicacion:
                minimo_ubicacion = me.getValue(mp.get(overview, key))
            
    
    if propiedad_conteo == "Experticia":
        return data_experticia, data_ubicacion, data_habilidad, ofertas_totales, maximo_experticia, minimo_experticia
    elif propiedad_conteo == "Ubicacion":
        return data_experticia, data_ubicacion, data_habilidad, ofertas_totales, maximo_ubicacion, minimo_ubicacion
    else:
        return data_experticia, data_ubicacion, data_habilidad, ofertas_totales, maximo_skill, minimo_skill
    
        
    
    
        
        
        
    


def req_8(data_structs, req):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    if req == 1:
        pass
    if req == 2:
        pass
    if req == 3:
        pass
    if req == 4:
        pass
    if req == 5:
        pass
    if req == 6:
        pass
    if req == 7:
        pass
    
    


# Funciones utilizadas para comparar elementos dentro de una lista

def compare(data_1, data_2):
    """
    Función encargada de comparar dos datos
    """
    #TODO: Crear función comparadora de la lista
    pass

# Funciones de ordenamiento
def sort_crit_req3(oferta1, oferta2):
    fecha1 = datetime.strptime(oferta1["published_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
    fecha2 = datetime.strptime(oferta2["published_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
    if fecha1 > fecha2:
        return True
    elif fecha1 < fecha2:
        return False
    else:
        if oferta1["salario_minimo"] > oferta2["salario_minimo"]:
            return True
        elif oferta1["salario_minimo"] < oferta2["salario_minimo"]:
            return False
        else: 
            return True


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
