# 演算法分析機測
# 學號: 11127101 / 11127103 / 11127126
# 姓名: 藍至奕 / 王芃穎 / 黃柏寧
# 中原大學資訊工程系

import heapq

class Node:
    def __init__(self, ch, freq):
        self.ch = ch
        self.freq = freq
        self.left = None
        self.right = None
        
    def __lt__(self, other):  # 用於heap比較
        return self.freq < other.freq

def build_huffman_tree(freq_map):
    heap = [Node(ch, freq) for ch, freq in freq_map.items()]
    heapq.heapify(heap) # 建立min-heap
    
    while len(heap) > 1:
        n1 = heapq.heappop(heap)
        n2 = heapq.heappop(heap)
        merged = Node(None, n1.freq + n2.freq)
        merged.left = n1
        merged.right = n2
        heapq.heappush(heap, merged)
    
    return heap[0] # 回傳root

def build_huffman_codes(node, preNum='', code_map=None):
    if node:
        if node.ch is not None:  # 是葉節點(字元都會在葉節點)
            code_map[node.ch] = preNum

        build_huffman_codes(node.left, preNum + '0', code_map)
        build_huffman_codes(node.right, preNum + '1', code_map)

    return code_map

def decode(encode_str, root):
    result = []
    node = root
    for bit in encode_str:
        node = node.left if bit == '0' else node.right
        if node.ch is not None:
            result.append(node.ch)
            node = root  # 回到root繼續解析

    # 把result中的字串合併成一個完整字串
    return ''.join(result)

if __name__ == "__main__":
    # 序號
    serial_num = 1                           

    while True:
        # 讀入資料
        n = int(input())
        if n == 0: break

        freq_map = {}
        for i in range(n):
            ch, freq = input().split()
            freq_map[ch] = int(freq)

        # 讀入已編碼的字串，並把字串的前後whitespace都清掉
        encode_str = input().strip()        
        
        # 建立Huffman Tree
        root = build_huffman_tree(freq_map)
        # 取得各個字元的Huffman Code
        code_map = build_huffman_codes(root)
        

        # 印出Huffman Code
        print("Huffman Codes #" + str(serial_num))
        for ch in sorted(code_map):  # 按照字母順序輸出
            print(f"{ch} {code_map[ch]}")
        
        # 解碼輸出
        decoded_str = decode(encode_str, root)
        print("Decode =", decoded_str)

        serial_num+=1
        # print()