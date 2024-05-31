def newList(type = "ARRAY_LIST", cmpfunction=None):
    if type == "ARRAY_LIST":
        lista = {'elements': [],
               'size': 0,
               'type': 'ARRAY_LIST',
               'cmpfunction': cmpfunction}    
    elif type == "SINGLE_LINKED":
        lista = {'first': None,
                'last': None,
                'size': 0,
                'type': 'SINGLE_LINKED',
                'cmpfunction': cmpfunction}    
    return lista

def newNode(elemento):
    node = {'info': elemento, 'next': None}
    return node

def addLast(lista, elemento):
    if lista['type'] == 'ARRAY_LIST':
        lista['elements'].append(elemento)
        lista['size'] += 1
    elif lista['type'] == 'SINGLE_LINKED':
        new_node = newNode(elemento)
        if lista['size'] == 0:
            lista['first'] = new_node
        else:
            lista['last']['next'] = new_node
        lista['last'] = new_node
        lista['size'] += 1
        
def addFirst(lista, elemento):
    if lista['type'] == 'ARRAY_LIST':
        lista['elements'].insert(0, elemento)
        lista['size'] += 1
    elif lista['type'] == 'SINGLE_LINKED':
        node = newNode(elemento)
        node['next'] = lista['first']
        lista['first'] = node
        if (lista['size'] == 0):
            lista['last'] = lista['first']
        lista['size'] += 1
        return lista
   
        
def get_size(lista):
    return lista['size']

def is_empty(lista):
    if lista['size'] == 0:
        return True
    else:
        return False
        
def isPresent(lista, elemento, criterio="ignorar"):
    if lista["type"] == "ARRAY_LIST":
        for i in range(0, get_size(lista)):
            if criterio == "ignorar" and lista["elements"][i] == elemento:
                return i
            elif criterio == "ignorar" and lista["elements"][i] != elemento:
                i = i
            elif lista["elements"][i][criterio] == elemento:
                return i
        return None
    elif type == "SINGLE_LINKED":
        actual = lista["first"]
        while actual != None:
            if actual[criterio] == elemento:
                return actual
            actual = actual["next"]
        return None   
    
def changeInfo(lista, pos, newinfo):
    if lista["type"] == "ARRAY_LIST":
        lista['elements'][pos] = newinfo
    elif lista["types"] == "SINGLE_LINKED":
        current = lista['first']
        cont = 1
        while cont < pos:
            current = current['next']
            cont += 1
        current['info'] = newinfo
    return lista

def get_first(lista):
    if lista['type'] == "ARRAY_LIST":
        return lista['elements'][0]
    elif lista['type'] == "SINGLE_LINKED":
        node = lista['first']
        return node['info']

def iterator(lista):
    if lista['type'] == "SINGLE_LINKED":
        if(lista != None):
          current = lista['first']
          while current != None:
            yield current['info']
            current = current['next']
    elif lista['type'] == "ARRAY_LIST":
        for posicion in range(0, lista['size']):
                yield lista['elements'][posicion]

def delete(lista, item):
    if lista['type'] == "ARRAY_LIST":
        for i in range(0, lista['size']):
            if lista['elements'][i] == item:
                lista['elements'].pop(i)
                lista['size'] -= 1
                break
    return lista
"""
    elif lista['type'] == "SINGLE_LINKED":
        node = lista['first']
        previo = lista['first']
        contador = 1
        if (pos == 1):
            lista['first'] = lista['first']['next']
            lista['size'] -= 1
        elif(pos > 1):
            while contador < pos:
                contador += 1
                previo = node
                node = node['next']
            previo['next'] = node['next']
            lista['size'] -= 1"""

def exchange(lista, pos1, pos2):
    info1 = getElement(lista, pos1)
    info2 = getElement(lista, pos2)
    changeInfo(lista, pos1, info2)
    changeInfo(lista, pos2, info1)
    
def subList(lista, pos, numeroElementos):
    if lista['type'] == "ARRAY_LIST":
        sublista = {'elements': [],
                  'size': 0,
                  'type': 'ARRAY_LIST'}
        elemento = pos-1
        contador = 1
        while contador <= numeroElementos and elemento < get_size(lista):
            sublista['elements'].append(lista['elements'][elemento])
            sublista['size'] += 1
            elemento += 1
            contador += 1
        return sublista
    elif lista['type'] == "SINGLE_LINKED":
        sublista = {'first': None,
                  'last': None,
                  'size': 0,
                  'type': 'SINGLE_LINKED'}
        contador = 1
        fijo = pos
        while contador <= numeroElementos:
            elem = getElement(lista, fijo)
            addLast(sublista, elem)
            fijo += 1
            contador += 1
        return sublista
    
def changeInfo(lista, pos, newinfo):
    if lista["type"] == "ARRAY_LIST":
        lista['elements'][pos] = newinfo
    elif lista["type"] == "SINGLE_LINKED":
        cont = 0
        act = lista["first"]
        while cont < pos:
            cont+=1
            act = act["next"]
        act['info']= newinfo        
    
def getElement(lista, pos):
    if lista['type'] == "ARRAY_LIST":
        return lista["elements"][pos]
    elif lista['type'] == "SINGLE_LINKED":
        valor = lista['first']
        count = 0
        while count < pos:
            count += 1
            valor = valor['next']
        return valor['info']
    
def getFirst(lista):
    if lista['type'] == "ARRAY_LIST":
        return lista['elements'][0]
    elif lista['type'] == "SINGLE_LINKED":
        node = lista['first']
        return node['info']
    
def concatenate(list1, list2):
    if list1['type'] == "ARRAY_LIST":
        list1['elements'].extend(list2['elements'])
        list1['size'] += list2['size']
        return list1
    elif list1['type'] == "SINGLE_LINKED":
        if list1['first'] is None:
            list1['first'] = list2['first']
        else:
            current = list1['first']
            while current['next'] is not None:
                current = current['next']
            current['next'] = list2['first']
        list1['size'] += list2['size']
        return list1

def first_last(lista):
    if lista['type'] == 'ARRAY_LIST':
        first = lista['elements'][:5]
        last = lista['elements'][get_size(lista)-5:get_size(lista)]
        firstlast=newList()
        for i in first:
            addLast(firstlast,i)
        for i in last:
            addLast(firstlast,i)
    return firstlast

def extend(lista1, lista2): #mismo que concatenate porque se me olvido que ya lo había hecho
    suma1 = lista1['elements']
    suma2 = lista2['elements']
    total = suma1.extend(suma2)
    lista = {'elements': total,
               'size': lista1['size'] + lista2['size'],
               'type': 'ARRAY_LIST',
               'cmpfunction': None} 
    return lista

def inverse(lista):
    lista['elements'] = lista['elements'][::-1]
    return lista

def find_min(lista):
    min_value = float('inf')
    for elemento in iterator(lista):
        if elemento < min_value:
            min_value = elemento
    return min_value

def find_max(lista):
    max_value = float('-inf')
    for elemento in iterator(lista):
        if elemento > max_value:
            max_value = elemento  
    return max_value
