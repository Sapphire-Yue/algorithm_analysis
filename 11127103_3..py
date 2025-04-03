# 演算法分析機測
# 學號: 11127101/11127103/11127126
# 姓名: 藍至奕/王芃穎/黃柏寧
# 中原大學資訊工程系

import time
from collections import deque

def waterJugPuzzle(a, b, target):
    visited = set()
    queue = deque([(0, 0, [])])  # (A水量, B水量, 步驟list)
    
    while queue:
        ca, cb, steps = queue.popleft()
        
        if cb == target:
            return steps + ["Success"]
        
        if (ca, cb) in visited:
            continue
        visited.add((ca, cb))
        
        # Fill A
        queue.append((a, cb, steps + ["Fill A"]))
        # Fill B
        queue.append((ca, b, steps + ["Fill B"]))
        # Empty A
        queue.append((0, cb, steps + ["Empty A"]))
        # Empty B
        queue.append((ca, 0, steps + ["Empty B"]))
        # Pour A -> B
        pour = min(ca, b - cb)
        queue.append((ca - pour, cb + pour, steps + ["Pour A B"]))
        # Pour B -> A
        pour = min(cb, a - ca)
        queue.append((ca + pour, cb - pour, steps + ["Pour B A"]))
    
    return ["No solution"]

# 讀取輸入並處理多組測試資料
def main():
    case_num = 1
    while True:
        print("input A, B and Target: ", end = "")
        a, b, target = map(int, input().split())
        if a == 0 and b == 0 and target == 0:
            break

        start_time = time.time()

        print(f"Case #{case_num}")
        for step in waterJugPuzzle(a, b, target):
            print(step)

        total_time = time.time() - start_time 
        print("running time: ", total_time)

        print()
        case_num += 1

if __name__ == "__main__":
    main()
