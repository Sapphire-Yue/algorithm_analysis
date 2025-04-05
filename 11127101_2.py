<<<<<<< HEAD
# 演算法分析機測
# 學號: 11127101/11127103/11127126
# 姓名: 藍至奕/王芃穎/黃柏寧
# 中原大學資訊工程系

import time

def findHamiltonianCycle(graph, path, visited, start, vertexNum):
    # 如果已經visited所有的vertex
    if len(path) == vertexNum:
        # 如果最後一個走到的vertex有在起點的adjacent中
        if path[-1] in graph[start]:
            # 輸出結果
            for vertex in path + [start]:
                print(vertex, end=" ")
            return True
        
        return False

    for neighbor in graph[path[-1]]:
        if not visited[neighbor]:
            visited[neighbor] = True
            path.append(neighbor)

            if findHamiltonianCycle(graph, path, visited, start, vertexNum):
                return True  # 找到hamiltonian cycle後就return回去main
            
            # backtrack
            visited[neighbor] = False
            path.pop()

    return False

def main():
    # 讀取輸入
    while True:
        num1, num2 = map(int, input().split())
        if num1 == 0 and num2 == 0:
            break
        else:
            vertexNum = num1
            edgeNum = num2

        # 創建每個vertex的adjacency list
        graph = {}
        for i in range(1, vertexNum + 1):
            graph[i] = []

        # 讀取所有的邊
        for i in range(edgeNum):
            u, v = map(int, input().split())
            graph[u].append(v)
            graph[v].append(u)


    # 從vertex 1開始找hamiltonian cycle
    visited = {}
    for i in range(1, vertexNum + 1):
        visited[i] = False

    visited[1] = True
    if not findHamiltonianCycle(graph, [1], visited, 1, vertexNum):
        print("No Hamiltonian Cycle")


if __name__ == "__main__":
    main()
=======
# 演算法分析機測
# 學號: 11127101/11127103/11127126
# 姓名: 藍至奕/王芃穎/黃柏寧
# 中原大學資訊工程系

import time

def findHamiltonianCycle(graph, path, visited, start, vertexNum):
    # 如果已經visited所有的vertex
    if len(path) == vertexNum:
        # 如果最後一個走到的vertex有在起點的adjacent中
        if path[-1] in graph[start]:
            # 輸出結果
            for vertex in path + [start]:
                print(vertex, end=" ")
            return True
        
        return False

    for neighbor in graph[path[-1]]:
        if not visited[neighbor]:
            visited[neighbor] = True
            path.append(neighbor)

            if findHamiltonianCycle(graph, path, visited, start, vertexNum):
                return True  # 找到hamiltonian cycle後就return回去main
            
            # backtrack
            visited[neighbor] = False
            path.pop()

    return False

def main():
    # 讀取輸入
    while True:
        num1, num2 = map(int, input().split())
        if num1 == 0 and num2 == 0:
            break
        else:
            vertexNum = num1
            edgeNum = num2

        # 創建每個vertex的adjacency list
        graph = {}
        for i in range(1, vertexNum + 1):
            graph[i] = []

        # 讀取所有的邊
        for i in range(edgeNum):
            u, v = map(int, input().split())
            graph[u].append(v)
            graph[v].append(u)


    # 從vertex 1開始找hamiltonian cycle
    visited = {}
    for i in range(1, vertexNum + 1):
        visited[i] = False

    visited[1] = True
    if not findHamiltonianCycle(graph, [1], visited, 1, vertexNum):
        print("No Hamiltonian Cycle")


if __name__ == "__main__":
    main()
>>>>>>> fd95d8deddb4da90bcd726d6b18afbad11eb1254
