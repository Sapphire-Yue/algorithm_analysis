import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
import heapq
import time 

start_time = time.time()

def split_image_to_tiles(image_path, tile_width=120, tile_height=120):
    """
    將圖片切割成多個小塊，每塊大小為 tile_width x tile_height。
    :param image_path: 圖片的路徑
    :param tile_width: 每個小塊的寬度
    :param tile_height: 每個小塊的高度
    :return: 切割後的小塊列表、行數、列數、每塊的高度和寬度
    """
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Image not found or format error.")
    
    tiles = []
    h, w = img.shape[:2]
    rows = h // tile_height
    cols = w // tile_width
    
    for i in range(rows):
        for j in range(cols):
            tile = img[i*tile_height:(i+1)*tile_height, j*tile_width:(j+1)*tile_width]
            tiles.append(tile)
    
    return tiles, rows, cols, tile_height, tile_width

def save_reconstructed_image(tiles, positions, tile_h, tile_w, filename):
    """
    將切割的圖片塊根據 positions 重新組合並保存為一張圖片。
    :param tiles: 切割後的圖片塊列表
    :param positions: 每個圖片塊的位置信息，格式為 {index: (row, col)}
    :param tile_h: 每個圖片塊的高度
    :param tile_w: 每個圖片塊的寬度
    :param filename: 保存的文件名
    """
    rows = [pos[0] for pos in positions.values()]
    cols = [pos[1] for pos in positions.values()]
    min_r, max_r = min(rows), max(rows)
    min_c, max_c = min(cols), max(cols)

    canvas_h = (max_r - min_r + 1) * tile_h
    canvas_w = (max_c - min_c + 1) * tile_w
    canvas = np.zeros((canvas_h, canvas_w, 3), dtype=np.uint8)

    for idx, (r, c) in positions.items():
        rr = r - min_r
        cc = c - min_c
        canvas[rr*tile_h:(rr+1)*tile_h, cc*tile_w:(cc+1)*tile_w] = tiles[idx]

    cv2.imwrite(filename, canvas)
    print(f"輸出影像檔: {filename}")

def extract_tile_features(tiles):
    """
    對所有 tile 預先轉換為多種顏色空間，避免重複轉換，回傳一個 list of dict
    每個 dict 包含: BGR, Gray, Lab, HSV, YCrCb
    """
    features = []
    for tile in tiles:
        gray = cv2.cvtColor(tile, cv2.COLOR_BGR2GRAY)
        lab = cv2.cvtColor(tile, cv2.COLOR_BGR2LAB)
        hsv = cv2.cvtColor(tile, cv2.COLOR_BGR2HSV)
        ycrcb = cv2.cvtColor(tile, cv2.COLOR_BGR2YCrCb)
        features.append({
            'bgr': tile,
            'gray': gray,
            'lab': lab,
            'hsv': hsv,
            'ycrcb': ycrcb
        })
    return features


# --- 邊緣形狀匹配（Canny） ---
def compute_canny_shape_diff(pic1, pic2, mode='col', edge_width=3):
    g1 = cv2.cvtColor(pic1, cv2.COLOR_BGR2GRAY)
    g2 = cv2.cvtColor(pic2, cv2.COLOR_BGR2GRAY)

    if mode == 'col':
        edge1 = g1[:, -edge_width:]
        edge2 = g2[:, :edge_width]
    else:
        edge1 = g1[-edge_width:, :]
        edge2 = g2[:edge_width, :]

    e1 = cv2.Canny(edge1, 50, 150)
    e2 = cv2.Canny(edge2, 50, 150)
    diff = np.mean(np.abs(e1.astype(np.float32) - e2.astype(np.float32))) / 255.0
    return diff

# --- 對齊邊緣特徵 shape ---
def crop_to_same_shape(x1, x2):
    h = min(x1.shape[0], x2.shape[0])
    w = min(x1.shape[1], x2.shape[1])
    return x1[:h, :w], x2[:h, :w]

# --- 單點 vs 上中下三點（取最小） ---
def fast_flexible_pixel_match(edge1, edge2):
    h = edge1.shape[0]
    pad = np.pad(edge2, ((1, 1), (0, 0)), mode='edge')  # 上中下 pad
    # 每個 row 對應三種 row: 上中下
    rolled = np.stack([
        pad[y:y + h] for y in range(3)
    ])  # shape: (3, H, C)

    diff = np.linalg.norm(rolled - edge1[None, :, :], axis=2)  # shape: (3, H)
    min_diff = np.min(diff, axis=0)  # shape: (H,)
    return np.mean(min_diff)


# --- 邊緣摘要 ---
def summarize_edge_by_mean(edge):
    if len(edge.shape) == 3:
        return np.mean(edge, axis=1)  # (H, C)
    else:
        return np.mean(edge, axis=1, keepdims=True)  # (H, 1)

def mean_vector_diff(vec1, vec2):
    return np.mean(np.linalg.norm(vec1 - vec2, axis=1))

# --- 特徵歐式距離計算（加速版） ---
def compute_edge_features(feat1, feat2, mode='col', edge_width=3, reverse=False, weight_config=None):
    pic1_lab = feat1['lab']
    pic2_lab = feat2['lab']
    pic1_gray = feat1['gray']
    pic2_gray = feat2['gray']
    pic1_hsv = feat1['hsv']
    pic2_hsv = feat2['hsv']
    pic1_ycrcb = feat1['ycrcb']
    pic2_ycrcb = feat2['ycrcb']

    if mode == 'col':
        if not reverse:
            a1 = pic1_lab[:, -edge_width:, :]
            a2 = pic2_lab[:, :edge_width, :]
            g1 = pic1_gray[:, -edge_width:]
            g2 = pic2_gray[:, :edge_width]
            h1 = pic1_hsv[:, -edge_width:, :]
            h2 = pic2_hsv[:, :edge_width, :]
            y1 = pic1_ycrcb[:, -edge_width:, :]
            y2 = pic2_ycrcb[:, :edge_width, :]
        else:
            a1 = pic2_lab[:, :edge_width, :]
            a2 = pic1_lab[:, -edge_width:, :]
            g1 = pic2_gray[:, :edge_width]
            g2 = pic1_gray[:, -edge_width:]
            h1 = pic2_hsv[:, :edge_width, :]
            h2 = pic1_hsv[:, -edge_width:, :]
            y1 = pic2_ycrcb[:, :edge_width, :]
            y2 = pic1_ycrcb[:, -edge_width:, :]
    else:
        if not reverse:
            a1 = pic1_lab[-edge_width:, :, :]
            a2 = pic2_lab[:edge_width, :, :]
            g1 = pic1_gray[-edge_width:, :]
            g2 = pic2_gray[:edge_width, :]
            h1 = pic1_hsv[-edge_width:, :, :]
            h2 = pic2_hsv[:edge_width, :, :]
            y1 = pic1_ycrcb[-edge_width:, :, :]
            y2 = pic2_ycrcb[:edge_width, :, :]
        else:
            a1 = pic2_lab[:edge_width, :, :]
            a2 = pic1_lab[-edge_width:, :, :]
            g1 = pic2_gray[:edge_width, :]
            g2 = pic1_gray[-edge_width:, :]
            h1 = pic2_hsv[:edge_width, :, :]
            h2 = pic1_hsv[-edge_width:, :, :]
            y1 = pic2_ycrcb[:edge_width, :, :]
            y2 = pic1_ycrcb[-edge_width:, :, :]

    if weight_config is None:
        weight_config = {
            'lab': 0.3,
            'gray': 0.0,
            'sobel': 0.1,
            'gradient_angle': 0.2,
            'hsv': 0.1,
            'ycrcb': 0.1,
            'gradient_heatmap': 0.0,
            'canny_shape': 0.0
        }

    a1, a2 = crop_to_same_shape(a1, a2)
    g1, g2 = crop_to_same_shape(g1, g2)
    h1, h2 = crop_to_same_shape(h1, h2)
    y1, y2 = crop_to_same_shape(y1, y2)

    # ---- Lab / YCrCb 用精緻比對 ----
    lab_diff = fast_flexible_pixel_match(a1.reshape(-1, a1.shape[-1]), a2.reshape(-1, a2.shape[-1]))  # shape: (H, C)
    ycrcb_diff = fast_flexible_pixel_match(y1.reshape(-1, y1.shape[-1]), y2.reshape(-1, y2.shape[-1]))

    # ---- HSV / Gray 用快速均值摘要比對 ----
    gray_diff = mean_vector_diff(summarize_edge_by_mean(g1), summarize_edge_by_mean(g2))
    hsv_diff = mean_vector_diff(summarize_edge_by_mean(h1), summarize_edge_by_mean(h2))

    sobel1_x = cv2.Sobel(g1, cv2.CV_64F, 1, 0, ksize=3)
    sobel1_y = cv2.Sobel(g1, cv2.CV_64F, 0, 1, ksize=3)
    sobel2_x = cv2.Sobel(g2, cv2.CV_64F, 1, 0, ksize=3)
    sobel2_y = cv2.Sobel(g2, cv2.CV_64F, 0, 1, ksize=3)
    sobel_diff = np.mean(np.abs(sobel1_x - sobel2_x) + np.abs(sobel1_y - sobel2_y))
    phase1 = cv2.phase(sobel1_x, sobel1_y, angleInDegrees=True)
    phase2 = cv2.phase(sobel2_x, sobel2_y, angleInDegrees=True)
    angle_diff = np.mean(np.abs(phase1 - phase2)) / 180.0

    final_score = (
        weight_config['lab'] * lab_diff +
        weight_config['gray'] * gray_diff +
        weight_config['sobel'] * sobel_diff +
        weight_config['gradient_angle'] * angle_diff +
        weight_config['hsv'] * hsv_diff +
        weight_config['ycrcb'] * ycrcb_diff
    )
    return final_score

# --- 雙向歐式距離平均（提升穩定性） ---
def compute_symmetric_distance(feat1, feat2, mode='col', edge_width=1, weight_config=None, alpha=0.0):
    d1 = compute_edge_features(feat1, feat2, mode=mode, edge_width=edge_width, reverse=False, weight_config=weight_config)
    d2 = compute_edge_features(feat1, feat2, mode=mode, edge_width=edge_width, reverse=True, weight_config=weight_config)
    asymmetry = abs(d1 - d2)
    return (d1 + d2) / 2 + alpha * asymmetry


# --- 重構 compute_distance_matrices 使用雙向距離與一致性懲罰 ---
def compute_distance_matrices(features, edge_width=1, weight_config=None):
    n = len(features)
    dist_matrix_right = np.full((n, n), np.inf)
    dist_matrix_bottom = np.full((n, n), np.inf)

    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            dist_matrix_right[i][j] = compute_symmetric_distance(
                features[i], features[j], mode='col',
                edge_width=edge_width, weight_config=weight_config
            )
            dist_matrix_bottom[i][j] = compute_symmetric_distance(
                features[i], features[j], mode='row',
                edge_width=edge_width, weight_config=weight_config
            )

    return dist_matrix_right, dist_matrix_bottom


# === Prims 拼圖重建（允許上下左右擴展，並動態追蹤可用邊界） ===
def prims_puzzle_reconstruct(dist_right, dist_bottom, num_rows, num_cols):
    n = dist_right.shape[0]
    visited = set()
    positions = {}
    used_pos = set()

    score = []
    for i in range(n):
        min_r = np.min(dist_right[i][dist_right[i] < np.inf])
        min_b = np.min(dist_bottom[i][dist_bottom[i] < np.inf])
        score.append(min_r + min_b)
    start_idx = int(np.argmin(score))

    visited.add(start_idx)
    positions[start_idx] = (0, 0)
    used_pos.add((0, 0))

    min_row, max_row = 0, 0
    min_col, max_col = 0, 0

    pq = []
    def push_valid_edges(src):
        r, c = positions[src]
        for direction, dr, dc, dist_matrix in [
            ('R', 0, 1, dist_right),
            ('B', 1, 0, dist_bottom),
            ('L', 0, -1, dist_right.T),
            ('T', -1, 0, dist_bottom.T)
        ]:
            for tgt in range(n):
                if tgt in visited:
                    continue
                new_r, new_c = r + dr, c + dc
                temp_min_r = min(min_row, new_r)
                temp_max_r = max(max_row, new_r)
                temp_min_c = min(min_col, new_c)
                temp_max_c = max(max_col, new_c)
                if (temp_max_r - temp_min_r + 1 <= num_rows and
                    temp_max_c - temp_min_c + 1 <= num_cols):
                    heapq.heappush(pq, (dist_matrix[src][tgt], src, tgt, direction))

    push_valid_edges(start_idx)

    while pq:
        dist, u, v, direction = heapq.heappop(pq)
        if v in visited or u not in positions:
            continue

        r, c = positions[u]
        if direction == 'R': new_pos = (r, c + 1)
        elif direction == 'B': new_pos = (r + 1, c)
        elif direction == 'L': new_pos = (r, c - 1)
        elif direction == 'T': new_pos = (r - 1, c)
        else: continue

        if new_pos in used_pos:
            continue

        temp_min_r = min(min_row, new_pos[0])
        temp_max_r = max(max_row, new_pos[0])
        temp_min_c = min(min_col, new_pos[1])
        temp_max_c = max(max_col, new_pos[1])

        if (temp_max_r - temp_min_r + 1 > num_rows or
            temp_max_c - temp_min_c + 1 > num_cols):
            continue

        min_row, max_row = temp_min_r, temp_max_r
        min_col, max_col = temp_min_c, temp_max_c

        positions[v] = new_pos
        visited.add(v)
        used_pos.add(new_pos)

        push_valid_edges(v)

    offset_r = -min_row
    offset_c = -min_col
    for k in positions:
        r, c = positions[k]
        positions[k] = (r + offset_r, c + offset_c)

    return positions


if __name__ == '__main__':
    # 步驟 1：讀入與切割
    picture = input("請輸入影像檔: ")
    tiles, num_rows, num_cols, tile_h, tile_w = split_image_to_tiles(picture)

    # 預先轉換所有 tile 特徵
    features = extract_tile_features(tiles)

    # 步驟 2：計算歐式距離矩陣
    weight_config = {
        'lab': 0.25,
        'gray': 0.0,
        'sobel': 0.1,
        'gradient_angle': 0.2,
        'hsv': 0.15,
        'ycrcb': 0.1,
        'canny_shape': 0.2,
        'gradient_heatmap': 0.0
    }

    # 可調參數
    dist_right, dist_bottom = compute_distance_matrices(features, edge_width=1, weight_config=weight_config)

    # 步驟 5：重構拼圖位置
    positions = prims_puzzle_reconstruct(dist_right, dist_bottom, num_rows, num_cols)

    # 步驟 6：輸出拼圖結果
    save_reconstructed_image(tiles, positions, tile_h, tile_w, picture.replace('.bmp', '_result.bmp'))

    total_time = time.time() - start_time
    print(total_time)