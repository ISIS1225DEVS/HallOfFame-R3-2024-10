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
import time
import config as cf
import sys
import controller
import re
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
assert cf
from tabulate import tabulate
import matplotlib.pyplot as plt
import folium
import random
import numpy
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
    print("10- Cambiar tipo de pruebas (Rapidez o almacenamiento)")
    print("11- Cambiar tamaño de muestra.. ")
    print("0- Salir")


def load_data(control):
    """
    Carga los datos
    """
    #TODO: Realizar la carga de datos
    control, prueba, nombre_prueba,sorted_list= controller.load_data(control)
    
    return control, prueba, nombre_prueba, sorted_list
    


def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    print("\n POR FAVOR DIGITE LOS SIGUIENTES DATOS PARA HACER EFECTIVA SU CONSULTA\n")
    print("\nConsultar las ofertas que se publicaron durante un periodo de tiempo\n")
    fecha0 = input("Digite el límite inferior del rango de fechas (Y-M-D): ")
    fecha1 = input("Digite el límite superior del rango de fechas (Y-M-D): ")
    
    correct0 = re.search(pattern=r"^[0-9]{4}-[0]{1}[0-9]{1}-[0-9]{2}$|^[0-9]{4}-[1]{1}[0-2]{1}-[0-9]{2}$", string= fecha0)
    correct1 = re.search(pattern=r"^[0-9]{4}-[0]{1}[0-9]{1}-[0-9]{2}$|^[0-9]{4}-[1]{1}[0-2]{1}-[0-9]{2}$", string= fecha1)
    
    if not correct0 or not correct1:
        print("-"*220)
        print("¡Digito mal el formato de fecha, por favor intentelo nuevamente!".center(220))
        print("-"*220)
        print_req_4(control)
        return None
    cantidad_ofertas, total_ofertas, cinco, prueba, nombre_prueba = controller.req_1(control, fecha0, fecha1)
    if nombre_prueba == "Rapidez":
        print(f"Se ha demorado un total de {prueba}[ms]")
    else:
        print(f"Se han consumido un total de {prueba}[kB]")
        
    print("-"*200)
    print("Los resultados de la consulta fueron los siguientes: ".center(220))
    print(f"La cantidad de ofertas publicadas desde {fecha0} hasta {fecha1} fueron: {cantidad_ofertas}".center(220))
    if cinco:
        
        primeras_cinco = lt.subList(total_ofertas, 1, 5)
        ultimas_cinco = lt.subList(total_ofertas, lt.size(total_ofertas)-6, 5)
        print("\nPRIMERAS CINCO OFERTAS\n")
        
        llaves=["published_at","title", "company_name", "experience_level", "country_code", "city","company_size", "workplace_type", "salario_promedio"]
        valores_a_imprimir1 = []
        
        for offer in lt.iterator(primeras_cinco):
            lst_provisional = []
            for llave in llaves:
                lst_provisional.append(offer[llave])
            valores_a_imprimir1.append(lst_provisional)
        
        
        valores_a_imprimir2 = []
        conteo = 1
        for offer in lt.iterator(primeras_cinco):
            lista_provisional = [conteo]
            for skill in lt.iterator(offer["habilidades_solicitadas"]):  
                lista_provisional.append(skill)
            conteo += 1
            valores_a_imprimir2.append(lista_provisional)
           
        print((tabulate(valores_a_imprimir1, headers=llaves)).center(220))
        print("\nHABILIDADES SOLICITADAS")
        print((tabulate(valores_a_imprimir2)))
        
        print("\nULTIMAS CINCO OFERTAS\n")
        
        valores_a_imprimir1 = []
        
        for offer in lt.iterator(ultimas_cinco):
            lst_provisional = []
            for llave in llaves:
                lst_provisional.append(offer[llave])
            valores_a_imprimir1.append(lst_provisional)
            
        
        valores_a_imprimir2 = []
        conteo = 1
        for offer in lt.iterator(ultimas_cinco):
            lista_provisional = [conteo]
            for skill in lt.iterator(offer["habilidades_solicitadas"]):  
                lista_provisional.append(skill)
            conteo += 1
            valores_a_imprimir2.append(lista_provisional)
           
        print((tabulate(valores_a_imprimir1, headers=llaves)).center(220))
        print("\nHABILIDADES SOLICITADAS")
        print((tabulate(valores_a_imprimir2)))
            
    else:
        
        llaves=["published_at","title", "company_name", "experience_level", "country_code", "city","company_size", "workplace_type", "salario_promedio"]
        valores_a_imprimir1 = []
        
        for offer in lt.iterator(total_ofertas):
            lst_provisional = []
            for llave in llaves:
                lst_provisional.append(offer[llave])
            valores_a_imprimir1.append(lst_provisional)
        
        
        valores_a_imprimir2 = []
        conteo = 1
        for offer in lt.iterator(total_ofertas):
            lista_provisional = [conteo]
            for skill in lt.iterator(offer["habilidades_solicitadas"]):  
                lista_provisional.append(skill)
            conteo += 1
            valores_a_imprimir2.append(lista_provisional)
           
        print((tabulate(valores_a_imprimir1, headers=llaves)).center(220))
        print("\nHABILIDADES SOLICITADAS")
        print((tabulate(valores_a_imprimir2)))
        


def print_req_2(control, salario_minimo, salario_maximo):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    return controller.req_2(control, salario_minimo, salario_maximo)



def print_req_3(control,pais,experticia, N):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    ofertas=controller.req_3(control,pais,experticia,N)
   
    size=ofertas[1]
    time=ofertas[2]
    print("Se han cargado un total de ",size, "ofertas publicadas en ", pais, "con nivel de experticia ", experticia)
    
    print("Se ha demorado un total de",time,"ms")
    imprimir=[]
    headers= ["Fecha d epublicación", "Título", "Empresa",
               "Experticia", "País", "Ciudad",
               "Tamaño_empresa", "Ubicación", "¿Contrata ucranianos?","Salario"]
    
    llaves=["published_at","title", "company_name", "experience_level", "country_code", "city","company_size","workplace_type","open_to_hire_ukrainians","salario_minimo"]
    for i in lt.iterator(ofertas[0]):
        provisional=[]
        for k in llaves:
            provisional.append(i[k])
        imprimir.append(provisional)
    print(tabulate(imprimir,headers=headers))
def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    N = int(input("¿Cuantas ofertas laborales desea consultar? ... "))
    ciudad = input("¿Cuál es el nombre de la ciudad que desea consultar ? ... ")
    ubicacion = input("¿Cúal tipo de ubicación de trabajo desea consultar? (remote, partly_remote, office)... ")
    cantidad_ofertas, ofertas_resultantes, cinco, prueba, nombre_prueba = controller.req_4(control, N, ciudad, ubicacion)
    
    if nombre_prueba == "Rapidez":
        print(f"Se ha demorado un total de {prueba}[ms]")
    else:
        print(f"Se han consumido un total de {prueba}[kB]")
        
    if cantidad_ofertas == False and ofertas_resultantes== False and cinco == False:
        print("-"*200)
        print("NO SE ENCONTRARON OFERTAS PARA LOS DATOS SUMINISTRADOS, POR FAVOR INTENTE NUEVAMENtE".center(220))
        print("-"*200)
        return None
    elif cantidad_ofertas == 0:
        print("-"*200)
        print("NO SE ENCONTRARON OFERTAS PARA LOS DATOS SUMINISTRADOS, POR FAVOR INTENTE NUEVAMENtE".center(220))
        print("-"*200)
        return None
    
    print("-"*200)
    print("Los resultados de la consulta fueron los siguientes: ".center(220))
    print(f"La cantidad de ofertas publicadas para {ciudad} con tipo de ubicación {ubicacion} fueron: {cantidad_ofertas}".center(220))
    if cinco:
        
        print("\nPRIMERAS CINCO OFERTAS\n")
        
        llaves=["published_at","title", "company_name", "experience_level", "country_code", "city","marker_icon", "workplace_type", "salario_minimo"]
        valores_a_imprimir1 = []
        
        for offer in lt.iterator(lt.subList(ofertas_resultantes,1, 5)):
            lst_provisional = []
            for llave in llaves:
                lst_provisional.append(offer[llave])
            valores_a_imprimir1.append(lst_provisional)
            
        print((tabulate(valores_a_imprimir1, headers=llaves)).center(220))
        
        print("\nULTIMAS CINCO OFERTAS\n")
        
        valores_a_imprimir1 = []
        
        for offer in lt.iterator(lt.subList(ofertas_resultantes, lt.size(ofertas_resultantes)-5,5)):
            lst_provisional = []
            for llave in llaves:
                lst_provisional.append(offer[llave])
            valores_a_imprimir1.append(lst_provisional)
            
        print((tabulate(valores_a_imprimir1, headers=llaves)).center(220))
            
    else:
        
        llaves=["published_at","title", "company_name", "experience_level", "country_code", "city","marker_icon", "workplace_type", "salario_minimo"]
        valores_a_imprimir1 = []
        
        for offer in lt.iterator(ofertas_resultantes):
            lst_provisional = []
            for llave in llaves:
                lst_provisional.append(offer[llave])
            valores_a_imprimir1.append(lst_provisional)
            
        print((tabulate(valores_a_imprimir1, headers=llaves)).center(220))
        

def print_req_5(control, numero_ofertas, tamano_minimo_compania,
          tamano_maximo_compania, skill, limite_inferior_skill, limite_superior_skill):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    return controller.req_5(control,  numero_ofertas, tamano_minimo_compania,
          tamano_maximo_compania, skill, limite_inferior_skill, limite_superior_skill)


def print_req_6(control,N,fecha1,fecha2,salario1,salario2):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    ofertas= controller.req_6(control,N,fecha1,fecha2,salario1,salario2)
    size=ofertas[0]
    ciudades= ofertas[1]
    lista= ofertas[2]
    tamaño=ofertas[3]
    time= ofertas[4]

    print("Se ha demorado un total de",time,"ms")
    print("Se publicaron un total de ",tamaño,"ofertas con la condiciones especificadas")
    print("un total de ", size, " ciudades publicaron ofertas en el rango de fechas y salarios especificados")
    print("Las ",N, "ciudades con mas ofertas publicadas fueron: ",ciudades,"\n")

    if lt.size(lista) <= 10:
        print("las ofertas publicadas por la ciudad con mas ofertas son: ","\n")
        imprimir=[]
        headers= ["Fecha de epublicación", "Título", "Empresa",
               "Experticia", "País", "Ciudad",
               "Tamaño_empresa", "Ubicación", "¿Contrata ucranianos?","Salario"]
    
        llaves=["published_at","title", "company_name", "experience_level", "country_code", "city","company_size","workplace_type","open_to_hire_ukrainians","salario_minimo"]
        for i in lt.iterator(lista):
            provisional=[]
            for k in llaves:
                provisional.append(i[k])
            imprimir.append(provisional)
        print(tabulate(imprimir,headers=headers))
    
    else:
        print("los primeros 5 elementos son: ","\n")
        listaP=lt.subList(lista,1,5)
        imprimir=[]
        headers= ["Fecha de publicación", "Título", "Empresa",
               "Nvl experticia", "País", "Ciudad",
               "Tamaño_empresa", "Ubicación", "¿Contrata ucranianos?"]
    
        llaves=["published_at","title", "company_name", "experience_level", "country_code", "city","company_size","workplace_type","open_to_hire_ukrainians"]
        for i in lt.iterator(listaP):
            provisional=[]
            for k in llaves:
                provisional.append(i[k])
            imprimir.append(provisional)
        print(tabulate(imprimir,headers=headers))

        print("los ultimos 5 elementos son: ","\n")
        listaU=lt.subList(lista,-4,5)
        imprimir=[]
        headers= ["Fecha de publicación", "Título", "Empresa",
               "Nvl experticia", "País", "Ciudad",
               "Tamaño_empresa", "Ubicación", "¿Contrata ucranianos?"]
    
        llaves=["published_at","title", "company_name", "experience_level", "country_code", "city","company_size","workplace_type","open_to_hire_ukrainians"]
        for i in lt.iterator(listaU):
            provisional=[]
            for k in llaves:
                provisional.append(i[k])
            imprimir.append(provisional)
        print(tabulate(imprimir,headers=headers),"\n")

def print_req_7(control):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    año = input("Por favor digite el año para el que desea efectuar la consulta: ")
    codigo_pais = input("Por favor digite el codigo del país para el que desea efectuar la consulta: ")
    print("Por favor digite la propiedad de conteo:")
    print("[1] Experticia ")
    print("[2] Ubicación ")
    print("[3] Habilidad ")
    opcion = input("opción: ")
    if opcion == "1":
        propiedad_conteo = "Experticia"
    
    elif opcion == "2":
        propiedad_conteo = "Ubicación"
    
    elif opcion == "3":
        propiedad_conteo = "Habilidad"
    
    else:
        print("-"*100)
        print("\nDigitó una opción incorrecta\n")
        print("intente nuevamente...")
        print("-"*100)
        
        print_req_7(control)
        return None
    bins = int(input("Por favor digite el número de bins en los que se divide el histograma: "))
    

    data_experticia, data_ubicacion, data_habilidad, ofertas_totales, maximo, minimo, prueba, nombre_prueba = controller.req_7(control, año, codigo_pais, propiedad_conteo, bins)
    if nombre_prueba == "Rapidez":
        print(f"Se ha demorado un total de {prueba}[ms]")
    else:
        print(f"Se han consumido un total de {prueba}[kB]")
        
    print("-"*200)
    print("Los resultados de la consulta fueron los siguientes: ".center(220))
    print(f"La cantidad de ofertas publicadas en el año {año} fue de {lt.size(ofertas_totales)}")
    print(f"La cantidad de ofertas publicadas usadas para hacer el gráfico fue de {lt.size(ofertas_totales)}")
    print(f"El valor máximo del histograma es {maximo}")
    print(f"El valor mínimo del histograma es {minimo}")
    
    #PREPARACIÓN HISTOGRAMA
    if propiedad_conteo == "Experticia":
        
        x =plt.hist(data_experticia, bins = bins, color = "skyblue", edgecolor = "black")
        plt.xlabel('Nivel de experiencia')
        plt.ylabel('Cantidad de ofertas')
        plt.title('Histograma')
        plt.show()
    
    if propiedad_conteo == "Ubicación":
        
        x = plt.hist(data_ubicacion, bins = bins, color = "skyblue", edgecolor = "black")
        plt.xlabel('Tipo de ubicación')
        plt.ylabel('Cantidad de ofertas')
        plt.title('Histograma')
        plt.show()
    
        
    if propiedad_conteo == "Habilidad":
        x =plt.hist(data_habilidad, bins = bins, color = "skyblue", edgecolor = "black")
        plt.xlabel('Habilidades')
        plt.ylabel('Cantidad de ofertas')
        plt.title('Histograma')
        plt.xticks(rotation=90, ha='right', va='bottom')
        plt.show()
    
    
    
def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    print("POR FAVOR ESCOJA QUE REQUERIMIENTO DESEA VISUALIZAR EN EL MAPA INTERACTIVO... ")
    req = int(input("Requerimiento... "))
    if req == 1:
        print("\n POR FAVOR DIGITE LOS SIGUIENTES DATOS PARA HACER EFECTIVA SU CONSULTA\n")
        print("\nConsultar las ofertas que se publicaron durante un periodo de tiempo\n")
        fecha0 = input("Digite el límite inferior del rango de fechas (Y-M-D): ")
        fecha1 = input("Digite el límite superior del rango de fechas (Y-M-D): ")
    
        correct0 = re.search(pattern=r"^[0-9]{4}-[0]{1}[0-9]{1}-[0-9]{2}$|^[0-9]{4}-[1]{1}[0-2]{1}-[0-9]{2}$", string= fecha0)
        correct1 = re.search(pattern=r"^[0-9]{4}-[0]{1}[0-9]{1}-[0-9]{2}$|^[0-9]{4}-[1]{1}[0-2]{1}-[0-9]{2}$", string= fecha1)
    
        if not correct0 or not correct1:
            print("-"*220)
            print("¡Digito mal el formato de fecha, por favor intentelo nuevamente!".center(220))
            print("-"*220)
            print_req_4(control)
            return None
        start_time = controller.get_time()
        cantidad_ofertas, total_ofertas, cinco, prueba, nombre_prueba = controller.req_1(control, fecha0, fecha1)
        oferta1 = lt.getElement(total_ofertas, 1)
        m = folium.Map(location=(float(oferta1["latitude"]), float(oferta1["longitude"])))
        for offer in lt.iterator(total_ofertas):
            folium.Marker(
            location=[float(offer["latitude"]), float(offer["longitude"])],
            tooltip="Click me!",
            popup=f"Título: {offer['title']}\n compañia: {offer['company_name']}, \n Nivel de experiencia: {offer['experience_level']}",
            icon=folium.Icon(color="green"),
            ).add_to(m)
        
        m.show_in_browser()
        end_time = controller.get_time()
        print(f"Se ha demorado un total de {controller.delta_time(start_time, end_time)}")
        
        
    
    
    if req == 2:
        start_time = controller.get_time()
        salario_minimo = int(input("Por favor digite el límite inferior del salario mínimo ofertado: "))
        salario_maximo = int(input("Por favor digite el límite inferior del salario mínimo ofertado: "))
        cantidad_ofertas,final,time, total_ofertas= print_req_2(control, salario_minimo, salario_maximo)
        
        if cantidad_ofertas == False:
            print("-"*200)
            print("NO SE ENCONTRARON OFERTAS PARA LOS DATOS SUMINISTRADOS, POR FAVOR INTENTE NUEVAMENtE".center(220))
            print("-"*200)
            return None
        elif cantidad_ofertas == 0:
            print("-"*200)
            print("NO SE ENCONTRARON OFERTAS PARA LOS DATOS SUMINISTRADOS, POR FAVOR INTENTE NUEVAMENtE".center(220))
            print("-"*200)
            return None
        oferta1 = lt.getElement(total_ofertas, 1)
        m = folium.Map(location=(float(oferta1["latitude"]), float(oferta1["longitude"])))
        for offer in lt.iterator(total_ofertas):
            #print(f"{offer["latitude"]},{offer["longitude"]}")
            
            folium.Marker(
            location=[float(offer["latitude"]), float(offer["longitude"])],
            tooltip="Click me!",
            popup=f"Título: {offer['title']}\n compañia: {offer['company_name']}, \n Salario mínimo: {offer['salario_minimo']} USD",
            icon=folium.Icon(color="green"),
            ).add_to(m)
        
        
        m.show_in_browser()
        end_time = controller.get_time()
        print(f"Se ha demorado un total de {controller.delta_time(start_time, end_time)}")
        
    if req == 3:
        pais=str(input("Por favor ingrese el codigo de pais que desea buscar: "))
        experticia= str(input("Por favor ingrese el nivel de experticia: "))
        N= int(input("Ingrese el numero de ofertas que desea listar: "))
        start_time = controller.get_time()
        ordenada,tamaño=controller.req_3(control,pais,experticia,N)
        if tamaño == 0:
            print("-"*200)
            print("NO SE ENCONTRARON OFERTAS PARA LOS DATOS SUMINISTRADOS, POR FAVOR INTENTE NUEVAMENtE".center(220))
            print("-"*200)
            return None
        oferta1 = lt.getElement(ordenada, 1)
        m = folium.Map(location=(float(oferta1["latitude"]), float(oferta1["longitude"])))
        for offer in lt.iterator(ordenada):
            #print(f"{offer["latitude"]},{offer["longitude"]}")
            
            folium.Marker(
            location=[float(offer["latitude"]), float(offer["longitude"])],
            tooltip="Click me!",
            popup=f"Título: {offer['title']}\n compañia: {offer['company_name']}, \n Nivel de experiencia: {offer['experience_level']}",
            icon=folium.Icon(color="green"),
            ).add_to(m)
        
        m.show_in_browser()
        end_time = controller.get_time()
        print(f"Se ha demorado un total de {controller.delta_time(start_time, end_time)}")
        

    if req == 4:
        N = int(input("Cuantas ofertas desea visualizar... "))
        ciudad = input("¿Cuál es el nombre de la ciudad que desea consultar ? ... ")
        ubicacion = input("¿Cúal tipo de ubicación de trabajo desea consultar? (remote, partialy, remote, office)... ")
        start_time = controller.get_time()
        
        cantidad_ofertas, ofertas_resultantes, cinco, prueba, nombre_prueba = controller.req_4(control, N, ciudad, ubicacion)
        
        if cantidad_ofertas == False and ofertas_resultantes== False and cinco == False:
            print("-"*200)
            print("NO SE ENCONTRARON OFERTAS PARA LOS DATOS SUMINISTRADOS, POR FAVOR INTENTE NUEVAMENtE".center(220))
            print("-"*200)
            return None
        elif cantidad_ofertas == 0:
            print("-"*200)
            print("NO SE ENCONTRARON OFERTAS PARA LOS DATOS SUMINISTRADOS, POR FAVOR INTENTE NUEVAMENtE".center(220))
            print("-"*200)
            return None
    
        oferta1 = lt.getElement(ofertas_resultantes, 1)
        m = folium.Map(location=(float(oferta1["latitude"]), float(oferta1["longitude"])))
        for offer in lt.iterator(ofertas_resultantes):
            #print(f"{offer["latitude"]},{offer["longitude"]}")
            
            folium.Marker(
            location=[float(offer["latitude"]), float(offer["longitude"])],
            tooltip="Click me!",
            popup=f"Título: {offer['title']}\n compañia: {offer['company_name']}, \n Nivel de experiencia: {offer['experience_level']}",
            icon=folium.Icon(color="green"),
            ).add_to(m)
        
        m.show_in_browser()
        end_time = controller.get_time()
        print(f"Se ha demorado un total de {controller.delta_time(start_time, end_time)}")
        
        
        
    if req == 5:
        numero_ofertas = int(input("Por favor digite el numero de ofertas a imprimir: "))
        tamano_minimo_compania = int(input("Por favor digite el el limite inferior del tamaño de la compañia: "))
        tamano_maximo_compania = int(input("Por favor digite el el limite superior del tamaño de la compañia: "))
        skill = input("Por favor digite el nombre de la habilidad solicitada: ")
        limite_inferior_skill = int(input("Por favor digite el limite inferior del nivel de la habilidad: "))
        limite_superior_skill = int(input("Por favor digite el limite superior del nivel de la habilidad: "))
        start_time = controller.get_time()
        
        cantidad_ofertas, final, time = print_req_5(control, numero_ofertas, tamano_minimo_compania,
        tamano_maximo_compania, skill, limite_inferior_skill, limite_superior_skill)
        if cantidad_ofertas == False:
            print("-"*200)
            print("NO SE ENCONTRARON OFERTAS PARA LOS DATOS SUMINISTRADOS, POR FAVOR INTENTE NUEVAMENtE".center(220))
            print("-"*200)
            return None
        elif cantidad_ofertas == 0:
            print("-"*200)
            print("NO SE ENCONTRARON OFERTAS PARA LOS DATOS SUMINISTRADOS, POR FAVOR INTENTE NUEVAMENtE".center(220))
            print("-"*200)
            return None
        oferta1 = lt.getElement(final, 1)
        m = folium.Map(location=(float(oferta1["latitude"]), float(oferta1["longitude"])))
        for offer in lt.iterator(final):
            #print(f"{offer["latitude"]},{offer["longitude"]}")
            
            folium.Marker(
            location=[float(offer["latitude"]), float(offer["longitude"])],
            tooltip="Click me!",
            popup=f"Título: {offer['title']}\n compañia: {offer['company_name']}, \n Salario mínimo: {offer['salario_minimo']} USD",
            icon=folium.Icon(color="green"),
            ).add_to(m)
        
        m.show_in_browser()
        end_time = controller.get_time()
        print(f"Se ha demorado un total de {controller.delta_time(start_time, end_time)}")
    if req == 6:
        start_time = controller.get_time()
        
        N= int(input("Ingrese el numero de ciudades que desea listar: "))
        fecha1=input("Ingrese la fecha inicial en formato %Y-%m-%\d ")
        fecha2=input("Ingrese la fecha final en formato %Y-%m-%\d ")
        salario1=float(input("Ingrese el salario inicial "))
        salario2=float(input("Ingrese el salario final "))
        tamaño,lista,lista_ofertas_ciudad,tamaño_total= controller.req_6(control,N,fecha1,fecha2,salario1,salario2)
        oferta1 = lt.getElement(lista_ofertas_ciudad, 1)
        m = folium.Map(location=(float(oferta1["latitude"]), float(oferta1["longitude"])))
        for offer in lt.iterator(lista_ofertas_ciudad):
            #print(f"{offer["latitude"]},{offer["longitude"]}")
            
            folium.Marker(
            location=[float(offer["latitude"]), float(offer["longitude"])],
            tooltip="Click me!",
            popup=f"Título: {offer['title']}\n compañia: {offer['company_name']}, \n Nivel de experiencia: {offer['experience_level']}",
            icon=folium.Icon(color="green"),
            ).add_to(m)
        
        m.show_in_browser()
        
        
        end_time = controller.get_time()
        print(f"Se ha demorado un total de {controller.delta_time(start_time, end_time)}")
        pass
    if req == 7:
        
        año = input("Por favor digite el año para el que desea efectuar la consulta: ")
        codigo_pais = input("Por favor digite el codigo del país para el que desea efectuar la consulta: ")
        print("Por favor digite la propiedad de conteo:")
        print("[1] Experticia ")
        print("[2] Ubicación ")
        print("[3] Habilidad ")
        opcion = input("opción: ")
        if opcion == "1":
            propiedad_conteo = "Experticia"
    
        elif opcion == "2":
            propiedad_conteo = "Ubicación"
    
        elif opcion == "3":
            propiedad_conteo = "Habilidad"
    
        else:
            print("-"*100)
            print("\nDigitó una opción incorrecta\n")
            print("intente nuevamente...")
            print("-"*100)
        
            print_req_7(control)
            return None
    
        bins = None
        start_time = controller.get_time()
        
        data_experticia, data_ubicacion, data_habilidad, ofertas_totales,maximo,minimo, prueba, nombre_prueba= controller.req_7(control, año, codigo_pais, propiedad_conteo, bins)
        if nombre_prueba == "Rapidez":
            print(f"El requerimiento se ha demorado un total de {prueba}[ms]")
        else:
            print(f"El requerimiento ha consumido un total de {prueba}[kB]")
        
        oferta1 = lt.getElement(ofertas_totales, 1)
        m = folium.Map(location=(float(oferta1["latitude"]), float(oferta1["longitude"])))
        colores_marcadores = [
        "blue", "green", "red", "purple", "orange", "darkred",
        "lightred", "beige", "darkblue", "darkgreen", "cadetblue",
        "darkpurple", "white", "pink", "lightblue", "lightgreen", "gray", "black"
        ]

        for offer in lt.iterator(ofertas_totales):
            #print(f"{offer["latitude"]},{offer["longitude"]}")
            
            if (offer["workplace_type"] == "remote" and opcion == "2") or (offer["experience_level"] == "junior" and opcion == "1"):
                folium.Marker(
                location=[float(offer["latitude"]), float(offer["longitude"])],
                tooltip="Click me!",
                popup=f"Título: {offer['title']}\n compañia: {offer['company_name']}, \n Nivel de experiencia: {offer['experience_level']}, \n Ubicación: {offer['workplace_type']}",
                icon=folium.Icon(color="red"),
                ).add_to(m)
            elif (offer["workplace_type"] == "partly_remote" and opcion == "2") or (offer["experience_level"] == "mid" and opcion == "1"):
                folium.Marker(
                location=[float(offer["latitude"]), float(offer["longitude"])],
                tooltip="Click me!",
                popup=f"Título: {offer['title']}\n compañia: {offer['company_name']}, \n Nivel de experiencia: {offer['experience_level']}, \n Ubicación: {offer['workplace_type']}",
                icon=folium.Icon(color="purple"),
                ).add_to(m)
            elif (offer["workplace_type"] == "office" and opcion == "2") or (offer["experience_level"] == "senior" and opcion == "1"):
                folium.Marker(
                location=[float(offer["latitude"]), float(offer["longitude"])],
                tooltip="Click me!",
                popup=f"Título: {offer['title']}\n compañia: {offer['company_name']}, \n Nivel de experiencia: {offer['experience_level']}, \n Ubicación: {offer['workplace_type']}",
                icon=folium.Icon(color="cadetblue"),
                ).add_to(m)
            
            else:
                skills = []
                for skill in lt.iterator(offer['habilidades_solicitadas']):
                    skills.append(skill)
                folium.Marker(
                location=[float(offer["latitude"]), float(offer["longitude"])],
                tooltip="Click me!",
                popup=f"Título: {offer['title']}\n compañia: {offer['company_name']}, \n Habilidades: {skills}",
                icon=folium.Icon(color=random.choice(colores_marcadores)),
                ).add_to(m)
            
        
        
        m.show_in_browser()
        end_time = controller.get_time()
        print(f"Se ha demorado un total de {controller.delta_time(start_time, end_time)}")
        
    controller.req_8(control, req)
    
def cambiar_pruebas(respuesta):
    prueba= controller.cambiar_pruebas(respuesta)
    return prueba

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
            control = new_controller()
            print("Cargando información de los archivos ....\n")
            data, prueba, nombre_prueba, sorted_list = load_data(control)
            primeras_cinco = lt.subList(sorted_list, 1, 5)
            ultimas_cinco = lt.subList(sorted_list, lt.size(sorted_list)-5, 5)
            print("\nPRIMERAS CINCO OFERTAS\n")
    
            llaves=["published_at","title", "company_name", "experience_level", "country_code", "city","company_size", "workplace_type", "salario_promedio"]
            valores_a_imprimir1 = []
        
            for offer in lt.iterator(primeras_cinco):
                lst_provisional = []
                for llave in llaves:
                    lst_provisional.append(offer[llave])
                valores_a_imprimir1.append(lst_provisional)
        
        
            
           
            print((tabulate(valores_a_imprimir1, headers=llaves)).center(220))
            
        
            print("\nULTIMAS CINCO OFERTAS\n")
        
            valores_a_imprimir1 = []
        
            for offer in lt.iterator(ultimas_cinco):
                lst_provisional = []
                for llave in llaves:
                    lst_provisional.append(offer[llave])
                valores_a_imprimir1.append(lst_provisional)
            print((tabulate(valores_a_imprimir1, headers=llaves)).center(220))
            if nombre_prueba == "Rapidez":
                print(f"Se ha demorado un total de {prueba}[ms]")
            else:
                print(f"Se han consumido un total de {prueba}[kB]")
            
        elif int(inputs) == 2:
            print_req_1(control)

        elif int(inputs) == 3:
            salario_minimo = int(input("Por favor digite el límite inferior del salario mínimo ofertado: "))
            salario_maximo = int(input("Por favor digite el límite inferior del salario mínimo ofertado: "))
            function = print_req_2(control, salario_minimo, salario_maximo)
            print("Los resultados de la consulta fueron los siguientes: ".center(220))
            if function[1]:
                print(f"La cantidad de ofertas publicadas entre ${salario_minimo} y ${salario_maximo} fueron: {function[0]}".center(220))

                    
                llaves=["published_at","title", "company_name", "experience_level", "country_code", "city","marker_icon", "workplace_type", "salario_minimo"]
                valores_a_imprimir1 = []
                    
                for offer in lt.iterator(function[1]):
                    lst_provisional = []
                    for llave in llaves:
                        lst_provisional.append(offer[llave])
                    valores_a_imprimir1.append(lst_provisional)
                    
                valores_a_imprimir2 = []
                conteo = 1
                for offer in lt.iterator(function[1]):
                    lista_provisional = [conteo]
                    for skill in lt.iterator(offer["habilidades_solicitadas"]):  
                        lista_provisional.append(skill)
                    conteo += 1
                    valores_a_imprimir2.append(lista_provisional)
                        
                print((tabulate(valores_a_imprimir1, headers=llaves)).center(220))
                print("\nHABILIDADES SOLICITADAS")
                print((tabulate(valores_a_imprimir2)))
                print(f"Se ha demorado un total de {function[2]}[ms]")

        elif int(inputs) == 4:
            pais=str(input("Por favor ingrese el codigo de pais que desea buscar: "))
            experticia= str(input("Por favor ingrese el nivel de experticia: "))
            N= int(input("Ingrese el numero de ofertas que desea listar: "))
            print_req_3(control,pais,experticia, N)

        elif int(inputs) == 5:
            print_req_4(control)

        elif int(inputs) == 6:
            numero_ofertas = int(input("Por favor digite el numero de ofertas a imprimir: "))
            tamano_minimo_compania = int(input("Por favor digite el el limite inferior del tamaño de la compañia: "))
            tamano_maximo_compania = int(input("Por favor digite el el limite superior del tamaño de la compañia: "))
            skill = input("Por favor digite el nombre de la habilidad solicitada: ")
            limite_inferior_skill = int(input("Por favor digite el limite inferior del nivel de la habilidad: "))
            limite_superior_skill = int(input("Por favor digite el limite superior del nivel de la habilidad: "))
            function = print_req_5(control, numero_ofertas, tamano_minimo_compania,
          tamano_maximo_compania, skill, limite_inferior_skill, limite_superior_skill)
            
            print("Los resultados de la consulta fueron los siguientes: ".center(220))
            
            if function[1]:
                print(f"La cantidad de ofertas publicadas buscando la skill de {skill} en compañias fueron: {function[0]}".center(220))

                    
                llaves=["published_at","title", "company_name", "experience_level", "country_code", "city","marker_icon", "workplace_type", "open_to_hire_ukrainians"]
                valores_a_imprimir1 = []
                    
                for offer in lt.iterator(function[1]):
                    lst_provisional = []
                    for llave in llaves:
                        lst_provisional.append(offer[llave])
                    valores_a_imprimir1.append(lst_provisional)
                    
                valores_a_imprimir2 = []
                conteo = 1
                for offer in lt.iterator(function[1]):
                    lista_provisional = [conteo]
                    for skill in lt.iterator(offer["habilidades_solicitadas"]):  
                        lista_provisional.append(skill)
                    conteo += 1
                    valores_a_imprimir2.append(lista_provisional)
                        
                print((tabulate(valores_a_imprimir1, headers=llaves)).center(220))
                print("\nHABILIDADES SOLICITADAS")
                print((tabulate(valores_a_imprimir2)))
                print(f"Se ha demorado un total de {function[2]}[ms]")

        elif int(inputs) == 7:
            N= int(input("Ingrese el numero de ciudades que desea listar: "))
            fecha1=input("Ingrese la fecha inicial en formato %Y-%m-%\d ")
            fecha2=input("Ingrese la fecha final en formato %Y-%m-%\d ")
            salario1=float(input("Ingrese el salario inicial "))
            salario2=float(input("Ingrese el salario final "))
            print_req_6(control,N,fecha1,fecha2,salario1,salario2)

        elif int(inputs) == 8:
            print_req_7(control)

        elif int(inputs) == 9:
            print_req_8(control)
        
        elif int(inputs) == 10:
            print("[1] Rapidez")
            print("[2] Almacenamiento\n")
            respuesta = input("¿Qué opción desea escoger? ")
            while respuesta != "1" and respuesta != "2":
                
                
                print("Opción no disponible\n")
                respuesta = input("¿Qué opción desea escoger? ")
            if respuesta == "1":
                cambiar_pruebas("Rapidez")
            elif respuesta == "2":
                cambiar_pruebas("Almacenamiento")
        elif int(inputs) == 11:
            print("\nPOR FAVOR DIGITE A CONTINUACIÓN EL SUFIJO DEL ARCHIVO PARA EL QUE DESEA MANIPULAR LA MUESTRA\n")
            sufijo = input("sufijo : ")
            
            if sufijo in ["10-por", "20-por", "30-por","40-por","50-por", "60-por", "70-por", "80-por","90-por","small","medium", "large"]:
                controller.cambiarTamañoMuestra(sufijo)
            else:
                print("\n no existen archivos con ese sufijo, intente nuevamente\n")

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa")
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
