import cv2
import numpy as np
import time 

start_time = time.time()
bmp = cv2.imread('One_Piece1.bmp')

# 將圖片切分為多個 120x120 的小圖，並存入一個 list
h, w, c = bmp.shape

tiles = []
for y in range(0, h, 120):
    for x in range(0, w, 120):
        tile = bmp[y:y+120, x:x+120]
        tiles.append(tile)

picture = np.array(tiles)
column_weight = dict()
row_weight = dict()

def find_the_close(index):
    """
    找出與第一個小圖與其他小圖的相似度權重
    :param pic: 第一個小圖
    :return: None
    """

    for i in range(0, len(picture)):
        column_weight[index, i] = two_picture_column_euclidean_distance(picture[index], picture[i])
        row_weight[index, i] = two_picture_row_euclidean_distance(picture[index], picture[i])

def two_picture_column_euclidean_distance(pic1, pic2):
    """
    計算兩個小圖右邊界與左邊界的歐式距離
    :param pic1: 第一個小圖
    :param pic2: 第二個小圖
    :return: 歐式距離
    """
    # Lab
    pic1_lab = cv2.cvtColor(pic1, cv2.COLOR_BGR2LAB)
    pic2_lab = cv2.cvtColor(pic2, cv2.COLOR_BGR2LAB)
    right_edge_lab = pic1_lab[:, -3:, :].reshape(-1, 3)
    left_edge_lab = pic2_lab[:, :3, :].reshape(-1, 3)
    lab_dist = np.mean(np.linalg.norm(right_edge_lab - left_edge_lab, axis=1))

    # HSV
    pic1_hsv = cv2.cvtColor(pic1, cv2.COLOR_BGR2HSV)
    pic2_hsv = cv2.cvtColor(pic2, cv2.COLOR_BGR2HSV)
    right_edge_hsv = pic1_hsv[:, -3:, :].reshape(-1, 3)
    left_edge_hsv = pic2_hsv[:, :3, :].reshape(-1, 3)
    hsv_dist = np.mean(np.linalg.norm(right_edge_hsv - left_edge_hsv, axis=1))

    # 加權平均
    return 0.5 * lab_dist + 0.5 * hsv_dist

def two_picture_row_euclidean_distance(pic1, pic2):
    """
    計算兩個小圖下邊界與上邊界的歐式距離
    :param pic1: 第一個小圖
    :param pic2: 第二個小圖
    :return: 歐式距離
    """
    # Lab
    pic1_lab = cv2.cvtColor(pic1, cv2.COLOR_BGR2LAB)
    pic2_lab = cv2.cvtColor(pic2, cv2.COLOR_BGR2LAB)
    right_edge_lab = pic1_lab[:, -3:, :].reshape(-1, 3)
    left_edge_lab = pic2_lab[:, :3, :].reshape(-1, 3)
    lab_dist = np.mean(np.linalg.norm(right_edge_lab - left_edge_lab, axis=1))

    # HSV
    pic1_hsv = cv2.cvtColor(pic1, cv2.COLOR_BGR2HSV)
    pic2_hsv = cv2.cvtColor(pic2, cv2.COLOR_BGR2HSV)
    right_edge_hsv = pic1_hsv[:, -3:, :].reshape(-1, 3)
    left_edge_hsv = pic2_hsv[:, :3, :].reshape(-1, 3)
    hsv_dist = np.mean(np.linalg.norm(right_edge_hsv - left_edge_hsv, axis=1))

    # 加權平均
    return 0.5 * lab_dist + 0.5 * hsv_dist

begin_index = 0

for i in range(0, 144):
    find_the_close(i)

# # 1. 準備所有邊
# edges = []
# for (i, j), w in column_weight.items():
#     if i != j:
#         edges.append((w, i, j, 'col'))
# for (i, j), w in row_weight.items():
#     if i != j:
#         edges.append((w, i, j, 'row'))

# # 2. 邊排序
# edges.sort()

# # 3. Union-Find 結構
# parent = [i for i in range(len(picture))]
# def find(x):
#     while parent[x] != x:
#         parent[x] = parent[parent[x]]
#         x = parent[x]
#     return x
# def union(x, y):
#     parent[find(x)] = find(y)

# # 4. Kruskal 主流程
# mst = []
# for w, u, v, direction in edges:
#     if find(u) != find(v):
#         union(u, v)
#         mst.append((u, v, w, direction))
#     if len(mst) == len(picture) - 1:
#         break

# # 5. 輸出 MST 結果
# for u, v, w, direction in mst:
#     print(f"{u} <-> {v}, weight={w:.2f}, direction={direction}")

#     # 將 picture[0] 與 picture[1] 橫向拼接
#     if direction == 'col':
#         concatenated = np.hstack((picture[u], picture[v]))
#     else:  # direction == 'row'
#         # 將圖片上下拼接
#         concatenated = np.vstack((picture[u], picture[v]))

#     # 儲存拼接後的圖片
#     cv2.imwrite('concatenated_output.bmp', concatenated)
#     cv2.imshow('Concatenated Image', concatenated)
#     cv2.waitKey(0)

total_time = time.time() - start_time 
print(total_time)