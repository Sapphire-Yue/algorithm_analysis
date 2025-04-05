# 演算法分析機測
# 學號: 11127101/11127103/11127126
# 姓名: 藍至奕/王芃穎/黃柏寧
# 中原大學資訊工程系

import time

def waterJugPuzzle(aCapacity, bCapacity, target):
    visited = set()
    queue = [(0, 0, [])]  # (A水量, B水量, 步驟list)
    
    while queue:
        curA, curB, steps = queue.pop(0)
        
        # 如果B的水量已等於target，則return所有的步驟並加上Success
        if curB == target:
            return steps + ["Success"]
        
        # 如果當前的A、B水量已走過，則直接找下一組
        if (curA, curB) in visited:
            continue
        visited.add((curA, curB))
        
        # 將A填滿
        queue.append((aCapacity, curB, steps + ["Fill A"]))
        # 將B填滿
        queue.append((curA, bCapacity, steps + ["Fill B"]))
        # 將A倒光
        queue.append((0, curB, steps + ["Empty A"]))
        # 將B倒光
        queue.append((curA, 0, steps + ["Empty B"]))
        # 把A的水倒給B
        pour = min(curA, bCapacity - curB)
        queue.append((curA - pour, curB + pour, steps + ["Pour A B"]))
        # 把B的水倒給A
        pour = min(curB, aCapacity - curA)
        queue.append((curA + pour, curB - pour, steps + ["Pour B A"]))
    
    return ["No solution"]

def main():
    case_num = 1
    # 讀取輸入，並處理多組測資
    while True:
        aCapacity, bCapacity, target = map(int, input().split())
        if aCapacity == 0 and bCapacity == 0 and target == 0:
            break

        print(f"Case #{case_num}")
        for step in waterJugPuzzle(aCapacity, bCapacity, target):
            print(step)

        print()
        case_num += 1

if __name__ == "__main__":
    main()
