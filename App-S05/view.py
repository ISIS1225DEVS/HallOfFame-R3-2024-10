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

import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.use('TkAgg') 

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


def load_data(control, muestra, mem):
    """
    Carga los datos
    """
    #TODO: Realizar la carga de datos
    
    answer = controller.load_data(control, muestra, memflag=mem)

    ofertas = answer[1]
    sizeof=lt.size(ofertas)
    
    tomaMemoriaTiempo=answer[0]
    
    if isinstance(tomaMemoriaTiempo, (list, tuple)) is True:
        print("Tiempo [ms]: ", f"{tomaMemoriaTiempo[0]:.3f}", "||",
              "Memoria [kB]: ", f"{tomaMemoriaTiempo[1]:.3f}")
    else:
        print("Tiempo [ms]: ", f"{tomaMemoriaTiempo:.3f}")
        
        
    print("Hay", sizeof, "ofertas publicadas.")


    if sizeof != 0: 
        final_primeros3=[0,0,0]
        i=0
        while i<3:
            temp={}
            for key in ofertas["elements"][i]:
                if key == "published_at" or key == "title" or key == "company_name" or key == "experience_level" or key == "country_code" or key == "city":
                  temp[key] = ofertas["elements"][i][key]

            final_primeros3[i]=temp
            i+=1
    
        final_ultimos3=[0,0,0]
        i=0
        while i<3:
            temp={}
            numjobs=sizeof
            for key in ofertas['elements'][numjobs-i-1]:
                if key == "published_at" or key == "title" or key == "company_name" or key == "experience_level" or key == "country_code" or key == "city":
                    temp[key]=ofertas['elements'][numjobs-i-1][key]

            final_ultimos3[i]=temp
            i+=1
                
        #Printing de las sublistas depuradas
        print("Los primeros tres son:")
        print("")
        table_primeros3 = tabulate(final_primeros3,headers='keys',tablefmt="fancy_outline")
        print(table_primeros3)
        print("")
    
        print("Los ultimos tres son:")
        print("")
        table_ultimos3 = tabulate(final_ultimos3,headers='keys',tablefmt="fancy_outline")
        print(table_ultimos3)
        print("")  
    pass


def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def print_req_1(control, memflag, fechai, fechaf):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1

    ofertas,timeMem = controller.req_1(control, memflag, fechai, fechaf)

    tomaMemoriaTiempo=timeMem
    if isinstance(tomaMemoriaTiempo, (list, tuple)) is True:
        print("Tiempo [ms]: ", f"{tomaMemoriaTiempo[0]:.3f}", "||",
              "Memoria [kB]: ", f"{tomaMemoriaTiempo[1]:.3f}")
    else:
        print("Tiempo [ms]: ", f"{tomaMemoriaTiempo:.3f}")

    
    sizeof=lt.size(ofertas)
    
    print("Hay", sizeof, "ofertas en ese rango de fechas.")


    if sizeof != 0: 
        final_primeros5=[0,0,0,0,0]
        i=0
        while i<5:
            temp={}
            for key in ofertas["elements"][i]:
                if key == "published_at" or key == "title" or key == "company_name" or key == "experience_level" or key == "country_code" or key == "city" or key == "company_size" or key == "workplace_type" or key == "skills_required":
                  temp[key] = ofertas["elements"][i][key]

            final_primeros5[i]=temp
            i+=1
    
        final_ultimos5=[0,0,0,0,0]
        i=0
        while i<5:
            temp={}
            numjobs=sizeof
            for key in ofertas['elements'][numjobs-i-1]:
                if key == "published_at" or key == "title" or key == "company_name" or key == "experience_level" or key == "country_code" or key == "city" or key == "company_size" or key == "workplace_type" or key == "skills_required":
                    temp[key]=ofertas['elements'][numjobs-i-1][key]

            final_ultimos5[i]=temp
            i+=1
                
        #Printing de las sublistas depuradas
        print("Los primeros cinco son:")
        print("")
        table_primeros5 = tabulate(final_primeros5,headers='keys',tablefmt="fancy_outline")
        print(table_primeros5)
        print("")
    
        print("Los ultimos cinco son:")
        print("")
        table_ultimos5 = tabulate(final_ultimos5,headers='keys',tablefmt="fancy_outline")
        print(table_ultimos5)
        print("")  




def print_req_2(control, memflag, salarioi, salariof):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2

    ofertas,timeMem = controller.req_2(control, memflag, salarioi, salariof)

    tomaMemoriaTiempo=timeMem
    if isinstance(tomaMemoriaTiempo, (list, tuple)) is True:
        print("Tiempo [ms]: ", f"{tomaMemoriaTiempo[0]:.3f}", "||",
              "Memoria [kB]: ", f"{tomaMemoriaTiempo[1]:.3f}")
    else:
        print("Tiempo [ms]: ", f"{tomaMemoriaTiempo:.3f}")

    
    sizeof=lt.size(ofertas)
    
    print("Hay", sizeof, "ofertas en ese rango de salarios.")


    if sizeof != 0: 
        final_primeros5=[0,0,0,0,0]
        i=0
        while i<5:
            temp={}
            for key in ofertas["elements"][i]:
                if key == "published_at" or key == "title" or key == "company_name" or key == "experience_level" or key == "country_code" or key == "city" or key == "company_size" or key == "workplace_type" or key == "salary_from" or key == "skills_required":
                  temp[key] = ofertas["elements"][i][key]

            final_primeros5[i]=temp
            i+=1
    
        final_ultimos5=[0,0,0,0,0]
        i=0
        while i<5:
            temp={}
            numjobs=sizeof
            for key in ofertas['elements'][numjobs-i-1]:
                if key == "published_at" or key == "title" or key == "company_name" or key == "experience_level" or key == "country_code" or key == "city" or key == "company_size" or key == "workplace_type" or key == "salary_from" or key == "skills_required":
                    temp[key]=ofertas['elements'][numjobs-i-1][key]

            final_ultimos5[i]=temp
            i+=1
                
        #Printing de las sublistas depuradas
        print("Los primeros cinco son:")
        print("")
        table_primeros5 = tabulate(final_primeros5,headers='keys',tablefmt="fancy_outline")
        print(table_primeros5)
        print("")
    
        print("Los ultimos cinco son:")
        print("")
        table_ultimos5 = tabulate(final_ultimos5,headers='keys',tablefmt="fancy_outline")
        print(table_ultimos5)
        print("")  



def print_req_3(control,memflag, N, country_code, experience_level):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """

    recent_jobs,timeMem = controller.req_3(control,memflag, N, country_code, experience_level)
    tomaMemoriaTiempo=timeMem
    if isinstance(tomaMemoriaTiempo, (list, tuple)) is True:
        print("Tiempo [ms]: ", f"{tomaMemoriaTiempo[0]:.3f}", "||",
              "Memoria [kB]: ", f"{tomaMemoriaTiempo[1]:.3f}")
    else:
        print("Tiempo [ms]: ", f"{tomaMemoriaTiempo:.3f}")


    print("Las N ofertas laborales publicadas más recientes que cumplan con las condiciones especificadas: ")

    keys = ['published_at', 'title', 'company_name', 'experience_level', 'country_code', 'city', 'company_size', 'workplace_type', 'salary_from', 'skills_required']

    # Filtrar las ofertas y recopilar la información necesaria
    filtered_offers = []
    for job in recent_jobs["elements"]:
        # Asegúrate de que 'job' es un diccionario antes de intentar usar .get()
        if isinstance(job, dict):
            filtered_job = {key: job.get(key, 'Desconocido') for key in keys}
            filtered_offers.append(filtered_job)
        else:
            # Manejar el caso en que 'job' no es un diccionario (puede que necesites ajustar esta parte)
            print("Un elemento de 'recent_jobs[\"elements\"]' no es un diccionario:", job)

    # Imprimir los resultados con tabulate
    print(tabulate(filtered_offers, headers='keys', tablefmt='fancy_outline'))

    # TODO: Imprimir el resultado del requerimiento 3



def print_req_4 (control, memflag, n, city, work_type):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4

    a,timeMem = controller.req_4(control, memflag, n, city, work_type)

    tomaMemoriaTiempo=timeMem
    if isinstance(tomaMemoriaTiempo, (list, tuple)) is True:
        print("Tiempo [ms]: ", f"{tomaMemoriaTiempo[0]:.3f}", "||",
              "Memoria [kB]: ", f"{tomaMemoriaTiempo[1]:.3f}")
    else:
        print("Tiempo [ms]: ", f"{tomaMemoriaTiempo:.3f}")

    ofertas = a[0]
    sizeof=lt.size(ofertas)
    print("Hay un total de",a[1],"ofertas de trabajo que cumplen los requisitos")
    

    if sizeof<10:
        tabla=[]
        for job in lt.iterator(ofertas):
            temp={}
            for key in job:
                if (key=="title" or key=="company_name" or key=="company_size" or key=="workplace_type" or key=="published_at" 
                    or key=="salary_from" or key=="city" or key == "experience_level" or key == "country_code" or key == "skills_required"):
                    temp[key]=job[key]
            tabla.append(temp.copy())
            
        tabla_imp = tabulate(tabla,headers='keys',tablefmt="fancy_outline")
        print("")
        print(tabla_imp)
        print("")

    else:
        final_primeros5=[0,0,0,0,0]
        i=1
        while i<6:
            temp={}
            for key in lt.getElement(ofertas, i) :
                if (key=="title" or key=="company_name" or key=="company_size" or key=="workplace_type" or key=="published_at" 
                    or key=="salary_from" or key=="city" or key == "experience_level" or key == "country_code" or key == "skills_required"):
                    temp[key]=lt.getElement(ofertas, i)[key]

            final_primeros5[i-1]=temp
            i+=1

        final_ultimos5=[0,0,0,0,0]
        i=0
        while i<5:
            temp={}
            numjobs = lt.size(ofertas)
            for key in lt.getElement(ofertas, numjobs-i) :
                if (key=="title" or key=="company_name" or key=="company_size" or key=="workplace_type" or key=="published_at" 
                    or key=="salary_from" or key=="city" or key == "experience_level" or key == "country_code" or key == "skills_required"):
                    temp[key]=lt.getElement(ofertas,numjobs-i)[key]

            final_ultimos5[i]=temp
            i+=1    
        

        print("Los primeros cinco son:")
        print("")
        table_primeros5 = tabulate(final_primeros5,headers='keys',tablefmt="fancy_outline")
        print(table_primeros5)
        print("")
        
        print("Los ultimos cinco son:")
        print("")
        table_ultimos5 = tabulate(final_ultimos5,headers='keys',tablefmt="fancy_outline")
        print(table_ultimos5)
        print("") 


    
    
    pass


def print_req_5(control, memflag, numOfertas, minCompSize, maxCompSize, skill, minSkillLev, maxSkillLev):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    
    answer=controller.req_5(control, memflag, numOfertas, minCompSize, maxCompSize, skill, minSkillLev, maxSkillLev)
    ans=answer[0]
    tomaMemoriaTiempo=answer[1]
    
    if isinstance(tomaMemoriaTiempo, (list, tuple)) is True:
        print("Tiempo [ms]: ", f"{tomaMemoriaTiempo[0]:.3f}", "||",
              "Memoria [kB]: ", f"{tomaMemoriaTiempo[1]:.3f}")
    else:
        print("Tiempo [ms]: ", f"{tomaMemoriaTiempo:.3f}")
        
    if lt.size(ans[0])<10:
        tabla=[]
        for job in lt.iterator(ans[0]):
            temp={}
            for key in job:
                if (key=="title" or key=="company_name" or key=="company_size" or key=="workplace_type" or key=="published_at" 
                    or key=="salary_from" or key=="city" or key == "experience_level" or key == "country_code" or key == "skills_required"):
                    temp[key]=job[key]
            tabla.append(temp.copy())
            
        tabla_imp = tabulate(tabla,headers='keys',tablefmt="fancy_outline")
        print("")
        print(tabla_imp)
        print("")

    else:
        final_primeros5=[0,0,0,0,0]
        i=1
        while i<6:
            temp={}
            for key in lt.getElement(ans[0], i) :
                if (key=="title" or key=="company_name" or key=="company_size" or key=="workplace_type" or key=="published_at" 
                    or key=="salary_from" or key=="city" or key == "experience_level" or key == "country_code" or key == "skills_required"):
                    temp[key]=lt.getElement(ans[0], i)[key]

            final_primeros5[i-1]=temp
            i+=1

        final_ultimos5=[0,0,0,0,0]
        i=0
        while i<5:
            temp={}
            numjobs = lt.size(ans[0])
            for key in lt.getElement(ans[0], numjobs-i) :
                if (key=="title" or key=="company_name" or key=="company_size" or key=="workplace_type" or key=="published_at" 
                    or key=="salary_from" or key=="city" or key == "experience_level" or key == "country_code" or key == "skills_required"):
                    temp[key]=lt.getElement(ans[0],numjobs-i)[key]

            final_ultimos5[i]=temp
            i+=1    
        

        print("Los primeros cinco son:")
        print("")
        table_primeros5 = tabulate(final_primeros5,headers='keys',tablefmt="fancy_outline")
        print(table_primeros5)
        print("")
        
        print("Los ultimos cinco son:")
        print("")
        table_ultimos5 = tabulate(final_ultimos5,headers='keys',tablefmt="fancy_outline")
        print(table_ultimos5)
        print("") 


    print("Hay un total de",ans[1],"ofertas de trabajo que cumplen los requisitos")
    
    pass


def print_req_6(control,memflag,N, start_date, end_date, min_salary, max_salary):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """

    answer = controller.req_6(control,memflag, N, start_date, end_date, min_salary, max_salary)
    tomaMemoriaTiempo=answer[1]

    if isinstance(tomaMemoriaTiempo, (list, tuple)) is True:
        print("Tiempo [ms]: ", f"{tomaMemoriaTiempo[0]:.3f}", "||",
              "Memoria [kB]: ", f"{tomaMemoriaTiempo[1]:.3f}")
    else:
        print("Tiempo [ms]: ", f"{tomaMemoriaTiempo:.3f}")

    ans=answer[0]
  
    total_offers=ans[0]
    top_cities=ans[1]
    top_city_details=ans[2]
    num_ciudades=ans[3]



    # Imprimir el número total de ofertas
    print(f"Número total de ofertas laborales publicadas: {total_offers}\n")
    
    # Imprimir el número de ciudades que cumplen con las especificaciones
    print("Número total de ciudades que cumplen con las especificaciones: ",str(num_ciudades))
    
    # Formatear y imprimir las N ciudades con más ofertas laborales publicadas
    cities_table = [[city, count] for city, count in lt.iterator(top_cities)]
    print(f"Las N ciudades que cumplen con las condiciones especificadas ordenadas alfabéticamente:")
    print(tabulate(cities_table, headers=["Ciudad", "Cantidad de Ofertas"], tablefmt="fancy_outline"))
    
    # Imprimir detalles de la ciudad con más ofertas
    if top_city_details:
        offers_table = []
        for offer in lt.iterator(top_city_details):
            offers_table.append({
                "Fecha de publicación": offer.get("published_at", ""),
                "Título": offer.get("title", ""),
                "Empresa": offer.get("company_name", ""),
                "Nivel de experiencia": offer.get("experience_level", ""),
                "País": offer.get("country_code", ""),
                "Ciudad de la empresa": offer.get("city", ""),
                "Tamaño de la empresa": offer.get("company_size", ""),
                "Tipo de ubicación": offer.get("workplace_type", ""),
                "Salario mínimo": offer.get("salary_from", ""),
                "Habilidades": offer.get("skills_required", "")
            })
        print(f"Detalles de la ciudad con la mayor cantidad de ofertas laborales publicadas:")
        print(tabulate(offers_table, headers="keys", tablefmt="fancy_outline"))


def print_req_7(control, memflag, year, pais, propiedad):
    """
        Función que imprime la solución del Requerimiento 7 en consola
        
    answer=[[numJobsYear, numJobsGrafica, infoGrafica, maxValue, minValue, jobsList], tomas de tiempo y mem]
    """
    
    # TODO: Imprimir el resultado del requerimiento 7
    
    answer=controller.req_7(control, memflag, year, pais, propiedad)
    ans=answer[0]
    tomaMemoriaTiempo=answer[1]
    
    if propiedad=="experticia":
        keyPropiedad="experience_level"
    elif propiedad=="ubicacion":
        keyPropiedad="workplace_type"
    else:
        keyPropiedad="skills_required"
    
    if isinstance(tomaMemoriaTiempo, (list, tuple)) is True:
        print("Tiempo [ms]: ", f"{tomaMemoriaTiempo[0]:.3f}", "||",
              "Memoria [kB]: ", f"{tomaMemoriaTiempo[1]:.3f}")
    else:
        print("Tiempo [ms]: ", f"{tomaMemoriaTiempo:.3f}")
        
    if lt.size(ans[5])<10:
        tabla=[]
        for job in lt.iterator(ans[5]):
            temp={}
            for key in job:
                if (key=="title" or key=="company_name" or key=="company_size" or key=="workplace_type" or key=="published_at" 
                    or key=="salary_from" or key==keyPropiedad or key=="city"):
                    temp[key]=job[key]
            tabla.append(temp.copy())
            
        tabla_imp = tabulate(tabla,headers='keys',tablefmt="fancy_outline")
        print("")
        print(tabla_imp)
        print("")

    else:
        final_primeros5=[0,0,0,0,0]
        i=0
        while i<5:
            temp={}
            for key in ans[5]['elements'][i]:
                if (key=="title" or key=="company_name" or key=="company_size" or key=="workplace_type" or key=="published_at" 
                    or key=="salary_from" or key==keyPropiedad or key=="city"):
                    temp[key]=ans[5]['elements'][i][key]

            final_primeros5[i]=temp
            i+=1

        final_ultimos5=[0,0,0,0,0]
        i=0
        while i<5:
            temp={}
            numjobs = ans[1] 
            for key in ans[5]['elements'][numjobs-i-1]:
                if (key=="title" or key=="company_name" or key=="company_size" or key=="country_code" or key=="published_at" or
                    key=="salary_from" or  key==keyPropiedad or key=="city"):
                    temp[key]=ans[5]['elements'][numjobs-i-1][key]

            final_ultimos5[i]=temp
            i+=1    
        

        print("Los primeros cinco son:")
        print("")
        table_primeros5 = tabulate(final_primeros5,headers='keys',tablefmt="fancy_outline")
        print(table_primeros5)
        print("")
        
        print("Los ultimos cinco son:")
        print("")
        table_ultimos5 = tabulate(final_ultimos5,headers='keys',tablefmt="fancy_outline")
        print(table_ultimos5)
        print("") 


    print("Hay un total de",ans[0],"ofertas de trabajo en el año", year)
    print("Hay un total de",ans[1],"ofertas de trabajo en el gráfico ")
    
    print("La propiedad con menor valor fue",ans[4])
    print("La propiedad con mayor valor fue",ans[3])
    
    infoGrafica=ans[2]
    
    
    # getting values against each value of y
    plt.barh(infoGrafica[0], infoGrafica[1], color="purple")
    
    # setting label of y-axis
    plt.ylabel(infoGrafica[2])
    
    # setting label of x-axis
    plt.xlabel("Número de ofertas") 
    plt.title(infoGrafica[3])
    plt.show()
    
    # Show Plot
    plt.show()
    
    print("")
    
    
    pass


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
            muestra=input("Digite el tamaño de la muetra: ")
            memflag=input("Desea observar uso de la memoria? ")
            memflag=castBoolean(memflag)
            print("Cargando información de los archivos ....\n")
            data = load_data(control, muestra, memflag)
            
        elif int(inputs) == 2:
            datei = input("Ingrese la fecha mínima (forma a-m-d): ")
            datef = input("Ingrese la fecha máxima (forma a-m-d): ")
            memflag=input("Desea observar uso de la memoria? ")
            memflag=castBoolean(memflag)
            print_req_1(control, memflag, datei, datef)

        elif int(inputs) == 3:
            salarioi = input("Ingrese el límite inferior del salario mínimo: ")
            salariof = input("Ingrese el límite superior del salario mínimo: ")
            memflag=input("Desea observar uso de la memoria? ")
            memflag=castBoolean(memflag)
            print_req_2(control, memflag, salarioi, salariof)

        elif int(inputs) == 4:

            N=int(input("ingrese el número de ofertas publicadas más recientes: "))
            country_code=input("ingrese el código del país para la consulta (ej.: PL, CO, ES, etc): ")
            experience_level= input("Nivel de experticia de las ofertas de interés (junior, mid, senior, indiferente:")
            memflag=input("Desea observar uso de la memoria? ")
            memflag=castBoolean(memflag)
            print_req_3(control,memflag,N, country_code, experience_level)

        elif int(inputs) == 5:
            n = input("N ofertas más recientes que desea conocer: ")
            city = input("Ciudad de las ofertas: ")
            work_type = input("Tipo de ubicación del tabajo (remote, partly_remote, office): ")
            memflag=input("Desea observar uso de la memoria? ")
            memflag=castBoolean(memflag)
            print_req_4(control, memflag, n, city, work_type)

        elif int(inputs) == 6:
            numOfertas=int(input("Digite el número de ofertas: "))
            minCompSize=input("Digite el tamaño mínimo de la compañía: ")
            maxCompSize=input("Digite el tamaño máximo de la compañía: ")
            skill=input("Digite el nombre de la habilidad: ")
            minSkillLev=input("Digite el nivel mínimo de la habilidad: ")
            maxSkillLev=input("Digite el nivel máximo de la habilidad: ")
            memflag=input("Desea observar uso de la memoria? ")
            memflag=castBoolean(memflag)
            print_req_5(control, memflag, numOfertas, minCompSize, maxCompSize, skill, minSkillLev, maxSkillLev)


        elif int(inputs) == 7:
            N=int(input("Digite el número de ciudades: "))
            start_date=input("Digite la fecha de inicio: ")
            end_date=input("Digite la fecha final: ")
            min_salary=input("Digite el salario mínimo: ")
            max_salary=input("Digite el salario máximo: ")
            memflag=input("Desea observar uso de la memoria? ")
            memflag=castBoolean(memflag)
            print_req_6(control,memflag,N, start_date, end_date, min_salary, max_salary)

        elif int(inputs) == 8:
            year=input("Digite el año que busca: ")
            pais=input("Digite el país que busca: ")
            propiedad=input("Digite la propiedad que busca (ubicacion, experticia o habilidad): ")
            memflag=input("Desea observar uso de la memoria? ")
            memflag=castBoolean(memflag)
            print_req_7(control, memflag, year, pais, propiedad)
            

        elif int(inputs) == 9:
            print_req_8(control)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa")
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
