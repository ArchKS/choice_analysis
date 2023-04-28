
import os
import pandas as pd
import matplotlib.pyplot as plt
import packaging.version
import shutil
import platform

# 设置全局字体
# from matplotlib.font_manager import FontProperties
# font = FontProperties(fname='./font/msyh.ttf')
#   # 使用黑体作为中文字体
os_name = platform.system()
if os_name == "Windows":
    plt.rcParams['font.sans-serif'] = ['SimHei']
elif os_name == "Darwin":
    plt.rcParams["font.family"] = 'Arial Unicode MS'
else:
    print("This is not a Windows or macOS system.")


plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号



# 获取pandas的格式化模型，用于处理header的默认字体加粗

# 获取padans的格式化模块，用于处理单元格文本粗细、字体字号等
def get_format_module():
    version = packaging.version.parse(pd.__version__)
    if version < packaging.version.parse('0.18'):
        return pd.core.format
    elif version < packaging.version.parse('0.20'):
        return pd.formats.format
    else:
        return pd.io.formats.excel.ExcelFormatter

# 移动文件 xls/xlsx
def move_file(qcode):
    print("Move File")
    # 获取当前目录下的文件列表
    files = os.listdir()

    # 确保目标目录存在
    os.makedirs('xls', exist_ok=True)
    os.makedirs('xlsx', exist_ok=True)

    # 遍历文件列表，查找以 .xls 结尾的文件
    for file in files:
        if file == qcode + '.xlsx':
            a = 1
        elif file.endswith('.xls'):
            # 将文件移动到 'xls' 目录
            shutil.move(file, os.path.join('xls', file))
        elif file.endswith('.xlsx'):
            shutil.move(file, os.path.join('xlsx', file))
