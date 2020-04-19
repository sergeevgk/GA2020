


#  возвращает все элементы из X \cap Y
# ¬ход: множества X и Y
def intersection(X: set, Y: set):
    for x in X: 
        for y in Y: 
            if x == y: 
                yield x #  возвращаем x
                break 

