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
# from DISClib.ADT import stack as st
# from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
# from DISClib.ADT import minpq as mpq
# from DISClib.ADT import indexminpq as impq
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import selectionsort as se
from DISClib.Algorithms.Sorting import mergesort as merg
from DISClib.Algorithms.Sorting import quicksort as quk
from datetime import datetime
assert cf
import folium

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""

# algoritmos de ordenamiento, por defecto no se ha seleccionado ninguno
sort_algorithm = None

# Construccion de modelos

def new_data_structs(data_structure, numelements):
    """
    Inicializa las estructuras de datos del modelo. Las crea de
    manera vacía para posteriormente almacenar la información.
    """
    catalog = { 
        'jobs': None,
        'jobs_by_date': None,
        'jobs_info': None
    }

    # Lista con ofertas de trabajo
    catalog['jobs'] = lt.newList('ARRAY_LIST')
    # Arbol. Llave: fecha de publicacion; Valor: lista con ofertas publicadas en esa fecha
    catalog['jobs_by_date'] = om.newMap(omaptype=data_structure, 
                                        cmpfunction=compare_dates)
    # Tabla de hash. Llave: id de la oferta; Valor: diccionario que contiene tres listas para la informacion adicional de la oferta
    catalog['jobs_info'] = mp.newMap(numelements, 
                                     maptype='CHAINING', 
                                     loadfactor=8)

    return catalog


# Funciones para agregar informacion al modelo

def add_map(catalog, data_structure, key, data):
    """
    Función para agregar nuevos elementos al mapa
    """
    data_structure.put(catalog, key, data)


def add_lst(catalog, data):
    """
    Función para agregar nuevas elementos a la lista
    """
    lt.addLast(catalog, data)


def add_job_by_date(catalog, key, data):
    """
    Función para agregar nuevas ofertas agrupadas por fecha
    """
    entry = get_entry(catalog, om, key)

    if entry is None:
        lst = lt.newList()
        add_map(catalog, om, key, lst)

    else:
        lst = me.getValue(entry)

    add_lst(lst, data)


# Funciones para creacion de datos

def new_job(catalog, data):
    """
    Crea una nueva estructura para modelar las ofertas
    """
    for key in data:
        if data[key] == 'Undefined':
            data[key] = 'Desconocido'

    # Agregar oferta a la lista 'jobs'
    add_lst(catalog['jobs'], data)
    # Agregar oferta al arbol 'jobs_by_date'
    add_job_by_date(catalog['jobs_by_date'], data['published_at'], data)
    # Crear estructura para modelar los datos
    job_info = {
        'skills': lt.newList(),
        'employment_types': lt.newList(),
        'multilocations': lt.newList()
    }
    # Agregar diccionario a la tabla de hash 'jobs_info'
    add_map(catalog['jobs_info'], mp, data['id'], job_info)


def new_employment_type(catalog, type, data):
    """
    Crea una nueva estructura para modelar los tipos de contratacion
    """
    for key in data:
        if data[key] == '':
            data[key] = '0'

    data['salary'] = exchange_money(data['currency_salary'], (int(data['salary_from']) + int(data['salary_to'])) / 2)
    data['salary_from'] = exchange_money(data['currency_salary'], data['salary_from'])
    data['salary_to'] = exchange_money(data['currency_salary'], data['salary_to'])

    new_data(catalog, type, data)


def new_data(catalog, type, data):
    """
    Obtiene la estructura para almacenar los datos
    """
    lst = me.getValue(get_entry(catalog, mp, data['id']))[type]
    add_lst(lst, data)


# Funciones de consulta

def get_data(catalog, id):
    """
    Retorna un dato por su ID.
    """
    return lt.getElement(catalog, id)


def get_entry(catalog, data_structure, key):
    """
    Retorna una entrada a partir de su llave
    """
    return data_structure.get(catalog, key)


def get_sublist(catalog, pos, numelem):
    """
    Retorna una sublista de una lista dada.
    """
    return lt.subList(catalog, pos, numelem)


def data_size(catalog, data_structure):
    """
    Retorna el tamaño de la lista de datos.
    """
    return data_structure.size(catalog)


def indexHeight(catalog):
    """
    Altura del arbol
    """
    return om.height(catalog)


# Funciones de requerimientos

def req_1(catalog, fehca_ini,fecha_fin):
    """
    Función que soluciona el requerimiento 1
    """
    jobs_by_date = catalog["jobs_by_date"]
    jobs = om.values(jobs_by_date,fehca_ini,fecha_fin)
    jobs_info = catalog['jobs_info']

    filtered_jobs = lt.newList('ARRAY_LIST')

    for joblist in lt.iterator(jobs):
        for job in lt.iterator(joblist):
            add_lst(filtered_jobs, job)
            info = me.getValue(get_entry(jobs_info, om, job['id']))
            skills = get_job_skills(info['skills'])
            job['skills'] = skills

            add_lst(filtered_jobs, job)

    # Ejecutar requerimiento 8 (mapa)
    req_8(filtered_jobs)

    if lt.isEmpty(filtered_jobs):

        # Si no se encuentra ninguna oferta devolver None
        return None, 0

    else:
        # Ordenar las ofertas, de mayor a menor, por la fecha de publicacion 
        sort(filtered_jobs, compare_dates_samuel)

        # Obtener el numero total de ofertas publicadas segun los requisitos
        total_offers = data_size(filtered_jobs, lt)
        
        return filtered_jobs, total_offers


def req_2(catalog, salario_ini, salario_fin):
    """
    Función que soluciona el requerimiento 2
    """
    jobs = catalog["jobs"]
    jobs_info = catalog['jobs_info']
    total_offers = 0
    rta = lt.newList("ARRAY_LIST")

    for job in lt.iterator(jobs):

        info = me.getValue(get_entry(jobs_info, om, job['id']))
        # Obtener el salario minimo de la oferta
        current_salary = get_min_salary(info['employment_types'])
        current_salary = get_min_salary(info['employment_types'])

        # Verificar si la oferta se encuentra entre el rango de salarios
        if float(salario_ini) <= float(current_salary) <= float(salario_fin):
            total_offers += 1
            skills = get_job_skills(info['skills'])

            # Añadir datos a la oferta
            job['min_salary'] = current_salary
            job['skills'] = skills
            lt.addLast(rta, job)

    # Ejecutar requerimiento 8 (mapa)
    req_8(rta)
    
    return total_offers, rta


def req_3(catalog, n_ofertas, experticia, pais):
    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3
    jobs = catalog["jobs"]
    jobs_info = catalog['jobs_info']
    res = lt.newList("ARRAY_LIST")
    total_offers = 0

    for job in lt.iterator(jobs):
        if job["country_code"].lower() == pais.lower():
            if job["experience_level"].lower() == experticia.lower():
                
                total_offers += 1

                info = me.getValue(get_entry(jobs_info, om, job['id']))
                # Obtener el salario minimo de la oferta
                current_salary = get_min_salary(info['employment_types'])
                skills = get_job_skills(info['skills'])

                # Añadir datos a la oferta
                job['min_salary'] = current_salary
                job['skills'] = skills
                lt.addLast(res,job)
    
    # Ejecutar requerimiento 8 (mapa)
    req_8(res)

    if lt.isEmpty(res):
        # Si no se encuentra ninguna oferta devolver None
        return None, 0
    
    else:

        # Obtener el numero total de ofertas publicadas segun los requisitos
        total_offers = data_size(res, lt)
        
        # Verificar que la lista sea menor o igual al tamaño recibido por parametro
        if total_offers > n_ofertas:
            res = get_sublist(res, 1, n_ofertas)

 

    return res, total_offers


def req_4(catalog, city, workplace, num_offers):
    """
    Función que soluciona el requerimiento 4
    """
    jobs = catalog['jobs']
    jobs_info = catalog['jobs_info']
    
    # Inicializar lista donde se guardaran las ofertas filtradas
    filtered_jobs = lt.newList('ARRAY_LIST')

    # Recorrer la lista de ofertas
    for job in lt.iterator(jobs):

        # Verificar si la ciudad coincide
        if job['city'].lower() == city.lower():

            # Verificar si la ubicacion de la oferta coincide
            if job['workplace_type'] == workplace.lower():

                info = me.getValue(get_entry(jobs_info, om, job['id']))
                # Obtener el salario minimo de la oferta
                min_salary = get_min_salary(info['employment_types'])
                # Obtener las habilidades solicitadas
                skills = get_job_skills(info['skills'])

                # Añadir datos a la oferta
                job['min_salary'] = min_salary
                job['skills'] = skills

                # Añadir oferta a la lista
                add_lst(filtered_jobs, job)

    # Ejecutar requerimiento 8 (mapa)
    req_8(filtered_jobs)

    if lt.isEmpty(filtered_jobs):
        # Si no se encuentra ninguna oferta devolver None
        return None, 0
    
    else:
        # Ordenar las ofertas, de mayor a menor, por la fecha de publicacion 
        sort(filtered_jobs, compare_date_and_salary)

        # Obtener el numero total de ofertas publicadas segun los requisitos
        total_offers = data_size(filtered_jobs, lt)
        
        # Verificar que la lista sea menor o igual al tamaño recibido por parametro
        if total_offers > num_offers:
            filtered_jobs = get_sublist(filtered_jobs, 1, num_offers)

        return filtered_jobs, total_offers


def req_5(catalog, num_offers, lim_inf_comp, lim_sup_com, skill_name, lim_inf_hab, lim_sup_hab):
    """
    Función que soluciona el requerimiento 5
    """
    jobs = catalog['jobs']
    jobs_info = catalog['jobs_info']

    filtered_jobs = lt.newList('ARRAY_LIST')
    
    # Recorrer la lista de ofertas
    for job in lt.iterator(jobs):

        # Verificar que el tamanio de la compania no sea Undefined. 
        if job["company_size"].isdigit():
            company_size = int(job["company_size"])
            # Verificar que el tamanio de la compania este dentro del rango
            if (company_size >= lim_inf_comp) and (company_size <= lim_sup_com):

                #Sacar las skills de la oferta y anadirlo a jobs
                info = me.getValue(get_entry(jobs_info, om, job['id']))

                # Obtener las skills.
                skills = get_job_skills_2(info['skills'])
                skills_2 = get_job_skills(info['skills'])


                # Obtener el salario minimo de la oferta.
                min_salary = get_min_salary(info['employment_types'])

                # Añadir datos a la oferta
                job['min_salary'] = min_salary

                
                
                job['skills'] = skills_2


                # Verificar que la skill por parametro este en la oferta
                if mp.get(skills,skill_name) is not None:

                    # Asignar el nivel de la experiencia a una variable
                    skill_value = me.getValue(mp.get(skills, skill_name))

                    # Verificar que el nivel de experiencia se encuentre dentro del rango
                    if (int(skill_value) >= lim_inf_hab) and (int(skill_value) <= lim_sup_hab):
                        
                        add_lst(filtered_jobs, job)
    
    # Ejecutar requerimiento 8 (mapa)
    req_8(filtered_jobs)

    if lt.isEmpty(filtered_jobs):

        # Si no se encuentra ninguna oferta devolver None
        return None, 0
    
    else:
        # Ordenar las ofertas, de mayor a menor, por la fecha de publicacion 
        sort(filtered_jobs, compare_date_and_salary_samuel)

        # Obtener el numero total de ofertas publicadas segun los requisitos
        total_offers = data_size(filtered_jobs, lt)

        # Verificar que la lista sea menor o igual al tamaño recibido por parametro
        if total_offers > num_offers:
            filtered_jobs = get_sublist(filtered_jobs, 1, num_offers)
        
        return filtered_jobs, total_offers
        

def req_6(catalog, dates, salary_range, num_cities):
    """
    Función que soluciona el requerimiento 6
    """
    jobs_by_date = catalog['jobs_by_date']
    jobs_info = catalog['jobs_info']

    # Inicializar la tabla donde se guardaran las ciudades filtradas
    cities = mp.newMap(1000,
                        maptype='PROBING',
                        loadfactor=0.1)

    total_offers = lt.newList()


    # Descomponer las tuplas de los rangos
    min_date, max_date = dates[0], dates[1]
    min_salary, max_salary = salary_range[0], salary_range[1] 

    # Obtener las ofertas en un rango de fechas
    jobs = om.values(jobs_by_date, min_date, max_date)

    for lst_jobs in lt.iterator(jobs):

        for job in lt.iterator(lst_jobs):

            info = me.getValue(get_entry(jobs_info, om, job['id']))
            # Obtener el salario minimo de la oferta
            current_salary = get_min_salary(info['employment_types'])

            # Verificar si la oferta se encuentra entre el rango de salarios
            if float(min_salary) <= float(current_salary) <= float(max_salary):

                # Obtener las habilidades solicitadas
                skills = get_job_skills(info['skills'])

                # Añadir datos a la oferta
                job['min_salary'] = current_salary
                job['skills'] = skills

                # Agregar 1 a las ofertas que cumplen con los criterios de busqueda
                add_lst(total_offers,job)
                # Obtener la pareja (llave, valor) de la ciudad. Si no existe es None
                city = get_entry(cities, mp, job['city'])

                if city is None:
                    # Crear estructura para modelar los datos de las ciudades
                    city = {
                        'name': job['city'],
                        'offers': lt.newList('ARRAY_LIST')
                    }

                    # Agregar oferta a la lista de ofertas de la ciudad
                    add_lst(city['offers'], job)
                    # Agregar ciudad al mapa de ciudades
                    add_map(cities, mp, city['name'], city)

                else:
                    # Obtener valor de la ciudad
                    city = me.getValue(city)
                    # Agregar oferta a la lista de ofertas de la ciudad
                    add_lst(city['offers'], job)

    # Ordenar las ciudades, de mayor a menor, por cantidad de ofertas
    cities = sort(mp.valueSet(cities), compare_city_offers)
    # Obtener el numero total de ofertas publicadas segun los requisitos
    total_cities = data_size(cities, lt)

    # Verificar que la lista sea menor o igual al tamaño recibido por parametro
    if total_cities > num_cities:
        cities = get_sublist(cities, 1, num_cities)

    # Obtener la mejor ciudad y ordenar sus ofertas, de mayor a menor, por la fecha de publicacion
    best_city = lt.firstElement(cities)
    sort(best_city['offers'], compare_date_and_salary)
    # Ordenar ciudades alfabeticamente
    sort(cities, compare_city_name)

    # Ejecutar requerimiento 8 (mapa)
    req_8(total_offers)

    return cities, (data_size(total_offers,lt), total_cities), best_city


def req_7(catalog, country, year, search_area):
    """
    Función que soluciona el requerimiento 7
    """
    jobs_by_date = catalog['jobs_by_date']
    jobs_info = catalog['jobs_info']

    filtered_jobs = om.newMap(omaptype='BST',
                              cmpfunction=compare_dates)
    graphical_offers = lt.newList()
    total_offers = 0

    # Obtener el intervalo del año de busqueda
    min_date, max_date = year + '-01-01', year + '-12-31'
    # Obtener las ofertas en un rango de fechas
    jobs = om.values(jobs_by_date, min_date, max_date)

    for lst_jobs in lt.iterator(jobs):

        # Agregar numero de ofertas al total de ofertas encontradas en ese año
        total_offers += data_size(lst_jobs, lt)

        for job in lt.iterator(lst_jobs):

            info = me.getValue(get_entry(jobs_info, om, job['id']))
            # Obtener el salario minimo de la oferta
            min_salary = get_min_salary(info['employment_types'])

            # Añadir datos a la oferta
            job['min_salary'] = min_salary
            job['skills'] = info['skills']

            if country.upper() == job['country_code']:
                # Añadir oferta al total de ofertas utilizadas para graficar 
                add_lst(graphical_offers, job)

                if search_area == 'skills':
                    
                    for skill in lt.iterator(job['skills']):
                    
                        entry = get_entry(filtered_jobs, om, skill['level'])

                        if entry is None:
                            # Crear estructura para modelar los datos de cada propiedad
                            property = {
                                'name': skill['level'],
                                'offers': 1
                            }
                            # Añadir propiedad al mapa
                            add_map(filtered_jobs, om, property['name'], property)

                        else:
                            # Obtener propiedad y agregarle 1 oferta
                            property = me.getValue(entry)
                            property['offers'] += 1

                else:

                    entry = get_entry(filtered_jobs, om, job[search_area])

                    if entry is None:
                        # Crear estructura para modelar los datos de cada propiedad
                        property = {
                            'name': job[search_area],
                            'offers': 1
                        }
                        # Añadir propiedad al mapa
                        add_map(filtered_jobs, om, property['name'], property)

                    else:
                        # Obtener propiedad y agregarle 1 oferta
                        property = me.getValue(entry)
                        property['offers'] += 1

    # Obtener los valores
    properties = om.valueSet(filtered_jobs)
    x = []
    y = []

    for property in lt.iterator(properties):
        # Descomponer los ejes X (nombre de la propiedad) y Y (numero de ofertas)
        x.append(property['name'])
        y.append(property['offers'])

    # Ordenar los valores, de menor a mayor, por numero de ofertas
    sort(properties, compare_property_offers)

    # Ejecutar requerimiento 8 (mapa)
    req_8(graphical_offers)

    return graphical_offers, (x, y), (total_offers, lt.firstElement(properties), lt.lastElement(properties))


def req_8(jobs):
    """
    Función que soluciona el requerimiento 8
    """
    # Crear mapa
    map = folium.Map()

    for job in lt.iterator(jobs):
        # Obtener las coordenadas como una tupla (latitud, longitud)
        coordenates = (job["latitude"],job["longitude"])
        # Mensaje que se mostrara al hacer click sobre un marcador
        message = f"""  
        {job["company_name"]}

        {job['country_code']}
        """

        # Añadir marcador al mapa
        folium.Marker(location=coordenates,
                      tooltip=job["city"],
                      popup=message).add_to(map)
        
    # Guardar mapa para poder visualizarlo
    map.save("mapa_req_8.html")


# Funciones utilizadas para comparar elementos

def compare_dates(date1, date2):
    """
    Función encargada de comparar dos llaves
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1

def compare_date_and_company(data_1, data_2):
    """
    Función encargada de comparar dos fechas
    """
    date_1 = convert_date(data_1['published_at'])
    date_2 = convert_date(data_2['published_at'])

    if date_1 > date_2:
        return True
    
    elif date_1 == date_2:
        if data_1['company_name'].lower() < data_2['company_name'].lower():
            return True
        
    return False
 
def compare_date_and_salary(data_1, data_2):
    """
    Función encargada de comparar dos fechas y salario mínimo ofertado
    """
    date_1 = convert_date(data_1['published_at'])
    date_2 = convert_date(data_2['published_at'])

    if date_1 > date_2:
        return True
    
    elif date_1 == date_2:
        if data_1['min_salary'] > data_2['min_salary']:
            return True
        
    return False

def compare_dates_samuel(data_1, data_2):
    """
    Función encargada de comparar dos fechas
    """
    date_1 = convert_date(data_1['published_at'])
    date_2 = convert_date(data_2['published_at'])

    if date_1 > date_2:
        return True
        
    return False

def compare_city_offers(data_1, data_2):
    """
    Función encargada de comparar la cantidad de ofertas de dos ciudades
    """
    if data_size(data_1['offers'], lt) > data_size(data_2['offers'], lt):
        return True
    else:
        return False 
    
def compare_property_offers(data_1, data_2):
    """
    Función encargada de comparar la cantidad de ofertas de dos propiedades
    """
    if data_1['offers'] < data_2['offers']:
        return True
    else:
        return False 

def compare_city_name(data_1, data_2):
    """
    Función encargada de comparar dos nombres de ciudades
    """
    if data_1['name'].lower() < data_2['name'].lower():
        return True
    else:
        return False

def compare_date_and_salary_samuel(data_1, data_2):
    """
    Función encargada de comparar dos fechas y salario mínimo ofertado
    """
    date_1 = convert_date(data_1['published_at'])
    date_2 = convert_date(data_2['published_at'])

    if date_1 < date_2:
        return True
    
    elif date_1 == date_2:
        if data_1['min_salary'] > data_2['min_salary']:
            return True
        
    return False

# Funciones de ordenamiento

def select_sort_algorithm(algorithm):
    """
    Permite seleccionar el algoritmo de ordenamiento.

    Args:
        algorithm (int): opcion de algoritmo de ordenamiento, las opciones son:
            1: Selection Sort
            2: Insertion Sort
            3: Shell Sort
            4: Merge Sort
            5: Quick Sort

    Returns:
        list: sort_algorithm (sort) la instancia del ordenamiento y
        msg (str) el texto que describe la configuracion del ordenamiento
    """
    sort_algorithm = None
    msg = None

    # opcion 1: Selection Sort
    if algorithm == 1:
        sort_algorithm = se
        msg = "Selection Sort"
    
    # opcion 2: Insertion Sort
    elif algorithm == 2:
        sort_algorithm = ins
        msg = "Insertion Sort"

    # opcion 3: Shell Sort
    elif algorithm == 3: 
        sort_algorithm = sa
        msg = "Shell Sort"

    # opcion 4: Merge Sort
    elif algorithm == 4:
        sort_algorithm = merg
        msg = "Merge Sort"

    # opcion 5: Quick Sort
    elif algorithm == 5:
        sort_algorithm = quk
        msg = "Quick Sort"

    return sort_algorithm, msg

def sort(catalog, sort_criteria=compare_date_and_company):
    """
    Función encargada de ordenar la lista con los datos
    """
    sorted_catalog = sort_algorithm.sort(catalog, sort_criteria)
    catalog = sorted_catalog

    return catalog


# Funciones adicionales

def convert_date(date):
    """
    Retorna una fecha en formato datetime
    """
    return datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')

def exchange_money(currency, value):
    """
    Retorna el valor en doláres
    """
    new_value = value

    if currency == 'pln':
        new_value = int(value) * 0.25
    elif currency == 'eur':
        new_value = int(value) * 1.07
    
    return str(new_value)

def get_job_salary(salaries):
    """
    Retorna la suma de los salarios
    """
    job_salary = 0

    for salary in lt.iterator(salaries):
        job_salary += int(salary['salary'])

    return job_salary / data_size(salaries, lt)

def get_job_skills(skills):
    """
    Retorna los nombres de las habilidades solicitadas
    """
    job_skills = ''

    for skill in lt.iterator(skills):
        job_skills += skill['name'] + ', '

    return job_skills[:-2]

def get_min_salary(salaries):
    """
    Retorna el salario minimo ofertado
    """
    min_salary = lt.firstElement(salaries)['salary_from']

    for salary in lt.iterator(salaries):

        if float(salary['salary_from']) < float(min_salary):
            min_salary = salary['salary_from']

    return min_salary

def get_job_skills_2(skills):
    """
    Retorna un mapa donde la llave es el nombre d ela skill y el valor es el nivel
    """
    mapa = mp.newMap(maptype='CHAINING', loadfactor=8)

    for skill in lt.iterator(skills):

        nombre = skill['name']
        nivel = skill["level"]

        mp.put(mapa, nombre , nivel)

    return mapa