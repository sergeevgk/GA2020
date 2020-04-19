# -*- coding: utf-8 -*-


#  Следующий алгоритм Уоршалла вычисляет транзитивное замыкание за O(n^3) шагов.
# Вход: матрица отношения R.
# Выход: матрица замыкания T.
def Warshall(R: list) -> list:
    m = len(R) 
    T = [[None for _ in range(m - 1 + 1)] for _ in range(m - 1 + 1)] 
    T = R 
    for i in range(1, m + 1, 1): 
        for j in range(1, m + 1, 1): 
            for k in range(1, m + 1, 1): 
                T[j - 1][k - 1] = T[j - 1][k - 1] or T[j - 1][i - 1] and T[i - 1][k - 1] 
    return T 

