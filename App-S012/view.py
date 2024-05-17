"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
assert cf
from tabulate import tabulate
from datetime import datetime
import matplotlib.pyplot as plt
# import matplotlib
# import traceback

default_limit = 1000 
sys.setrecursionlimit(default_limit*10)

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

# Se crea el controlador asociado a la vista

def new_controller(data_structure, data_size):
    """
    Se crea una instancia del controlador
    """
    control = controller.new_controller(data_structure, data_size)

    return control


# Imprimir menú

def print_menu():
    print("\nBIENVENIDO")
    print("0- Cargar información")
    print("1- Ejecutar Requerimiento 1")
    print("2- Ejecutar Requerimiento 2")
    print("3- Ejecutar Requerimiento 3")
    print("4- Ejecutar Requerimiento 4")
    print("5- Ejecutar Requerimiento 5")
    print("6- Ejecutar Requerimiento 6")
    print("7- Ejecutar Requerimiento 7")
    print("8- Configuración")
    print("9- Salir\n")


# Funciones para la carga de datos

def load_data(control, filename, memflag):
    """
    Carga los datos
    """
    jobs, jobs_by_date, time, memory = controller.load_data(control, filename, memflag)
    print("Datos cargados correctamente...")

    print_jobs(jobs, 3, 'load_data')

    return controller.get_data_size(jobs, lt), jobs_by_date, time, memory


# Funciones para imprimir datos

def print_data(control, id, type):
    """
    Función que imprime datos dado su ID
    """
    if type == 'load_data':
        job = controller.get_data(control, id)
        job_date = controller.convert_date(job['published_at'])

        data = [
            ('Fecha de publicación: ', job_date),
            ('Titulo de la oferta: ', job['title']),
            ('Nombre de la empresa: ', job['company_name']),
            ('Nivel de experiencia: ', job['experience_level']),
            ('País: ', job['country_code']),
            ('Ciudad: ', job['city'])
        ]
        

    elif type == 'req-1':
        job = controller.get_data(control, id)
        job_date = controller.convert_date(job['published_at'])

        data = [
            ('Fecha de publicación: ', job_date),
            ('Titulo de la oferta: ', job['title']),
            ('Nombre de la empresa: ', job['company_name']),
            ('Nivel de experiencia: ', job['experience_level']),
            ('País: ', job['country_code']),
            ('Ciudad: ', job['city']),
            ('Tamaño de la empresa: ', job['company_size']),
            ('Tipo de ubicación: ', job['workplace_type']),
            ('Habilidades solicitadas: ', job['skills'])
        ]

    elif type == 'req-4':
        job = controller.get_data(control, id)
        job_date = controller.convert_date(job['published_at'])

        data = [
            ('Fecha de publicación: ', job_date),
            ('Titulo de la oferta: ', job['title']),
            ('Nombre de la empresa: ', job['company_name']),
            ('Nivel de experiencia: ', job['experience_level']),
            ('País: ', job['country_code']),
            ('Ciudad: ', job['city']),
            ('Tamaño de la empresa: ', job['company_size']),
            ('Tipo de ubicación: ', job['workplace_type']),
            ('Salario mínimo ofertado: ', job['min_salary']),
            ('Habilidades solicitadas: ', job['skills'])
        ]

    elif type == 'req-7':
        job = controller.get_data(control, id)
        job_date = controller.convert_date(job['published_at'])

        data = [
            ('Fecha de publicación: ', job_date),
            ('Titulo de la oferta: ', job['title']),
            ('Nombre de la empresa: ', job['company_name']),
            ('País: ', job['country_code']),
            ('Ciudad: ', job['city']),
            ('Tamaño de la empresa: ', job['company_size']),
            ('Salario mínimo ofertado: ', job['min_salary'])
        ]
        
    print(tabulate(data))


def print_jobs(control, sample, type):
    """
    Función que imprime las n ofertas de la lista
    """
    size = controller.get_data_size(control, lt)
    
    if size == 1:
        print('\nLa única oferta encontrada es: ')
        print_data(control, 1, type)

    elif size <= sample*2:
        print("\nLas", size, "ofertas son:")
        i = 1
        while i <= size:
            print_data(control, i, type)
            i += 1

    else:
        print("\nLas", sample, "primeras ofertas son:")
        i = 1
        while i <= sample:
            print_data(control, i, type)
            i += 1

        print("\nLas", sample, "últimas ofertas son:")
        i = size - sample + 1
        while i <= size:
            print_data(control, i, type)
            i += 1


# Funciones de requerimientos

def print_req_1(control,fehca_ini,fecha_fin,memflag):
    """
    Función que imprime la solución del Requerimiento 1 en consola
    """
    filtered_jobs, stadistics, deltaTime, deltaMemory = controller.req_1(control, fehca_ini,fecha_fin,memflag)

    if filtered_jobs is None:
        return None, 0, 0

    print('Ofertas encontradas: ' + str(controller.get_data_size(filtered_jobs, lt)))
    print_jobs(filtered_jobs, 5, 'req-1')

    return stadistics, deltaTime, deltaMemory


def print_req_2(control, salario_ini, salario_fin, memflag):
    """
    Función que imprime la solución del Requerimiento 2 en consola
    """
    total_offers, rta, deltaTime, deltaMemory  = controller.req_2(control, salario_ini, salario_fin, memflag)
    if rta is None:
        return None
        
    print_jobs(rta, 5,"req-4")
    print("El total de ofertas es: ", total_offers)
    print("El tiempo de respuesta es: ", deltaTime)
    print("La memoria utilizada es: ", deltaMemory)
    

def print_req_3(control, n_ofertas, experticia, pais, memflag):
    """
    Función que imprime la solución del Requerimiento 3 en consola
    """
    res, total_offers, deltaTime, deltaMemory = controller.req_3(control, n_ofertas, experticia, pais, memflag)
    if res is None:
        return None
    
    print_jobs(res, n_ofertas,"req-4")
    print("El total de ofertas es: ", total_offers)
    print("Tiempo de ejecucion: ", deltaTime)
    print("Memoria usada: ", deltaMemory)


def print_req_4(control, city, workplace, num_offers, memflag):
    """
    Función que imprime la solución del Requerimiento 4 en consola
    """
    filtered_jobs, stadistics, deltaTime, deltaMemory = controller.req_4(control, city, workplace, num_offers, memflag)

    if filtered_jobs is None:
        return None, 0, 0
    
    print('Ofertas encontradas: ' + str(controller.get_data_size(filtered_jobs, lt)))
    print_jobs(filtered_jobs, 5, 'req-4')

    return stadistics, deltaTime, deltaMemory


def print_req_5(control,num_offers, lim_inf_comp, lim_sup_com, skill_name, lim_inf_hab, lim_sup_hab,memflag):
    """
    Función que imprime la solución del Requerimiento 5 en consola
    """
    filtered_jobs, stadistics, deltaTime, deltaMemory = controller.req_5(control, num_offers, lim_inf_comp, lim_sup_com, skill_name, lim_inf_hab, lim_sup_hab,memflag)

    if filtered_jobs is None:
        return None, 0, 0

    print('Ofertas encontradas: ' + str(controller.get_data_size(filtered_jobs, lt)))
    print_jobs(filtered_jobs, 5, 'req-4')

    return stadistics, deltaTime, deltaMemory


def print_req_6(control, dates, salary_range, num_cities, memflag):
    """
    Función que imprime la solución del Requerimiento 6 en consola
    """
    filtered_cities, stadistics, best_city, deltaTime, deltaMemory = controller.req_6(control, dates, salary_range, num_cities, memflag)

    if filtered_cities is None:
        return None, 0, 0
    
    print('Ciudades encontradas: ' + str(controller.get_data_size(filtered_cities, lt)) + '\n')
    for city in lt.iterator(filtered_cities):
        print(' · ' + city['name'])

    print('\n' + best_city['name'] + ' es la ciudad con mayor cantidad de ofertas con un total de ' + str(controller.get_data_size(best_city['offers'], lt)) + ' ofertas.')
    print_jobs(best_city['offers'], 5, 'req-4')

    return stadistics, deltaTime, deltaMemory


def print_req_7(control, country, year, search_area, memflag):
    """
    Función que imprime la solución del Requerimiento 7 en consola
    """
    filtered_jobs, coordinates, stadistics, deltaTime, deltaMemory = controller.req_7(control, country, year, search_area, memflag)

    print('\nOfertas para gráficar: ' + str(controller.get_data_size(filtered_jobs, lt)))
    print('Imprimiendo gráfica...')

    if search_area == 'experience_level':
        search_area = 'Nivel de experticia'

    elif search_area == 'workplace_type':
        search_area = 'Tipo de ubicación'

    else:
        search_area = 'Nivel de habilidad'

    plt.bar(coordinates[0], coordinates[1], color='purple', edgecolor='black')

    for i in range(len(coordinates[0])):
        plt.text(coordinates[0][i], coordinates[1][i], str(coordinates[1][i]), ha='center', va='bottom')

    plt.xlabel(search_area, weight='bold')
    plt.ylabel('Cantidad de ofertas', weight='bold')
    plt.title(f'[{country.upper()}] {search_area} - {year}', weight='bold')
    plt.show()

    if filtered_jobs is None:
        return None, 0, 0

    print_jobs(filtered_jobs, 5, 'req-7')

    return stadistics, deltaTime, deltaMemory


# Funciones adicionales

def choose_data_structure():
    """
    Función que permite elegir la estructura de datos
    """
    print("""\nPor favor elija la estructura de datos que prefiera:
    1. Binary Search Tree (BST)
    2. Red-Black Tree (RBT)\n""")

    user_input = int(input("Seleccione una opción: "))

    if user_input == 1:
        data_structure = 'BST'
    else:
        data_structure = 'RBT'

    print('Ha escogido ' + str(data_structure) + ' como estructura de datos.')
    
    return data_structure


def choose_data_size():
    """
    Función que permite cambiar el tamaño de los datos
    """
    print("""\nPor favor elija el tamaño de archivo a cargar:
    1. Small
    2. Medium
    3. Large
    4. Elegir porcentaje\n""")

    choice = int(input('Seleccione una opción: '))

    if choice == 1:
        return 'small', 120000
    elif choice == 2:
        return 'medium', 200000
    elif choice == 3:
        return 'large', 204000
    else:
        pct_input = int(input('Ingrese el porcentaje que desea ver: '))
        pct = (pct_input // 10) * 10

        if pct > 50:
            return str(pct) + '-por', 140000
        else:
            return str(pct) + '-por', 210000


def choose_sort_algorithm():
    """
    Función que permite elegir el algoritmo de ordenamiento
    """
    print("""\nSeleccione el algoritmo de ordenamiento:
    1. Selection Sort
    2. Insertion Sort
    3. Shell Sort
    4. Merge Sort
    5. Quick Sort\n""")
    
    choice = int(input('Seleccione una opción: '))

    return choice


def choose_memory_measurement():
    """
    Función que permite elegir si se desea medir la memoria
    """
    print("\nDesea observar el uso de memoria? (y/n)")
    
    memflag = input('Respuesta: ')
    memflag = castBoolean(memflag.lower())

    return memflag


def castBoolean(value):
    """
    Convierte un valor a booleano
    """
    if value in ('si', 's', 'yes', 'y', '1'):
        return True
    else:
        return False
    

def select_search_area():
    """
    Funcion que permite elegir la propiedad de interés
    """
    print("""\nSeleccione la propiedad de interés:
    1. Nivel de experticia
    2. Tipo de ubicación
    3. Habilidades\n""")

    choice = input('Seleccione una opción: ')

    search_areas = {
        '1': 'experience_level',
        '2': 'workplace_type',
        '3': 'skills'
    }

    return search_areas[choice]


def settings():
    """
    Configura las condiciones de la aplicación
    """
    print("""\nPor favor elije que deseas modificar:
    1. Tamaño de los datos
    2. Estructura de datos
    3. Algoritmo de ordenamiento
    4. Medición de memoria
    0. Cancelar\n""")
    
    choice = int(input("Selecciona una opción: "))

    if choice == 1: # Cambiar tamaño de los datos
        filename, data_size = choose_data_size()
        print('Has escogido el tamaño de archivo: ' + filename)
        print('\nSeleccione la opción 0 para volver a cargar los datos...')

        return filename, choice

    elif choice == 2: # Cambiar la estructura de datos
        data_structure = choose_data_structure()     
        print('\nSeleccione la opción 0 para volver a cargar los datos...')

        return data_structure, choice

    elif choice == 3: # Cambiar algoritmo de ordenamiento
        algorithm = choose_sort_algorithm()
        selected_algo = controller.set_sort_algorithm(algorithm)
        print("Eligió la configuración - " + selected_algo)

        return None, None

    elif choice == 4: # Cambiar medicion de memoria
        memflag = choose_memory_measurement()

        return memflag, choice

    else:
        print('Regresando al menú principal...')
        
        return None, None


# Parametros para la ejecucion del programa
control = None
filename = None
data_structure = None
algorithm = None
memflag = None

def menu_cycle(control, filename, data_structure, algorithm, memflag):
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')

        if int(inputs) == 0: # Carga de datos
            if data_structure == None:
                data_structure = choose_data_structure()    
        
            if filename == None:
                filename, data_size = choose_data_size()
                print('Ha escogido el tamaño de archivo: ' + filename)

            if algorithm == None:
                algorithm = choose_sort_algorithm()
                selected_algo = controller.set_sort_algorithm(algorithm)
                print("Eligió la configuración - " + str(selected_algo))

            if memflag == None:
                memflag = choose_memory_measurement()

            print("\nCargando información de los archivos ....\n")
            control = new_controller(data_structure, data_size)

            jb, tree, time, memory = load_data(control, filename, memflag)
            delta_time = f"{time:.3f}"
            delta_memory = f"{memory:.3f}"

            print("Total de ofertas de trabajo cargadas: " + str(jb))
            print("Altura del arbol: " + str(controller.indexHeight(tree)))
            print("Elementos en el arbol: " + str(controller.get_data_size(tree, om)))

            print("\nTiempo de ejecución:", str(delta_time), "[ms]")
            print("Memoria utilizada:", str(delta_memory), "[kb]")

        elif int(inputs) == 1: # Requerimiento 1
            fehca_ini = input('\nIngrese la fecha inicial a buscar: ')
            fecha_fin = input('\nIngrese la fecha final a buscar: ')

            print('\nBuscando ofertas...')

            req_1, deltaTime, deltaMemory = print_req_1(control, fehca_ini,fecha_fin,memflag)

            if req_1 is not None:
                time = f"{deltaTime:.3f}"
                memory = f"{deltaMemory:.3f}"

                print(f"En total hay {str(req_1)} ofertas publicadas que cumplen con los criterios de búsqueda.")
                print(f"\nTiempo de ejecución : {str(delta_time)} [ms]")
                print(f"Memoria utilizada: {str(delta_memory)} [kb]")
            else:
                print('\nNo hay niguna oferta que cumpla con los criterios de busqueda.')

        elif int(inputs) == 2: # Requerimiento 2
            
            print("\nA continuación debe ingresar los limites de salario mínimo ofertado para la busqueda...")
            salario_ini = input('Ingrese el limite inferior de busqueda: ')
            salario_fin = input('Ingrese el limite superior de busqueda: ')
           
            print_req_2(control, salario_ini, salario_fin, memflag)

        elif int(inputs) == 3: # Requerimiento 3
            n_ofertas = int(input("Ingrese el numero de ofertas que quiere analizar: "))
            experticia = input("Ingrese la experticia que desea analizar: ")
            pais  = input("Ingrese el pais que desea analizar: ")
            print_req_3(control, n_ofertas, experticia, pais, memflag)

        elif int(inputs) == 4: # Requerimiento 4
            city = input('\nIngrese el nombre de la ciudad a buscar: ')
            workplace = input('Ingrese el tipo de ubicación de trabajo: ')
            num_offers = int(input('\nIngrese la cantidad de ofertas que desea listar: '))

            print('\nBuscando ofertas...')
            req_4, deltaTime, deltaMemory = print_req_4(control, city, workplace, num_offers, memflag)

            if req_4 is not None:
                time = f"{deltaTime:.3f}"
                memory = f"{deltaMemory:.3f}"

                print(f"En total hay {str(req_4)} ofertas publicadas que cumplen con los criterios de búsqueda.")
                print(f"\nTiempo de ejecución : {str(time)} [ms]")
                print(f"Memoria utilizada: {str(memory)} [kb]")
            else:
                print('\nNo hay niguna oferta que cumpla con los criterios de busqueda.')

        elif int(inputs) == 5: # Requerimiento 5
            num_offers = int(input('\nIngrese la cantidad de ofertas que desea listar: '))
            lim_inf_comp = int(input("\nIngrese el limite inferior del tamanio de la compania: "))
            lim_sup_com = int(input("\nIngrese el limite superior del tamanio de la compania: "))
            skill_name = input("\nIngrese el nombre de la habilidad a buscar: ")
            lim_inf_hab = int(input("\nIngrese el limite inferior del nivel de la habilidad: "))
            lim_sup_hab = int(input("\nIngrese el limite superior del nivel de la habilidad: "))

            print('\nBuscando ofertas...')

            req_5, deltaTime, deltaMemory = print_req_5(control,num_offers, lim_inf_comp, lim_sup_com, skill_name, lim_inf_hab, lim_sup_hab,memflag)
            
            if req_5 is not None:
                time = f"{deltaTime:.3f}"
                memory = f"{deltaMemory:.3f}"

                print(f"En total hay {str(req_5)} ofertas publicadas que cumplen con los criterios de búsqueda.")
                print(f"\nTiempo de ejecución : {str(delta_time)} [ms]")
                print(f"Memoria utilizada: {str(delta_memory)} [kb]")
            else:
                print('\nNo hay niguna oferta que cumpla con los criterios de busqueda.')

        elif int(inputs) == 6: # Requerimiento 6
            print("\nA continuación debe ingresar las fechas limites para la busqueda (ej. 2024-04-21)...")
            min_date = input('Ingrese el limite inferior de busqueda: ')
            max_date = input('Ingrese el limite superior de busqueda: ')

            min_date = f"{min_date}T00:00:00.000Z"
            max_date = f"{max_date}T00:00:00.000Z"

            print("\nA continuación debe ingresar los limites de salario mínimo ofertado para la busqueda...")
            min_salary = input('Ingrese el limite inferior de busqueda: ')
            max_salary = input('Ingrese el limite superior de busqueda: ')

            num_cities = int(input('\nIngrese la cantidad de ciudades que desea listar: '))

            print('\nBuscando ciudades...')
            req_6, deltaTime, deltaMemory = print_req_6(control, (min_date, max_date), (min_salary, max_salary), num_cities, memflag)

            if req_6 is not None:
                time = f"{deltaTime:.3f}"
                memory = f"{deltaMemory:.3f}"

                print(f"En total hay {str(req_6[0])} ofertas publicadas que cumplen con los criterios de búsqueda.")
                print(f"Se encontraron un total de {str(req_6[1])} ciudades que cumplen con las especificaciones.")
                print(f"\nTiempo de ejecución : {str(time)} [ms]")
                print(f"Memoria utilizada: {str(memory)} [kb]")
            else:
                print('\nNo hay niguna oferta que cumpla con los criterios de busqueda.')

        elif int(inputs) == 7: # Requerimiento 7
            country = input('\nIngrese el nombre del país a buscar: ')
            year = input('Ingrese el año de busqueda (ej. 2024): ')
            search_area = select_search_area()

            stadistics, deltaTime, deltaMemory = print_req_7(control, country, year, search_area, memflag)

            req_7, min_value, max_value = stadistics[0], stadistics[1], stadistics[2]
            
            if req_7 is not None:
                time = f"{deltaTime:.3f}"
                memory = f"{deltaMemory:.3f}"

                print(f"En total hay {str(req_7)} ofertas publicadas en el año ingresado.\n")
                print("Valor mínimo: " + min_value['name'] + " (" + str(min_value['offers']) + " ofertas).")
                print("Valor máximo: " + max_value['name'] + " (" + str(max_value['offers']) + " ofertas).")
                print(f"\nTiempo de ejecución : {str(time)} [ms]")
                print(f"Memoria utilizada: {str(memory)} [kb]")
            else:
                print('\nNo hay niguna oferta que cumpla con los criterios de busqueda.')

        elif int(inputs) == 8: # Configuraciones
            change, choice = settings()

            if choice == 1:
                filename = change
            elif choice == 2:
                data_structure = change
            elif choice == 4:
                memflag = change

        elif int(inputs) == 9:
            working = False
            print("\nGracias por utilizar el programa")
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)

# main del reto
if __name__ == "__main__":
    menu_cycle(control, filename, data_structure, algorithm, memflag)