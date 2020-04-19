# -*- coding: utf-8 -*-
import math



class heap:
    arr: list
    len: int


#  �������������� �������� ����
# ����: ���� A, ������ i.
# �����: ����������������� �������� ���� � ��������� � ������ A[i], ������ ����� � ������ ���������� ����� �������� ����.
def Heapify(A: heap, i: int):
    l = 2 * i; r = 2 * i + 1; m = i # �������������
    if (l <= A.len) and (A.arr[l - 1] > A.arr[i - 1]):
        m = l
    if (r <= A.len) and (A.arr[r - 1] > A.arr[m - 1]):
        m = r
    if i != m:
        A.arr[i - 1], A.arr[m - 1] = A.arr[m - 1], A.arr[i - 1] # ������������ ��������� �������
        Heapify(A, m)


#  ���������� ����
# ����: ���� A
# �����: ��������������� �������� ���� � ������, �������� �������� A.arr
def MakeHeap(A: heap):
    for i in range(math.floor(A.len / 2), 1 + -1, -1): Heapify(A, i)


#  ��������� �������� �������� ����
# ����: ���� A, ������ ����������� �������� i, ����� �������� k.
# �����: �������� �������� � �������� i ���������� �� k ��� ��������� ������� �������� ����.
def IncElt(A: heap, i: int, k: float):
    if k < A.arr[i - 1]:
        raise Exception("fail") # ����� �������� �� ������ ���� ������
    A.arr[i - 1] = k
    while (i > 1) and (A.arr[math.floor(i / 2) - 1] < A.arr[i - 1]):
        A.arr[i - 1], A.arr[math.floor(i / 2) - 1] = A.arr[math.floor(i / 2) - 1], A.arr[i - 1] # ������������ ���������
        i = math.floor(i / 2)


#  ������� ������ �������� � ����
# ����: ���� A, ����� ������� k.
# �����: � ���� ����������� ������� �� ��������� k ��� ��������� ������� �������� ����.
def InsElt(A: heap, k: float):
    if A.len == len(A.arr):
        raise Exception("fail") #  ���� ������ ��������
    A.len = A.len + 1
    A.arr[A.len - 1] = -float("inf")
    IncElt(A, A.len, k)


#  ���������� ������������� �������� �� ����
# ����: ���� A
# �����: ���������� ������������� �������� �� ���� � ����������� ������� �������� ����
def GetMax(A: heap) -> float:
    if A.len == 0: raise Exception("fail")  # ���� �����
    m = A.arr[1 - 1] # ���������� �������� ��������� ��������
    A.arr[1 - 1] = A.arr[A.len - 1] # ����������� ���������� �������� � ������ ������
    A.len = A.len - 1 # ���������� ����� �������
    Heapify(A, 1)
    return m

