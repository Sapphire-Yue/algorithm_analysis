# 演算法分析機測
# 學號: 11127101 / 11127103 / 11127126
# 姓名: 藍至奕 / 王芃穎 / 黃柏寧
# 中原大學資訊工程系

import copy

def pre_bfs(matrix, queue):
    """確定各位置是否能與箱子轉彎，不能轉彎的結構將被封住，並把整條死路給封住"""
    next = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    next_pos = set()
    for cur in queue:
        count = 0
        for i in next:
            # 如果有牆壁，需計算該位置的牆壁數量，若總和為 3 則代表該位置無法與箱子一同轉彎
            x = cur[0] + i[0]
            y = cur[1] + i[1]
            if x < 0 or y < 0 or x >= len(matrix) or y >= len(matrix[0]): 
                count += 1
                continue
            elif matrix[x][y] == '*' or matrix[x][y] == 'T' : 
                if matrix[x][y] == 'T':
                    # 若目標位置後面還有路徑可走，需繼續搜尋
                    for j in next:
                        x2 = x + j[0]
                        y2 = y + j[1]
                        if x2 < 0 or y2 < 0 or x2 >= len(matrix) or y2 >= len(matrix[0]): continue
                        elif matrix[x2][y2] == '.': next_pos.add((x2, y2))
                continue

            if matrix[x][y] == '#': #若遇到牆壁，計算數量
                count += 1
                continue
            
            if matrix[x][y] != 'S': matrix[x][y] = '*'  #該節點可走入
            next_pos.add((x, y))

        if count == 3 and matrix[cur[0]][cur[1]] == '*':
            matrix[cur[0]][cur[1]] = '.'    #封路結構
            

    if ( next_pos == set() ):
        return
    pre_bfs(matrix, next_pos)

    # 將整條死路給封住
    for cur in queue:
        count = 0
        for i in next:
            x = cur[0] + i[0]
            y = cur[1] + i[1]
            if x < 0 or y < 0 or x >= len(matrix) or y >= len(matrix[0]): 
                count += 1
                continue
            if matrix[x][y] == '#' or matrix[x][y] == '.': 
                count += 1
        if count != 3 or matrix[cur[0]][cur[1]] == 'S' or matrix[cur[0]][cur[1]] == 'B' or matrix[cur[0]][cur[1]] == 'T': continue
        matrix[cur[0]][cur[1]] = '.'



def find_next_step(matrix, index, end, route):
    """人在箱子可移動的下一步"""
    """若走到目標，則回傳路徑"""
    
    next = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    next_pos = set()
    get_target = False
    path = []

    for i in next:
        x = index[0] + i[0]
        y = index[1] + i[1]
        if x < 0 or y < 0 or x >= len(matrix) or y >= len(matrix[0]): continue
        
        if (x, y) == end:
            # 如果找到目標
            get_target = True
            path.append((x, y))
            route[x, y] = (index[0], index[1])
        elif matrix[x][y] != '.' and matrix[x][y] != 'S' and matrix[x][y] != 'T': continue
        else:
            next_pos.add((x, y))
            route[x, y] = (index[0], index[1])

    if get_target: return path
    return next_pos

def bfs(matrix, queue, end, count = 0, route = {}):
    """人在箱子可移動的最短路徑"""
    """若走到目標，則回傳路徑"""
    if not queue: return
    
    next_pos = set()
    path = []
    for cur in queue:
        matrix[cur[0]][cur[1]] = str(count)
        temp = find_next_step(matrix, cur, end, route)
        if type(temp) == list:  # 如果有找到目標
            path += temp
        else: next_pos.update(temp)

    road = []
    # 往前搜索，將整條路徑都找出來
    for p in path:
        temp = [p]
        while temp[-1] in route:
            temp.append(route[temp[-1]])
        temp.reverse()
        if road != [] and len(road[0]) > len(temp):
            road = []
            road.append(temp)
        elif road == []:
            road.append(temp)

    if len(road) > 0: return road
    elif len(next_pos) == 0: return
    return bfs(matrix, next_pos, end, count + 1, route)
    
def find_next_pos(matrix, index, route):
    """找尋箱子可移動的下一步"""
    next = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    next_pos = set()
    get_target = False
    path = []

    for i in next:
        x = index[0] + i[0]
        y = index[1] + i[1]
        if x < 0 or y < 0 or x >= len(matrix) or y >= len(matrix[0]): continue
        
        if matrix[x][y] == 'T':
            get_target = True
            path.append((x, y))
            route[x, y] = (index[0], index[1])
        elif matrix[x][y] != '.' and matrix[x][y] != 'S': continue
        elif matrix[x - 2 * i[0]][y - 2 * i[1]] != '#':
            # 如果推動的反方向位置不是牆壁
            next_pos.add((x, y))
            route[x, y] = (index[0], index[1])

    if get_target: return path
    return next_pos

def find_box_path(matrix, queue, count = 0, route = {}):
    """找尋箱子可移動的最短路徑"""
    if not queue: return
    
    next_pos = set()
    path = []
    for cur in queue:
        matrix[cur[0]][cur[1]] = str(count)
        temp = find_next_pos(matrix, cur, route)
        if type(temp) == list:  # 如果有找到目標
            path += temp
        else: next_pos.update(temp)

    road = []
    # 往前搜索，將整條路徑都找出來
    for p in path:
        temp = [p]
        while temp[-1] in route:
            temp.append(route[temp[-1]])
        temp.reverse()
        road.append(temp)    
    
    if len(road) > 0: return road
    return find_box_path(matrix, next_pos, count + 1)
    

def get_path(matrix, box_path, cur):
    """取得全程路徑"""
    path = []
    dirction = ()
    dictionary = dict()
    if len(dirction) == 0:
        dirction = (box_path[1][0] - box_path[0][0], box_path[1][1] - box_path[0][1])
    temp = bfs(copy.deepcopy(matrix), {cur}, (box_path[0][0] - dirction[0], box_path[0][1] - dirction[1]), route = dictionary)
    if temp == None :
        if cur != (box_path[0][0] - dirction[0], box_path[0][1] - dirction[1]):
            return
    else:
        path += temp
    
    
    before = box_path[0]
    path += {before}
    for p in box_path[1:]:
        dictionary = dict()
        if p[0] - before[0] != dirction[0] or p[1] - before[1] != dirction[1]:
            cur = (before[0] - dirction[0], before[1] - dirction[1])
            dirction = (p[0] - before[0], p[1] - before[1])
            # 如果方向改變了，則需要重新尋找路徑
            temp = bfs(copy.deepcopy(matrix), {cur}, (before[0] - dirction[0], before[1] - dirction[1]), route = dictionary)
            if temp == None:
                return
            path += temp + [before] + [p]
            matrix[before[0]][before[1]] = '.'
            matrix[p[0]][p[1]] = 'B'
        else:
            path += [p]
            matrix[before[0]][before[1]] = '.'
            matrix[p[0]][p[1]] = 'B'
        before = p

    return path

def transform_path(path):
    """將路徑轉換成輸出格式"""
    if path == None: return
    dirction_box = {(1, 0): 'S', (-1, 0): 'N', (0, 1): 'E', (0, -1): 'W'}
    dirction = {(1, 0): 's', (-1, 0): 'n', (0, 1): 'e', (0, -1): 'w'}
    result = []
    before = ()
    for p in path:
        if type(p) == tuple:
            if before == ():
                before = p
            else:
                result.append(dirction_box[(p[0] - before[0], p[1] - before[1])])
                before = p
        else:
            before = p[0]
            for i in p[1:]:
                result.append(dirction[(i[0] - before[0], i[1] - before[1])])
                before = i
            before = ()

    return result

r, c = map(int, input().split())
num = 0

while (r, c) != (0, 0):
    num += 1

    if ( r > 20 or r < 1 ) or ( c > 20 or c < 1 ):
        raise ValueError("Input ERROR")

    print("row:", r)
    print("column:", c)
    matrix = list()
    box_matrix = list()

    for i in range(r):
        s = list(input().strip())
        matrix.append(s)
        box_matrix.append(s.copy())

        if 'S' in s:
            start = (i, s.index('S'))
        if 'B' in s:
            box = (i, s.index('B'))

    original = copy.deepcopy(matrix)
    # 確定人是否能與箱子轉彎
    pre_bfs(matrix, {start})

    #將處理好的地圖作為箱子移動的地圖
    for i in range (0, r):
        for j in range (0, c):
            if matrix[i][j] == '.':
                box_matrix[i][j] = '#'

    box_path = find_box_path(box_matrix, {(box[0], box[1])})
    
    matrix = original

    #將處理好的地圖作為人移動的地圖
    for i in range (0, r):
        for j in range (0, c):
            if box_matrix[i][j] == '#' and original[i][j] != 'S':
                matrix[i][j] = '#'

    print("Maze #{}".format(num))
    if box_path == None:
        print("Impossible")

    else:
        result_path = []
        minimum_path = []

        for p in box_path:
            result_path.append(transform_path(get_path(copy.deepcopy(matrix), p, start)))
            if minimum_path == []:
                minimum_path = result_path[-1]
            elif len(minimum_path) > len(result_path[-1]):
                minimum_path = result_path[-1]

        for c in minimum_path:
            print(c, end = '')
        print()

    r, c = map(int, input().split())