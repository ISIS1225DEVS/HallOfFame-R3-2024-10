import New_Functions as nf

def create_vacio():
    return {'info': {'root': None, 'left':None, 'right': None}, 'size': 0}

def create(elem):
    bst = {'info': {'root': elem, 'left':create_vacio(), 'right': create_vacio()}, 'size': 1}
    return bst

def tamanio(bst):
    if bst['info']['root'] == None:
        return 0
    else:
        return bst['size']    

def is_empty(bst):
    return bst['info']['root'] == None

def add(bst, elem): # elem esta en la forma elem= {"key": 2, "valor": "asd"}
    if is_empty(bst):
        return create(elem)
    if elem["key"] < bst['info']['root']["key"]:
        bst['info']['left'] = add(bst['info']['left'], elem)
    elif elem["key"] > bst['info']['root']["key"]:
        bst['info']['right'] = add(bst['info']['right'], elem)
    else:
        bst['info']['root'] == elem
    
    leftsize = tamanio(bst['info']['left'])
    rightsize = tamanio(bst['info']['right'])
    bst['size'] = 1 + leftsize + rightsize
    
    return bst

def is_leaf(bst):
    return is_empty(bst['info']['left']) and is_empty(bst['info']['right']) and bst['info']['root'] != None

def height(bst): #aprobado
    #max{left, right} + 1
    if is_empty(bst):
        return 0
    elif is_leaf(bst):
        return 0
    else:
        return max(height(bst['info']['left']), height(bst['info']['right'])) + 1
    
def balanced(bst):
    if is_empty(bst):
        return True
    elif is_leaf(bst):
        return True
    else:
        hl = height(bst['info']['left'])
        hr = height(bst['info']['right'])
        diff = abs(hl - hr)
        return balanced(bst['info']['left']) and balanced(bst['info']['right']) and diff <= 1
    
    
def delete(bst, elem):
    #manera complicada
    #más facil es eliminar el valor, y agregar todos los valores otra vez
    if is_leaf(bst['info']['left']) and bst['info']['left']['root'] == elem:
        bst['info']['left'] = create_vacio()
    elif is_leaf(bst['info']['right'])  and bst['info']['right']['root'] == elem:
        bst['info']['right'] = create_vacio()
    elif bst['info']['left']['root'] == elem:
        bst['info']['left'] = create_vacio()
    elif bst['info']['right']['root'] == elem:
        bst['info']['right'] = create_vacio()
    
def posorder(bst):
    def posorden(bst, l):
        if is_empty(bst):
            return []
        else:
            posorden(bst['info']['left'], l)
            posorden(bst['info']['right'], l)
            l.append(bst['info']['root'])
    l = []
    posorden(bst, l)
    return l

#bst = create({"key": 1, "valor": "asd"})
#bst = add(bst,{"key": 2, "valor": "asd"})
#bst = add(bst,{"key": 3, "valor": "asd"})

def preorder(bst):
    def preorden(bst, l):
        if is_empty(bst):
            return
        else:
            l.append(bst['info']['root'])
            preorden(bst['info']['left'], l)
            preorden(bst['info']['right'], l)
    l = []
    preorden(bst, l)
    return l

def inorder(bst):
    #lista con todos los elementos
    #no esta terminado
    def inorden(bst, l):
        if is_empty(bst):
            return []
        else: 
            inorden(bst['info']['left'], l)
            l.append(bst['info']['root'])
            inorden(bst['info']['right'], l)
    l=[]
    inorden(bst, l)
    return l

def keys_range(bst, key_low, key_high, lista, cmpfunction):  
    if bst['info']['root']!= None:
        complo = cmpfunction(key_low, bst['info']['root']['key'])
        comphi = cmpfunction(key_high, bst['info']['root']['key'])

        if (complo < 0):
            keys_range(bst['info']['left'], key_low, key_high, lista, cmpfunction)
        if ((complo <= 0) and (comphi >= 0)):
            nf.addLast(lista, bst['info']['root']['value'])
        if (comphi > 0):
            keys_range(bst['info']['right'], key_low, key_high, lista, cmpfunction)
    return lista

def keys(bst, key_lo, key_high, cmpfunction):
    lista= nf.newList()
    if not is_empty(bst):
        keys_range(bst, key_lo, key_high, lista, cmpfunction)
    return lista
    

def get(bst, key):
    root = bst['info']['root']
    node = None
    if root != None:
        if root['key'] != None:
            if str(root['key']) == str(key):
                node = root
            elif root['key'] > key:
                node = get(bst['info']['left'], key)
            else:
                node = get(bst['info']['right'], key)
    return node #node esta en la forma {"key": blahh, "valor": blahhh}

def getValue(node):
    return node['valor']

def getKey(node):
    return node['key']

def size(bst):
    return bst['size']

def minKey(bst):
    min = None
    if (bst['info']['root']['key'] is not None):
        if (bst['info']['left']['info']['root'] is None):
            min = bst['info']['root']
        else:
            min = minKey(bst['info']['left'])
    return min #esto da ['key] y ['value']

def maxKey(bst):
    max = None
    if (bst['info']['root']['key'] is not None):
        if (bst['info']['right']['info']['root'] is None):
            max = bst['info']['root']
        else:
            max = maxKey(bst['info']['right'])
    return max #lo mismo que con el max

def algo(a, b):
    if (a == b):
        return 0
    elif (a > b):
        return 1
    else:
        return -1
    
#bst = create_vacio()
#bst = add(bst, {'key': 1, "value": "a"})
#bst = add(bst, {'key': -2, "value": "a"})
#bst = add(bst, {'key': 5, "value": "a"})
#bst = add(bst, {'key': -10, "value": "a"})
#print(bst)