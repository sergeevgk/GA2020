import math



class heap:
    arr: list
    len: int


#  Восстановление свойства кучи
# Вход: куча A, индекс i.
# Выход: восстанавливается свойство кучи в поддереве с корнем A[i], причём левое и правое поддеревья имеют свойства кучи.
def Heapify(A: heap, i: int):
    l = 2 * i; r = 2 * i + 1; m = i # инициализация
    if (l <= A.len) and (A.arr[l - 1] > A.arr[i - 1]): 
        m = l 
    if (r <= A.len) and (A.arr[r - 1] > A.arr[m - 1]): 
        m = r 
    if i != m: 
        A.arr[i - 1], A.arr[m - 1] = A.arr[m - 1], A.arr[i - 1] # транспозиция элементов массива
        Heapify(A, m) 


#  Построение кучи
# Вход: куча A
# Выход: устанавливается свойство кучи в дереве, заданным массивом A.arr
def MakeHeap(A: heap):
    for i in range(math.floor(A.len / 2), 1 + -1, -1): Heapify(A, i) 


#  Изменение значения элемента кучи
# Вход: куча A, индекс изменяемого элемента i, новое значение k.
# Выход: значение элемента с индексом i изменяется на k без нарушения свойств двоичной кучи.
def IncElt(A: heap, i: int, k: float):
    if k < A.arr[i - 1]: 
        raise Exception("fail") # новое значение не должно быть меньше
    A.arr[i - 1] = k 
    while (i > 1) and (A.arr[math.floor(i / 2) - 1] < A.arr[i - 1]): 
        A.arr[i - 1], A.arr[math.floor(i / 2) - 1] = A.arr[math.floor(i / 2) - 1], A.arr[i - 1] # транспозиция элементов
        i = math.floor(i / 2) 


#  Вставка нового элемента в кучу
# Вход: куча A, новый элемент k.
# Выход: в кучу добавляется элемент со значением k без нарушения свойств двоичной кучи.
def InsElt(A: heap, k: float):
    if A.len == len(A.arr): 
        raise Exception("fail") #  весь массив заполнен
    A.len = A.len + 1 
    A.arr[A.len - 1] = -float("inf") 
    IncElt(A, A.len, k) 


#  Извлечение максимального элемента из кучи
# Вход: куча A
# Выход: извлечение максимального элемента из кучи с сохранением свойств двоичной кучи
def GetMax(A: heap) -> float:
    if A.len == 0: raise Exception("fail")  # куча пуста
    m = A.arr[1 - 1] # сохранение значения корневого элемента
    A.arr[1 - 1] = A.arr[A.len - 1] # копирование последнего элемента в корень дерева
    A.len = A.len - 1 # уменьшение длины массива
    Heapify(A, 1) 
    return m 

