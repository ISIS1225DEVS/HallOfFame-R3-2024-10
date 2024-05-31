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
assert cf
default_limit = 1000
sys.setrecursionlimit(default_limit*10)
from tabulate import tabulate
import matplotlib.pyplot as plt
import traceback
import New_Functions as nf
import threading

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
    control= controller.new_controller()
    return control

def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Conocer las ofertas laborales publicadas entre dos fechas")
    print("3- Conocer las ofertas laborales publicadas cuyo salario mínimo esté en un rango dado")
    print("4- Consultar las N ofertas laborales más recientes según un país y un nivel de experiencia requerido")
    print("5- Consultar las N ofertas laborales más recientes según una ciudad y el tipo de ubicación")
    print("6- Consultar las N ofertas laborales más antiguas para las compañías en un rango dado de tamaño y con una habilidad solicitada")
    print("7- Reportar las N ciudades con el mayor número de ofertas laborales publicadas entre dos fechas y en un rango de salario ofertado")
    print("8- Graficar en un histograma anual de las ofertas laborales para un país de acuerdo a características específicas de la oferta ")
    print("9- Visualizar las ofertas laborales de cada requerimiento en un mapa interactivo")
    print("0- Salir")


def load_data(control,mem):
    """
    Carga los datos
    """
    return controller.load_data(control,mem)


def print_data(control):
    """
        Función que imprime un dato dado su ID
    """
    lista = controller.data_org(control)
    headers = ['Numero', 'Fecha de publicación','Título de la oferta', 'Nombre de la empresa', 'Nivel de experiencia', 
               'Pais', 'Ciudad', 'Tamaño de la empresa', 'Tipo de ubicación de trabajo']
    total = controller.size_control(control)[0]
    tabla = []
    for i in range(0, total):
        if i < 3 or i >= total-3:
            tabla.append([i+1,
                        nf.getElement(lista,i)["published_at"],
                        nf.getElement(lista,i)["title"],
                        nf.getElement(lista,i)["company_name"],
                        nf.getElement(lista,i)["experience_level"],
                        nf.getElement(lista,i)["country_code"], 
                        nf.getElement(lista,i)["city"],
                        nf.getElement(lista,i)["company_size"],
                        nf.getElement(lista,i)["workplace_type"],
                        nf.getElement(lista,i)["salary"],
                        nf.getElement(lista,i)['skill']]
                     )
    print(tabulate(tabla, headers=headers, tablefmt="grid"))
    

def print_req_1(control, initialDate, finalDate):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    data_structs= control['model']
    r= controller.req_1(data_structs, initialDate, finalDate)
    total, lista= r
    para_tabular, headers= lista
    print('El total de ofertas publicadas entre las fechas es de: ' + str(total))
    print(tabulate(para_tabular, headers=headers, tablefmt='fancygrid'))


def print_req_2(control, salario_min, salario_max):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    data_structs= control['model']
    total, lista= controller.req_2(data_structs, salario_min, salario_max)
    lista = nf.inverse(lista)
    print('El total de ofertas publicadas entre los salarios es de: ' + str(total))
    headers = ['Numero', 'Fecha de publicación','Título de la oferta', 'Nombre de la empresa', 'Nivel de experiencia', 
               'Pais', 'Ciudad', 'Tamaño de la empresa', 'Tipo de ubicación de trabajo', 'Salario Minimo', 'Habilidades']
    tabla = []
    for i in range(0, total):
        if i < 5 or i >= total-5:
            tabla.append([i+1,
                        nf.getElement(lista,i)["published_at"],
                        nf.getElement(lista,i)["title"],
                        nf.getElement(lista,i)["company_name"],
                        nf.getElement(lista,i)["experience_level"],
                        nf.getElement(lista,i)["country_code"], 
                        nf.getElement(lista,i)["city"],
                        nf.getElement(lista,i)["company_size"],
                        nf.getElement(lista,i)["workplace_type"],
                        nf.getElement(lista,i)["salary"],
                        nf.getElement(lista,i)['skill']]
                     )
    print(tabulate(tabla, headers=headers, tablefmt="grid"))
        
    
    # TODO: Imprimir el resultado del requerimiento 2


def print_req_3(control, numero, pais, experticia):
    data_structs= control['model']
    total, lista= controller.req_3(data_structs, pais, experticia)
    print('El total de ofertas publicadas entre los salarios es de: ' + str(total))
    headers = ['Numero', 'Fecha de publicación','Título de la oferta', 'Nombre de la empresa', 'Nivel de experiencia', 
               'Pais', 'Ciudad', 'Tamaño de la empresa', 'Tipo de ubicación de trabajo', 'Salario Minimo', 'Habilidades']
    tabla = []
    for i in range(0, total):
        if i < numero:
            tabla.append([i+1,
                        nf.getElement(lista,i)["published_at"],
                        nf.getElement(lista,i)["title"],
                        nf.getElement(lista,i)["company_name"],
                        nf.getElement(lista,i)["experience_level"],
                        nf.getElement(lista,i)["country_code"], 
                        nf.getElement(lista,i)["city"],
                        nf.getElement(lista,i)["company_size"],
                        nf.getElement(lista,i)["workplace_type"],
                        nf.getElement(lista,i)["salary"],
                        nf.getElement(lista,i)['skill']]
                     )
    print(tabulate(tabla, headers=headers, tablefmt="grid"))


def print_req_4(control, numero, ciudad, ubicacion):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    data_structs = control['model']
    tamaño, lista = controller.req_4(data_structs, ciudad, ubicacion)
    print('El total de ofertas publicadas es de: ' + str(tamaño))
    headers = ['Numero', 'Fecha de publicación','Título de la oferta', 'Nombre de la empresa', 'Nivel de experiencia', 
               'Pais', 'Ciudad', 'Tamaño de la empresa', 'Tipo de ubicación de trabajo', 'Salario Minimo', 'Habilidades']
    tabla = []
    for i in range(0, tamaño):
        if i < numero:
            tabla.append([i+1,
                        nf.getElement(lista,i)["published_at"],
                        nf.getElement(lista,i)["title"],
                        nf.getElement(lista,i)["company_name"],
                        nf.getElement(lista,i)["experience_level"],
                        nf.getElement(lista,i)["country_code"], 
                        nf.getElement(lista,i)["city"],
                        nf.getElement(lista,i)["company_size"],
                        nf.getElement(lista,i)["workplace_type"],
                        nf.getElement(lista,i)["salary"],
                        nf.getElement(lista,i)['skill']]
                     )
    print(tabulate(tabla, headers=headers, tablefmt="grid"))

def print_req_5(control,n,tamanio_low,tamanio_high,habilidad,nivel_low,nivel_high):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    data_structs= control['model']
    r= controller.req_5(data_structs,n,tamanio_low,tamanio_high,habilidad,nivel_low,nivel_high)
    total_ofertas, tabla = r
    table_data, headers= tabla
    print('El numero de ofertas laborales publicadas para las compañías con un tamaño de entre {} y {} y que requieran {}: '.format(tamanio_low,tamanio_high,habilidad),total_ofertas )
    
    print(tabulate(table_data, headers=headers, tablefmt='fancygrid'))
    
def print_req_6(data_structs, n, initialDate, finalDate, salMin, salMax):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    data_structs = control['model']
    r = controller.req_6(data_structs, n, initialDate, finalDate, salMin, salMax)
    total_ofertas, total_ciudades, nciudades, ciudad, tabla= r
    para_tabular, headers= tabla

    print('El número de ofertas laborales publicadas entre las fechas y el salario solicitado son: ', total_ofertas )
    print('El número de ciudades que cumplen las especificaciones es de: ', total_ciudades)
    print('Las n ciudades que cumplen las especificaciones son: ', nciudades)
    print('Mostrando las ofertas de la ciudad: ', ciudad)
    print(tabulate(para_tabular, headers=headers, tablefmt='fancygrid'))

def print_req_7(control,anio,pais,conteo):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    data_structs= control['model']
    r= controller.req_7(data_structs,anio,pais,conteo)
    total_anio, total_histograma, minimo, maximo, lista, tabla= r
    para_tabular, headers= tabla
    llaves, frecuencias= lista
    
    print('El número de ofertas laborales publicadas en {} es de: '.format(anio),total_anio )
    print('El número de ofertas laborales publicadas utilizados para crear el histograma de {} es de: '.format(conteo),total_histograma)
    print('Para {} el minimo es {}, y el maximo es {}.'.format(conteo,minimo,maximo))
    
    #Tabulate
    print(tabulate(para_tabular, headers=headers, tablefmt='fancygrid'))
    
    if conteo!= 'habilidad':
        rotation= 0
    else: 
        rotation= 90
    
    #Diagrama de barras
    plt.bar(llaves, edgecolor='black', height=frecuencias)  
    plt.xlabel('Propiedad '+ conteo)
    plt.ylabel('Frecuencia')
    plt.title('Diagrama de '+ conteo)
    plt.grid(True)
    plt.xticks(rotation=rotation)
    plt.show()

def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    pass

def castBoolean(value):
    """
    Convierte un valor a booleano
    """
    if value in ('True', 'true', 'TRUE', 'T', 't', '1', 1, True):
        return True
    else:
        return False

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
            print("Cargando información de los archivos ....\n")
            mem = castBoolean(input("Desea observar el uso de memoria? (True/False): "))
            data = load_data(control,mem)
            print('Datos cargados: ' + str(controller.size_control(control)))
            print(data)
            print_data(control)
        elif int(inputs) == 2:
            initialDate= input('Fecha desde la cual quiere consultar ofertas: ')
            finalDate= input('Fecha hasta la cual quiere recibir ofertas: ')
            print_req_1(control, initialDate, finalDate)
        elif int(inputs) == 3:
            salario_min = int(input("Ingresar el salario minimo: "))
            salario_max = int(input("Ingresar el salario máximo: "))
            print_req_2(control, salario_min, salario_max)

        elif int(inputs) == 4:
            numero = int(input("Ingresar el número N de ofertas laborales a consultatar: "))
            pais = input("Ingresar el código del país de consulta: ")
            experticia = input("Ingresar el nivel de experticia: ")
            print_req_3(control, numero, pais, experticia)

        elif int(inputs) == 5:
            numero = int(input("Ingresar el número N de ofertas laborales a consultar: "))
            ciudad = input("Ingresar el nombre de una ciudad: ")
            ubicacion = input("Ingresar el tipo de ubicación: ")
            print_req_4(control, numero, ciudad, ubicacion)

        elif int(inputs) == 6:
            n= int(input('Ingrese el número (N) de ciudades s para consultar: '))
            tamanio_low = input('Ingrese el límite inferior del tamaño de la compañía: ')
            tamanio_high = input('El límite superior del tamaño de la compañía: ')
            habilidad = input('Nombre de la habilidad solicitada: ')
            nivel_low = input('El límite inferior del nivel de la habilidad: ')
            nivel_high = input('El límite superior del nivel de la habilidad: ')
            print_req_5(control,n,tamanio_low,tamanio_high,habilidad,nivel_low,nivel_high)

        elif int(inputs) == 7:
            numero = int(input("Ingresar el número N de ofertas laborales a consultar: "))
            initialDate= input('Fecha desde la cual quiere consultar ofertas: ')
            finalDate= input('Fecha hasta la cual quiere recibir ofertas: ')
            salMin = input("Ingresar el salario minimo: ")
            salMax = input("Ingresar el salario máximo: ")
            print_req_6(control, numero, initialDate, finalDate, salMin, salMax)

        elif int(inputs) == 8:
            anio=int(input('Ingrese el año del cual quiere conocer la informacion: '))
            pais=input('Ingrese el código del país para la consulta: ')
            conteo=input('Ingrese la propiedad de conteo (experticia, ubicación, o habilidad): ')
            print_req_7(control,anio,pais,conteo)

        elif int(inputs) == 9:
            print_req_8(control)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa")
        else:
            print("Opción errónea, vuelva a elegir.\n")
    threading.stack_size(67108864*2) # 128MB stack
    sys.setrecursionlimit(default_limit*1000000) 
    thread = threading.Thread(target=print_menu())
    thread.start()
    sys.exit(0)

