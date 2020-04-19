import random


def select(it):
    x = random.sample(it, 1)[0]
    it.remove(x)
    return x


class stack:
    arr: list

    def __init__(self):
        self.arr = []

    def push(self, x):
        self.arr.append(x)

    def pop(self):
        return self.arr.pop()

    def top(self):
        return self.arr[-1]

    def empty(self):
        return len(self.arr) == 0

    def clear(self):
        return self.arr.clear()


class queue:
    arr: list

    def __init__(self):
        self.arr = []

    def enqueue(self, x):
        self.arr.append(x)

    def dequeue(self):
        return self.arr.pop(0)

    def empty(self):
        return len(self.arr) == 0

    def clear(self):
        return self.arr.clear()


#  Обход графа в ширину
# Вход: граф Г(V, E), представленный списками смежности G.
# Выход: последовательность вершин обхода.
def BFS(G: list):
    T = queue() 
    V = set() 
    x = [None for _ in range(len(G) - 1 + 1)] 
    V = set(range(1, len(G) + 1)) 
    for v in V: x[v - 1] = 0  # вначале все вершины не отмечены
    v = select(V) # начало обхода — произвольная вершина
    T.enqueue(v) # помещаем v в структуру данных T...
    x[v - 1] = 1 # ... и отмечаем вершину v
    while True: 
        u = T.dequeue() # извлекаем вершину из структуры данных T...
        yield u # ... и возвращаем её в качестве очередной пройденной
        for w in G[u - 1]: 
            if x[w - 1] == 0: 
                T.enqueue(w) # помещаем w в структуру данных T...
                x[w - 1] = 1 # ... и отмечаем вершину w
        if T.empty(): break


#  Обход графа в глубину
# Вход: граф Г(V, E), представленный списками смежности G.
# Выход: последовательность вершин обхода.
def DFS(G: list):
    T = stack() 
    V = set() 
    x = [None for _ in range(len(G) - 1 + 1)] 
    V = set(range(1, len(G) + 1)) 
    for v in V: x[v - 1] = 0  # вначале все вершины не отмечены
    v = select(V) # начало обхода — произвольная вершина
    T.push(v) # помещаем v в структуру данных T...
    x[v - 1] = 1 # ... и отмечаем вершину v
    while True: 
        u = T.pop() # извлекаем вершину из структуры данных T...
        yield u # ... и возвращаем её в качестве очередной пройденной
        for w in G[u - 1]: 
            if x[w - 1] == 0: 
                T.push(w) # помещаем w в структуру данных T...
                x[w - 1] = 1 # ... и отмечаем вершину w
        if T.empty(): break


