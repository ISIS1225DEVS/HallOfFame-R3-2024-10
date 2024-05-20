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
import traceback
import threading
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

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

# Se crea el controlador asociado a la vista
control = new_controller()

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
    loaded = controller.load_data(control)
    return loaded

def Datesort(lista):
    listaord = controller.Datesort(lista)
    return listaord

def printSorted(head, data):
    HoT = controller.tabulation3(data, head)
    print(tabulate(HoT, headers = "keys", tablefmt="pretty"))

def print_N(data, head, keep, N):
    HoT = controller.tabulation_N(data, head, keep, N)
    print(tabulate(HoT, headers= "keys", tablefmt="pretty"))

def print_5(data, head, keep):
    HoT = controller.tabulation5(data, head,keep)
    print(tabulate(HoT, headers= "keys", tablefmt="pretty"))

def print_req_1(control,fecha_inicial,fecha_final):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    res = controller.req_1(control,fecha_inicial,fecha_final)
    print("La cantidad de ofertas para las fechas especificadas son: "+str(res[0]))
    keep = ["published_at","title","company_name","experience_level","country_code","city","company_size","workplace_type","skill_name"]
    res_sorted = Datesort(res[1])
    if lt.size(res[1]) >= 10:
        print("Para las 5 primeras: ")
        printlist = controller.tabulation5(res_sorted,False,keep)
        print(tabulate(printlist, headers = "keys", tablefmt="pretty"))
        print("Para las 5 últimas: ")
        printlist = controller.tabulation5(res_sorted,True,keep)
        print(tabulate(printlist, headers = "keys", tablefmt="pretty"))
    else:
        print("Ofertas: ")
        printlist = controller.tabulation_N(res_sorted,False,keep,lt.size(res_sorted))
        print(tabulate(printlist,headers = "keys", tablefmt="pretty"))
    


def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    salario_min= input("Ingrese el rango inferior del salario_min: ")
    salario_max= input("Ingrese el rango superior del salario_min: ")
    ofertas_cumplen, total_ofertas= controller.req_2(control, salario_min, salario_max)

    keep= ["published_at", "title", "company_name", "experience_level", "country_code", "city", "company_size", "workplace_type", "salary_from", "skill_name"]
    
    print("El total de ofertas es: " + str(total_ofertas))
    print("Las primeras 5: ")
    print_5(ofertas_cumplen, False, keep)
    print("-----------------------------------------------------------------")
    print("Las ultimas 5 son: ")
    print_5(ofertas_cumplen, True, keep)
    
def print_req_3(control, n, CountryCode, ExpLvl):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """

    ans = controller.req_3(control, n, CountryCode, ExpLvl)
    print("La cantidad de ofertas el país y nivel de experticia dado son: : "+str(ans[0]))
    keep = ["published_at","title","company_name","experience_level","country_code","city","company_size","workplace_type","salary_from","skill_name"]
    print('-' * 60) 
    if n >= 10:
        print("5 más recientes: ")
        printlist = controller.tabulation5(ans[1],True,keep)
        print(tabulate(printlist, headers = "keys", tablefmt="pretty"))
        print("5 más antiguas: ")
        printlist = controller.tabulation5(ans[1],False,keep)
        print(tabulate(printlist, headers = "keys", tablefmt="pretty"))
    else:
        print("Ofertas: ")
        anslist = ans[1]
        anslist = lt.subList(anslist, 1, n)
        
        print(tabulate(anslist['elements'], headers = "keys", tablefmt="pretty"))
    pass


def print_req_4(control, n, ciudad, trabajo_ubicacion):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    res = controller.req_4(control, n, ciudad, trabajo_ubicacion)
    print("La cantidad de ofertas para una ciudad y ubicación especifica son: "+str(res[0]))
    keep = ["published_at","title","company_name","experience_level","country_code","city","company_size","workplace_type","salary_from","skill_name"]
    res_sorted = Datesort(res[1])
    if n >= 10 and res[0] >= 10:
        print("Para las 5 primeras: ")
        printlist = controller.tabulation5(res_sorted,False,keep)
        print(tabulate(printlist, headers = "keys", tablefmt="pretty"))
        print("Para las 5 últimas: ")
        printlist = controller.tabulation5(res_sorted,True,keep)
        print(tabulate(printlist, headers = "keys", tablefmt="pretty"))
    else:
        print("Ofertas: ")
        printlist = controller.tabulation_N(res_sorted,False,keep,lt.size(res_sorted))
        print(tabulate(printlist,headers = "keys", tablefmt="pretty"))
    
    pass


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    N= input("Ingrese la cantidad de de ofertas laborales: ")
    size_min= input("Ingrese rango inferior del tamaño: ")
    size_max= input("Ingrese rango superior del tamaño: ")
    habilidad= input("Ingrese el nombre de la habilidad deseada: ")
    skill_min= input("Ingrese el rango min del skill: ")
    skill_max= input("Ingrese el rango max del skill: ")

    ofertas_lista, total_ofertas= controller.req_5(control, size_min, size_max, habilidad, skill_min, skill_max)
    
    keep= ["published_at", "title", "company_name", "experience_level", "country_code", "city", "company_size", "workplace_type", "salary_from", "skill_name"]
        
    print("El total de ofertas es:" + str(total_ofertas))
   
    if int(N) < 10:
        print("Las ultimas son: ")
        print_N(ofertas_lista, True, keep, int(N))
    else:
        print("Las primeras 5: ")
        print_5(ofertas_lista, True, keep)
        print("Las ultimas 5: ")
        print_5(ofertas_lista, False, keep)
    
    
#* Mini Helper
def makePythonListOFDic(lip):
    lit = []
    for dic in lt.iterator(lip):
        lit.append(dic)
    return lit
    
def print_req_6(control, OldestDate, RecentDate, minSalary, maxSalary, n):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    ans = controller.req_6(control, OldestDate, RecentDate, minSalary, maxSalary)
    # ans = NumberoOfCriteria, TotalCities, SortedCities, TopCity, TopCityInfo
    print("El número total de ofertas laborales publicadas entre las fehcas y  rango de salario : "+str(ans[0]))
    print("Total de ciudades que cumplen con las especificaciones: "+ str(ans[1]))
    print("Las N ciudades que cumplan las condiciones especificadas ordenadas alfabéticamente: ")

    NCities = makePythonListOFDic(lt.subList(ans[2], 1, n)) # Las 'n ciudades ordenadas alfabéticamente'
    NCities = [NCities]
    print(tabulate(NCities, tablefmt="grid"))
    
    print("*"*60)
    print("Para la ciudad con la mayor cantidad de ofertas laborales publicada: ")
    keep = ["published_at","title","company_name","experience_level","country_code","city","company_size","workplace_type","salary_from","skill_name"]
    print('-' * 60) 
    if n >= 10:
        print("5 más recientes: ")
        printlist = controller.tabulation5(ans[4],True,keep)
        print(tabulate(printlist, headers = "keys", tablefmt="pretty"))
        print("5 más antiguas: ")
        printlist = controller.tabulation5(ans[4],False,keep)
        print(tabulate(printlist, headers = "keys", tablefmt="pretty"))
    else:
        print("Ofertas: ")
        anslist = ans[4]
        anslist = lt.subList(anslist, 1, n)
        anslist = makePythonListOFDic(anslist)
        print(tabulate(anslist, headers = "keys", tablefmt="pretty"))
    pass

def print_req_7(control, año, CODpais, propiedad_conteo):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    res = controller.req_7(control, año, CODpais, propiedad_conteo)
    if propiedad_conteo == "habilidad" or propiedad_conteo == "h":
        key = "habilidad"
        keepkey = "skill_name"
    elif propiedad_conteo == "ubicación" or propiedad_conteo == "u":
        key = "ubicación"
        keepkey = "workplace_type"
    elif propiedad_conteo == "experticia" or propiedad_conteo == "e":
        key = "experticia"
        keepkey = "experience_level"
    keep = ["published_at","title","company_name","country_code","city","company_size","salary_from",keepkey]
    print("Cantidad de ofertas laborales publicadas dentro del periodo relevante: "+str(res[1]))
    res_sorted = Datesort(res[0])
    if lt.size(res[0]) >= 10:
        print("Para las 5 primeras: ")
        printlist = controller.tabulation5(res_sorted,False,keep)
        print(tabulate(printlist, headers = "keys", tablefmt="pretty"))
        print("Para las 5 últimas: ")
        printlist = controller.tabulation5(res_sorted,True,keep)
        print(tabulate(printlist, headers = "keys", tablefmt="pretty"))
    else:
        print("Ofertas: ")
        printlist = controller.tabulation_N(res_sorted,False,keep,lt.size(res[0]))
        print(tabulate(printlist,headers = "keys", tablefmt="pretty"))
    if lt.size(res[0]) != 0:
        print("Cantidad de ofertas laborales publicadas utilizadas para crear el gráfico: "+str(res[2]))
        print("Valor mínimo de la propiedad consultada en el gráfico es "+str(res[3]["key"])+" con el valor "+str(res[3]["value"]))
        print("Valor máximo de la propiedad consultada en el gráfico es "+str(res[4]["key"])+" con el valor "+str(res[4]["value"]))
        x=list(res[5].keys())
        y=list(res[5].values())
        plt.title("Cantidad por "+key+" de "+CODpais)
        plt.xlabel(key)
        plt.ylabel("cantidad")
        plt.bar(x,y)
        plt.xticks(rotation=90)
        plt.show()


def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    controller.req_8(control) 

# Se crea el controlador asociado a la vista
control = new_controller()
load_data(control)

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
            data = load_data(control)
            data_sorted = Datesort(data)
            print('Total ofertas Cargadas: ' + str(lt.size(data)))
            print('Tres primeras ofertas (Earliest): ')
            printSorted(False, data_sorted)
            print('Tres últimas ofertas (Latest):' )
            printSorted(True, data_sorted)
        elif int(inputs) == 2:
            fecha_inicial=input("Ingrese la fecha inicial con el formato (%Y-%m-%d): ")
            fecha_final=input("Ingrese la fecha final con el formato (%Y-%m-%d): ")
            print_req_1(control,fecha_inicial,fecha_final)

        elif int(inputs) == 3:
            print_req_2(control)

        elif int(inputs) == 4:
            n = int(input("Ingrese el número de ofertas laborales a consultar: "))
            CountryCode = input("Ingrese el código de país a consultar: ")
            ExpLvl = input("Ingrese el nivel de experiencia a consultar: ")
            print_req_3(control, n, CountryCode, ExpLvl)

        elif int(inputs) == 5:
            n = int(input("Ingrese el número de ofertas laborales a consultar: "))
            ciudad = input("Ingrese el nombre de la ciudad a consultar: ")
            trabajo_ubicacion = input("Ingrese el tipo de ubicación de trabajo (remote, partly_remote u office): ")
            print_req_4(control, n, ciudad, trabajo_ubicacion)

        elif int(inputs) == 6:
            print_req_5(control)
            
        elif int(inputs) == 7:
            OldestDate = input("Introduzca la fecha de inicio de intervalo (más antigua): YYYY-MM-DD  - ")
            RecentDate = input("Introduzca la fecha de fin de intervalo (más reciente): YYYY-MM-DD  - ")
            minSalary = float(input("Introduzca el salario mínimo: "))
            maxSalary = float(input("Introduzca el salario máximo: "))
            n = int(input("Introduzca el número de ciudades n: "))
            print_req_6(control, OldestDate, RecentDate, minSalary, maxSalary, n)

        elif int(inputs) == 8:
            año = input("Ingrese el año a consultar: ")
            CODpais = input("Ingrese el código del país a consultar: ")
            propiedad_conteo = input("Ingrese la propiedad de conteo a consultar (experticia, ubicación, o habilidad): ")
            print_req_7(control, año, CODpais, propiedad_conteo)

        elif int(inputs) == 9:
            print_req_8(control)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa")
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)