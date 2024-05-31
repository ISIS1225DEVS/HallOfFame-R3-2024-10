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
import codigo_arboles as bst
import arboles_rojo_negro as bst_rn
import hash_table_lp as ht
import heap 
import New_Functions as nf
import Sorts
from datetime import datetime 

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""

# Construccion de modelos

capacity= 1000000
lfactor= 0.3

def new_data_structs():
    """
    Inicializa las estructuras de datos del modelo. Las crea de
    manera vacía para posteriormente almacenar la información.
    """
    model = {'jobs': nf.newList(),
               'skills': nf.newList(),
               'employments_types': nf.newList(),
               'multilocation': nf.newList(),}
    
    #Indices
    model['dateIndex']= bst_rn.create_vacio()
    model['sizeIndex']= bst_rn.create_vacio()
    model['salario_min']= bst_rn.create_vacio()
    model['pais']= ht.hash_table(1000,lfactor) 
    model['ciudad']= ht.hash_table(1000,lfactor) 
    model['anio']= ht.hash_table(10,lfactor)
    model['id_job']= ht.hash_table(capacity,lfactor)
    model['id_skill']= ht.hash_table(capacity,lfactor)
    model['todos_salarios'] = ht.hash_table(capacity, lfactor)
    #model['id_por_habilidad'] = ht.hash_table(capacity,lfactor)
    model['id_employment_type']= ht.hash_table(capacity,lfactor)
    return model

# Funciones para agregar informacion al modelo
def addJob(data_structs, job):
    """
    Esta funcion adiciona un trabajo a la lista de trabajos,
    adicionalmente lo guarda en un Map usando como llave su Id.
    Tambien se guarda la referencia en mapas por: el nombre de 
    la empresa, el pais, la ciudad, y el nivel de experticie.
    """
    nf.addLast( data_structs['jobs'], job)
    ht.put(data_structs['id_job'],job['id'],job)
    #hash de paises y experticias
    pais = job['country_code']
    e = ht.get_value(data_structs['pais'],pais) 
    if e != None:
        e = ht.get_value(data_structs['pais'],pais)[1]
        exp = job['experience_level']
        e_e = ht.get_value(e, exp)[1]
        ht.put(e_e, job['id'], job)
    else:
        experience = ht.hash_table(15, 0.2)
        empty = ht.hash_table(100, 0.5)
        new_list = ht.hash_table(100, 0.5)
        ht.put(new_list, job['id'], job)
        if job['experience_level'] == "senior":
            ht.put(experience, "senior", new_list)
            ht.put(experience, "mid", empty)
            ht.put(experience, "junior", empty)
        elif job['experience_level'] == "mid":
            ht.put(experience, "senior", empty)
            ht.put(experience, "mid", new_list)
            ht.put(experience, "junior", empty)
        elif job['experience_level'] == "junior":
            ht.put(experience, "senior", empty)
            ht.put(experience, "mid", empty)
            ht.put(experience, "junior", new_list)
        ht.put(data_structs['pais'], pais, experience)
        experience = None

def addJobCity(data_structs, job):
    nf.addLast( data_structs['jobs'], job)
    ht.put(data_structs['id_job'], job['id'], job)
    # Hash de Ciudades y Tipo de Ubicación
    ciudad = job['city']
    elem = ht.get_value(data_structs['ciudad'],ciudad)
    if elem == None:
        ubicacion = ht.hash_table(15, 0.2)
        empty = ht.hash_table(100, 0.5)
        lista = ht.hash_table(100, 0.5)
        ht.put(lista, job['id'], job)
        if job['workplace_type'] == "office":
            ht.put(ubicacion, "office", lista)
            ht.put(ubicacion, "remote", empty)
            ht.put(ubicacion, "partly_remote", empty)
        elif job['workplace_type'] == "remote":
            ht.put(ubicacion, "office", empty)
            ht.put(ubicacion, "remote", lista)
            ht.put(ubicacion, "partly_remote", empty)
        elif job['workplace_type'] == "partly_remote":
            ht.put(ubicacion, "office", empty)
            ht.put(ubicacion, "remote", empty)
            ht.put(ubicacion, "partly_remote", lista)
        ht.put(data_structs['ciudad'], ciudad, ubicacion)
        ubicacion = None
    else:
        elem = ht.get_value(data_structs['ciudad'],ciudad)[1]
        work = job['workplace_type']
        elemwork = ht.get_value(elem, work)[1]
        ht.put(elemwork, job['id'], job)

def updateSizeIndex(data_structs,skill):
    """
    Se toma la el tamaño de la compañia del trabajo y se busca si ya existe en el arbol
    dicho tamaño.  Si es asi,  se actualiza el indice de habilidades en el nodo. (req 5)
    
    Si no se encuentra creado un nodo para ese tamaño en el arbol
    se crea y se actualiza el indice de trabajo
    """
    job= ht.get_value(data_structs['id_job'],skill['id'])[1]
    arbol= data_structs['sizeIndex']
    csize = job['company_size']
    entry = bst.get(arbol, csize)
    if entry is None:
        sizentry = newSkillIndex()
        arbol= bst.add(arbol, {'key': csize, 'value': sizentry}) 
    else:
        sizentry = entry['value']
    data_structs['sizeIndex']= arbol
    addLevelTree(sizentry['skillIndex'], job,skill)
    return arbol

def updateDateSalary(data_structs,employment):
    job= ht.get_value(data_structs['id_job'],employment['id'])[1]
    arbol= data_structs['dateIndex']
    published_at = job['published_at']
    date = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%S.%fZ")

    entry = bst.get(arbol,date)
    if entry is None:
        datentry = newDataEntry(job)
        arbol= bst.add(arbol, {'key': date, 'value': datentry}) 
    else:
        datentry = entry['value']

    lst = datentry['lstjobs']
    nf.addLast(lst, job)
    arbol2= datentry['salaryTree']
    csize =employment['salary_from']

    entry = bst.get(arbol2, csize)
    if entry is None:
        sizentry = newLevelEntry()
        arbol2= bst.add(arbol2, {'key': csize, 'value': sizentry}) 
    else:
        sizentry = entry['value']
    nf.addLast(sizentry['lstjobs'],job)
    datentry['salaryTree']=arbol2
    return arbol


def updateYearIndex(data_structs,skill):
    """
    Actualiza un indice de anio de publicacion.  Este indice tiene una lista
    de trabajos, una tabla de hash cuya llave es la habilidad y
    el valor es un arbol binario por nivel de experiencia, y otro arbol binario por salario minimo donde el valor  en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    job = ht.get_value(data_structs['id_job'], skill['id'])[1]
    anio= int(job['published_at'][:4])
    pais = job['country_code']
    offentry= ht.get_value(data_structs['anio'],anio)
    if (offentry is None):
        entry = newYearEntry()
        ht.put(data_structs['anio'], anio, entry)
        offentry = ht.get_value(data_structs['anio'], anio)
    nf.addLast(offentry[1]['lstjobs'],job)
    mapa= offentry[1]['countryMap']
    offentry2 = ht.get_value(mapa, pais)
    if (offentry2 is None):
        yentry = newCountryEntry()
        ht.put(mapa, pais, yentry)
        offentry2 = ht.get_value(mapa, pais)
    nf.addLast(offentry2[1]['lstjobs'],job)
    addConteo(offentry2[1],job,skill)

def addLevelTree(sizentry, job, skill):
    """
    Actualiza un indice por habilidad.  Este indice tiene un arbol
    por nivel de experiencia.
    """
    offentry = ht.get_value(sizentry, skill['name'])
    if (offentry is None):
        entry = newSkillEntry()
        ht.put(sizentry, skill['name'], entry)
        offentry = ht.get_value(sizentry, skill['name'])
    nf.addLast(offentry[1]['lstjobs'],job)
    arboln= offentry[1]['levelTree']
    nivel = skill['level']
    entry = bst_rn.get(arboln, nivel)
    if entry is None:
        entry = newLevelEntry()
        arboln= bst_rn.add(arboln, {'key': nivel, 'value': entry}) 
    else:
        entry = entry['value']
    lst = entry['lstjobs']
    nf.addLast(lst, job)
    offentry[1]['levelTree']= arboln
    
def addConteo(countryentry,job,skill):
    habilidad = skill['name']
    location= job['workplace_type']
    level= job['experience_level']
    offentry= ht.get_value(countryentry['skillMap'],habilidad)
    if (offentry is None):
        entry = newProperty()
        ht.put(countryentry['skillMap'], habilidad, entry)
        offentry = ht.get_value(countryentry['skillMap'], habilidad)
    nf.addLast(offentry[1]['lstjobs'],job)
    offentry= ht.get_value(countryentry['locationMap'],location)
    if (offentry is None):
        entry = newProperty()
        ht.put(countryentry['locationMap'], location, entry)
        offentry = ht.get_value(countryentry['locationMap'], location)
    nf.addLast(offentry[1]['lstjobs'],job)
    offentry= ht.get_value(countryentry['levelMap'],level)
    if (offentry is None):
        entry = newProperty()
        ht.put(countryentry['levelMap'],level, entry)
        offentry = ht.get_value(countryentry['levelMap'],level)
    nf.addLast(offentry[1]['lstjobs'],job)
    
def newDataEntry(job):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'lstjobs': None, 'salaryTree': None}
    entry['lstjobs'] = nf.newList()
    entry['salaryTree'] = bst.create_vacio()
    return entry

def newSkillIndex():
    """
    Crea una entrada en el indice por habilidad.
    """
    entry = {'skillIndex': None}
    entry['skillIndex'] = ht.hash_table(30,0.5,compare)
    return entry

def newLevelEntry():
    """
    Crea una lista de trabajos en un arbol por nivel de habilidad.
    """
    entry = {'lstjobs': None}
    entry['lstjobs'] = nf.newList()
    return entry

def newSkillEntry(): 
    """
    Crea una entrada en el indice por nivel de habilidad, es decir en
    el arbol, que se encuentra en cada habilidad en el mapa.
    """
    skillentry = {'levelTree': None, 'lstjobs': None}
    skillentry['levelTree'] = bst_rn.create_vacio()
    skillentry['lstjobs']=nf.newList()
    return skillentry

def newYearEntry(): 
    """
    Crea una entrada en el indice por año de publicacion
    """
    skillentry = {'countryMap': None}
    skillentry['countryMap'] = ht.hash_table(170,lfactor)
    skillentry['lstjobs']=nf.newList()
    return skillentry
    
def newCountryEntry():
    """
    Crea una entrada en el indice por pais de publicacion, se agrega al mapa por año.
    Se crea un mapa por propiedad de conteo.
    """
    skillentry = {}
    skillentry['skillMap'] = ht.hash_table(capacity,lfactor)
    skillentry['locationMap'] = ht.hash_table(capacity,lfactor)
    skillentry['levelMap'] = ht.hash_table(20,lfactor)
    skillentry['lstjobs']=nf.newList()
    return skillentry

def newProperty():
    skillentry = {}
    skillentry['lstjobs']=nf.newList()
    return skillentry
 
def addSkill(data_structs, skill):
    """
    Esta funcion adiciona una habilidad a la lista de habilidades,
    adicionalmente lo guarda en un Map usando como llave su Id, si
    la Id ya esta presente se agrega a la lista y se crea un arbol 
    por tamaño de la compamia(req 5).
    """
    nf.addLast(data_structs['skills'], skill)
    addIdHabilidad(data_structs, skill)
    data_structs['sizeIndex']= updateSizeIndex(data_structs,skill)
    updateYearIndex(data_structs,skill)
    
def addIdHabilidad(data_structs, skill):
    id_habilidad= skill['id']
    if ht.get_value(data_structs['id_skill'],id_habilidad):
        e = (ht.get_value(data_structs['id_skill'],id_habilidad))[1]
    else:
        e = newIdHabilidad(id_habilidad)
        ht.put(data_structs['id_skill'], id_habilidad, e)
    e['ofertas'].append(skill)
        
def addEmploymentType(data_structs, employment_types):
    """
    Esta funcion adiciona un tipo de empleo a la lista de tipos de empleos,
    adicionalmente lo guarda en un Map usando como llave su Id.Tambien se 
    guarda por tipo de trabajo y por tipo de moneda.
    """
    data_structs['dateIndex']=updateDateSalary(data_structs,employment_types)
    valor = ht.get_value(data_structs['todos_salarios'],  employment_types['id'])
    if valor == None:
        if employment_types['salary_from'] != "Unknown":
            currency = employment_types['currency_salary']
            employment_types['salary_from'] = str(convertir_to_usd(int(employment_types['salary_from']), currency))
        nf.addLast(data_structs['employments_types'], employment_types)
        ht.put(data_structs['id_employment_type'], employment_types['id'], employment_types)
        agregar = nf.newList()
        nf.addLast(agregar, employment_types['salary_from'])
        ht.put(data_structs['todos_salarios'], employment_types['id'], agregar)
    else:
        if ((str(valor[1]) > str(employment_types['salary_from']) and str(employment_types['salary_from']) != "Unknown" and str(valor[1]) != "Unknown")
            or (str(valor[1]) == "Unknown") and str(employment_types['salary_from']) != "Unknown"):
            nf.changeInfo(valor[1], 0, employment_types['salary_from'])
            #salarioMinExiste(data_structs, valor, employment_types)
        
def salarioMinExiste(data_structs, job, nueva_info):
    salary = int(job[1]['salary_from'])
    id = job[1]['id']
    previous = bst.get(data_structs['salario_min'], salary)['value']['keys']
    #info previa
    info = (ht.get_value(data_structs['id_job'], id))[1]
    del previous[id]
    #info nueva
    info['salary'] = int(nueva_info['salary_from'])
    currency = nueva_info['currency_salary']
    info['salary'] = convertir_to_usd(info['salary'], currency)
    lugar = bst_rn.get(data_structs['salario_min'], info['salary'])
    if lugar == None:
        total = nuevaInfoGeneral(id, info)
        nuevo = bst_rn.create_node(int(info['salary']), total)
        data_structs['salario_min'] = bst_rn.add(data_structs['salario_min'], nuevo)
    else:
        agregar = lugar['value']['keys']
        agregar[id] = info
    #agregar salario Min a req_3
    req3 = data_structs['pais']
    req3 = ht.get_value(req3, info['country_code'])[1]
    req3 = ht.get_value(req3, info['experience_level'])[1]
    req3 = req3['keys'][id]
    req3['salary'] = info['salary']
    
    
    #eliminar y agregar 
    
def salarioMinimo(data_structs, job):
    salary = job['salary_from']
    id = job['id']
    info = (ht.get_value(data_structs['id_job'], id))[1]
    req3 = data_structs['pais']
    req3 = ht.get_value(req3, info['country_code'])[1]
    req3 = ht.get_value(req3, info['experience_level'])[1]['keys']
    req3 = req3[id]
    habilidades = ht.get_value(data_structs['id_skill'], id)[1]['ofertas']
    habilidades = retomarHabilidades(habilidades)
    if job['salary_from'] == "Unknown":
        req3['salary'] = "Unknown"
    elif salary != "Unknown":
        salary = int(salary)
        ubi_salario = bst_rn.get(data_structs['salario_min'], int(salary))
        info['salary'] = salary
        info['skill'] = habilidades
        if ubi_salario == None:
            total = nuevaInfoGeneral(id, info)
            nuevo = bst_rn.create_node(salary, total)
            data_structs['salario_min'] = bst_rn.add(data_structs['salario_min'], nuevo)
        else:
            ubi_salario = ubi_salario['value']['keys']
            ubi_salario[id] = info
        req3['salary'] = info['salary']
    req3['skill'] = habilidades
    
def crear_arbol_salarios(data_structs):
    keys = ht.keySet(data_structs['todos_salarios'])
    for i in keys['elements']:
        lugar = ht.get_value(data_structs['todos_salarios'], i)[1]['elements']
        info = (ht.get_value(data_structs['id_job'], i))[1]
        info['salary'] = lugar[0]
        habilidades = ht.get_value(data_structs['id_skill'], i)[1]['ofertas']
        habilidades = retomarHabilidades(habilidades)
        info['skill'] = habilidades
        if info['salary'] != "Unknown":
            ubi_salario = bst_rn.get(data_structs['salario_min'], int(float(info['salary'])))
            if ubi_salario == None:
                lista = nf.newList()
                nf.addLast(lista, info)
                nuevo = bst_rn.create_node(int(float(info['salary'])), lista)
                data_structs['salario_min'] = bst_rn.add(data_structs['salario_min'], nuevo)
            else:
                ubi_salario = ubi_salario['value']
                nf.addLast(ubi_salario, info)
        req3 = data_structs['pais']
        req3 = ht.get_value(req3, info['country_code'])[1]
        req3 = ht.get_value(req3, info['experience_level'])[1]
        req3 = ht.get_value(req3, info['id'])[1]
        req3['salary'] = info['salary']
        
            
def convertir_to_usd(amount, from_currency):
    currencies = {'usd': 1,
                  'chf': 1.09,
                  'pln': 0.25,
                   'gbp': 1.25,
                   'eur': 1.07} #estable porque si no explotaba
    usd_amount = amount * currencies[from_currency]
    return usd_amount

def retomarHabilidades(info): #toma la info de habilidades y lo vuelve un str
    habilidades = ""
    for i in info:
        if habilidades == "":
            habilidades = i['name']
        else:
            habilidades = habilidades + ", " +  i['name']   
    return habilidades   

def sortJobsFinal(jobs):
    final = Sorts.MergeSort(jobs, Sorts.mayor_menor_published)
    return final

def addMultilocation(data_structs, multilocation):
    """
    Esta funcion adiciona las locaciones a la lista de locaciones,
    adicionalmente lo guarda en un Map usando como llave su Id, si
    la Id ya esta presente se le suma 1.
    """
    nf.addLast(data_structs['multilocation'], multilocation)
        
# Funciones para creacion de datos

def addLocaciones(data_structs, multilocation):
    id_locacion= multilocation['id']
    if ht.get_value(data_structs['sedes'],id_locacion) != None:
        e = (ht.get_value(data_structs['sedes'],id_locacion))[1]
    else:
        e = newLocacion(id_locacion)
        ht.put(data_structs['sedes'], id_locacion, e)
    e['locaciones']+=1
        
        
def newIdHabilidad(habilidad):
    """
    Esta funcion crea la estructura de habilidades asociadas
    al id.
    """
    entry = {'id': habilidad, 
             "ofertas": []}
    return entry    

def newTipo(tipo):
    """
    Esta funcion crea la estructura de ofertas asociadas
    por tipo de trabajo.
    """
    entry = {'tipo': tipo, 
             "ofertas": []}
    return entry

def nuevaInfoGeneral(key=None, value=None):
    if key == None:
        return {'keys': {}}
    else:
        return {'keys': {key:value}}

def newCityCounter(city, counter):
    entry = {"city": city,
             "conteo": counter}
    
def newLocacion(id_locacion):
    """
    Esta funcion crea la estructura de oferetas asociadas
    por la divisa.
    """
    entry = {'id': id_locacion, 
             "locaciones": 0}
    
    return entry

# Funciones de consulta

def habilidades(data_structs,id):
    lsthabilidades=[]
    lst= ht.get_value(data_structs['id_skill'],id)[1]['ofertas']
    for i in range(len(lst)):
        habilidad= lst[i]['name']
        lsthabilidades.append(habilidad)
    return lsthabilidades

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
    return data_structs['size']


def req_1(data_structs, initialDate, finalDate):
    """
    Función que soluciona el requerimiento 1
    """
    lst = bst.keys(data_structs['dateIndex'], initialDate, finalDate, compareDates) 
    ofertas= nf.newList()
    for i in range(nf.get_size(lst)):
        lista= nf.getElement(lst,i)['lstjobs']
        for j in range(nf.get_size(lista)) :   
            oferta= nf.getElement(lista,j)
            nf.addLast(ofertas,oferta)
        
    totcrimes = nf.get_size(ofertas)
    Sorts.TimSort(ofertas,fecha_salary)
    if totcrimes>10:
        tabular= nf.first_last(ofertas)
    else:
        tabular= ofertas
    para_tabular= []
    for oferta in tabular['elements']:
        fila= []
        fila.append(oferta["published_at"])
        fila.append(oferta['title'] )
        fila.append(oferta['company_name'] )
        fila.append(oferta['experience_level'] )
        fila.append(oferta['country_code'] )
        fila.append(oferta['city'] )
        fila.append(oferta['company_size'] )
        fila.append(oferta['workplace_type'] )
        fila.append(ht.get_value(data_structs['id_employment_type'],oferta['id'])[1]['currency_salary'])
        fila.append(oferta.get('skill',habilidades(data_structs,oferta['id'])))
        para_tabular.append(fila)

    headers = ['Fecha de publicación','Título de la oferta', 'Nombre de la empresa','Nivel','Pais','Ciudad' ,'Tamaño de la empresa','Tipo de ubicacion', 'Divisa','Habilidades']
    
    return totcrimes, (para_tabular, headers)

def req_2(data_structs, initialDate, finalDate):
    """
    Función que soluciona el requerimiento 2
    """
    lst_keys = bst_rn.keys(data_structs['salario_min'], initialDate, finalDate, compare)
    totcrimes = nf.get_size(lst_keys)
    counter_real = 0
    total = nf.newList()
    for i in range(0, totcrimes):
        lugar = bst_rn.get(data_structs['salario_min'], int(float(lst_keys['elements'][i])))['value']
        counter_real += data_size(lugar)
        item = Sorts.MergeSort(lugar, Sorts.mayor_menor_published)
        nf.extend(total, item)
    return counter_real, total

def req_3(data_structs, pais, experticia):
    """
    Función que soluciona el requerimiento 3
    """
    lista = data_structs['pais']
    lista = ht.get_value(lista, pais)[1]
    lista = ht.get_value(lista, experticia)[1]
    #conversión de hash a lista - temas de tiempo en la carga (remove)
    lista = ht.valueSet(lista)
    lista = Sorts.MergeSort(lista, Sorts.published_salario)
    return data_size(lista), lista
    
    

def req_4(data_structs,ciudad,ubicacion):
    """
    Función que soluciona el requerimiento 4
    """
    # TODO: Realizar el requerimiento 4
    ofertas = data_structs['ciudad']
    ofertas = ht.get_value(ofertas, ciudad)[1]
    ofertas = ht.get_value(ofertas, ubicacion)[1]
    ofertas = ht.valueSet(ofertas)
    ofertas = Sorts.TimSort(ofertas, Sorts.published_salario)
    return data_size(ofertas), ofertas


def req_5(data_structs,n,tamanio_low,tamanio_high,habilidad,nivel_low,nivel_high):
    """
    Función que soluciona el requerimiento 5
    """
    #Carga de datos: updateSizeIndex, addLevelTree, newSkillIndex, newLevelEntry, newSkillEntry
    arbol=data_structs['sizeIndex']
    en_rango= bst.keys(arbol,tamanio_low,tamanio_high,compare)
    arbol_nivel= nf.newList()
    lsthabilidad= nf.newList()
    lstfinal= nf.newList()
    for i in range(nf.get_size(en_rango)):
        fecha= nf.getElement(en_rango,i)
        mapa= fecha['skillIndex']
        la_habilidad= ht.get_value(mapa,habilidad)
        if la_habilidad!= None:
            nf.addLast(arbol_nivel,la_habilidad[1]['levelTree'])
            for i in range(nf.get_size(la_habilidad[1]['lstjobs'])):
                oferta= nf.getElement(la_habilidad[1]['lstjobs'],i)
                nf.addLast(lsthabilidad,oferta)
    total_ofertas= nf.get_size(lsthabilidad)
    for i in range(nf.get_size(arbol_nivel)):
        el_arbol= nf.getElement(arbol_nivel,i)
        nivel_rango= bst.keys(el_arbol,nivel_low,nivel_high,compare)
        for i in range(nf.get_size(nivel_rango)):
            lst= nf.getElement(nivel_rango,i)['lstjobs']
            for j in range(nf.get_size(lst)): 
                oferta= nf.getElement(lst,j)
                nf.addLast(lstfinal,oferta)
    Sorts.TimSort(lstfinal,fecha_salary)
    if nf.get_size(lstfinal)>n:
        antiguas= nf.subList(lstfinal,0,n)
    else:
        antiguas= lstfinal
    para_tabular= []
    for oferta in antiguas['elements']:
        fila= []
        fila.append(oferta["published_at"])
        fila.append(oferta['title'] )
        fila.append(oferta['company_name'] )
        fila.append(oferta['experience_level'] )
        fila.append(oferta['country_code'] )
        fila.append(oferta['city'] )
        fila.append(oferta['company_size'] )
        fila.append(oferta['workplace_type'] )
        fila.append(oferta.get('salary',ht.get_value(data_structs['id_employment_type'],oferta['id'])[1]['salary_from']))
        fila.append(oferta.get('skill',habilidades(data_structs,oferta['id'])))
        para_tabular.append(fila)

    headers = ['Fecha de publicación','Título de la oferta', 'Nombre de la empresa', 'Nivel de experticia','Pais','Ciudad' ,'Tamaño de la empresa','Tipo de ubicacion','Salario minimo', 'Habilidades']
    
    return total_ofertas, (para_tabular, headers)

def req_6(data_structs,n,initialDate,finalDate,salMin,salMax):
    """
    Función que soluciona el requerimiento 6
    """
    mapa_ciudades= ht.hash_table(200,lfactor)
    en_rango= bst.keys(data_structs['dateIndex'], initialDate, finalDate, compareDates)
    lstfinal= nf.newList()
    for i in range(nf.get_size(en_rango)):
        fecha= nf.getElement(en_rango,i)
        arbol2= fecha['salaryTree']
        en_salario=bst.keys(arbol2,salMin, salMax, compare)
        for j in range(nf.get_size(en_salario)):
            salario= nf.getElement(en_salario,j)
            oferta= salario['lstjobs']
            for k in range(nf.get_size(oferta)):
                el_salario= nf.getElement(oferta,k)
                nf.addLast(lstfinal,el_salario)
                ciudad=el_salario['city']
                if ht.get_value(mapa_ciudades,ciudad):
                    e = (ht.get_value(mapa_ciudades,ciudad))[1]
                else:
                    e = nf.newList()
                    ht.put(mapa_ciudades, ciudad, e)
                nf.addLast(e,el_salario)
    total_ofertas= nf.get_size(lstfinal)
    lstciudades= ht.keySet(mapa_ciudades)
    total_ciudades= nf.get_size(lstciudades)
    lstciudades=Sorts.MergeSort(lstciudades,Sorts.menor_mayor)
    i=0
    nciudades= nf.newList()
    while n>0 and total_ciudades>=i:
        ciudad=nf.getElement(lstciudades,i)
        nf.addLast(nciudades, ciudad)
        n-=1
        i+=1
    mayor=0
    c_mayor= None
            
    for i in range(nf.get_size(lstciudades)):
        ciudad= nf.getElement(lstciudades,i)
        ofertas= nf.get_size(ht.get_value(mapa_ciudades,ciudad)[1])
        if ofertas>mayor:
            mayor= ofertas
            c_mayor= ciudad
    
    lsttabular= ht.get_value(mapa_ciudades,c_mayor)
    if lsttabular!= None:
        lsttabular=lsttabular[1]        
        if nf.get_size(lsttabular)>10:
            tabular= nf.first_last(lsttabular)['elements']
        else:
            tabular= lsttabular['elements']
    else:
        tabular= []
    para_tabular= []
    for oferta in tabular:
        fila= []
        fila.append(oferta["published_at"])
        fila.append(oferta['title'] )
        fila.append(oferta['company_name'] )
        fila.append(oferta['experience_level'] )
        fila.append(oferta['country_code'] )
        fila.append(oferta['city'] )
        fila.append(oferta['company_size'] )
        fila.append(oferta['workplace_type'] )
        fila.append(oferta.get('salary',ht.get_value(data_structs['id_employment_type'],oferta['id'])[1]['salary_from']))
        fila.append(oferta.get('skill',habilidades(data_structs,oferta['id'])))
        para_tabular.append(fila)

    headers = ['Fecha de publicación','Título de la oferta', 'Nombre de la empresa', 'Nivel de experticia','Pais','Ciudad' ,'Tamaño de la empresa','Tipo de ubicacion','Salario minimo', 'Habilidades']
    return total_ofertas, total_ciudades, nciudades['elements'], c_mayor, (para_tabular,headers)

def req_7(data_structs,anio,pais,conteo):
    """
    Función que soluciona el requerimiento 7
    """
    el_anio= ht.get_value(data_structs['anio'],anio)[1]
    lst_anio= el_anio['lstjobs']
    mapa_paises= el_anio['countryMap']
    total_anio= nf.get_size(lst_anio)
    el_pais=ht.get_value(mapa_paises,pais)[1]
    lst_pais= el_pais['lstjobs']
    total_histograma= nf.get_size(lst_pais)
    if conteo=='experticia':
        propiedad= 'levelMap'
    elif conteo== 'habilidad':
        propiedad= 'skillMap'
    else:
        propiedad= 'locationMap'
    el_mapa= el_pais[propiedad]
    llaves= ht.keySet(el_mapa)
    frecuencias= nf.newList()
    for i in range(nf.get_size(llaves)):
        llave= nf.getElement(llaves,i)
        valores= ht.get_value(el_mapa, llave)[1]['lstjobs']
        frecuencia= nf.get_size(valores)
        nf.addLast(frecuencias,frecuencia)
    minimo= nf.getElement(llaves,nf.isPresent(frecuencias,nf.find_min(frecuencias)))
    maximo= nf.getElement(llaves,nf.isPresent(frecuencias,nf.find_max(frecuencias)))
    
    if total_histograma>10:
        tabular= nf.first_last(lst_pais)
    else:
        tabular= lst_pais
    para_tabular= []
    for oferta in tabular['elements']:
        fila= []
        fila.append(oferta["published_at"])
        fila.append(oferta['title'] )
        fila.append(oferta['company_name'] )
        fila.append(oferta['country_code'] )
        fila.append(oferta['city'] )
        fila.append(oferta['company_size'] )
        fila.append(oferta.get('salary',ht.get_value(data_structs['id_employment_type'],oferta['id'])[1]['salary_from']))
        fila.append(conteo)
        para_tabular.append(fila)

    headers = ['Fecha de publicación','Título de la oferta', 'Nombre de la empresa','Pais','Ciudad' ,'Tamaño de la empresa','Salario minimo', 'Propiedad de conteo']
    
    return total_anio, total_histograma, minimo,maximo, (llaves['elements'],frecuencias['elements']), (para_tabular, headers)

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
    if data_1 == data_2:
        return 0
    elif data_1 > data_2:
        return 1
    else:
        return -1

def compareDates(date1, date2):
    """
    Compara dos fechas
    """
    date1= date1.date()
    date2= date2.date()
    if date1 == date2:
        return 0
    elif date1 > date2:
        return 1
    else:
        return -1

# Funciones de ordenamiento


def fecha_salary(a,b):
    if a['published_at']>b['published_at']:
        return True
    elif a['published_at']==b['published_at']:
        if a.get('salary','Unknown')!='Unknown' and b.get('salary','Unknown')!= 'Unknown':
            return a['salary']>b['salary']

def sort(data_structs):
    """
    Función encargada de ordenar la lista con los datos
    """
    #TODO: Crear función de ordenamiento
    pass
