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
from datetime import datetime as dt
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import orderedmap as om
from DISClib.ADT import map as mp
assert cf
from tabulate import tabulate
import traceback
import threading 
from datetime import datetime
import matplotlib.pyplot as plt
import folium
import webbrowser
import subprocess
import pandas
from tqdm import tqdm
from tqdm.auto import tqdm
from colorama import Fore, Back, Style
default_limit = 1000
sys.setrecursionlimit(default_limit*10)
"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def new_controller():
    """
        Se crea una instancia del controlador
    """
    control = controller.new_controller()
    return control


def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Ejecutar Requerimiento 1")
    print("3- Ejecutar Requerimiento 2")
    print("4- Ejecutar Requerimiento 3")
    print("5- Ejecutar Requerimiento 4")
    print("6- Ejecutar Requerimiento 5")
    print("7- Ejecutar Requerimiento 6")
    print("8- Ejecutar Requerimiento 7")
    print("9- Ejecutar Requerimiento 8")
    print("0- Salir")

def print_menu_req8():
    print("SELECCIONE EL MAPA QUE QUIERA GRAFICAR")
    print("1- Requerimiento 1")
    print("2- Requerimiento 2")
    print("3- Requerimiento 3")
    print("4- Requerimiento 4")
    print("5- Requerimiento 5")
    print("6- Requerimiento 6")
    print("7- Requerimiento 7")
    print("8- Mapa interactivo de todos los requerimientos en un solo mapa---- (cuidado el computador explotara seguro)")
    print("0- Salir")
    
    
def select_file_type():
    print('Archivos disponibles por tamaño: ')
    print('\n(1) small')
    print('(2) 10-por')
    print('(3) 20-por')
    print('(4) 30-por')
    print('(5) 50-por')
    print('(6) 80-por')
    print('(7) large\n')

    file_type_input = int(input('Seleccione el tamaño del archivo deseado: '))

    if file_type_input == 1:
        file_type = 'small'
    elif file_type_input == 2:
        file_type = '10-por'
    elif file_type_input == 3:
        file_type = '20-por'
    elif file_type_input == 4:
        file_type = '30-por'
    elif file_type_input == 5:
        file_type = '50-por'
    elif file_type_input== 6:
        file_type = '80-por'
    else:
        if file_type_input != 7:
            print('Respuesta inválida, se cargarán los datos con el la etiqueta "large".')
        file_type = 'large'
        
    return file_type


def load_data(control, file_size):
    """
    Carga los datos
    """
    jobs_size, employments_size, multilocations_size, skills_size = controller.load_data(control, file_size)

    return jobs_size, employments_size, multilocations_size, skills_size
def print_data(control):
    respuesta = []   
    if lt.size(control) > 0:
        for data in lt.iterator(control):
            for valor in data:
                fila = []
                if isinstance(valor, dict):
                    if len(valor) >= 10:
                        indices_primeros = list(range(1, 6))
                        indices_ultimos = list(range(len(valor) - 4, len(valor) + 1))
                        indices_combinados = indices_primeros + indices_ultimos
                        respuesta_final_d = dict(list(valor.items())[:5] + list(valor.items())[-5:])
                        fila.append(tabulate(respuesta_final_d.items(), headers=["TITULO", "VALOR"], tablefmt='simple', showindex=indices_combinados))
                    else:
                        fila.append(tabulate(list(valor.items()), headers=["Key", "Value"], tablefmt='simple'))
                elif isinstance(valor, list):
                    if len(valor) >= 10:
                        indices_primeros = list(range(1, 6))
                        indices_ultimos = list(range(len(valor) - 4, len(valor) + 1))
                        indices_combinados = indices_primeros + indices_ultimos
                        respuesta_final_d = valor[:5] + valor[-5:]
                        fila.append(tabulate([k for k in (respuesta_final_d)], tablefmt='simple', showindex=indices_combinados))
                    else:
                        indices_primeros = list(range(1, len(valor)+1))
                        fila.append(tabulate([k for k in (valor)], tablefmt='simple',showindex=indices_primeros))
                else:
                    fila.append(valor)
            respuesta.append(fila)
    
    
    
        indices_primeros = list(range(1, len(respuesta)+1))
        print(tabulate(respuesta,tablefmt ='fancy_grid',showindex=indices_primeros))
    else:
        print("la lista esta vacia <3 // No hay datos disponibles ;(  ")

def tabular_6(control):
    titulos = []
    respuesta_final = []
    datos_por_ciudad = {}

    
    
    
    if lt.size(control) > 0:
        x = lt.getElement(control, 1)
        for h in x.keys():
            titulos.append(h)

        for i in lt.iterator(control):
            for ciudad, trabajo in i.items():
                if ciudad not in datos_por_ciudad:
                    datos_por_ciudad[ciudad] = []
                datos_por_ciudad[ciudad].append(trabajo)
                
                

        filas = []
        counter = 1
        muro = False
        for ciudad, trabajos in datos_por_ciudad.items():
      
         
            if counter <= 5 and muro == False:             
                filas.append([f'--- {counter} --------- {ciudad} ---'])
                counter += 1 
                
            else:
                filas.append([f'------------ {ciudad} ---'])



                
            for trabajo in trabajos:
                if isinstance(trabajo, dict):
                    if len(trabajo) >= 10:
                        indices_primeros = list(range(1, 6))
                        indices_ultimos = list(range(len(trabajo) - 4, len(trabajo) + 1))
                        indices_combinados = indices_primeros + indices_ultimos
                        respuesta_final_d = dict(list(trabajo.items())[:5] + list(trabajo.items())[-5:])
                        filas.append([tabulate(respuesta_final_d.items(), headers=["TITULO", "VALOR"], tablefmt='simple',showindex=indices_combinados)])
                    else:
                        indices_primeros = list(range(1, len(trabajo)+1))
                        filas.append([ tabulate(list(trabajo.items()), headers=["Key", "Value"], tablefmt='simple',showindex=indices_primeros)])
                elif isinstance(trabajo, list):
                    if len(trabajo) >= 10:
                        indices_primeros = list(range(1, 6))
                        indices_ultimos = list(range(len(trabajo) - 4, len(trabajo) + 1))
                        indices_combinados = indices_primeros + indices_ultimos
                        respuesta_final_d = trabajo[:5] + trabajo[-5:]
                        filas.append([tabulate([k for k in (respuesta_final_d)], tablefmt='simple',showindex=indices_combinados)])
                    else:
                        indices_primeros = list(range(1, len(trabajo)+1))
                        filas.append([tabulate([k for k in (trabajo)], tablefmt='simple',showindex=indices_primeros)])
                else:
                    filas.append(trabajo)

        if len(filas) >= 20:
            filas = filas[:10] + filas[-10:]
            print(tabulate(filas, tablefmt='fancy_grid'))
        else:
            print(tabulate(filas, tablefmt='fancy_grid'))
    else:
        print("la lista esta vacia <3 // No hay datos disponibles ;(  ")

        
def tabular(control):
    
    titulos = []
    
    respuesta_final = []
    if lt.size(control) > 0:
        x = lt.getElement(control, 1)
        for h in x.keys():
            titulos.append(h)
        
        for i in lt.iterator(control):
            fila = []
            for clave, valor in i.items():
                if isinstance(valor, dict):
                    if len(valor) >= 10:
                        indices_primeros = list(range(1, 6))
                        indices_ultimos = list(range(len(valor) - 4, len(valor) + 1))
                        indices_combinados = indices_primeros + indices_ultimos
                        respuesta_final_d = dict(list(valor.items())[:5] + list(valor.items())[-5:])
                        fila.append(tabulate(respuesta_final_d.items(), headers=["TITULO", "VALOR"], tablefmt='simple', showindex=indices_combinados))
                    else:
                        fila.append(tabulate(list(valor.items()), headers=["Key", "Value"], tablefmt='simple'))
                elif isinstance(valor, list):
                    if len(valor) >= 10:
                        indices_primeros = list(range(1, 6))
                        indices_ultimos = list(range(len(valor) - 4, len(valor) + 1))
                        indices_combinados = indices_primeros + indices_ultimos
                        respuesta_final_d = valor[:5] + valor[-5:]
                        fila.append(tabulate([k for k in (respuesta_final_d)], tablefmt='simple', showindex=indices_combinados))
                    else:
                        indices_primeros = list(range(1, len(valor)+1))
                        fila.append(tabulate([k for k in (valor)], tablefmt='simple',showindex=indices_primeros))
                else:
                    fila.append(valor)
            respuesta_final.append(fila)
        
        if len(respuesta_final) >= 10:
            indices_primeros = list(range(1, 6))
            indices_ultimos = list(range(len(respuesta_final) - 4, len(respuesta_final) + 1))
            indices_combinados = indices_primeros + indices_ultimos
            
            respuesta_final = respuesta_final[:5] + respuesta_final[-5:]
            
            print(tabulate(respuesta_final, headers=titulos, tablefmt='fancy_grid', showindex=indices_combinados))
        else:
            indices_primeros = list(range(1, len(respuesta_final)+1))
            print(tabulate(respuesta_final, headers=titulos, tablefmt='fancy_grid', showindex=indices_primeros))
    else:
        print("la lista esta vacia <3 // No hay datos disponibles ;(  ")

def generacion_respuesta(titulos, data_list):
    respuesta = lt.newList("ARRAY_LIST")
    
    for data in lt.iterator(data_list):
        nuevo_diccionario = {i: None for i in titulos}
            
        if isinstance(data,list):    
            for data1 in data:
                for key, value in data1.items():
                
                    if key in titulos:
                        nuevo_diccionario[key] = value
        else: 
            for key, value in data.items():
                
                    if key in titulos:
                        nuevo_diccionario[key] = value
        lt.addLast(respuesta, nuevo_diccionario)
        
    return respuesta
def data_sample(control):
    jobs = control["model"]["jobs"]
    jobs = om.valueSet(jobs)
    jobs_size = lt.size(jobs)
    jobs_first = lt.subList(jobs, 0, 3)
    jobs_last = lt.subList(jobs, int(jobs_size - 3), 3)
    
    multilocations = control["model"]["multilocations"]
    multilocations = mp.valueSet(multilocations)
    multilocations_size = lt.size(multilocations)
    multilocations_first = lt.subList(multilocations, 0, 3)
    multilocations_last = lt.subList(multilocations, int(multilocations_size - 3), 3)

    employments = control["model"]["employments"]
    employments = mp.valueSet(employments)
    employments_size = lt.size(employments)
    employments_first = lt.subList(employments, 0, 3)
    employments_last = lt.subList(employments, int(employments_size - 3), 3)

    skills = control["model"]["skills"]
    skills = mp.valueSet(skills)
    skills_size = lt.size(skills)
    skills_first = lt.subList(skills, 0, 3)
    skills_last = lt.subList(skills, int(skills_size - 3), 3)
    
    titulos = ["published_at","title","company_name","experience_level","country_code","city","company_size"]

    print('\nPrimeros tres elementos del archivo Jobs')
    jobs_first = generacion_respuesta(titulos,jobs_first)
    tabular(jobs_first)
    print('\nUltimos tres elementos del archivo Jobs')
    jobs_last = generacion_respuesta(titulos,jobs_last)
    tabular(jobs_last)
    print('\n\nPrimeros tres elementos del archivo Multilocations')
    print_data(multilocations_first)
    print('\nUltimos tres elementos del archivo Multilocations')
    print_data(multilocations_last)
    print('\n\nPrimeros tres elementos del archivo Employments')
    print_data(employments_first)
    print('\nUltimos tres elementos del archivo Employments')
    print_data(employments_last)
    print('\n\nPrimeros tres elementos del archivo Skills')
    print_data(skills_first)
    print('\nUltimos tres elementos del archivo Skills')
    print_data(skills_last)
    print('\n\n')

def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    fecha_inicial= str(input("""La fecha inicial del periodo a consultar (con formato "%Y-%m-%d"):  """))
    fecha_final= str(input("""La fecha final del periodo a consultar (con formato "%Y-%m-%d"):  """))
    t1 = controller.get_time()
    contador ,  respuesta = controller.req_1(control,fecha_inicial,fecha_final)
    tabular(respuesta)
    t2 = controller.get_time()
    dt = controller.delta_time(t1,t2)
    print ("El número total de ofertas laborales publicadas durante las fechas indicadas son: "+str(contador))
    print ("El tiempo transcurrido por el requerimiento fue: " +str(dt)+" ms")
    

def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    salario_minimo= int(input("""El límite inferior del salario mínimo ofertad:  """))
    salario_maximo= int(input("""El límite superior del salario mínimo ofertado:  """))
    t1 = controller.get_time()
    contador , respuesta = controller.req_2(control,salario_minimo,salario_maximo)
    tabular(respuesta)
    t2 = controller.get_time()
    dt = controller.delta_time(t1,t2)
    print ("El número total de ofertas laborales publicadas en los rangos salariales requeridos son: "+str(contador))
    print ("El tiempo transcurrido por el requerimiento fue: " +str(dt)+" ms")



def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    n= int(input("""El número (N) de ofertas laborales a consultar:  """))
    codigo_pais= str(input("""Código del país para la consulta (ej.: PL, CO, ES, etc):  """))
    nivel_experticia= str(input("""Nivel de experticia de las ofertas de interés (junior, mid, senior, indiferente):  """))
    t1 = controller.get_time()
    contador , respuesta = controller.req_3(control,n,codigo_pais,nivel_experticia)
    tabular(respuesta)
    t2 = controller.get_time()
    dt = controller.delta_time(t1,t2)
    print ("El número total de ofertas laborales publicadas en los rangos salariales requeridos son: "+str(contador))
    print ("El tiempo transcurrido por el requerimiento fue: " +str(dt)+" ms")


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    n_offers = int(input('El número (N) de ofertas laborales a consultar: '))
    city_name = str(input('Nombre de la ciudad para la consulta: '))
    job_location = str(input('Tipo de ubicación de trabajo ( remote, partialy, remote, office) : '))
    t1 = controller.get_time()
    ans, size = controller.req_4(control, n_offers, city_name, job_location)
    t2 = controller.get_time()
    dt = controller.delta_time(t1,t2)
    tabular(ans)
    print(f'El número total de ofertas publicadas para {city_name} con el tipo de ubicación {job_location} fue: {size}')
    print ("El tiempo transcurrido por el requerimiento fue: " +str(dt)+" ms")


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    n = int(input("""El número (N) de ofertas laborales a consultar:  """))
    li_companysize = str(input("""límite inferior del tamaño de la compañía: """))
    ls_companysize = str(input("""límite superior del tamaño de la compañía: """))
    skill = str(input("""Nombre de la habilidad solicitada: """))
    li_companyskill = int(input("""límite inferior del nivel de la habilidad: """))
    ls_companyskill = int(input("""límite superior del nivel de la habilidad: """))
    t1 = controller.get_time()
    contador , respuesta = controller.req_5(n,ls_companysize,li_companysize,skill,ls_companyskill,li_companyskill,control)
    tabular(respuesta)
    t2 = controller.get_time()
    dt = controller.delta_time(t1,t2)
    print ("El número total de ofertas laborales publicadas para las compañías con un tamaño y habilidad especificas es: "+str(contador))
    print ("El tiempo transcurrido por el requerimiento fue: " +str(dt)+" ms")
    


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    n= int(input("""El número (N) de ciudades a consultar:  """))
    fecha_inicial= str(input("""La fecha inicial del periodo a consultar (con formato "%Y-%m-%d"):  """))
    fecha_final= str(input("""La fecha final del periodo a consultar (con formato "%Y-%m-%d"):  """))
    salario_minimo= int(input("""El límite inferior del salario mínimo ofertad:  """))
    salario_maximo= int(input("""El límite superior del salario mínimo ofertado:  """))
    t1 = controller.get_time()
    contador,total_ciudades,n_ciudades_cumplen,respuesta = controller.req_6(control,n,fecha_inicial,fecha_final,salario_minimo,salario_maximo)
    tabular_6(respuesta)
    t2 = controller.get_time()
    dt = controller.delta_time(t1,t2)
    print ("El número total de ofertas laborales publicadas entre un par de fechas y que estén en un rango de salario ofertado: "+str(contador))
    print ("El número total de ciudades que cumplen con las especificaciones son: "+str(total_ciudades))
    print ("Las N ciudades que cumplan las condiciones especificadas ordenadas alfabéticamente son: "+str(n_ciudades_cumplen))
    print ("El tiempo transcurrido por el requerimiento fue: " +str(dt)+" ms")



def print_req_7(control):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    year = input('El año relevante (en formato “%Y”): ')
    country_code = input('Código del país para la consulta (ej.: PL, CO, ES, etc): ')
    property_input = input('La propiedad de conteo (experticia [1], ubicación [2], o habilidad [3]): ')
    t1 = controller.get_time()
    ans, general_size, graph_size, distribution = controller.req_7(control, year, country_code, property_input)
    t2 = controller.get_time()
    dt = controller.delta_time(t1,t2)
    tabular(ans)
    print(f"El número de ofertas laborales publicadas dentro del periodo anual relevante es: {general_size}")
    print(f"El número de ofertas laborales publicadas utilizados para crear el gráfico de barras: {graph_size}")
    print ("El tiempo transcurrido por el requerimiento fue: " +str(dt)+" ms")
    
    plt.bar(distribution.keys(), distribution.values(), color='skyblue')
    plt.xlabel("Nombres")
    plt.ylabel("Cantidad")
    plt.title("Gráfica de distribución")
    plt.show()




def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    select = int(input("ingrese si quiere los datos bases o ersonalisados (personalisados == 1 ,bases == 2): "))
    
    # Aqui se piden todos los datos de los requerimientos 
    if select == 1:
        n= int(input("""El número (N) de ofertas laborales a consultar // y el numero de paises que quiera consultar:  """))
        fecha_inicial= str(input("""La fecha inicial del periodo a consultar (con formato "%Y-%m-%d"):  """))
        fecha_final= str(input("""La fecha final del periodo a consultar (con formato "%Y-%m-%d"):  """))
        salario_minimo= int(input("""El límite inferior del salario mínimo ofertad:  """))
        salario_maximo= int(input("""El límite superior del salario mínimo ofertado:  """))
        codigo_pais= str(input("""Código del país para la consulta (ej.: PL, CO, ES, etc):  """))
        nivel_experticia= str(input("""Nivel de experticia de las ofertas de interés (junior, mid, senior, indiferente):  """))
        city_name = str(input('Nombre de la ciudad para la consulta: '))
        job_location = str(input('Tipo de ubicación de trabajo (remote, partialy, remote, office): '))
        li_companysize = str(input("""límite inferior del tamaño de la compañía: """))
        ls_companysize = str(input("""límite superior del tamaño de la compañía: """))
        skill = str(input("""Nombre de la habilidad solicitada: """))
        li_companyskill = int(input("""límite inferior del nivel de la habilidad: """))
        ls_companyskill = int(input("""límite superior del nivel de la habilidad: """))
        year = input('El año relevante (en formato “%Y”): ')
        property_input = input('La propiedad de conteo (experticia [1], ubicación [2], o habilidad [3]): ')
    else: 
        n= int(5)
        fecha_inicial= str("2000-01-01")
        fecha_final= str("2025-01-01")
        salario_minimo= int(1)
        salario_maximo= int(1000000)
        codigo_pais= str("PL")
        nivel_experticia= str("mid")
        city_name = str("Warszawa")
        job_location = str("office")
        li_companysize = str(1)
        ls_companysize = str(100000)
        skill = str("JAVASCRIPT")
        li_companyskill = int(1)
        ls_companyskill = int(100000000)
        year = str("2022")
        property_input = str("2")   
    #aqui puede ir tiempo inicial. 
    
    tqdm.pandas(ascii=True, bar_format='{l_bar}%s{bar}%s{r_bar}' % (Fore.GREEN, Fore.RESET))

    #aqui se guardan  las respuestas de cada uno 
    print('\n\nCargando los datos de cada requerimiento')
    for funcion in tqdm([controller.req_1, controller.req_2, controller.req_3, controller.req_4, controller.req_5, controller.req_6, controller.req_7], colour='green',desc ="Cargando reqs " ):
        # Llama a la función y obtén la respuesta
        if funcion == controller.req_1:
            contador, respuesta_req1 = funcion(control, fecha_inicial, fecha_final)
        elif funcion == controller.req_2:
            contador, respuesta_req2 = funcion(control, salario_minimo, salario_maximo)
        elif funcion == controller.req_3:
            contador, respuesta_req3 = funcion(control, n, codigo_pais, nivel_experticia)
        elif funcion == controller.req_4:
            respuesta_req4, size = funcion(control, n, city_name, job_location)
        elif funcion == controller.req_5:
            contador, respuesta_req5 = funcion(n, ls_companysize, li_companysize, skill, ls_companyskill, li_companyskill, control)
        elif funcion == controller.req_6:
            contador, total_ciudades, n_ciudades_cumplen, respuesta_req6 = funcion(control, n, fecha_inicial, fecha_final, salario_minimo, salario_maximo)
        elif funcion == controller.req_7:
            respuesta_req7, general_size, graph_size, distribution = funcion(control, year, codigo_pais, property_input)
    
    print('\n\nLos datos de cada requerimiento han sido cargados')
    
   
    working_8 = True
    #ciclo del menu
    while working_8:
        print_menu_req8()
        choose =int(input("Ingrese el requerimiento que quiera ver en el mapa interactivo : "))
        t1 = controller.get_time()
        if int(choose) == 1:
            controller.req_8(control,respuesta_req1,1,"Requerimiento 1")

        elif int(choose) == 2:
            controller.req_8(control,respuesta_req2,1,"Requerimiento 2")

        elif int(choose) == 3:
            controller.req_8(control,respuesta_req3,1,"Requerimiento 3")

        elif int(choose) == 4:
            controller.req_8(control,respuesta_req4,1,"Requerimiento 4")

        elif int(choose) == 5:
            controller.req_8(control,respuesta_req5,1,"Requerimiento 5")

        elif int(choose) == 6:
            controller.req_8(control,respuesta_req6,2,"Requerimiento 6")

        elif int(choose) == 7:
            controller.req_8(control,respuesta_req7,1,"Requerimiento 7")
        
        elif int(choose) == 8:    
            controller.req_8_todos(respuesta_req1,respuesta_req2,respuesta_req3,respuesta_req4,respuesta_req5,respuesta_req6,respuesta_req7)
        
        elif int(choose) == 0:
            working_8 = False
            print("\nMenu Cerrado")
        else:
            print("Opción errónea, vuelva a elegir.\n")
        t2 = controller.get_time()
        dt = controller.delta_time(t1,t2)
        print ("El tiempo transcurrido por el requerimiento fue: " +str(dt)+" ms")

            
            
        
    



def print_divisa(control):
    respuesta = controller.ver_divisa(control)
    data = [respuesta]

# Crear la tabla utilizando tabulate con header="keys"
    table = tabulate(data, headers="keys",tablefmt ='fancy_grid')
    print(table) 
    
# Se crea el controlador asociado a la vista
control = new_controller()

# main del reto
if __name__ == "__main__":
    threading.stack_size(67108864*2) # 128MB stack
    sys.setrecursionlimit(default_limit*1000000)
    
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 1:
            file_size = select_file_type()
            print("Cargando información de los archivos ....\n")
            jobs_size, employments_size, multilocations_size, skills_size= load_data(control, file_size)
            
            
            print(f'\nLos Datos se han cargado correctamente.')
            print(f'Datos cargados del archivo jobs.csv: {jobs_size}')
            print(f'Datos cargados del archivo employments_types.csv: {employments_size}')
            print(f'Datos cargados del archivo multilocations.csv: {multilocations_size}')
            print(f'Datos cargados del archivo skills.csv: {skills_size}\n')
            
            
            print('---------------------------------------------------------------\n')
            data_sample(control)
        elif int(inputs) == 2:
            print_req_1(control)

        elif int(inputs) == 3:
            print_req_2(control)

        elif int(inputs) == 4:
            print_req_3(control)

        elif int(inputs) == 5:
            print_req_4(control)

        elif int(inputs) == 6:
            print_req_5(control)

        elif int(inputs) == 7:
            print_req_6(control)

        elif int(inputs) == 8:
            print_req_7(control)

        elif int(inputs) == 9:
            print_req_8(control)

        elif int(inputs) == 69:
            print_divisa(control)
        
        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa")
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
    
