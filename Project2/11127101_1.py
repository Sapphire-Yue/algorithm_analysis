# 演算法分析機測
# 學號: 11127101 / 11127103 / 11127126
# 姓名: 藍至奕 / 王芃穎 / 黃柏寧
# 中原大學資訊工程系

def knapsack(W, n, items):
    # 讓物品從編號1開始操作，item[0]: weight, item[1]: values
    weights = [0] + [item[0] for item in items]
    values = [0] + [item[1] for item in items]

    # 建立一個 (n+1) x (W+1) 的二維陣列，dp[0][w]: 不選任何物品時的最大值，dp[i][0]: 背包容量為 0
    dp = [[0] * (W + 1) for _ in range(n + 1)] 

    # 計算
    for i in range(1, n + 1):
        for w in range(W + 1):
            if weights[i] <= w: dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weights[i]] + values[i])
            else: dp[i][w] = dp[i - 1][w]

    # 取得選取項目
    taken = []
    w = W
    # 如果 dp[i][w] != dp[i-1][w]，代表從 dp[i-1][w - weights[i]] + values[i] 選進來，加入該物品編號 i，然後扣掉該物品重量 weights[i]，繼續往前回推
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            taken.append(i)
            w -= weights[i]

    taken.sort() # 排序
    return dp[n][W], taken

def main():
    while True:
        W = int(input()) # 總重量
        if W == 0: break

        n = int(input()) # 物品數量
        items = []
        for _ in range(n): # 讀入物品數量 n，並建立一個 list(items) 存每個物品的weight跟value
            w, v = map(int, input().split())
            items.append((w, v))

        totalValue, takenItems = knapsack(W, n, items)
        print(f"Total Value = {totalValue}")
        print("Take Items", ", ".join(map(str, takenItems)))

main()