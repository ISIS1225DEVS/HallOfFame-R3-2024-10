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
import time
import matplotlib.pyplot as plt
import numpy as np

import matplotlib as mpl
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
    return controller.new_controller()


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


def load_data(control, file_size):
    """
    Carga los datos
    """
    data = controller.load_data(control, file_size)
    
    
    
    
    size = data["size"]
    
    print(f"\nSe cargaron exitosamente {size} ofertas de trabajo")
    print("\nLas 3 mas recientes y mas antiguos son las siguientes: ")
    print(tabulate(lt.iterator(data), headers="keys"))
    
    


def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def print_req_1(lista):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    data = lista
    
    
    size = data["size"]
    
    print(f"\nSe cargaron exitosamente {size} ofertas de trabajo")
    print("\nLas 3 mas recientes y mas antiguos son las siguientes: ")
    print(tabulate(lt.iterator(data), headers="keys"))
    

def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    pass


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    pass


def print_req_4(tabulador,tamanio,n,tiempo):
    print(f"Dados estos criterios se encontraron {tamanio} ofertas de las cuales las {n} mas recientes son las siguintes")
    print(tabulate(tabulador, headers="keys"))
    print(f"Se ejecuto en {tiempo} segudnos")


def print_req_5(lista):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    data = lista
    
    
    size = data["size"]
    
    print(f"\nSe cargaron exitosamente {size} ofertas de trabajo")
    print("\nLas 3 mas recientes y 3 ultimas son las siguientes: ")
    print(tabulate(lt.iterator(data), headers="keys"))
    

def print_req_6(numero, cantidad_ofertas, cantidad_ciudades,lista_de_ciudades,lista_ofertas_max_ciudad, max_ciudad ):
    print('Las ciudades que encajan con los criterios son: ')
    if lt.size(lista_de_ciudades)> numero:
        for i in range(numero):
            city = lt.getElement(lista_de_ciudades, i+1)
            print(city)
    else:
        for ciudad in lt.iterator(lista_de_ciudades):
            print(ciudad)
    dato = lista_ofertas_max_ciudad
    print("Hay una cantidad de  "+ str(cantidad_ofertas)+ " y un total de " +str(cantidad_ciudades)+ " ciudades")
    print('El numero de ciudades son '+ str(cantidad_ciudades))
    print('La ciudad con mayor de ofertas es: ' +max_ciudad)
    print('Las ofertas de '+ max_ciudad +' es: ')
    print(tabulate(lt.iterator(dato), headers="keys"))


def print_req_7(control):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    pass


def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    pass


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
            
            size_file = input("De la base de datos de qué tamaño quieres los datos? \n")
            
            #cargar datos con tiempo
            t1 = time.time()
            print("Cargando información de los archivos ....\n")
            load_data(control, size_file)
            t2 = time.time()
            
            tiempo = t2-t1
            print(f"\n\nEl tiempo de carga fue {tiempo:.3f} segundos")
            #primeros,ultimos=controller.primer_ultimo(control)
            
        elif int(inputs) == 2:
            keylo = input('Ingrese fecha inicial')
            keyhi = input('Ingrese fecha final')
            size, lista = controller.req_1(control, keylo, keyhi)
            print_req_1(lista)
            print('El numero de ofertas encontradas es: '+ str(size))

        elif int(inputs) == 3:
            print_req_2(control)

        elif int(inputs) == 4:
            print_req_3(control)

        elif int(inputs) == 5:
            n=input("¿Cuantas ofertas desea consultar? ")
            ciudad=input("¿Para cual ciudad? ")
            continuar=True
            print("1- Remote")
            print('2- Partly Remote')
            print('3- Office')
            ubi=int(input('Seleccione un tipo de ubicacion de trabajo '))
            time1=time.time()
            if ubi==1:
                ubi='remote'
            elif ubi==2:
                ubi='partly_remote'
            elif ubi==3:
                ubi='office'
            else:
                print("Opcion Invalida")
                continuar=False
            if continuar:
                retorno,tamanio=controller.req_4(control,n,ciudad,ubi)
            tabulador=lt.iterator(retorno)
            time2=time.time()
            tiempo=time2-time1
            print_req_4(tabulador,tamanio,n,tiempo)
                

        elif int(inputs) == 6:
            keylo4 = input('Ingrese tamano inicial: ')
            keyhi4 = input('Ingrese tamano final: ')
            skill = input('Ingrese habilidad deseada: ')
            keylo_skill = input('Ingrese nivel minimo: ')
            keyhi_skill = input('Ingrese nivel maximo: ')
            
            peso, lista, size = controller.req_5(control, keylo4, keyhi4, skill, keylo_skill,keyhi_skill)
            #print_req_5(lista)
            print_req_5(lista)
            print('El total de ofertas es: '+ str(peso))
            

        elif int(inputs) == 7:
            fecha1 = input('Ingrese fecha inicial: ')
            fecha2 = input('Ingrese fecha final: ')
            salmin = input('Ingrese salario minimo (usd): ')
            salmax = input('Ingrese salario maixmo (usd): ')
            numero = input('Cantidad de ciudad que quieras consultar: ')
            cantidad_ofertas, cantidad_ciudades,lista_de_ciudades,lista_ofertas_max_ciudad, max_ciudad = controller.req_6(control, fecha1,fecha2,salmin, salmax)
            print_req_6(int(numero), cantidad_ofertas, cantidad_ciudades,lista_de_ciudades,lista_ofertas_max_ciudad, max_ciudad )

        elif int(inputs) == 8:
            anio=input("Ingrese que año desea evaluar: ")
            pais=input("¿Que pais desea evaluar? ")
            continuar=True
            print("1- Experticie")
            print('2- Ubicacion de Trabajo')
            print('3- Habilidad')
            critint=int(input('Seleccione un tipo de ubicacion de trabajo '))
            t1=time.time()
            if critint==1:
                crit='experience_level'
            elif critint==2:
                crit='workplace_type'
            elif critint==3:
                crit='skill'
            else:
                print("Opcion Invalida")
                continuar=False
            if continuar:
                if critint<3:
                    header,values,tamanio,maxi,maxim,mini,minim,ofertas=controller.req7noskill(control,anio,pais,crit)
                else:
                    header,values,tamanio,maxi,maxim,mini,minim,ofertas=controller.req7skill(control,anio,pais)
            header=list(lt.iterator(header))
            values=list(lt.iterator(values))
            plt.bar(header, values)
            plt.xlabel(crit)
            plt.ylabel('Catntidad')
            plt.title(f"Cantidad de ofertas en {anio} con criterio de {crit} ")
            t2=time.time()
            plt.show()
            e1=f"Bajo estos criterios se encontraron {tamanio} ofertas. "
            e2=f"La menor categoria es {minim} con {mini} ofertas. "
            e3=f"La mayor categoria es {maxim} con {maxi} ofertas. "
            print(e1)
            print(e2)
            print(e3)
            print(tabulate(ofertas, headers="keys"))
            print(t2-t1)
            
                

        elif int(inputs) == 9:
            print_req_8(control)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa")
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)

