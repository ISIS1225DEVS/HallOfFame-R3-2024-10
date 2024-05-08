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
from DISClib.DataStructures import mapentry as me
assert cf
from tabulate import tabulate
import matplotlib.pyplot as plt
import traceback

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
    #TODO: Llamar la función del controlador donde se crean las estructuras de datos

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


def load_data(control):
    """
    Carga los datos
    """
    tamanho = ''
    c = int(input('Elija el tamaño del archivo que desea usar: \n 1-10pct\n 2-20pct\n 3-30pct\n 4-50pct\n 5-70pct\n 6-90pct\n 7-large\n 8-small\n'))
    if c == 1:
        tamanho = '10-por'
    elif c == 2:
        tamanho = '20-por'
    elif c == 3:
        tamanho = '30-por'
    elif c == 4:
        tamanho = '50-por'
    elif c == 5:
        tamanho = '70-por'
    elif c == 6:
        tamanho = '90-por'
    elif c == 7:
        tamanho = 'large'
    elif c == 8:
        tamanho = 'small'
    else:
        tamanho = 'small'

    #id_jobs = controller.load_id_jobs(control, tamanho)
    skills = controller.load_id_skills(control,tamanho)
    #salary = controller.load_salary(control, tamanho)
    employments = controller.load_id_employments_types(control,tamanho)
    multilocations = controller.load_id_multilocations(control,tamanho)
    tamanio,ofertas, delta_time_2, delta__memory_2=controller.load_data(control,tamanho)
    country = controller.load_country_jobs(control, tamanho)
    city = controller.load_city_jobs(control, tamanho)
    jobs_id = controller.load_id_jobs(control, tamanho)
    carga = lt.newList("ARRAY_LIST")
    for oferta in range (1, lt.size(ofertas)):
        dic_rpta = {"fecha_oferta":lt.getElement(ofertas,oferta)["published_at"],
                          "titulo":lt.getElement(ofertas, oferta)["title"],
                          "empresa": lt.getElement(ofertas, oferta)['company_name'],
                          "nivel_experticia":lt.getElement(ofertas, oferta)["experience_level"],
                          "ciudad":lt.getElement(ofertas, oferta)["city"],
                          "pais":lt.getElement(ofertas, oferta)["country_code"],
                          }
        lt.addLast(carga, dic_rpta)
    print("Se han cargado ",tamanio," ofertas")
    print(tabulate(lt.iterator(carga),headers="keys",tablefmt="grid"))
    print("Se ha tardado", delta_time_2, "milisegundos")
    print("Se ha utilizado",delta__memory_2,"memoria")
    return country, skills, employments, multilocations, city, jobs_id
    #TODO: Realizar la carga de datos
    



def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    fecha_i= input("Ingrese la fecha inicial: ")
    fecha_f= input("Ingrese la fecha final: ")
    tamanio,ofertas, deltatime= controller.req_1(control,fecha_i,fecha_f)
    print("Se han encontrado ",tamanio," ofertas")
    ans = lt.newList("ARRAY_LIST")
    for oferta in range (1, lt.size(ofertas)):
        dic_rpta = {"fecha_oferta":lt.getElement(ofertas,oferta)["published_at"],
                          "titulo":lt.getElement(ofertas, oferta)["title"],
                          "empresa": lt.getElement(ofertas, oferta)['company_name'],
                          "nivel_experticia":lt.getElement(ofertas, oferta)["experience_level"],
                          "ciudad":lt.getElement(ofertas, oferta)["city"],
                          "pais":lt.getElement(ofertas, oferta)["country_code"],
                          "tamaño_empresa":lt.getElement(ofertas, oferta)["company_size"],
                          "ubicacion":lt.getElement(ofertas, oferta)["workplace_type"],
                          "habilidades":lt.getElement(ofertas, oferta)["name_skill"],
                          }
        lt.addLast(ans, dic_rpta)
    print("Se han cargado ",tamanio," ofertas")
    print("El tiempo de ejecución es: "+ str(round(deltatime,2))+" milisegundos")
    print(tabulate(lt.iterator(ans),headers="keys",tablefmt="grid"))
    

def print_req2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    lim_inf_salary= float(input("Ingrese el salario minimo: "))
    lim_sup_salary= float(input("Ingrese el salario maximo: "))
    tamanio,salarios, deltatime= controller.req2(control,lim_inf_salary, lim_sup_salary)
    print("Se han encontrado ",tamanio," ofertas")
    ans = lt.newList("ARRAY_LIST")
    for oferta in range (1, lt.size(salarios)):
        dic_rpta = {"fecha_oferta":lt.getElement(salarios,oferta)["published_at"],
                          "titulo":lt.getElement(salarios, oferta)["titulo"],
                          "empresa": lt.getElement(salarios, oferta)['nombre_empresa'],
                          "nivel_experticia":lt.getElement(salarios, oferta)["experticia"],
                          "ciudad":lt.getElement(salarios, oferta)["ciudad"],
                          "pais":lt.getElement(salarios, oferta)["pais"],
                          "tamaño_empresa":lt.getElement(salarios, oferta)["tamanio_empresa"],
                          "ubicacion":lt.getElement(salarios, oferta)["ubicacion"],
                          "salario_usd": lt.getElement(salarios,oferta)["salary_in_usd"],
                          "habilidades":lt.getElement(salarios, oferta)["name_skill"],
                          }
        lt.addLast(ans, dic_rpta)
    #print(salarios)
    print("El tiempo de ejecución es: "+ str(round(deltatime,2))+" milisegundos")
    print(tabulate(lt.iterator(ans),headers="keys",tablefmt="grid"))


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    N = int(input("Ingrese el número de ofertas de trabajo que desea ver: "))
    country_code = input("Ingrese el código del país: ")
    experience_level = input("Ingrese el nivel de experiencia (junior, mid, senior): ")
    ofertas, deltatime= controller.req_3(control,N, country_code, experience_level)
    print("El tiempo de ejecución es: "+ str(round(deltatime,2))+" milisegundos")
    
    print(tabulate(lt.iterator(ofertas),headers="keys",tablefmt="grid"))


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    N = int(input("Ingrese el número de ofertas de trabajo que desea ver: "))
    city = input("Ingrese la ciudad: ")
    tipo_ubicacion = input("Ingrese el tipo de ubicacion ((remote, partly_remote, office): ")
    ofertas, deltatime= controller.req_4(control,N, city, tipo_ubicacion)
    print("El tiempo de ejecución es: "+ str(round(deltatime,2))+" milisegundos")
    print(tabulate(lt.iterator(ofertas),headers="keys",tablefmt="grid"))



def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    N = int(input("ingrese el numero de ofertas laborales: "))
    limite_inf_tamano = int(input("Ingrese el limite inferior de tamaño: "))
    limite_sup_tamano = int(input("Ingrese el limite superior de tamaño: "))
    skill = input("ingrese la habilidad que solicita: ")
    limite_inf_nivel_habilidad = input("Ingrese el limite inferior del nivel de habilidad: ")
    limite_sup_nivel_habilidad = input("Ingrese el limite superior del nivel de habilidad: ")
    tamanio,ofertas, deltatime= controller.req_5(control,N, limite_inf_tamano, limite_sup_tamano, skill, limite_inf_nivel_habilidad, limite_sup_nivel_habilidad)
    print("Se han encontrado ",tamanio," ofertas")
    ans = lt.newList("ARRAY_LIST")
    for oferta in range (1, lt.size(ofertas)):
        dic_rpta = {"fecha_oferta":lt.getElement(ofertas,oferta)["published_at"],
                          "titulo":lt.getElement(ofertas, oferta)["title"],
                          "empresa": lt.getElement(ofertas, oferta)['company_name'],
                          "nivel_experticia":lt.getElement(ofertas, oferta)["experience_level"],
                          "ciudad":lt.getElement(ofertas, oferta)["city"],
                          "pais":lt.getElement(ofertas, oferta)["country_code"],
                          "tamaño_empresa":lt.getElement(ofertas, oferta)["company_size"],
                          "ubicacion":lt.getElement(ofertas, oferta)["workplace_type"],
                          "salario_min_in_usd": lt.getElement(ofertas, oferta)["salary_in_usd"],
                          "habilidades":lt.getElement(ofertas, oferta)["name_skill"],
                          }
        lt.addLast(ans, dic_rpta)
    print("El tiempo de ejecución es: "+ str(round(deltatime,2))+" milisegundos")
    print(tabulate(lt.iterator(ans),headers="keys",tablefmt="grid"))


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    N_ciudades = int(input("ingrese el numero de ciudades a consultar: "))
    fecha_i= input("Ingrese la fecha inicial: ")
    fecha_f= input("Ingrese la fecha final: ")
    limite_inf_salario = float(input("Ingrese el limite inferior del salario: "))
    limite_sup_salario = float(input("Ingrese el limite superior del salario: "))
    tamanio ,numero_ciudades, ciudades_mayores,ofertas, deltatime= controller.req_6(control,N_ciudades, fecha_i, 
                                                                   fecha_f, limite_inf_salario, 
                                                                   limite_sup_salario)
    print("Se han encontrado ",tamanio," ofertas")
    print("El número de ciudades encotradas son: ", numero_ciudades)
    print(ciudades_mayores['elements'])
    ans = lt.newList("ARRAY_LIST")
    for oferta in range (1, lt.size(ofertas)):
        dic_rpta = {"fecha_oferta":lt.getElement(ofertas,oferta)["published_at"],
                          "titulo":lt.getElement(ofertas, oferta)["title"],
                          "empresa": lt.getElement(ofertas, oferta)['company_name'],
                          "nivel_experticia":lt.getElement(ofertas, oferta)["experience_level"],
                          "ciudad":lt.getElement(ofertas, oferta)["city"],
                          "pais":lt.getElement(ofertas, oferta)["country_code"],
                          "tamaño_empresa":lt.getElement(ofertas, oferta)["company_size"],
                          "ubicacion":lt.getElement(ofertas, oferta)["workplace_type"],
                          "salario_min": lt.getElement(ofertas, oferta)["salary_in_usd"],
                          "habilidades":lt.getElement(ofertas, oferta)["name_skill"],
                          }
        lt.addLast(ans, dic_rpta)
    print("El tiempo de ejecución es: "+ str(round(deltatime,2))+" milisegundos")
    print(tabulate(lt.iterator(ans),headers="keys",tablefmt="grid"))


def print_req_7(control):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    anio = input("Ingrese el anio a buscar: ")
    codigo_pais = input("Ingrese el codigo del pais a buscar: ")
    propiedad = input("Ingrese el tipo de propiedad por el que desea buscar(ubicacion, experticia, habilidad): ")
    dicc_ans, cantidad_ofertas,lista_variable, deltatime = controller.req_7(control, anio, codigo_pais, propiedad)
    print("El requerimiento se demoró: " + str(deltatime))
    llaves = dicc_ans.keys()
    lengs = []
    for lista in dicc_ans.values():
        lengs.append(lt.size(lista))
    plt.figure(figsize=(10, 5))
    plt.bar(llaves, lengs)
    plt.show()

    print(cantidad_ofertas)
    print(tabulate(lt.iterator(lista_variable),headers="keys",tablefmt="grid"))
    ans = lt.newList("ARRAY_LIST")
    for oferta in range (1, lt.size(lista_variable)):
        dic_rpta = {"fecha_oferta":lt.getElement((lista_variable),oferta)["published_at"],
                          "titulo":lt.getElement((lista_variable), oferta)["title"],
                          "empresa": lt.getElement((lista_variable), oferta)['company_name'],
                          "nivel_experticia":lt.getElement((lista_variable), oferta)["experience_level"],
                          "ciudad":lt.getElement((lista_variable), oferta)["city"],
                          "pais":lt.getElement((lista_variable), oferta)["country_code"],
                          "tamaño_empresa":lt.getElement((lista_variable), oferta)["company_size"],
                          "ubicacion":lt.getElement((lista_variable), oferta)["workplace_type"],
                          "salario_min": lt.getElement((lista_variable), oferta)["salary_in_usd"],
                          "propiedad":propiedad,
                          }
        lt.addLast(ans, dic_rpta)
    print("El tiempo de ejecución es: "+ str(round(deltatime,2))+" milisegundos")
    print(tabulate(lt.iterator(ans),headers="keys",tablefmt="grid"))
    


def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    pass


# Se crea el controlador asociado a la vista
#control = new_controller()

# main del reto
if __name__ == "__main__":
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 1:
            print("Cargando información de los archivos ....\n")
            control = new_controller()
            load_data(control)
            
        elif int(inputs) == 2:
            print_req_1(control)

        elif int(inputs) == 3:
            print_req2(control)

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

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa")
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
