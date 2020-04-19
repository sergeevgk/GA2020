# -*- coding: utf-8 -*-


def n_char(a: str) -> int:
    for i in range(1, n + 1, 1): 
        if alphabet[i - 1] == a: return i 

def a_char(i: int) -> str:
    return alphabet[i - 1] 

def n_string(alpha: str) -> int:
    i = 0 
    for j in range(1, len(alpha) + 1, 1): 
        i = n * i + n_char(alpha[j - 1]) 
    return i 

def a_string(i: int) -> str:
    alpha = "" 
    a = "" 
    alpha = "" 
    while i > 0: 
        if i % n == 0: a = a_char(n); i = i - n 
        else: a = a_char(i % n) 
        alpha = a + alpha; i = i // n 
    return alpha 

