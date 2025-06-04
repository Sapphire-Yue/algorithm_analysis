import cv2
import numpy as np

def compute_cost(patch1, patch2):
    diff = patch1.astype(np.int32) - patch2.astype(np.int32)
    return np.sqrt(np.sum(diff**2, axis=2))

def find_min_seam(cost):
    H, W = cost.shape
    dp = cost.copy()                     # dp[i,j] = 到 (i,j) 的最小累積誤差
    backtrack = np.zeros_like(dp, int)   # 記錄最佳前驅

    # 從第二列開始累積
    for i in range(1, H):
        for j in range(W):
            candidates = [j] # 新增可從中上下來
            if j > 0:      candidates.append(j-1) # 從左上下來
            if j < W-1:    candidates.append(j+1) # 從右上下來
            best_prev = min(candidates, key=lambda x: dp[i-1, x]) # 找到最小的是從哪個下來
            dp[i, j] += dp[i-1, best_prev] # 把路徑花費加起來
            backtrack[i, j] = best_prev # 紀錄是從哪個位置來的

    # 回溯從最後一列找最小起點
    seam = np.zeros(H, int)
    seam[-1] = int(np.argmin(dp[-1]))
    for i in range(H-2, -1, -1):
        seam[i] = backtrack[i+1, seam[i+1]]
    return seam

def stitch_horizontal(img1, img2, overlap):
    H, W, C = img1.shape

    # 左側非重疊區
    left_body = img1[:, :W-overlap, :]

    # 各取重疊區
    ov1 = img1[:, W-overlap:, :]     # img1 的右側 overlap 列
    ov2 = img2[:, :overlap, :]       # img2 的左側 overlap 列

    # 計算誤差並找縫
    cost = compute_cost(ov1, ov2)    # shape = (H, overlap)
    seam = find_min_seam(cost)       # 長度 H

    # 合併重疊區：沿著縫的每一列選取像素
    merged_overlap = np.zeros_like(ov1)
    for i in range(H):
        cut = seam[i]
        merged_overlap[i, :cut, :] = ov1[i, :cut, :] # 縫前（左側）採用 img1 的像素
        merged_overlap[i, cut:, :] = ov2[i, cut:, :] # 縫後（右側）採用 img2 的像素

    # 右側非重疊區
    right_body = img2[:, overlap:, :]

    # 拼接：左 + 縫合重疊 + 右
    result = np.hstack([left_body, merged_overlap, right_body])
    return result

def stitch_vertical(img1, img2, overlap):
    H, W, C = img1.shape

    # 上半部（非重疊區）
    top_body = img1[:H-overlap, :, :]

    # 各取重疊區
    ov1 = img1[H-overlap:, :, :]    # img1 的下側 overlap 行
    ov2 = img2[:overlap, :, :]      # img2 的上側 overlap 行

    # 計算誤差並找縫
    cost = compute_cost(ov1, ov2)     # shape = (overlap, W)
    seam = find_min_seam(cost.T)      # 先轉置，得到長度 W 的縫索引

    # 合併重疊區：沿著縫的每一列（對應原圖的每一欄）選取像素
    merged_overlap = np.zeros_like(ov1)
    for j in range(W):
        cut = seam[j]
        merged_overlap[:cut, j, :] = ov1[:cut, j, :] # 縫前（上方）採用 img1 的像素
        merged_overlap[cut:, j, :] = ov2[cut:, j, :] # 縫後（下方）採用 img2 的像素

    # 下半部（非重疊區）
    bottom_body = img2[overlap:, :, :]

    # 拼接：上 + 縫合重疊 + 下
    result = np.vstack([top_body, merged_overlap, bottom_body])
    return result


if __name__ == "__main__":
    # 讀入檔名並複製兩張一樣的影像
    fileName = input("請輸入影像檔案 : ").strip()
    img = cv2.imread(fileName, cv2.IMREAD_COLOR)
    img1 = img.copy()
    img2 = img.copy()

    # 選擇拼貼方向
    direction = input("請輸入拼貼方向 (1)水平 (2)垂直 : ").strip()

    # 輸入重疊比例
    percent = int(input("請輸入重疊比例 (%) : ").strip())
    overlap = int((percent/100) * (img.shape[1] if direction == '1' else img.shape[0]))

    # 執行拼貼
    if direction == '1':
        result = stitch_horizontal(img1, img2, overlap)
    else:
        result = stitch_vertical(img1, img2, overlap)

    # 輸出結果
    outname = fileName.rsplit('.',1)[0] + "_result.bmp"
    cv2.imwrite(outname, result)
    print(f"完成！結果已儲存為：{outname}")

