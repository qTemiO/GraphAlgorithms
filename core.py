import math
from typing import Iterator

from loguru import logger

def getWorshellCol(iteration, rows, matrix):
    WC = []
    #print('DEBUG: Iteration - ' + str(iteration))
    for i in range(rows):
        #print(matrix[i][iteration])
        WC.append(matrix[i][iteration])
    return WC 
    
def getWorshelRowIndex(WC, Index):
    # Если стартуем, то чекаем с самого начала
    if Index == -1:
        NewIndex = WC.index(1)
        return NewIndex
    # Если уже не стартуем, а например знаем что в 0 или где-то ещё есть 1
    else:
        # Смотрим со следующего, т.к в питоне нумерация с нуля, чтобы не попасть в петлю делаем +1
        NewIndex = WC[Index + 1:].index(1)
        # Если он находит следующий элемент еденицей - возвращаем его номер в общем списке
        if NewIndex == 0:
            return Index + 1
        # Если там ещё есть элементы, то выкидываем ему до этого элемента +1, т.к брали с +1 погрешностью
        else:
            return Index + NewIndex + 1

def getWorshellMatrix(matrix, rows, cols):
    MatrixShape = (rows, cols)
    changedMatrix = 0
    for i in range(MatrixShape[0]):
        #Определяю итерационные столбцы и строки
        WorshellRow = matrix[i]
        WorshellCol = getWorshellCol(i, rows, matrix)
        print("Current summing row is - " + str(WorshellRow) + '\n')
        SummerBag = []
        
        #Проверяю есть ли 1 в столбце итерации
        if 1 in WorshellCol:
            checker = True
            # Здесь индекс -1 чтобы обозначить старт проверки
            Index = -1
            while checker:
                # Использую функцию получения индекса строки с 1
                Index = getWorshelRowIndex(WorshellCol, Index)
                #print('Matrix row with 1 ' + str(matrix[Index]))
                
                # Добавляю в датасет индекс строки в которой нашлась еденица и саму строку
                
                SummerBag.append({
                    'row': matrix[Index],
                    'index': Index,
                })
                # Если дальше едениц нету, то прекращяем проверку
                if 1 not in WorshellCol[Index+1:]: checker = False
        
        
        print("-- Iteration "+ str(i+1) + " SummerBag: --")
        
        #Вывожу результаты сверки
        for data in SummerBag:
            print('Index of row with 1: ' + str(data['index'] + 1))
            print('Row: ' + str(data['row']))
            
            indx = 0
            newRow = []
            # Прохожусь по всем числам в строке итерации и в строке где нашел едiницу, если случайно получаю 1+1 делаю их сумму 1
            for num in matrix[data['index']]:
                if (num + WorshellRow[indx]) >= 1:
                    newRow.append(1)
                elif (num + WorshellRow[indx]) == 0:
                    newRow.append(0)
                indx += 1
                
            
            matrix[data['index']] = newRow
            print('New Row, updated: ' + str(newRow) + '\n')
        print('\n')
        
    print('Program end!')
    return matrix

def getChoisePoints(matrix, position):
    points = []
    index = 0
    for element in matrix[position]:
        if element != 0:
            points.append(index) 
        index += 1 
    return points

def getBellmanMatrix(matrix, rows, cols, startPoint):
    totalIterations = rows

    distance = []
    for iterations in range(totalIterations):
        distance.append(math.inf)
    distance[startPoint - 1] = 0

    theWay = []

    currentPosition = startPoint - 1

    for iteration in range(totalIterations):
        
        theWay.append(currentPosition)
        print(f'Current position  - {currentPosition}')

        connectiblePoints = getChoisePoints(matrix, currentPosition)
        
        print(f'Points with this position - {connectiblePoints}')

        for point in connectiblePoints:
            if distance[point] > distance[currentPosition] + matrix[currentPosition][point]:
                distance[point] = distance[currentPosition] + matrix[currentPosition][point]

        minimalIndex = getMinimalIndex(distance, theWay)
        if minimalIndex == -1:
            for i in range(rows):
                if i not in theWay:
                    if distance[i] == math.inf:
                        logger.warning('List ended')
        else: 
            currentPosition = minimalIndex
            
    return distance

def getFloydMatrix(matrix, rows, cols):
    current_matrix = matrix
    for row in range(rows):
        for col in range(cols):
            if current_matrix[row][col] == 0 and row != col:
                current_matrix[row][col] = math.inf

    totalIterations = rows
    for iteration in range(totalIterations):
        new_matrix = []
        for row in range(rows):
            row_list = []
            for col in range(cols):
                if current_matrix[row][col] > current_matrix[row][iteration] + current_matrix[iteration][col]:
                    row_list.append(current_matrix[row][iteration] + current_matrix[iteration][col])
                else:
                    row_list.append(current_matrix[row][col])
            new_matrix.append(row_list)
        current_matrix = new_matrix

    floydMatrix = current_matrix
    return floydMatrix

def getMinimalIndex(distance, theWay):
    
    index = 0
    minimal = math.inf
    minimalIndex = -1
    for dist in distance:
        if (dist < minimal) and (index not in theWay): 
            minimal = dist
            minimalIndex = index
        index += 1

    return minimalIndex        

def getDextraWay(matrix, rows, cols, startPoint):
    totalIterations = rows

    distance = []
    pointsPath = []
    for iterations in range(totalIterations):
        distance.append(math.inf)
        pointsPath.append(str(''))

    pointsPath[startPoint - 1] = '0'
    distance[startPoint - 1] = 0
    
    theWay = []

    currentPosition = startPoint - 1

    for iteration in range(totalIterations):
        theWay.append(currentPosition)
        print(f'Current position  - {currentPosition}')

        connectiblePoints = getChoisePoints(matrix, currentPosition)
        
        print(f'Points with this position - {connectiblePoints}')

        for point in connectiblePoints:
            if distance[point] > distance[currentPosition] + matrix[currentPosition][point]:
                distance[point] = distance[currentPosition] + matrix[currentPosition][point]
                pointsPath[point] = f'{ pointsPath[currentPosition] }{ point }'


        minimalIndex = getMinimalIndex(distance, theWay)
        if minimalIndex == -1:
            for i in range(rows):
                if i not in theWay:
                    if distance[i] == math.inf:
                        logger.warning('List ended')
        else: 
            currentPosition = minimalIndex
        
    for row in range(rows):
        logger.warning(matrix[row])

    print('\n')
    updated_point_path = []
    for point in pointsPath:
        point_path = ''
        for edge in point:
            point_path += f'{int(edge) + 1}'
        updated_point_path.append(point_path)

    return distance, theWay, updated_point_path
        
