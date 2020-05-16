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


#  ����� ����� � ������
# ����: ���� �(V, E), �������������� �������� ��������� G.
# �����: ������������������ ������ ������.
def BFS(G: list):
    T = queue() 
    V = set() 
    x = [None for _ in range(len(G) - 1 + 1)] 
    V = set(range(1, len(G) + 1)) 
    for v in V: x[v - 1] = 0  # ������� ��� ������� �� ��������
    v = select(V) # ������ ������ � ������������ �������
    T.enqueue(v) # �������� v � ��������� ������ T...
    x[v - 1] = 1 # ... � �������� ������� v
    while True: 
        u = T.dequeue() # ��������� ������� �� ��������� ������ T...
        yield u # ... � ���������� � � �������� ��������� ����������
        for w in G[u - 1]: 
            if x[w - 1] == 0: 
                T.enqueue(w) # �������� w � ��������� ������ T...
                x[w - 1] = 1 # ... � �������� ������� w
        if T.empty(): break


#  ����� ����� � �������
# ����: ���� �(V, E), �������������� �������� ��������� G.
# �����: ������������������ ������ ������.
def DFS(G: list):
    T = stack() 
    V = set() 
    x = [None for _ in range(len(G) - 1 + 1)] 
    V = set(range(1, len(G) + 1)) 
    for v in V: x[v - 1] = 0  # ������� ��� ������� �� ��������
    v = select(V) # ������ ������ � ������������ �������
    T.push(v) # �������� v � ��������� ������ T...
    x[v - 1] = 1 # ... � �������� ������� v
    while True: 
        u = T.pop() # ��������� ������� �� ��������� ������ T...
        yield u # ... � ���������� � � �������� ��������� ����������
        for w in G[u - 1]: 
            if x[w - 1] == 0: 
                T.push(w) # �������� w � ��������� ������ T...
                x[w - 1] = 1 # ... � �������� ������� w
        if T.empty(): break


