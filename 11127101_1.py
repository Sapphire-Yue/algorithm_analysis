# 演算法分析機測
# 學號: 11127101 / 11127103 / 11127126
# 姓名: 藍至奕 / 王芃穎 / 黃柏寧
# 中原大學資訊工程系

import time
import re # 用於正則表達式，方便解析多項式字串
from collections import defaultdict # collections 裡的特殊字典，當查詢不存在的鍵時，會自動賦值為預設類型（這裡是 int，即預設值為 0）

#start_time = time.time()

def changeFormat(poly_str): # 解析字串，轉換為字典形式 {次方: 係數}
    poly_dict = defaultdict(int)
    poly_str = poly_str.replace(" ", "")  # 移除空格
    # 把整個多項式拆成每一項（term） ex: "3x^2+2x-5" -> ['3x^2', '+2x', '-5']
    terms = re.findall(r'([+-]?\d*x?(?:\^\d+)?)', poly_str)

    for term in terms:
        if not term: continue

        if 'x' in term:
            # partition('^') 把字串分三部分 ex: "3x^2" -> coef = '3x', _ = '^', exp = '2'
            # 因為只需要次方跟係數，且'^'不會用到，所以用'_'來取代
            coef, _, exp = term.partition('^') 
            # 沒有'^'，代表次方為1
            if not exp: exp = 1
            else: exp = int(exp)

            coef = coef.replace('x', '')
            # "x" -> '' -> 1, "-x" -> '-' -> -1, "3x" -> '3' -> 3
            if coef in {'', '+'}: coef = 1
            elif coef == '-': coef = -1
            else: coef = int(coef)
        else: # 處理常數項
            coef = int(term)
            exp = 0 # 次方設為0
        
        poly_dict[exp] += coef
    
    return dict(poly_dict)

def horner(poly, x): # 使用 Horner's Rule 計算多項式函數值
    # 原本要進行很多次 x^n 的運算，現在只需要 n 次乘法 和 n 次加法
    # ex: 3x² + 2x - 5 -> ((3)x + 2)x - 5
    sorted_exps = sorted(poly.keys(), reverse=True) # 把所有的次方排序(從大到小)
    result = 0
    for exp in sorted_exps:
        result = result * x + poly[exp]
    return result

def add(p1, p2): # 計算兩個多項式的和
    result = defaultdict(int, p1) # 把result用p1初始化
    for exp, coef in p2.items(): # 把次方 -> 係數，轉成(exp, coef)
        result[exp] += coef # 根據對應的次方把係數相加，若某一項不存在，defaultdict 會補成0，再加上coef
    return dict(result)

def multiply(p1, p2): # 計算兩個多項式的積
    result = defaultdict(int)
    for exp1, coef1 in p1.items():
        for exp2, coef2 in p2.items():
            result[exp1 + exp2] += coef1 * coef2
    return dict(result)

def Subtract(p1, p2): # 計算兩個多項式的差
    result = defaultdict(int, p1)
    for exp, coef in p2.items():
        result[exp] -= coef
    return dict(result)

def divide(p1, p2): # 計算兩個多項式的商式與餘式
    quotient = defaultdict(int)
    remainder = dict(p1)  # 初始餘數是 p1

    while remainder and max(remainder.keys()) >= max(p2.keys()): # 執行長除法
        # 計算商的係數
        exp_diff = max(remainder.keys()) - max(p2.keys())
        coef_div = int(remainder[max(remainder.keys())] / p2[max(p2.keys())])  # 轉換為整數
        
        quotient[exp_diff] = coef_div # 更新商
        
        temp_poly = {exp + exp_diff: coef_div * coef for exp, coef in p2.items()} # 創建對應的減去項
        # 將餘數減去對應的項
        for exp, coef in temp_poly.items():
            remainder[exp] = remainder.get(exp, 0) - coef
            if remainder[exp] == 0:
                del remainder[exp]  # 刪除餘數中為0的項

    return dict(quotient), remainder # 返回商和餘數

def format_polynomial(poly):
    
    if isinstance(poly, tuple): # 確保傳入的type式dictionary
        quotient, remainder = poly
        return f"Quotient: {format_polynomial(quotient)}, Remainder: {format_polynomial(remainder)}"

    terms = []
    for exp in sorted(poly.keys(), reverse=True):
        coef = poly[exp]

        if coef == 0: continue
            
        if exp == 0:  term = f"{coef}" # 常數項
        elif exp == 1:  term = f"{'' if abs(coef) == 1 else abs(coef)}x" # x^1 項  
        else: term = f"{'' if abs(coef) == 1 else abs(coef)}x^{exp}" # x^n (n > 1) 項
    
        # 處理正負號
        if coef < 0: terms.append(f"-{term}")  # 負號直接加
        else:
            if terms: terms.append(f"+{term}")
            else: terms.append(f"{term}")  # 第一項不要加 `+`

    # 拼接字串，移除開頭的 `+`
    result = "".join(terms)
    if result.startswith("+"): result = result[1:]  # 去掉開頭的 `+`

    return result.replace("+-", "-").replace("-1x", "-x").replace("+1x", "+x").replace("--", "-")

def main():
    poly_dict = {}
    storeResults = [] # 儲存各個運算的結果

    for _ in range(2): # 讀兩個多項式
        poly_input = input().strip()
        name, expr = poly_input.split("=") # 先找出多項式的名稱及運算式
        poly_name = name.strip().split("(")[0]
        poly_dict[poly_name] = changeFormat(expr.strip())

        # print(name, expr, poly_name, poly_dict[poly_name])
        # ex: p1(x) = x^3+2x^2+3x+5
        # name = p1(x), expr = x^3+2x^2+3x+5, poly_name = p1, poly_dict[poly_name] = {3: 1, 2: 2, 1: 3, 0: 5}

    while True:
        command = input().strip()

        if command == "0": break
        # a-zA-Z_ : 支援字母與底線作為多項式名稱, \w*：表示 0 或多個字元，可以是字母、數字、底線
        # \d: 數字, \(\d+\): (數字), [+-]?: 數字為正或負
        elif re.match(r'[a-zA-Z_]\w*\([+-]?\d+\)', command.strip()): # 計算
            poly_name = command.strip().split("(")[0]
            #\(([+-]?\d+)\): 找到括號中的數字，例如(2)會取出2, .group(1): 取出第一個括號裡的內容
            x = int(re.search(r'\(([+-]?\d+)\)', command).group(1))

            if poly_name in poly_dict: storeResults.append(f"{poly_name}({x}) = {horner(poly_dict[poly_name], x)}")
            else: storeResults.append(f"Error: 多項式 {poly_name}(x) 未定義") # 錯誤處理

        # ([a-zA-Z_]+\d*\([xX]\)): 第一個多項式名稱（如 y1(x), \s*: 任意數量的空格, ([\+\-\*/]): 運算符號：加、減、乘、除
        elif re.match(r'([a-zA-Z_]+\d*\([xX]\))\s*([\+\-\*/])\s*([a-zA-Z_]+\d*\([xX]\))', command):  # 運算
            match = re.match(r'([a-zA-Z_]+\d*\([xX]\))\s*([\+\-\*/])\s*([a-zA-Z_]+\d*\([xX]\))', command)
            poly1, op, poly2 = match.groups()

            # 取得key
            poly1_key = poly1.strip().split("(")[0]
            poly2_key = poly2.strip().split("(")[0]

            # 錯誤處理
            if poly1_key not in poly_dict or poly2_key not in poly_dict:
                if poly1_key not in poly_dict and poly2_key not in poly_dict: storeResults.append(f"Error: 未定義多項式 {poly1} 及 {poly2}")
                elif poly2_key not in poly_dict: storeResults.append(f"Error: 未定義多項式 {poly2}")
                elif poly1_key not in poly_dict: storeResults.append(f"Error: 未定義多項式 {poly1}")

                continue

            p1 = poly_dict[poly1_key]
            p2 = poly_dict[poly2_key]

            if op == '+': storeResults.append(f"{poly1_key}(x) + {poly2_key}(x) = {format_polynomial(add(p1, p2))}")
            elif op == '-': storeResults.append(f"{poly1_key}(x) - {poly2_key}(x) = {format_polynomial(Subtract(p1, p2))}")
            elif op == '*': storeResults.append(f"{poly1_key}(x) * {poly2_key}(x) = {format_polynomial(multiply(p1, p2))}")
            elif op == '/': storeResults.append(f"{poly1_key}(x) / {poly2_key}(x) = {format_polynomial(divide(p1, p2))}")

    for result in storeResults: # 依序印出結果
        print(result)

    #total_time = time.time() - start_time
    #print(f"所花時間: {total_time}")

main()


