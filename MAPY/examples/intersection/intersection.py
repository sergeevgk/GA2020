


#  ���������� ��� �������� �� X \cap Y
# ����: ��������� X � Y
def intersection(X: set, Y: set):
    for x in X: 
        for y in Y: 
            if x == y: 
                yield x #  ���������� x
                break 

