# 演算法分析機測
# 學號: 11127101 / 11127103 / 11127126
# 姓名: 藍至奕 / 王芃穎 / 黃柏寧
# 中原大學資訊工程系

import time
import re
from collections import defaultdict

start_time = time.time()

def parse_String(poly_str): # 解析字串，轉換為字典形式 {次方: 係數}
    poly_dict = defaultdict(int)
    poly_str = poly_str.replace(" ", "")  # 移除空格
    terms = re.findall(r'([+-]?\d*x?(?:\^\d+)?)', poly_str)

    for term in terms:
        if not term:
            continue
        
        if 'x' in term:
            coef, _, exp = term.partition('^')
            if not exp:
                exp = 1
            else:
                exp = int(exp)
            coef = coef.replace('x', '')
            if coef in {'', '+'}:
                coef = 1
            elif coef == '-':
                coef = -1
            else:
                coef = int(coef)
        else:
            coef = int(term)
            exp = 0
        
        poly_dict[exp] += coef
    
    return dict(poly_dict)

def horner(poly, x): # 使用 Horner's Rule 計算多項式函數值
    sorted_exps = sorted(poly.keys(), reverse=True)
    result = 0
    for exp in sorted_exps:
        result = result * x + poly[exp]
    return result

def add(p1, p2): # 計算兩個多項式的和
    result = defaultdict(int, p1)
    for exp, coef in p2.items():
        result[exp] += coef
    return dict(result)

def multiply(p1, p2): # 計算兩個多項式的積
    result = defaultdict(int)
    for exp1, coef1 in p1.items():
        for exp2, coef2 in p2.items():
            result[exp1 + exp2] += coef1 * coef2
    return dict(result)

def Subtraction(p1, p2): # 計算兩個多項式的差
    result = defaultdict(int, p1)
    for exp, coef in p2.items():
        result[exp] -= coef
    return dict(result)

def divide(p1, p2): # 計算兩個多項式的商式與餘式
    
    quotient = defaultdict(int)
    remainder = dict(p1)  # 初始餘數是 p1

    # 逐步執行長除法
    while remainder and max(remainder.keys()) >= max(p2.keys()):
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

    # 確保傳入的type式dictionary
    if isinstance(poly, tuple):
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
        if coef < 0:
            terms.append(f"-{term}")  # 負號直接加
        else:
            if terms:
                terms.append(f"+{term}")
            else:
                terms.append(f"{term}")  # 第一項不要加 `+`

    # 拼接字串，移除開頭的 `+`
    result = "".join(terms)
    if result.startswith("+"): result = result[1:]  # 去掉開頭的 `+`

    return result.replace("+-", "-").replace("-1x", "-x").replace("+1x", "+x").replace("--", "-")

# 讀取輸入
p1_str = input().split('=')[1].strip() # 第一個多項式
p2_str = input().split('=')[1].strip() # 第二個多項式
# 分析字串
p1 = parse_String(p1_str) 
p2 = parse_String(p2_str)

storeResults = [] # 儲存各個運算的結果

while True:
    command = input().strip()

    if command == "0": break
    elif re.search(r'p[1]\(\d+\)', command):
        x = int(re.search(r'\((\d+)\)', command).group(1))
        storeResults.append(f"p1({x}) = {horner(p1, x)}")

    elif re.search(r'p[2]\(\d+\)', command):
        x = int(re.search(r'\((\d+)\)', command).group(1))
        storeResults.append(f"p2({x}) = {horner(p2, x)}")

    elif "p1(x) + p2(x)" in command or "p2(x) + p1(x)" in command: 
        if "p1(x) + p2(x)" in command: storeResults.append(f"p1(x) + p2(x) = {format_polynomial(add(p1, p2))}")
        elif "p2(x) + p1(x)" in command: storeResults.append(f"p2(x) + p1(x) = {format_polynomial(add(p2, p1))}")

    elif "p1(x) * p2(x)" in command or "p2(x) * p1(x)" in command: 
        if "p1(x) * p2(x)" in command: storeResults.append(f"p1(x) * p2(x) = {format_polynomial(multiply(p1, p2))}")
        elif "p2(x) * p1(x)" in command: storeResults.append(f"p2(x) * p1(x) = {format_polynomial(multiply(p2, p1))}")

    elif "p1(x) - p2(x)" in command or "p2(x) - p1(x)" in command: 
        if "p1(x) - p2(x)" in command: storeResults.append(f"p1(x) - p2(x) = {format_polynomial(Subtraction(p1, p2))}")
        elif "p2(x) - p1(x)" in command: storeResults.append(f"p2(x) - p1(x) = {format_polynomial(Subtraction(p2, p1))}")

    elif "p1(x) / p2(x)" in command or "p2(x) / p1(x)" in command: 
        if "p1(x) / p2(x)" in command: 
            result = divide(p1, p2)
            storeResults.append(f"p1(x) / p2(x) = {format_polynomial(result)}")
        elif "p2(x) / p1(x)" in command: 
            result = divide(p2, p1)
            storeResults.append(f"p2(x) / p1(x) = {format_polynomial(result)}")

for result in storeResults: # 依序印出結果
    print(result)

total_time = time.time() - start_time
print(total_time)