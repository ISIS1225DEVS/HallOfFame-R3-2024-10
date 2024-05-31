import math
def make_heah(n):
    return {'pq': [None for _ in range(n+1)], 'size': 1}

def insert(heap, elem):
    pass

def swim(heap, pos):
    #dada la posición de un elemento lo ordena ascendentemente
    parent = pos // 2
    if heap['pq'][parent] < heap['pq'][pos]:
        temp = heap['pq'][parent]
        heap['pq'][parent] = heap['pq'][pos]
        heap['hp'][pos] = temp
        swim(heap, parent)

def delete(heap):
    pass