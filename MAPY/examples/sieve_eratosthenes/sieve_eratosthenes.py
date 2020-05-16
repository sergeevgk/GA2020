

#  ��� ���������� ��������� ������� �����, �� ������������� ������� ����� n,
#  ���������� ������� ������, ���������� ������� ����������.
# ����: ����������� ����� n > 1.
# �����: ��������� ������� �����, �� ������������� n.
def Eratosthenes(n: int):
    B = set() 
    B = set(range(2, n + 1)) 
    while bool(B): 
        x = min(B) # ���������� ������� B
        yield x # ������ x
        B = B.difference({x}) # ������� x �� B
        y = x ** 2 
        while y <= n: 
            B = B.difference({y}); y = y + x # ������� �� B ��� �����, ������� x

