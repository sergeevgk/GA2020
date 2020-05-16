

#  ��������� �������� �������� ��������� ������������ ��������� �� O(n^3) �����.
# ����: ������� ��������� R.
# �����: ������� ��������� T.
def Warshall(R: list) -> list:
    m = len(R) 
    T = [[None for _ in range(m - 1 + 1)] for _ in range(m - 1 + 1)] 
    T = R 
    for i in range(1, m + 1, 1): 
        for j in range(1, m + 1, 1): 
            for k in range(1, m + 1, 1): 
                T[j - 1][k - 1] = T[j - 1][k - 1] or T[j - 1][i - 1] and T[i - 1][k - 1] 
    return T 

