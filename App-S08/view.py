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
import folium
import webbrowser
import folium.plugins
default_limit=1000000

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
    control=controller.new_controller()
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


def tamanio_archivo():
    """
    Función que le pide al usuario que seleccione el tamaño del archivo que desea cargar

    Returns:
    retorno: string con el tamaño del archivo que se va a cargar
    """
    #Se le muestra al usuario las opciones de tamaño de archivo que puede cargar
    print("Seleccione el tamaño del archivo a cargar")
    opciones={"1": "10",
              "2": "20",
              "3": "30",
              "4": "40",
              "5": "50",
              "6": "60",
              "7": "70",
              "8": "80",
              "9": "90",
              "10": "small",
              "11": "medium",
              "12": "large"}
    #Se iteran las opciones y se imprimen
    for opcion in opciones:
        print(opcion + "- " + opciones[opcion])
    #Se le pide al usuario que seleccione una opción
    inputs = input('Seleccione una opción para continuar\n')
    #Se valida que la opción seleccionada sea válida y exista en el diccionario de opciones
    if inputs in opciones:
        retorno= opciones[inputs]
    else:
        print("Opción errónea, vuelva a elegir.\n")
        retorno= tamanio_archivo()
    return retorno
def load_data(control,memoria):
    """
    Carga los datos
    Args:
    control: instancia del controlador con el modelo cargado en memoria
    Returns:
    datos: diccionario con la información de los archivos cargados
    """
    #Se inicia una variable donde la elección del tamaño del archivo es False
    eleccion=False
    tamanio=None
    #Se itera hasta que el usuario seleccione un tamaño de archivo
    while eleccion==False:
        tamanio=tamanio_archivo()
        if tamanio_archivo!=None:
            eleccion=True
    #Se le muestra al usuario el tamaño de archivo que seleccionó
    print("-"*20)
    print("El tamaño elegido es "+ tamanio)
    print("-"*20)
    print("Cargando información de los archivos ....\n")
    #Se llama la función load_data del controlador
    datos=controller.load_data(control, tamanio, memoria)
    return datos


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
    fecha_inicio = input("Ingrese la fecha de inicio en formato YYYY-MM-DD: ")
    fecha_fin = input("Ingrese la fecha de fin en formato YYYY-MM-DD: ")
    memoria=memoria_pregunta()
    datos=controller.req_1(control, fecha_inicio, fecha_fin, memoria)
    print("El tiempo que ha tomado en la ejecución es:",datos[1],"ms")
    if memoria==True:
        print("La memoria usada ha sido:",datos[2],"KB")
    print("La cantidad de ofertas encontradas fue de:",datos[0][1])
    info=datos[0][0]
    header=("#","Fecha","Titulo oferta", "Nombre empresa", "Nivel experticia", "Pais de oferta", "Ciudad de oferta","Tamaño empresa","Tipo trabajo","Habilidades")
    tabla=[]
    if lt.size(info)>10:
        for i in range(1,6):
            tabla.append([i,lt.getElement(info,i)[0], lt.getElement(info,i)[1], lt.getElement(info,i)[2], lt.getElement(info,i)[3], lt.getElement(info,i)[4], lt.getElement(info,i)[5],lt.getElement(info,i)[6],lt.getElement(info,i)[7],lt.getElement(info,i)[8]])
        print(tabulate(tabla, headers=header, tablefmt="grid"))
        tabla=[]
        for i in range(lt.size(info)-4, lt.size(info)+1):
            tabla.append([i,lt.getElement(info,i)[0], lt.getElement(info,i)[1], lt.getElement(info,i)[2], lt.getElement(info,i)[3], lt.getElement(info,i)[4], lt.getElement(info,i)[5],lt.getElement(info,i)[6],lt.getElement(info,i)[7],lt.getElement(info,i)[8]])
        print(tabulate(tabla, headers=header, tablefmt="grid"))
    else:
        for i in range(1,lt.size(info)+1):
            tabla.append([i,lt.getElement(info,i)[0], lt.getElement(info,i)[1], lt.getElement(info,i)[2], lt.getElement(info,i)[3], lt.getElement(info,i)[4], lt.getElement(info,i)[5],lt.getElement(info,i)[6],lt.getElement(info,i)[7],lt.getElement(info,i)[8]])
        print(tabulate(tabla, headers=header, tablefmt="grid"))
    return info


def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    minimo_salario = float(input("Ingrese el salario mínimo: "))
    maximo_salario = float(input("Ingrese el salario máximo: "))
    memoria=memoria_pregunta()
    datos=controller.req_2(control, minimo_salario, maximo_salario, memoria)
    print("El tiempo que ha tomado en la ejecución es:",datos[1],"ms")
    if memoria==True:
        print("La memoria usada ha sido:",datos[2],"KB")
    print("La cantidad de ofertas encontradas fue de:",datos[0][1])
    info=datos[0][0]
    header=("#","Fecha","Titulo oferta", "Nombre empresa", "Nivel experticia", "Pais de oferta", "Ciudad de oferta","Tamaño empresa","Tipo trabajo","Habilidades","Salario")
    tabla=[]
    if lt.size(info)>10:
        for i in range(1,6):
            tabla.append([i,lt.getElement(info,i)[0], lt.getElement(info,i)[1], lt.getElement(info,i)[2], lt.getElement(info,i)[3], lt.getElement(info,i)[4], lt.getElement(info,i)[5],lt.getElement(info,i)[6],lt.getElement(info,i)[7],lt.getElement(info,i)[8],lt.getElement(info,i)[9]])
        print(tabulate(tabla, headers=header, tablefmt="grid"))
        tabla=[]
        for i in range(lt.size(info)-4, lt.size(info)+1):
            tabla.append([i,lt.getElement(info,i)[0], lt.getElement(info,i)[1], lt.getElement(info,i)[2], lt.getElement(info,i)[3], lt.getElement(info,i)[4], lt.getElement(info,i)[5],lt.getElement(info,i)[6],lt.getElement(info,i)[7],lt.getElement(info,i)[8],lt.getElement(info,i)[9]])
        print(tabulate(tabla, headers=header, tablefmt="grid"))
    else:
        for i in range(1,lt.size(info)+1):
            tabla.append([i,lt.getElement(info,i)[0], lt.getElement(info,i)[1], lt.getElement(info,i)[2], lt.getElement(info,i)[3], lt.getElement(info,i)[4], lt.getElement(info,i)[5],lt.getElement(info,i)[6],lt.getElement(info,i)[7],lt.getElement(info,i)[8],lt.getElement(info,i)[9]])
        print(tabulate(tabla, headers=header, tablefmt="grid"))
    return info

def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    numero_ofertas = int(input("Ingrese el número de ofertas que desea mostrar: "))
    cod_pais = input("Ingrese el codigo del pais: ")
    nivel_exp = input("Ingrese el nivel de experticia: ")
    memoria=memoria_pregunta()
    datos=controller.req_3(control, numero_ofertas, cod_pais, nivel_exp, memoria)
    print("El tiempo que ha tomado en la ejecución es:",datos[1],"ms")
    if memoria==True:
        print("La memoria usada ha sido:",datos[2],"KB")
    print("La cantidad de ofertas encontradas fue de:",datos[0][2]) 
    info=datos[0][0]
    header=("#","Fecha","Titulo oferta", "Nombre empresa", "Nivel experticia", "Pais de oferta", "Ciudad de oferta","Tamaño empresa","Tipo trabajo","Habilidades","Salario")
    tabla=[]
    if lt.size(info)>10:
        for i in range(1,6):
            tabla.append([i,lt.getElement(info,i)[0], lt.getElement(info,i)[1], lt.getElement(info,i)[2], lt.getElement(info,i)[3], lt.getElement(info,i)[4], lt.getElement(info,i)[5],lt.getElement(info,i)[6],lt.getElement(info,i)[7],lt.getElement(info,i)[8], lt.getElement(info,i)[9]]) 
        print(tabulate(tabla, headers=header, tablefmt="grid"))
        tabla=[]
        for i in range(lt.size(info)-4, lt.size(info)+1):
            tabla.append([i,lt.getElement(info,i)[0], lt.getElement(info,i)[1], lt.getElement(info,i)[2], lt.getElement(info,i)[3], lt.getElement(info,i)[4], lt.getElement(info,i)[5],lt.getElement(info,i)[6],lt.getElement(info,i)[7],lt.getElement(info,i)[8], lt.getElement(info,i)[9]]) 
        print(tabulate(tabla, headers=header, tablefmt="grid"))
    else:
        for i in range(1,lt.size(info)+1):
            tabla.append([i,lt.getElement(info,i)[0], lt.getElement(info,i)[1], lt.getElement(info,i)[2], lt.getElement(info,i)[3], lt.getElement(info,i)[4], lt.getElement(info,i)[5],lt.getElement(info,i)[6],lt.getElement(info,i)[7],lt.getElement(info,i)[8], lt.getElement(info,i)[9]]) 
        print(tabulate(tabla, headers=header, tablefmt="grid"))
    return info

def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    n_ofertas=int(input("Ingrese el número de ofertas laborales a consultar: "))
    ciudad=input("Ingrese la ciudad que desea consultar: ")
    tipo=input("Ingrese tipo de ubicación de trabajo: ")
    print("-"*20+"Cargando..."+"-"*20)
    memoria=memoria_pregunta()
    datos=controller.req_4(control, n_ofertas, ciudad, tipo,memoria)
    retorno=datos[0][0]
    if retorno== None:
        return None
    print("El tiempo que ha tomado en la ejecución es:",round(datos[1],2),"ms")
    if memoria==True:
        print("La memoria usada ha sido:",round(datos[2],2),"KB")
    print("El total de ofertas publicadas en "+str(ciudad)+" y de tipo de ubicación "+str(tipo)+" es de " +str(datos[0][1])+" ofertas")
    
    header=["#","Fecha de publicacion","Titulo oferta", "Nombre empresa","Nivel experticia","País de la empresa","Ciudad de la empresa","Tamaño de la empresa", "Tipo de ubicación trabajo", "Habilidades solicitadas","Salario mínimo"]
    tabla=[]
    if lt.size(retorno)>10:
        for i in range(1,6):
            tabla.append([i,lt.getElement(retorno,i)[0], lt.getElement(retorno,i)[1], lt.getElement(retorno,i)[2], lt.getElement(retorno,i)[3], lt.getElement(retorno,i)[4], lt.getElement(retorno,i)[5],lt.getElement(retorno,i)[6],lt.getElement(retorno,i)[7],lt.getElement(retorno,i)[8],lt.getElement(retorno,i)[9]])
        print(tabulate(tabla, headers=header, tablefmt="grid"))
        tabla=[]
        for i in range(lt.size(retorno)-4, lt.size(retorno)+1):
            tabla.append([i,lt.getElement(retorno,i)[0], lt.getElement(retorno,i)[1], lt.getElement(retorno,i)[2], lt.getElement(retorno,i)[3], lt.getElement(retorno,i)[4], lt.getElement(retorno,i)[5],lt.getElement(retorno,i)[6],lt.getElement(retorno,i)[7],lt.getElement(retorno,i)[8],lt.getElement(retorno,i)[9]])
        print(tabulate(tabla, headers=header, tablefmt="grid"))
    else:
        for i in range(1,lt.size(retorno)+1):
            tabla.append([i,lt.getElement(retorno,i)[0], lt.getElement(retorno,i)[1], lt.getElement(retorno,i)[2], lt.getElement(retorno,i)[3], lt.getElement(retorno,i)[4], lt.getElement(retorno,i)[5],lt.getElement(retorno,i)[6],lt.getElement(retorno,i)[7],lt.getElement(retorno,i)[8],lt.getElement(retorno,i)[9]])
        print(tabulate(tabla, headers=header, tablefmt="grid"))
    return retorno

def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    numero_ofertas = int(input("Ingrese el número de ofertas que desea ver: "))
    tamanio_minimo = int(input("Ingrese el tamaño mínimo de la empresa: "))
    tamanio_maximo = int(input("Ingrese el tamaño máximo de la empresa: "))
    habilidades = input("Ingrese la habilidad que desea buscar: ")
    nivel_habilidad_minimo = int(input("Ingrese el nivel mínimo de la habilidad: "))
    nivel_habilidad_maximo = int(input("Ingrese el nivel máximo de la habilidad: "))
    memoria=memoria_pregunta()
    datos=controller.req_5(control, numero_ofertas, tamanio_minimo, tamanio_maximo, habilidades, nivel_habilidad_minimo, nivel_habilidad_maximo, memoria)
    print("El tiempo que ha tomado en la ejecución es:",datos[1],"ms")
    if memoria==True:
        print("La memoria usada ha sido:",datos[2],"KB")
    print("La cantidad de ofertas encontradas fue de:",datos[0][1])
    info=datos[0][0]
    header=("#","Fecha","Titulo oferta", "Nombre empresa", "Nivel experticia", "Pais de oferta", "Ciudad de oferta","Tamaño empresa","Tipo trabajo","Habilidades","Salario")
    tabla=[]
    if lt.size(info)>10:
        for i in range(1,6):
            tabla.append([i,lt.getElement(info,i)[0], lt.getElement(info,i)[1], lt.getElement(info,i)[2], lt.getElement(info,i)[3], lt.getElement(info,i)[4], lt.getElement(info,i)[5],lt.getElement(info,i)[6],lt.getElement(info,i)[7],lt.getElement(info,i)[8],lt.getElement(info,i)[9]])
        print(tabulate(tabla, headers=header, tablefmt="grid"))
        tabla=[]
        for i in range(lt.size(info)-4, lt.size(info)+1):
            tabla.append([i,lt.getElement(info,i)[0], lt.getElement(info,i)[1], lt.getElement(info,i)[2], lt.getElement(info,i)[3], lt.getElement(info,i)[4], lt.getElement(info,i)[5],lt.getElement(info,i)[6],lt.getElement(info,i)[7],lt.getElement(info,i)[8],lt.getElement(info,i)[9]])
        print(tabulate(tabla, headers=header, tablefmt="grid"))
    else:
        for i in range(1,lt.size(info)+1):
            tabla.append([i,lt.getElement(info,i)[0], lt.getElement(info,i)[1], lt.getElement(info,i)[2], lt.getElement(info,i)[3], lt.getElement(info,i)[4], lt.getElement(info,i)[5],lt.getElement(info,i)[6],lt.getElement(info,i)[7],lt.getElement(info,i)[8],lt.getElement(info,i)[9]])
        print(tabulate(tabla, headers=header, tablefmt="grid"))
    return info

def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    numero_ciudades = int(input("Ingrese el número de ciudades que desea ver: "))
    fecha_inicio = input("Ingrese la fecha de inicio en formato YYYY-MM-DD: ")
    fecha_fin = input("Ingrese la fecha de fin en formato YYYY-MM-DD: ")
    salario_minimo = float(input("Ingrese el salario mínimo: "))
    salario_maximo = float(input("Ingrese el salario máximo: "))
    memoria=memoria_pregunta()
    datos=controller.req_6(control, numero_ciudades, fecha_inicio, fecha_fin, salario_minimo, salario_maximo, memoria)
    
    if memoria==True:
        print("La memoria usada ha sido:",datos[2],"KB")
    print("El tiempo que ha tomado en la ejecución es:",datos[1],"ms")
    print("La cantidad de ofertas encontradas fue de:",datos[0][1])
    print("El numero de ciudades encontradas fue de:",datos[0][2])
    print("Las ciudades ordenadas alfabeticamente son:")
    ciudades=datos[0][3]
    header=("#","Ciudad", "Cantidad")
    tabla=[]
    cantidad=0
    for i in lt.iterator(ciudades):
        cantidad+=1
        tabla.append([cantidad,i[0],i[1]])
    print(tabulate(tabla, headers=header, tablefmt="grid"))
    tabla=[]
    print("Las ofertas en la ciudad con mauor cantidad de ofertas laborales publicadas son:")
    info=datos[0][0]
    header=("#","Fecha","Titulo oferta", "Nombre empresa", "Nivel experticia", "Pais de oferta", "Ciudad de oferta","Tamaño empresa","Tipo trabajo","Habilidades","Salario")
    if lt.size(info)>10:
        for i in range(1,6):
            tabla.append([i,lt.getElement(info,i)[0], lt.getElement(info,i)[1], lt.getElement(info,i)[2], lt.getElement(info,i)[3], lt.getElement(info,i)[4], lt.getElement(info,i)[5],lt.getElement(info,i)[6],lt.getElement(info,i)[7],lt.getElement(info,i)[8],lt.getElement(info,i)[9]])
        print(tabulate(tabla, headers=header, tablefmt="grid"))
        tabla=[]
        for i in range(lt.size(info)-4, lt.size(info)+1):
            tabla.append([i,lt.getElement(info,i)[0], lt.getElement(info,i)[1], lt.getElement(info,i)[2], lt.getElement(info,i)[3], lt.getElement(info,i)[4], lt.getElement(info,i)[5],lt.getElement(info,i)[6],lt.getElement(info,i)[7],lt.getElement(info,i)[8],lt.getElement(info,i)[9]])
        print(tabulate(tabla, headers=header, tablefmt="grid"))
    else:
        for i in range(1,lt.size(info)+1):
            tabla.append([i,lt.getElement(info,i)[0], lt.getElement(info,i)[1], lt.getElement(info,i)[2], lt.getElement(info,i)[3], lt.getElement(info,i)[4], lt.getElement(info,i)[5],lt.getElement(info,i)[6],lt.getElement(info,i)[7],lt.getElement(info,i)[8],lt.getElement(info,i)[9]])
        print(tabulate(tabla, headers=header, tablefmt="grid"))
    return info


def print_req_7(control):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    anio=int(input("Ingrese el año que desea consultar: "))
    codigo_pais=input("Ingrese el código del país que desea consultar: ")
    propiedad_conteo=input("Ingrese la propiedad por la que desea contar (Experticia, Ubicacion, Habilidad): ")
    memoria=memoria_pregunta()
    if propiedad_conteo.lower()=="experticia":
        propiedad_conteo="experience_level"
        retorno=controller.req_7(control, anio, codigo_pais, propiedad_conteo, memoria)
    elif propiedad_conteo.lower()=="ubicacion":
        propiedad_conteo="workplace_type"
        retorno=controller.req_7(control, anio, codigo_pais, propiedad_conteo, memoria)
    elif propiedad_conteo.lower()=="habilidad":
        propiedad_conteo="skills"
        retorno=controller.req_7(control, anio, codigo_pais, propiedad_conteo, memoria)
    else:
        print("Opción errónea, vuelva a elegir.\n")
        print_req_7(control)
    datos=retorno[0]
    tiempo=retorno[1]
    if memoria==True:
        print("La memoria usada ha sido:",retorno[2],"KB")
    print("El tiempo que ha tomado en la ejecución es:",tiempo,"ms")
    print("La cantidad de ofertas encontradas dentro del periodo actual son de:",datos[1])
    print("La cantidad de ofertas usadas para el gráfico son de:",datos[2])
    print("El elemento con mayor valor es "+datos[5][0]+" con "+str(datos[5][1]))
    print("El elemento con menor valor es "+datos[6][0]+" con "+str(datos[6][1]))
    
    header=("#","Fecha", "Titulo oferta", "Nombre empresa", "Pais", "Ciudad", "Tamaño empresa", "Salario", propiedad_conteo)
    tabla=[]
    info=datos[0]
    if lt.size(info)>10:
        for i in range(1,6):
            tabla.append([i,lt.getElement(info,i)[0], lt.getElement(info,i)[1], lt.getElement(info,i)[2], lt.getElement(info,i)[3], lt.getElement(info,i)[4], lt.getElement(info,i)[5],lt.getElement(info,i)[6],lt.getElement(info,i)[7]])
        print(tabulate(tabla, headers=header, tablefmt="grid"))
        tabla=[]
        for i in range(lt.size(info)-4, lt.size(info)+1):
            tabla.append([i,lt.getElement(info,i)[0], lt.getElement(info,i)[1], lt.getElement(info,i)[2], lt.getElement(info,i)[3], lt.getElement(info,i)[4], lt.getElement(info,i)[5],lt.getElement(info,i)[6],lt.getElement(info,i)[7]])
        print(tabulate(tabla, headers=header, tablefmt="grid"))
    else:
        for i in range(1,lt.size(info)+1):
            tabla.append([i,lt.getElement(info,i)[0], lt.getElement(info,i)[1], lt.getElement(info,i)[2], lt.getElement(info,i)[3], lt.getElement(info,i)[4], lt.getElement(info,i)[5],lt.getElement(info,i)[6],lt.getElement(info,i)[7]])
        print(tabulate(tabla, headers=header, tablefmt="grid"))
    plt.title("Cantidad de ofertas laborales en "+str(propiedad_conteo)+" durante el año "+str(anio))
    plt.xlabel(str(propiedad_conteo))
    plt.ylabel("Cantidad de ofertas")
    plt.bar(datos[3], datos[4], color='black')
    plt.show()
    return info, propiedad_conteo
    # TODO: Imprimir el resultado del requerimiento 7

def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    eleccion=int(input("Ingrese el requerimiento que desea ejecutar (1,2,3): "))
    mapa=folium.Map(location=[4.570868, -74.297333], zoom_start=5, tiles=folium.TileLayer(no_wrap=True))
    if eleccion==1:
        datos=print_req_1(control)
    elif eleccion==2:
        datos=print_req_2(control)
    elif eleccion==3:
        datos=print_req_3(control)
    elif eleccion==4:
        datos=print_req_4(control)
    elif eleccion==5:
        datos=print_req_5(control)
    elif eleccion==6:
        datos=print_req_6(control)
    elif eleccion==7:
        info=print_req_7(control)
        datos=info[0]
        propiedad_conteo=info[1]
    else:
        print("Opción errónea, vuelva a elegir.\n")
        print_req_8(control)
    memoria=memoria_pregunta()
    print("="*20+"Cargando mapa"+"="*20)
    if eleccion==7:
        info=controller.req_8(datos, mapa, eleccion, propiedad_conteo, memoria)
    else:
        req7=False
        info=controller.req_8(datos, mapa, eleccion, req7, memoria)
    print("El tiempo que ha tomado en la ejecución es:",info[1],"ms")
    if memoria==True:
        print("La memoria usada ha sido:",info[2],"KB")
    archivo=cf.app_dir+"mapa.html"
    mapa.save(archivo)
    webbrowser.open(archivo,new=2)

def memoria_pregunta():
    pregunta=input("¿Desea ver la memoria usada? (s/n): ")
    if pregunta.lower()=="s":
        return True
    else:
        return False
def divisa_pregunta():
    valor=input("Desea ingresar sus propios valores de conversión?: (s/n):")
    if valor.lower()=="s":
        usd_usd=float(input("Ingrese el valor de 1 dolar en dolares: "))
        eur_usd=float(input("Ingrese el valor de 1 euro en dolares: "))
        gbp_usd=float(input("Ingrese el valor de 1 libra esterlina en dolares: "))
        pln_usd=float(input("Ingrese el valor de 1 esloti en dolares: "))
        chf_usd=float(input("Ingrese el valor de 1 franco suizo en dolares: "))
        controller.conversor_divisas(usd_usd,eur_usd,gbp_usd,pln_usd,chf_usd)   
# Se crea el controlador asociado a la vista
control = new_controller()

# main del reto
if __name__ == "__main__":
    """
    Menu principal
    """
    #ciclo del menu
    def menu_principal():
        datos_cargados = False
        working = True
        algoritmo_orden_seleccionado = False
        while working:
            print_menu()
            inputs = input('Seleccione una opción para continuar\n')
            if int(inputs) == 1:
                if datos_cargados==False:
                    control = new_controller()
                    memoria=memoria_pregunta()
                    divisa_pregunta()
                    data = load_data(control,memoria)
                    print("El tiempo que ha tomado en la ejecución es:",data[1],"ms")
                    datos=controller.obtener_datos(control, "jobs-lista")
                    print("-"*10+"Carga de datos exitosa"+"-"*10)
                    size=lt.size(datos)
                    print("Se han cargado "+str(size)+" trabajos")
                    header=["#","Fecha","Titulo oferta", "Nombre empresa", "Nivel experticia", "Pais de oferta", "Ciudad de oferta"]
                    tabla=[]
                    for i in range(1,4):
                        tabla.append([i,lt.getElement(datos,i)["published_at"], lt.getElement(datos,i)["title"], lt.getElement(datos,i)["company_name"], lt.getElement(datos,i)["experience_level"], lt.getElement(datos,i)["country_code"], lt.getElement(datos,i)["city"]])
                    print(tabulate(tabla, headers=header, tablefmt="grid"))
                    tabla=[]
                    for i in range(size-2, size+1):
                        print(".")
                        tabla.append([i,lt.getElement(datos,i)["published_at"], lt.getElement(datos,i)["title"], lt.getElement(datos,i)["company_name"], lt.getElement(datos,i)["experience_level"], lt.getElement(datos,i)["country_code"], lt.getElement(datos,i)["city"]])
                    print(tabulate(tabla, headers=header, tablefmt="grid"))
                    datos_cargados=True
                    print("="*40)
                    if memoria==True:
                        print("La memoria usada ha sido:",data[2],"KB")
                    print("="*40)
                else:
                    print("Los datos ya han sido cargados")

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
            elif int(inputs)==0:
                working=False
                print("\nGracias por utilizar el programa") 
            else:
                print("Opción errónea, vuelva a elegir.\n")
        sys.exit(0)
    threading.stack_size(67108864*2)
    sys.setrecursionlimit(default_limit*10)
    thread=threading.Thread(target=menu_principal)
    menu_principal()
