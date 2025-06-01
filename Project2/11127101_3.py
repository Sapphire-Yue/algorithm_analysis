# 演算法分析機測
# 學號: 11127101 / 11127103 / 11127126
# 姓名: 藍至奕 / 王芃穎 / 黃柏寧
# 中原大學資訊工程系

from collections import deque

N = 8  # 棋盤大小

# 移動方式：8 個方向
moves = [(-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1)]

def chess_to_index(pos): # 將棋盤座標 ("a1") 轉換成 (row, col)
    col = ord(pos[0]) - ord('a') # 字母 a~h -> 欄位 index 0~7
    row = int(pos[1]) - 1 # 數字 1~8 -> 列 index 0~7
    return (row, col)
 
def findShortestPath(start, end): # 計算最短步數(BFS)
    visited = [[False] * N for _ in range(N)] # 建立一個 8x8 的 visited 二維陣列，初始都為 False
    queue = deque() # 使用 deque 來建立 BFS 用的 queue
    queue.append((start[0], start[1], 0))  # (row, col, steps)
    visited[start[0]][start[1]] = True

    while queue:
        x, y, steps = queue.popleft() # 取出目前位置和走的步數
        if (x, y) == end: return steps # 到達目標位置，回傳步數
        
        for dx, dy in moves:  # 走向騎士能移動的 8 種方向
            nx, ny = x + dx, y + dy
            if 0 <= nx < N and 0 <= ny < N and not visited[nx][ny]:
                visited[nx][ny] = True # 標記為已拜訪
                queue.append((nx, ny, steps + 1))  # 加入新位置，步數 + 1

def main():
    allInput = [] # 用來儲存所有的測資
    results = [] # 記錄所有輸出結果

    while True:
        line = input().strip()
        if line == "0 0": break
        allInput.append(line)

    for line in allInput:
        start_str, end_str = line.split() # 取得起點及終點
        # 轉換為座標
        start = chess_to_index(start_str) 
        end = chess_to_index(end_str)
        steps = findShortestPath(start, end) # 計算最短步數
        results.append(f"From {start_str} to {end_str}, Knight Moves = {steps}")

    for res in results:
        print(res)

main()