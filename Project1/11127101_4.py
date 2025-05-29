# 演算法分析機測
# 學號: 11127101 / 11127103 / 11127126
# 姓名: 藍至奕 / 王芃穎 / 黃柏寧
# 中原大學資訊工程系

import time
from collections import deque # 實作的queue

def search(r, c, visited, label, graph, R, C): # 使用BFS尋找
        q = deque() # 一個雙向佇列
        q.append((r, c))
        visited[r][c] = label
        size = 1
 
        while q: # 只要還有點在 queue 裡
            x, y = q.popleft() # 取出第一個點
            # 尋找相鄰及相連的點(上、下、左、右、左上、左下、右上、右下), x軸: 垂直，y軸: 水平
            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < R and 0 <= ny < C:
                    #點沒走過且值為1，代表相連(鄰)
                    if graph[nx][ny] == 1 and visited[nx][ny] == 0:
                        visited[nx][ny] = label
                        q.append((nx, ny)) # 加到queue裡
                        size += 1
        return size

def findAllConnectedComponent(graph, R, C): # 找出所有連通元
    visited = [[0] * C for _ in range(R)] # 初始化紀錄哪些點已走過的list
    label = 1 # 第幾組連通元
    component_sizes = [] # 記錄這張圖的各個連通元的面積

    for i in range(R):
        for j in range(C):
            if graph[i][j] == 1 and visited[i][j] == 0: # 目前的點值為1且還沒走過
                size = search(i, j, visited, label, graph, R, C)
                component_sizes.append(size)
                label += 1

    return component_sizes

def main():
    allResults = [] # 儲存全部圖片的結果
    eachResult = [] # 儲存一張圖的總結果
    graph = [] # 儲存圖的像素值
    graphNum = 1 # 目前第幾張圖

    while True:
        #start_time = time.time()
        try:
            line = input().strip()
            if not line: continue

            R, C = map(int, line.split())

            if R == 0 and C == 0: break
            # 初始化
            eachResult.clear() 
            graph.clear()

            for i in range(R): # 讀取二值影像的每一列資料，並轉換成數字組成的二維陣列
                row = input().strip()

                #錯誤檢查
                if len(row) != C: raise ValueError(f"第 {i+1} 列長度錯誤，應為 {C} 行但實際為 {len(row)} 行")
                if not all(c in '01' for c in row): raise ValueError(f"第 {i+1} 列包含無效字元，僅允許 0 或 1: {row}")

                graph.append([int(c) for c in row]) # ex: 字串"00011"轉成[0, 0, 0, 1, 1]
                #graph.append(list(map(int, list(row))))

            # sizes: 儲存一張圖裡面，各個連通元的面積
            sizes = findAllConnectedComponent(graph, R, C)
            
            if graphNum > 1: eachResult.append(f"\nImage #{graphNum}")
            else: eachResult.append(f"Image #{graphNum}")

            eachResult.append(f"Number of Connected Components = {len(sizes)}")

            # 每個連通元的編號和它的面積
            # enumerate(sizes, 1): 會同時回傳idx(從1開始)及size: 
            for idx, size in enumerate(sizes, 1):
                eachResult.append(f"Connected Component #{idx} Area = {size}")
            
            allResults.append('\n'.join(eachResult))
            graphNum += 1

        except EOFError:
            break

    print("\n".join(allResults))
    '''total_time = round(time.time() - start_time, 3)
    print(f"\n所花時間: {total_time}秒")'''

main()