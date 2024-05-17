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


def load_data(control, filename, memory_sign, forma_de_carga):
    """
    Carga los datos
    """
    #TODO: Realizar la carga de datos
    jobs, employments_types, multilocations, skills, tiempo, memoria = controller.load_data(control, filename, memory_sign, forma_de_carga)
    return jobs, employments_types, multilocations, skills, tiempo, memoria



def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def print_req_1(control):
    fecha_inicial = input("Digite la fecha inicial: ")
    fecha_final = input("Digite la fecha final: ")
    bono = input("Desea ver el bono? (si, no): ")
    
    headers = ["Date", "Title", "Company", "Experience", "Country", "City", "Size", "Place", "Promedio$", "Skills"]
   
    memory_sign = input("¿Desea ver la memoria ocupada? Responda True o False: ")
    memory_sign = controller.convertir_bool(memory_sign)
    
    numero , primeras5 , ultimas5, n_ofertas, tiempo_total, cambio_memoria = controller.req_1(control, fecha_inicial, fecha_final, memory_sign, bono)
    
    if(memory_sign):
        print("El tiempo total fue de: " + str(round(tiempo_total, 3)) + "ms.")
        print("El espacio ocupado fue de: " + str(round(cambio_memoria, 3)) + "kB. ")
    else:
        print("El tiempo total fue de: " + str(round(tiempo_total, 3)) + "ms.")
        
    print("El total de ofertas fue de: " +str(n_ofertas))
    
    if numero == 2:
        resultado = []
        ofertas = []
        for oferta in lt.iterator(primeras5): #En este caso la lista completa

            if mp.get(oferta, "salario_promedio") == None:
                resultado = [me.getValue(mp.get(oferta, "fecha")), 
                            me.getValue(mp.get(oferta, "titulo")), 
                            me.getValue(mp.get(oferta, "empresa")) , 
                            me.getValue(mp.get(oferta, "experticia")), 
                            me.getValue(mp.get(oferta, "pais")), 
                            me.getValue(mp.get(oferta, "ciudad")), 
                            me.getValue(mp.get(oferta, "tamanio")), 
                            me.getValue(mp.get(oferta, "ubicacion")), 
                            "N/A",
                            me.getValue(mp.get(oferta, "habilidades_solicitadas"))]
            else:
                resultado = [me.getValue(mp.get(oferta, "fecha")), 
                         me.getValue(mp.get(oferta, "titulo")), 
                         me.getValue(mp.get(oferta, "empresa")) , 
                         me.getValue(mp.get(oferta, "experticia")), 
                         me.getValue(mp.get(oferta, "pais")), 
                         me.getValue(mp.get(oferta, "ciudad")), 
                         me.getValue(mp.get(oferta, "tamanio")), 
                         me.getValue(mp.get(oferta, "ubicacion")), 
                         me.getValue(mp.get(oferta, "salario_promedio")),
                         me.getValue(mp.get(oferta, "habilidades_solicitadas"))]
            ofertas.append(resultado)
            resultado = []
        print(tabulate(ofertas, headers=headers, tablefmt="rounded_grid"))
    elif numero == 1:
        resultado=[]
        print("Primeras 5")
        primeras_5 = []
        for oferta in lt.iterator(primeras5):

            #print(oferta)
            if mp.get(oferta, "salario_promedio") == None:
                resultado = [me.getValue(mp.get(oferta, "fecha")), 
                            me.getValue(mp.get(oferta, "titulo")), 
                            me.getValue(mp.get(oferta, "empresa")) , 
                            me.getValue(mp.get(oferta, "experticia")), 
                            me.getValue(mp.get(oferta, "pais")), 
                            me.getValue(mp.get(oferta, "ciudad")), 
                            me.getValue(mp.get(oferta, "tamanio")), 
                            me.getValue(mp.get(oferta, "ubicacion")), 
                            "N/A",
                            me.getValue(mp.get(oferta, "habilidades_solicitadas"))]
            else:
                resultado = [me.getValue(mp.get(oferta, "fecha")), 
                         me.getValue(mp.get(oferta, "titulo")), 
                         me.getValue(mp.get(oferta, "empresa")) , 
                         me.getValue(mp.get(oferta, "experticia")), 
                         me.getValue(mp.get(oferta, "pais")), 
                         me.getValue(mp.get(oferta, "ciudad")), 
                         me.getValue(mp.get(oferta, "tamanio")), 
                         me.getValue(mp.get(oferta, "ubicacion")), 
                         me.getValue(mp.get(oferta, "salario_promedio")),
                         me.getValue(mp.get(oferta, "habilidades_solicitadas"))]
            primeras_5.append(resultado)
            resultado = []
        print(tabulate(primeras_5, headers=headers, tablefmt="rounded_grid"))
        resultado = []
        print("Últimas 5")
        ultimas_5 = []
        for oferta in lt.iterator(ultimas5):

            #print(oferta)
            if mp.get(oferta, "salario_promedio") == None:
                resultado = [me.getValue(mp.get(oferta, "fecha")), 
                            me.getValue(mp.get(oferta, "titulo")), 
                            me.getValue(mp.get(oferta, "empresa")) , 
                            me.getValue(mp.get(oferta, "experticia")), 
                            me.getValue(mp.get(oferta, "pais")), 
                            me.getValue(mp.get(oferta, "ciudad")), 
                            me.getValue(mp.get(oferta, "tamanio")), 
                            me.getValue(mp.get(oferta, "ubicacion")), 
                            "N/A",
                            me.getValue(mp.get(oferta, "habilidades_solicitadas"))]
            else:
                resultado = [me.getValue(mp.get(oferta, "fecha")), 
                         me.getValue(mp.get(oferta, "titulo")), 
                         me.getValue(mp.get(oferta, "empresa")) , 
                         me.getValue(mp.get(oferta, "experticia")), 
                         me.getValue(mp.get(oferta, "pais")), 
                         me.getValue(mp.get(oferta, "ciudad")), 
                         me.getValue(mp.get(oferta, "tamanio")), 
                         me.getValue(mp.get(oferta, "ubicacion")), 
                         me.getValue(mp.get(oferta, "salario_promedio")),
                         me.getValue(mp.get(oferta, "habilidades_solicitadas"))]
            ultimas_5.append(resultado)
            resultado = []
        print(tabulate(ultimas_5, headers=headers, tablefmt="rounded_grid"))
    


def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    salario_inf = float(input('Ingrese el limite inferior del rango de salarios a buscar (usd): '))
    salario_sup = float(input('Ingrese el limite superior del rango de salarios a buscar (usd): '))
    bono = input("Desea ver el bono? (si, no): ")
    memory_sign = input("¿Desea ver la memoria ocupada? Responda True o False: ")
    memory_sign = controller.convertir_bool(memory_sign)
    total, lst, tiempo_total, cambio_memoria = controller.req_2(control, salario_inf, salario_sup, memory_sign, bono)
    if(memory_sign):
        print("El tiempo total fue de: " + str(round(tiempo_total, 3)) + "ms.")
        print("El espacio ocupado fue de: " + str(round(cambio_memoria, 3)) + "kB. ")
    else:
        print("El tiempo total fue de: " + str(round(tiempo_total, 3)) + "ms.")
    print('El número de ofertas laborales publicadas en el rango de búsqueda fueron: ' + str(total))
    if lt.size(lst) > 10:
        lista1 = lt.subList(lst, 1, 5)
        lista2 = lt.subList(lst, lt.size(lst) - 4, 5)
        print("\nPrimeros 5\n")
        for x in lt.iterator(lista1):
            l1_skill = []
            for s in lt.iterator(x['skill']):
                l1_skill.append(s)
            x['skill'] = tabulate([l1_skill],tablefmt='fancy_grid')
            print(tabulate([x], headers='keys', tablefmt="fancy_grid"))
        print("\nÚltimos 5\n")
        for y in lt.iterator(lista2):
            l2_skill = []
            for t in lt.iterator(y['skill']):
                l2_skill.append(t)
            y['skill'] = tabulate([l2_skill],tablefmt='fancy_grid')
            print(tabulate([y], headers='keys', tablefmt="fancy_grid"))    
    else:
        for z in lt.iterator(lst):
            l_skill = []
            for r in lt.iterator(z['skill']):
                l_skill.append(r)
            z['skill'] = tabulate([l_skill],tablefmt='fancy_grid')
            print(tabulate([z], headers='keys', tablefmt="fancy_grid"))              

def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    n_ofertas = int(input("Digite el número de ofertas a consultar: "))
    pais = input("Digite el nombre del país: ")
    experticia = input("Digite el nivel de experticia (junior/mid/senior)")
    bono = input("Desea ver el bono? (si, no): ")
    
    headers = ["Fecha", "Título", "Empresa", "Experticia", "País", "Ciudad", "Tamaño", "Lugar", "Salario$", "Habilidad"]
    
    memory_sign = input("¿Desea ver la memoria ocupada? Responda True o False: ")
    memory_sign = controller.convertir_bool(memory_sign)
    
    numero, primeras5, ultimas5, n_ofertas_tot, tiempo_total, cambio_memoria = controller.req_3(control, n_ofertas, pais, experticia, memory_sign, bono)
    
    print("El número total de ofertas laborales publicadas para un país y que requieran un nivel de experiencia especifico es: " + str(n_ofertas_tot))
    
    if(memory_sign):
        print("El tiempo total fue de: " + str(round(tiempo_total, 3)) + "ms.")
        print("El espacio ocupado fue de: " + str(round(cambio_memoria, 3)) + "kB. ")
    else:
        print("El tiempo total fue de: " + str(round(tiempo_total, 3)) + "ms.")
        
    if numero == 2:
        resultado = []
        ofertas = []
        for oferta in lt.iterator(primeras5): #En este caso la lista completa

            if mp.get(oferta, "salary_from") == None:
                resultado = [me.getValue(mp.get(oferta, "fecha")), 
                            me.getValue(mp.get(oferta, "titulo")), 
                            me.getValue(mp.get(oferta, "empresa")) , 
                            me.getValue(mp.get(oferta, "experticia")), 
                            me.getValue(mp.get(oferta, "pais")), 
                            me.getValue(mp.get(oferta, "ciudad")), 
                            me.getValue(mp.get(oferta, "tamanio")), 
                            me.getValue(mp.get(oferta, "ubicacion")), 
                            "N/A"]
            else:
                resultado = [me.getValue(mp.get(oferta, "fecha")), 
                         me.getValue(mp.get(oferta, "titulo")), 
                         me.getValue(mp.get(oferta, "empresa")) , 
                         me.getValue(mp.get(oferta, "experticia")), 
                         me.getValue(mp.get(oferta, "pais")), 
                         me.getValue(mp.get(oferta, "ciudad")), 
                         me.getValue(mp.get(oferta, "tamanio")), 
                         me.getValue(mp.get(oferta, "ubicacion")), 
                         me.getValue(mp.get(oferta, "salary_from")),
                         me.getValue(mp.get(oferta, "habilidades_solicitadas"))]
            ofertas.append(resultado)
            resultado = []
        print(tabulate(ofertas, headers=headers, tablefmt="rounded_grid"))
    elif numero == 1:
        resultado=[]
        print("Primeras 5")
        primeras_5 = []
        for oferta in lt.iterator(primeras5):

            #print(oferta)
            if mp.get(oferta, "salary_from") == None:
                resultado = [me.getValue(mp.get(oferta, "fecha")), 
                            me.getValue(mp.get(oferta, "titulo")), 
                            me.getValue(mp.get(oferta, "empresa")) , 
                            me.getValue(mp.get(oferta, "experticia")), 
                            me.getValue(mp.get(oferta, "pais")), 
                            me.getValue(mp.get(oferta, "ciudad")), 
                            me.getValue(mp.get(oferta, "tamanio")), 
                            me.getValue(mp.get(oferta, "ubicacion")), 
                            "N/A"]
            else:
                resultado = [me.getValue(mp.get(oferta, "fecha")), 
                         me.getValue(mp.get(oferta, "titulo")), 
                         me.getValue(mp.get(oferta, "empresa")) , 
                         me.getValue(mp.get(oferta, "experticia")), 
                         me.getValue(mp.get(oferta, "pais")), 
                         me.getValue(mp.get(oferta, "ciudad")), 
                         me.getValue(mp.get(oferta, "tamanio")), 
                         me.getValue(mp.get(oferta, "ubicacion")), 
                         me.getValue(mp.get(oferta, "salary_from")),
                         me.getValue(mp.get(oferta, "habilidades_solicitadas"))]
            primeras_5.append(resultado)
            resultado = []
        print(tabulate(primeras_5, headers=headers, tablefmt="rounded_grid"))
        resultado = []
        print("Últimas 5")
        ultimas_5 = []
        for oferta in lt.iterator(ultimas5):

            #print(oferta)
            if mp.get(oferta, "salary_from") == None:
                resultado = [me.getValue(mp.get(oferta, "fecha")), 
                            me.getValue(mp.get(oferta, "titulo")), 
                            me.getValue(mp.get(oferta, "empresa")) , 
                            me.getValue(mp.get(oferta, "experticia")), 
                            me.getValue(mp.get(oferta, "pais")), 
                            me.getValue(mp.get(oferta, "ciudad")), 
                            me.getValue(mp.get(oferta, "tamanio")), 
                            me.getValue(mp.get(oferta, "ubicacion")), 
                            "N/A"]
            else:
                resultado = [me.getValue(mp.get(oferta, "fecha")), 
                         me.getValue(mp.get(oferta, "titulo")), 
                         me.getValue(mp.get(oferta, "empresa")) , 
                         me.getValue(mp.get(oferta, "experticia")), 
                         me.getValue(mp.get(oferta, "pais")), 
                         me.getValue(mp.get(oferta, "ciudad")), 
                         me.getValue(mp.get(oferta, "tamanio")), 
                         me.getValue(mp.get(oferta, "ubicacion")), 
                         me.getValue(mp.get(oferta, "salary_from")),
                         me.getValue(mp.get(oferta, "habilidades_solicitadas"))]
            ultimas_5.append(resultado)
            resultado = []
        print(tabulate(ultimas_5, headers=headers, tablefmt="rounded_grid"))
    


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    cantidad_n = int(input("Digite el número de ofertas laborales para la consulta: "))
    ciudad = input("Digite el nombre de la ciudad a consultar: ")
    ubicacion = input("Ingrese el tipo de ubicación del trabajo: ")
    ans = input("Desea verlo ordenado cronológicamente, en donde los primeros son los más recientes y los últimos los más antiguos? True or False: ")
    ans = controller.convertir_bool(ans)
    ans_2 = input("Desea que los salarios mínimos estén antes, o después? Diga True si prefiere que estén antes: ")
    ans_2 = controller.convertir_bool(ans_2)
    memory_sign = input("¿Desea ver la memoria ocupada? Responda True o False: ")
    memory_sign = controller.convertir_bool(memory_sign)
    
    total, ofertas, tiempo_total, cambio_memoria = controller.req_4(control, cantidad_n, ciudad, ubicacion, memory_sign, ans, ans_2)
    if(memory_sign):
        print("El tiempo total fue de: " + str(round(tiempo_total, 3)) + "ms.")
        print("El espacio ocupado fue de: " + str(round(cambio_memoria, 3)) + "kB. ")
    else:
        print("El tiempo total fue de: " + str(round(tiempo_total, 3)) + "ms.")
    
    print("La cantidad total de ofertas publicadas para la ciudad solicitada fue: " + str(total))
    print_resultado_req4(ofertas)
    
    
def print_resultado_req4(lst):
    if(lt.size(lst) > 10):
        lista1 = lt.subList(lst, 1, 5)
        lista2 = lt.subList(lst, lt.size(lst) - 5, 5)
        resultado = []
        print("\nPrimeros 5\n")
        primeras_5 = []
        ultimas_5 = []
        for oferta in lt.iterator(lista1):
            if(oferta["Salario minimo"] == ""):
                sal = "Desconocido"
            else:
                sal = oferta["Salario minimo"]
            if(oferta["Habilidades solicitadas"] == ""):
                hab = "Desconocido"
            else:
                hab = oferta["Habilidades solicitadas"]["elements"]
            if(oferta["Tipo Ubicacion"] == ""):
                ubi = "Desconocido"
            else:
                ubi = oferta["Tipo Ubicacion"]
            if(oferta["Tamaño"] == ""):
                tam = "Desconocido"
            else:
                tam = oferta["Tamaño"]
            resultado = [oferta["Fecha"],
                         oferta["Título"],
                         oferta["Empresa"],
                         oferta["Experiencia"],
                         oferta["Ciudad"],
                         oferta["Pais"],
                         tam,
                         ubi,
                         sal,
                         hab]
            primeras_5.append(resultado)
        print(tabulate(primeras_5, headers=["Fecha", "Titulo", "Empresa", "Experiencia", "Ciudad", "Pais", "Tamaño", "Tipo Ubicacion", "Salario minimo", "habilidades solicitadas"], tablefmt="rounded_grid"))
        resultado = []
        
        print("\nUltimos 5\n")
        resultado = []
        for oferta in lt.iterator(lista2):
            if(oferta["Salario minimo"] == ""):
                sal = "Desconocido"
            else:
                sal = oferta["Salario minimo"]
            if(oferta["Habilidades solicitadas"] == ""):
                hab = "Desconocido"
            else:
                hab = oferta["Habilidades solicitadas"]["elements"]
            if(oferta["Tipo Ubicacion"] == ""):
                ubi = "Desconocido"
            else:
                ubi = oferta["Tipo Ubicacion"]
            if(oferta["Tamaño"] == ""):
                tam = "Desconocido"
            else:
                tam = oferta["Tamaño"]
            resultado = [oferta["Fecha"],
                         oferta["Título"],
                         oferta["Empresa"],
                         oferta["Experiencia"],
                         oferta["Ciudad"],
                         oferta["Pais"],
                         tam,
                         ubi,
                         sal,
                         hab]
            ultimas_5.append(resultado)
        print(tabulate(ultimas_5, headers=["Fecha", "Titulo", "Empresa", "Experiencia", "Ciudad", "Pais", "Tamaño", "Tipo Ubicacion", "Salario minimo", "habilidades solicitadas"], tablefmt="rounded_grid"))
        resultado = []
    else:    
        resultado = []
        caso_extra = []
        for oferta in lt.iterator(lst):
            if(oferta["Salario minimo"] == ""):
                sal = "Desconocido"
            else:
                sal = oferta["Salario minimo"]
            if(oferta["Habilidades solicitadas"] == ""):
                hab = "Desconocido"
            else:
                hab = oferta["Habilidades solicitadas"]["elements"]
            if(oferta["Tipo Ubicacion"] == ""):
                ubi = "Desconocido"
            else:
                ubi = oferta["Tipo Ubicacion"]
            if(oferta["Tamaño"] == ""):
                tam = "Desconocido"
            else:
                tam = oferta["Tamaño"]
            resultado = [oferta["Fecha"],
                         oferta["Título"],
                         oferta["Empresa"],
                         oferta["Experiencia"],
                         oferta["Ciudad"],
                         oferta["Pais"],
                         tam,
                         ubi,
                         sal,
                         hab]
            caso_extra.append(resultado)
        print(tabulate(caso_extra, headers=["Fecha", "Titulo", "Empresa", "Experiencia", "Ciudad", "Pais", "Tamaño", "Tipo Ubicacion", "Salario minimo", "habilidades solicitadas"], tablefmt="rounded_grid"))
        resultado = []

def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    n_ofertas = int(input('Ingrese el número N de ofertas laborales para la consulta: ')) 
    size_inf = float(input('Ingrese el limite inferior del tamaño de la compañía a filtrar: '))
    size_sup = float(input('Ingrese el limite superior del tamaño de la compañía a filtrar: '))
    habilidad = input('Ingrese el nombre de la habilidad solicitada: ')
    skill_inf = float(input('Ingrese el limite inferior de la habilidad: '))
    skill_sup = float(input('Ingrese el limite superior de la habilidad: '))
    bono = input("Desea ver el bono? (si, no): ")
    memory_sign = input("¿Desea ver la memoria ocupada? Responda True o False: ")
    memory_sign = controller.convertir_bool(memory_sign)
    total, lst, tiempo_total, cambio_memoria = controller.req_5(control, n_ofertas, size_inf, size_sup, habilidad, skill_inf, skill_sup, memory_sign, bono)
    if(memory_sign):
        print("El tiempo total fue de: " + str(round(tiempo_total, 3)) + "ms.")
        print("El espacio ocupado fue de: " + str(round(cambio_memoria, 3)) + "kB. ")
    else:
        print("El tiempo total fue de: " + str(round(tiempo_total, 3)) + "ms.")
    print('El número de ofertas laborales publicadas en el rango de búsqueda fueron: ' + str(total))
    if lt.size(lst) > 10:
        lista1 = lt.subList(lst, 1, 5)
        lista2 = lt.subList(lst, lt.size(lst) - 5, 5)
        print("\nPrimeros 5\n")
        for x in lt.iterator(lista1):
            l1_skill = []
            for s in lt.iterator(x['skills']):
                l1_skill.append(s)
            x['skills'] = tabulate([l1_skill],tablefmt='fancy_grid')
            print(tabulate([x], headers='keys', tablefmt="fancy_grid"))
        print("\nÚltimos 5\n")
        for y in lt.iterator(lista2):
            l2_skill = []
            for t in lt.iterator(y['skills']):
                l2_skill.append(t)
            y['skills'] = tabulate([l2_skill],tablefmt='fancy_grid')
            print(tabulate([y], headers='keys', tablefmt="fancy_grid"))    
    else:
        for z in lt.iterator(lst):
            l_skill = []
            for r in lt.iterator(z['skills']):
                l_skill.append(r)
            z['skills'] = tabulate([l_skill],tablefmt='fancy_grid')
            print(tabulate([z], headers='keys', tablefmt="fancy_grid"))  

def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    n_ciudades = int(input("Digite la cantidad de ciudades a consultar: "))
    fecha_inicial = input("Digite la fecha inicial: ")
    fecha_final = input("Digite la fecha final: ")
    salario_inicial = float(input("Digite el salario final: "))
    salario_final = float(input("Digite el salario inicial: "))
    bono = input("Desea ver el bono? (si, no): ")
    
    headers = ["Fecha", "Título", "Empresa", "Experticia", "País", "Ciudad", "Tamaño", "Lugar", "Salario$", "Habilidad"]
    
    memory_sign = input("¿Desea ver la memoria ocupada? Responda True o False: ")
    memory_sign = controller.convertir_bool(memory_sign)
    
    numero, primeras5, ultimas5, n_ofertas, cantidad_ciudades_requisitos, ciudades_ordenadas, tiempo_total, cambio_memoria = controller.req_6(control, n_ciudades, fecha_inicial, fecha_final, salario_inicial, salario_final, memory_sign, bono)
    
    print("Número total de ofertas laborales: "+ str(n_ofertas))
    print("El número total de ciudades que cumplan con las especificaciones: " + str(cantidad_ciudades_requisitos))
    print("Las N ciudades que cumplan las condiciones especificadas ordenadas alfabéticamente: ")
    if int(lt.size(ciudades_ordenadas)) > 10:
        ciudades_primeras5 = lt.subList(ciudades_ordenadas, 1 , 5)
        ciudades_ultimas5 = lt.subList(ciudades_ordenadas, int(lt.size(ciudades_ordenadas)) - 5, 5)
    
    print("Ciudades Ordenadas")
    headers_ciudades = ["Ciudad", "Cantidad"]
    ciudades = []
    ciudades2 = []
    if int(lt.size(ciudades_ordenadas)) > 10:
        print("primeras 5")
        for ciudad in lt.iterator(ciudades_primeras5):
            nombre = ciudad["ciudad"]
            cantidad = ciudad["cantidad"]
            ciudades = [nombre, cantidad]
            ciudades2.append(ciudades)
            ciudades = []
        print(tabulate(ciudades2, headers=headers_ciudades, tablefmt="rounded_grid"))
        
        ciudades = []
        ciudades2 = []
        print("ultimas 5")
        for ciudad in lt.iterator(ciudades_ultimas5):
            nombre = ciudad["ciudad"]
            cantidad = ciudad["cantidad"]
            ciudades = [nombre, cantidad]
            ciudades2.append(ciudades)
            ciudades = []
        print(tabulate(ciudades2, headers=headers_ciudades, tablefmt="rounded_grid"))
    else:
        for ciudad in lt.iterator(ciudades_ordenadas):
            nombre = ciudad["ciudad"]
            cantidad = ciudad["cantidad"]
            ciudades = [nombre, cantidad]
            ciudades2.append(ciudades)
            ciudades = []
        print(tabulate(ciudades2, headers=headers_ciudades, tablefmt="rounded_grid"))
    if(memory_sign):
        print("El tiempo total fue de: " + str(round(tiempo_total, 3)) + "ms.")
        print("El espacio ocupado fue de: " + str(round(cambio_memoria, 3)) + "kB. ")
    else:
        print("El tiempo total fue de: " + str(round(tiempo_total, 3)) + "ms.")
        
    
    if numero == 2:
        resultado = []
        ofertas = []
        for oferta in lt.iterator(primeras5): #En este caso la lista completa

            if mp.get(oferta, "salary_from") == None:
                resultado = [me.getValue(mp.get(oferta, "fecha")), 
                            me.getValue(mp.get(oferta, "titulo")), 
                            me.getValue(mp.get(oferta, "empresa")) , 
                            me.getValue(mp.get(oferta, "experticia")), 
                            me.getValue(mp.get(oferta, "pais")), 
                            me.getValue(mp.get(oferta, "ciudad")), 
                            me.getValue(mp.get(oferta, "tamanio")), 
                            me.getValue(mp.get(oferta, "ubicacion")), 
                            "N/A"]
            else:
                resultado = [me.getValue(mp.get(oferta, "fecha")), 
                         me.getValue(mp.get(oferta, "titulo")), 
                         me.getValue(mp.get(oferta, "empresa")) , 
                         me.getValue(mp.get(oferta, "experticia")), 
                         me.getValue(mp.get(oferta, "pais")), 
                         me.getValue(mp.get(oferta, "ciudad")), 
                         me.getValue(mp.get(oferta, "tamanio")), 
                         me.getValue(mp.get(oferta, "ubicacion")), 
                         me.getValue(mp.get(oferta, "salary_from")),
                         me.getValue(mp.get(oferta, "habilidades_solicitadas"))]
            ofertas.append(resultado)
            resultado = []
        print(tabulate(ofertas, headers=headers, tablefmt="rounded_grid"))
    elif numero == 1:
        resultado=[]
        print("Primeras 5")
        primeras_5 = []
        for oferta in lt.iterator(primeras5):

            #print(oferta)
            if mp.get(oferta, "salary_from") == None:
                resultado = [me.getValue(mp.get(oferta, "fecha")), 
                            me.getValue(mp.get(oferta, "titulo")), 
                            me.getValue(mp.get(oferta, "empresa")) , 
                            me.getValue(mp.get(oferta, "experticia")), 
                            me.getValue(mp.get(oferta, "pais")), 
                            me.getValue(mp.get(oferta, "ciudad")), 
                            me.getValue(mp.get(oferta, "tamanio")), 
                            me.getValue(mp.get(oferta, "ubicacion")), 
                            "N/A"]
            else:
                resultado = [me.getValue(mp.get(oferta, "fecha")), 
                         me.getValue(mp.get(oferta, "titulo")), 
                         me.getValue(mp.get(oferta, "empresa")) , 
                         me.getValue(mp.get(oferta, "experticia")), 
                         me.getValue(mp.get(oferta, "pais")), 
                         me.getValue(mp.get(oferta, "ciudad")), 
                         me.getValue(mp.get(oferta, "tamanio")), 
                         me.getValue(mp.get(oferta, "ubicacion")), 
                         me.getValue(mp.get(oferta, "salary_from")),
                         me.getValue(mp.get(oferta, "habilidades_solicitadas"))]
            primeras_5.append(resultado)
            resultado = []
        print(tabulate(primeras_5, headers=headers, tablefmt="rounded_grid"))
        resultado = []
        print("Últimas 5")
        ultimas_5 = []
        for oferta in lt.iterator(ultimas5):
            if mp.get(oferta, "salary_from") == None:
                resultado = [me.getValue(mp.get(oferta, "fecha")), 
                            me.getValue(mp.get(oferta, "titulo")), 
                            me.getValue(mp.get(oferta, "empresa")) , 
                            me.getValue(mp.get(oferta, "experticia")), 
                            me.getValue(mp.get(oferta, "pais")), 
                            me.getValue(mp.get(oferta, "ciudad")), 
                            me.getValue(mp.get(oferta, "tamanio")), 
                            me.getValue(mp.get(oferta, "ubicacion")), 
                            "N/A"]
            else:
                resultado = [me.getValue(mp.get(oferta, "fecha")), 
                         me.getValue(mp.get(oferta, "titulo")), 
                         me.getValue(mp.get(oferta, "empresa")) , 
                         me.getValue(mp.get(oferta, "experticia")), 
                         me.getValue(mp.get(oferta, "pais")), 
                         me.getValue(mp.get(oferta, "ciudad")), 
                         me.getValue(mp.get(oferta, "tamanio")), 
                         me.getValue(mp.get(oferta, "ubicacion")), 
                         me.getValue(mp.get(oferta, "salary_from")),
                         me.getValue(mp.get(oferta, "habilidades_solicitadas"))]
            ultimas_5.append(resultado)
            resultado = []
        print(tabulate(ultimas_5, headers=headers, tablefmt="rounded_grid"))
    


def print_req_7(control):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    anio = str(input('Ingrese el año de consulta: '))
    pais = str(input('Ingrese el codigo del pais de la consulta: '))
    propiedad = int(input(' Escoja la propiedad de conteo: \n 0. Experticia \n 1. Ubicación \n 2. Habilidad\n  '))
    memory_sign = input("¿Desea ver la memoria ocupada? Responda True o False: ")
    bono = input("Desea ver el bono? (si, no): ")
    memory_sign = controller.convertir_bool(memory_sign)
    total_ofertas, total_grafico, lst, tiempo_total, cambio_memoria = controller.req_7(control, anio, pais, propiedad, memory_sign, bono)
    
    if(memory_sign):
        print("El tiempo total fue de: " + str(round(tiempo_total, 3)) + "ms.")
        print("El espacio ocupado fue de: " + str(round(cambio_memoria, 3)) + "kB. ")
    else:
        print("El tiempo total fue de: " + str(round(tiempo_total, 3)) + "ms.")
        
    print('El número de ofertas laborales publicadas en el rango de búsqueda fueron: ' + str(total_ofertas))
    print('El número de ofertas laborales que se graficaron en el diagrama de barras fueron: ' + str(total_grafico))
    
    if lt.size(lst) > 10:
        lista1 = lt.subList(lst, 1, 5)
        lista2 = lt.subList(lst, lt.size(lst) - 5, 5)
        print("\nPrimeros 5\n")
        for x in lt.iterator(lista1):
            print(tabulate([x], headers='keys', tablefmt="fancy_grid"))
        print("\nÚltimos 5\n")
        for y in lt.iterator(lista2):
            print(tabulate([y], headers='keys', tablefmt="fancy_grid"))    
    else:
        for z in lt.iterator(lst):
            print(tabulate([z], headers='keys', tablefmt="fancy_grid"))  


def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    pass



def imprimir_skills(lst):
    resultado = []
    tabla = []
    for x in lt.iterator(lst):
        for y in x:
            if(y == "name"):
                if(x["name"] != ""):
                    resultado.append(x["name"])
                else:
                    resultado.append("Desconocido")
            if(y == "level"):
                if(x["level"] != ""):
                    resultado.append(x["level"])
                else:
                    resultado.append("Desconocido")
            if(y == "id"):
                resultado.append(x["id"])
        tabla.append(resultado)
        #print("\n")
        resultado = []
    print(tabulate(tabla, headers=["Nombre", "Nivel", "Id"], tablefmt="rounded_grid"))
    
def imprimir_multilocations(lst):
    resultado = []
    tabla = []
    for x in lt.iterator(lst):
        for y in x:
            if(y == "city"):
                resultado.append(x["city"])
            if(y == "street"):
                resultado.append(x["street"])
            if(y == "id"):
                resultado.append(x["id"])
        tabla.append(resultado)
        #print("\n")
        resultado = []
    print(tabulate(tabla, headers=["Ciudad", "Calle", "Id"], tablefmt="rounded_grid"))
    
def imprimir_employments(lst):
    resultado = []
    tabla = []
    for x in lt.iterator(lst):
        for y in x:
            if(y == "type"):
                resultado.append(x["type"])
            if(y == "currency_salary"):
                if x["currency_salary"] != "":
                    resultado.append(x["currency_salary"])
                else:
                    resultado.append("Desconocido")
            if(y == "salary_from"):
                if x["salary_from"] != "":
                    resultado.append(x["salary_from"])
                else:
                    resultado.append("Desconocido")
            if(y == "salary_to"):
                if x["salary_to"] != "":
                    resultado.append(x["salary_to"])
                else:
                    resultado.append("Desconocido")
            if(y == "id"):
                resultado.append(x["id"])
        tabla.append(resultado)
        #print("\n")
        resultado = []
    print(tabulate(tabla, headers=["Tipo", "Id", "Currency salary", "Salario desde" , "Salario Hasta"], tablefmt="rounded_grid"))




# Se crea el controlador asociado a la vista
control = new_controller()

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
            
            print("Seleccione que dimensiones quiere cargar de los datos: ")
            
            print("1. 10-por")
            print("2. 20-por")
            print("3. 30-por")
            print("4. 40-por")
            print("5. 50-por")
            print("6. 60-por")
            print("7. 70-por")
            print("8. 80-por")
            print("9. 90-por")
            print("10. small")
            print("11. medium")
            print("12. large")
            tamanio = input()
            if int(tamanio) == 1:
                tamanio_carga = "10-por-"
            elif int(tamanio) == 2:
                tamanio_carga = "20-por-"
            elif int(tamanio) == 3:
                tamanio_carga = "30-por-"
            elif int(tamanio) == 4:
                tamanio_carga = "40-por-"
            elif int(tamanio) == 5:
                tamanio_carga = "50-por-"
            elif int(tamanio) == 6:
                tamanio_carga = "60-por-"
            elif int(tamanio) == 7:
                tamanio_carga = "70-por-"
            elif int(tamanio) == 8:
                tamanio_carga = "80-por-"
            elif int(tamanio) == 9:
                tamanio_carga = "90-por-"
            elif int(tamanio) == 10:
                tamanio_carga = "small-"
            elif int(tamanio) == 11:
                tamanio_carga = "medium-"
            elif int(tamanio) == 12:
                tamanio_carga = "large-"
                
            nombre_archivo_jobs = tamanio_carga + "jobs.csv"
            nombre_archivo_employment = tamanio_carga + "employments_types.csv"
            nombre_archivo_skills = tamanio_carga + "skills.csv"
            nombre_archivo_multilocations = tamanio_carga + "multilocations.csv"
            
            filename = nombre_archivo_jobs, nombre_archivo_employment, nombre_archivo_skills, nombre_archivo_multilocations
            
            memory_sign = input("¿Desea ver la memoria ocupada? Responda True o False: ")
            memory_sign = controller.convertir_bool(memory_sign)
            
            forma_de_carga = input("Quiere cargar los datos de la forma 2 para el requerimiento 6? True o False")
            forma_de_carga = controller.convertir_bool(forma_de_carga)
            
            # Se crea el controlador asociado a la vista
            control = new_controller()
            
            print("Cargando información de los archivos ....\n")
            
            data = load_data(control, filename, memory_sign, forma_de_carga)
            
            print('Ofertas de trabajo cargadas: ' + str(data[0]))
            print("\n")
            
            tiempo = round(data[4],2)
            print("El tiempo de carga fue de: " + str(tiempo) + "ms.")
            print("\n")
            

            
            if(data[5] != None):
                espacio = round(data[5],2)
                print("La memoria utilizada fue de "+ str(espacio) + "kB")
            
            ansss = input("Desea ordenar las ofertas de trabajo? True o False: ")
            ansss = controller.convertir_bool(ansss)
            if ansss == True:
            
                print("Seleccione el metodo de ordenamiento: ")
                print("1. Insertion sort")
                print("2. Mergesort")
                print("3. Quicksort")
                print("4. Selectionsort")
                print("5. Shellsort")
                print("6. Timsort")
                rta = int(input("Opcion: "))
                
                controller.decidir_metodo_sort(rta, control["model"]["jobs"])
            
            primeros_3 = controller.imprimir_n(control, 1, 3)
   
            ultimos_3 = controller.imprimir_n(control, lt.size(control["model"]["jobs"])-2,3)
            
            
            array_primeros_3_skills = lt.newList("ARRAY_LIST")
            array_ultimos_3_skills = lt.newList("ARRAY_LIST")
            
            array_primeros_3_employments = lt.newList("ARRAY_LIST")
            array_ultimos_3_employments = lt.newList("ARRAY_LIST")
            
            array_primeros_3_multilocations = lt.newList("ARRAY_LIST")
            array_ultimos_3_multilocations = lt.newList("ARRAY_LIST")
            
            for z in lt.iterator(primeros_3):
                id_especial = z["id"]
                valor_asociado_emp = me.getValue(mp.get(control["model"]["employmentsId"], id_especial))
                valor_asociado_skills = me.getValue(mp.get(control["model"]["skillsId"], id_especial))
                valor_asociado_multilocations = me.getValue(mp.get(control["model"]["multilocationsId"], id_especial))
                
                lt.addLast(array_primeros_3_employments, valor_asociado_emp)
                lt.addLast(array_primeros_3_skills, valor_asociado_skills)
                lt.addLast(array_primeros_3_multilocations, valor_asociado_multilocations)
                
            for z in lt.iterator(ultimos_3):
                id_especial = z["id"]
                valor_asociado_emp = me.getValue(mp.get(control["model"]["employmentsId"], id_especial))
                valor_asociado_skills = me.getValue(mp.get(control["model"]["skillsId"], id_especial))
                valor_asociado_multilocations = me.getValue(mp.get(control["model"]["multilocationsId"], id_especial))
                
                lt.addLast(array_ultimos_3_employments, valor_asociado_emp)
                lt.addLast(array_ultimos_3_skills, valor_asociado_skills)
                lt.addLast(array_ultimos_3_multilocations, valor_asociado_multilocations)
                
                

            print("Primeras 3 ofertas de trabajo: ")
            controller.mostrar_en_pantalla(primeros_3)
            
            print("\n")
            
            print("Primeras 3 informaciones skills: ")
            imprimir_skills(array_primeros_3_skills)
            
            print("\n")
            
            print("Primeras 3 informaciones multilocations: ")
            imprimir_multilocations(array_primeros_3_multilocations)
            
            print("\n")
            
            print("Primeras 3 informaciones employments: ")
            imprimir_employments(array_primeros_3_employments)
            
            print("\n")
            
            print("Últimas 3 ofertas de trabajo: ")
            controller.mostrar_en_pantalla(ultimos_3)
            
            print("\n")
            
            print("Últimas 3 informaciones skills: ")
            imprimir_skills(array_ultimos_3_skills)
            
            print("\n")
            
            print("Últimas 3 informaciones multilocations: ")
            imprimir_multilocations(array_ultimos_3_multilocations)
            
            print("\n")
            
            print("últimas 3 informaciones employments: ")
            imprimir_employments(array_ultimos_3_employments)
            
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

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa")
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)