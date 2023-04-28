
import os
import re
import openpyxl
import pandas as pd
from config import FIELDS_To_REMOVE, Limit_Year
from utils import get_format_module


# 处理Excel，如删除指定行，删除年年报 删除亿元
def simplify_excel(file_name, FIELDS_To_REMOVE, with_head=False):
    xls_path = './xls/' + file_name + '.xls'
    xlsx_path = './xlsx/' + file_name + '.xlsx'

    if os.path.exists(xls_path):
        # 读取.xls文件
        xls_file = pd.read_excel(xls_path, engine='xlrd')

        # 将数据保存为.xlsx文件
        xls_file.to_excel(xlsx_path, index=False, engine='openpyxl')

        # 读取.xlsx文件
        df = pd.read_excel(xlsx_path, engine='openpyxl')

        # 删除单位，将 无形资产(亿元) => 无形资产
        df.iloc[:, 0] = df.iloc[:, 0].str.replace(r'\(亿元\)', '', regex=True)
        df.iloc[:, 0] = df.iloc[:, 0].str.replace(':', '')
        # df.iloc[:, 0] = df.iloc[:, 0].apply(lambda x: re.sub(r"[\u4e00-\u9fa5]+、", "", x.str))
        df.iloc[:, 0] = df.iloc[:, 0].apply(lambda x: re.sub(
            r"[\u4e00-\u9fa5]+、", "", x) if isinstance(x, str) else x)
        df.iloc[:, 0] = df.iloc[:, 0].apply(lambda x: re.sub(
            r'\([\u4e00-\u9fa5]+\)', "", x) if isinstance(x, str) else x)

        # 将2000年年报修改为2000
        df.columns = [col.replace('年年报', '') for col in df.columns]

        # 删除不需要的字段，如公告日期
        df = df[~df.iloc[:, 0].isin(FIELDS_To_REMOVE)]

        # 删除第二列开始全是 "查看" 的行
        df = df[df.iloc[:, 1:].ne('查看').all(axis=1)]

        # 首行首列置空,默认Unnamed: 0
        df.columns.values[0] = "Year"

        # 获取列数
        num_columns = len(df.columns)

        # 截取第一列和后 Limit_Year 列
        if num_columns > Limit_Year:
            df = df.iloc[:, [0] +
                         list(range(num_columns - Limit_Year, num_columns))]

        # 设置单元格格式
        format_module = get_format_module()
        format_module.header_style = {
            "font": {"bold": False, "color": "FF1F497D"}
        }
        # 将处理好的文件写入到新的xlsx中
        df.to_excel(xlsx_path, index=False,
                    engine='openpyxl', header=with_head)

# 批量处理excel


def simplify_excels(raw_sheet):
    index = 0
    for sheet_name in raw_sheet:
        index += 1
        print('== Finish ' + sheet_name + " ==")
        if index == 1:
            simplify_excel(sheet_name, FIELDS_To_REMOVE, True)
        else:
            simplify_excel(sheet_name, FIELDS_To_REMOVE)


# 生成带正确目录的xls文件和路径，如 ./xls/现金流量表_300059.xls
def get_raw_sheets(SHEETS,qcode):
    # raw_SHEETS = [s+"_"+CODE for s in SHEETS]
    raw_sheet = []
    for sheet_name in SHEETS:
        file_path = './xls/'+sheet_name+"_"+qcode+'.xls'
        if os.path.exists(file_path):
            raw_sheet.append(sheet_name+"_"+qcode)
    return raw_sheet

# 设置excel文件宽度


def set_column_width(exceL_path, width):
    # 打开 Excel 文件
    workbook = openpyxl.load_workbook(exceL_path)

    # 选择第一个工作表
    worksheet = workbook.active

    # 设置第一列的宽度，单位为字符宽度
    worksheet.column_dimensions['A'].width = width

    # 保存更改后的 Excel 文件
    workbook.save(exceL_path)

# 将xlsx文件合并为一个CODE.xlsx文件


def merge_excels(raw_sheet,merged_excel):
    # 文件列表，包含您要合并的 Excel 文件名
    files = ["./xlsx/"+sheet_name+".xlsx" for sheet_name in raw_sheet]
    # 创建一个空的 DataFrame，用于存储合并后的数据
    merged_data = pd.DataFrame()
    # 遍历文件列表，读取每个文件并将其添加到 merged_data
    for idx, file in enumerate(files):
        data = pd.read_excel(file, header=None)  # 不将第一行作为 header
        if idx > 0:
            # 在合并时，在不同表之间插入空行
            empty_row = pd.DataFrame(columns=data.columns, index=[0])
            merged_data = pd.concat(
                [merged_data, empty_row, data], axis=0, ignore_index=True)
        else:
            merged_data = pd.concat(
                [merged_data, data], axis=0, ignore_index=True)

    # 将合并后的数据保存到一个新的 Excel 文件中
    merged_data.to_excel(merged_excel, index=False, header=False)

# 将excel数据格式化成map的格式

def g_map_data(excel_path):
    # 读取.xlsx文件
    df = pd.read_excel(excel_path, engine='openpyxl')

    row_arrays = [row.to_numpy() for index, row in df.iterrows()]
    dfl = df.columns.tolist()
    excel_map = { 
        dfl[0]: dfl[1:] #Year: [ 1999 2000 ... ]
    }

    # 打印转换后的数组
    for row in row_arrays:
        excel_map[row[0]] = row[1:]

    return excel_map

