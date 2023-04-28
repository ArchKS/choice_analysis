""" 
打开资产负债表.xls文件，删除第一列字符为"报表类型"、"公司类型"的行
pip install pandas openpyxl xlrd
"""

import shutil
from config import SHEETS,  FORMULAS, STACK_FORMULAS,Need_Combine_Excel
from calc import mini_calculate, calc_formulas, elementwise_operation
from excel import simplify_excels, set_column_width, merge_excels, g_map_data, get_raw_sheets
from draw import draw_plot, draw_stack_bar
from utils import move_file
import os
import re


def get_qcode():
    qcode = ""
    for _, _, files in os.walk('xls'):
        qcode = re.findall(r'_(.*?)\.', files[0])[0]
    return qcode

# 从ed_map里找到需要的值
# {A:['N1','N2']}
# =>
# {A: {N1: [1,2,3], N2: [1,2,3]}}


def get_stack_fmt_data(excel_data_map, stack_formulas):
    ret_data = {}
    for k, v in stack_formulas.items():
        ret_data[k] = {}
        for key_name in v:
            if "=" in key_name:
                # key_name = 应收款=应收票据及应收账款+其他应收款合计
                res_dict = calc_formulas(excel_data_map, [key_name])
                for dict_key, dict_val in res_dict.items():
                    ret_data[k][dict_key] = dict_val
            else:
                ret_data[k][key_name] = excel_data_map[key_name]

    for k, v in ret_data.items():
        if k.startswith("%"):
            addkey = ""
            mini_dic_res = {}
            for ik, iv in v.items():
                addkey = addkey+"+"+ik
            addkey = "TOTAL_VALUES="+addkey[1:]
            mini_res = mini_calculate(v, addkey)
            mini_dic_res[k] = list(mini_res.values())[0]
            for ik, iv in v.items():
                calc_arr = elementwise_operation(iv, mini_dic_res[k], '/')
                calc_arr = [round(x*100, 1) for x in calc_arr]
                ret_data[k][ik] = calc_arr
    return ret_data


def draw_multi_formula(excel_map_data, qcode):
    for key, value in FORMULAS.items():
        dic = calc_formulas(excel_map_data, value)
        dic["Year"] = excel_map_data["Year"]
        draw_plot(dic, key, qcode)


def draw_stack_formula(excel_data_map,qcode):
    stack_data = get_stack_fmt_data(excel_data_map, STACK_FORMULAS)
    # loop stack_data
    for stk_key, stk_obj in stack_data.items():
        # stk_key %资产性质
        if '%' in stk_key:
            draw_stack_bar(stk_obj, excel_data_map["Year"], stk_key.replace('%', ''), qcode, True)
        else:
            draw_stack_bar(stk_obj, excel_data_map["Year"], stk_key, qcode)


def main():
    QCODE = get_qcode()
    MERGED_EXCEL = QCODE+".xlsx"

    if Need_Combine_Excel:
        move_file(QCODE)  # 移动xlsx文件到指定目录
        raw_sheet = get_raw_sheets(SHEETS,QCODE)
        simplify_excels(raw_sheet)  # 清理原始excel
        merge_excels(raw_sheet,MERGED_EXCEL)  # 将干净的excel合并为新的excel

        set_column_width(MERGED_EXCEL, 40)

    # 将excel数据格式化成map的格式
    ed_map = g_map_data(MERGED_EXCEL)

    # 绘图
    draw_multi_formula(ed_map, QCODE)  # 折线图
    draw_stack_formula(ed_map,QCODE)  # 堆积柱状图

    # 删除xlsx文件夹
    if Need_Combine_Excel:
        shutil.rmtree('./xlsx/')


main()
