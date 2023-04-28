

import re
import numpy as np


""" 
@ 迷你计算
给出对象 data = {
    营业总收入：[2,4,6],
    营业成本:[1,2,3]
}
计算字符串"平均=(B1营业成本+营业成本)/2"
"B1营业成本"是构造一个向右位移一位的数组，保持数组长度，缺省的地方用0填充，即[0,1,2]
最后计算得出的数组为 [0.5,1.5,2.5]
写一个这样的功能函数
"""


def shifted_list(lst, shift):
    l_arr = [-x for x in lst.tolist()[0:shift]]
    r_arr = lst.tolist()[:-shift]
    return l_arr + r_arr


def mini_calculate(data, expression, percent=False):
    result_arr = []
    left_exp_key, right_exp_val = expression.split('=')

    # 使用正则表达式识别 B 前缀的变量
    b_variables = re.findall(r'B(\d+)(\w+)', right_exp_val)

    # 对于每个 B 前缀的变量，创建一个相应的向右位移数组
    for shift, key in b_variables:
        if key not in data:
            continue
        shifted_key = f'B{shift}{key}'
        data[shifted_key] = shifted_list(data[key], int(shift))

    for values in zip(*data.values()):
        # 使用 locals() 将变量名称与其值进行映射，方便在表达式中使用变量名称
        values = np.where(np.isnan(values), 0, values)  # 将excel里空的nan替换为0
        variables = {k: v for k, v in zip(data.keys(), values)}
        result = eval(right_exp_val, variables)
        result_arr.append(result)

    scale = 1
    suffix = ''
    if percent:
        scale = 100
        suffix = "%"

    return {
        left_exp_key+suffix: [round(x*scale, 1) for x in result_arr]
    }




# 给出两个参数，dict 和 "毛利率=(营业收入-营业成本)/营业收入"，进行字典数组的数学运算
def calc_formulas(excel_map_data, My_Formulas):
    d = {}
    for expr in My_Formulas:
        if expr.startswith("%"):
            global hasPercent
            hasPercent = True
            res = mini_calculate(excel_map_data, expr[1:], percent=True)
        else:
            res = mini_calculate(excel_map_data, expr, percent=False)
        key = list(res.keys())[0]
        d[key] = list(res.values())[0]
    return d



# 数组运算
def elementwise_operation(arr1, arr2, operation):
    if len(arr1) != len(arr2):
        raise ValueError("Both input arrays must have the same length.")
    if operation == '+':
        return [a + b for a, b in zip(arr1, arr2)]
    elif operation == '-':
        return [a - b for a, b in zip(arr1, arr2)]
    elif operation == '*':
        return [a * b for a, b in zip(arr1, arr2)]
    elif operation == '/':
        return [a / b for a, b in zip(arr1, arr2)]
    else:
        raise ValueError("Invalid operation. Supported operations: '+', '-', '*', '/'")
