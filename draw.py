
import os
import matplotlib.pyplot as plt
import numpy as np
from config import FGHEIGHT, FGWIDTH, Define_Colors, FGDPI

hasPercent = False
# 根据计算结果绘制图像


def draw_plot(dict_map_data, pic_name, qcode):
    if hasPercent:
        for key, value in dict_map_data.items():
            dict_map_data[key] = value[1:]

    # 获取 x 轴数据
    x = dict_map_data['Year']
    plt.figure(figsize=(FGWIDTH, FGHEIGHT), dpi=FGDPI)

    # 绘制折线图
    color_index = 0
    for key, y in dict_map_data.items():
        color = Define_Colors[color_index]
        color_index += 1
        if key != 'Year':
            plt.plot(x, y, label=key, linewidth=1.5,
                     marker='o', linestyle='solid', color=color)
        for a, b in zip(x, y):
            plt.annotate(b, xy=(a, b), xytext=(a-0.1, b+0.14))

    bwith = 1  # 边框宽度设置为2
    ax = plt.gca()  # 获取边框
    # 设置边框
    ax.spines['bottom'].set_linewidth(bwith)  # 图框下边
    ax.spines['left'].set_linewidth(bwith)  # 图框左边
    ax.spines['top'].set_linewidth(bwith)  # 图框上边
    ax.spines['right'].set_linewidth(bwith)  # 图框右边

    # 显示网格线
    # plt.grid(True)
    pic_name = "L_"+qcode+"_"+pic_name
    # 设置 x 轴的刻度，显示每个年份的数值
    plt.xticks(x)
    plt.title(pic_name)

    # 添加图例
    plt.legend()

    # 显示图形
    # plt.show()
    dirname = "draw/"
    # 保存为图片
    os.makedirs(dirname, exist_ok=True)

    file_name = dirname+pic_name+".png"
    plt.savefig(file_name, bbox_inches='tight')

    print("Save Picture: " + file_name)

# 遍历公式对象里所有的公式，得出的数据是 {key: [...]} 形式


def draw_stack_bar(data, x_labels, pic_name, qcode, is_percent=False):
    N = len(data[list(data.keys())[0]])  # 数据中的样本数量
    ind = np.arange(N)  # 组位置
    width = 0.35  # 条形图的宽度

    bottoms = np.zeros(N)
    bars = []
    bottoms = np.where(np.isnan(bottoms), 0, bottoms)

    # 预定义颜色列表

    # 使用预定义的颜色列表替换原来的颜色列表
    colors = Define_Colors[:len(data)]

    plt.figure(figsize=(FGWIDTH, FGHEIGHT), dpi=FGDPI)

    # 绘制堆积柱状图并添加数据标签
    for idx, (category, values) in enumerate(list(data.items())):
        for i, v in enumerate(values):
            if  isinstance(v, int) or isinstance(v, float):
                values[i] = abs(v)
            elif np.nan(v):
                values[i] = 0

        bar = plt.bar(ind, values, width, bottom=bottoms,
                      color=colors[len(data) - idx - 1])
        bars.append(bar[0])  # 只添加第一个矩形作为图例的代表

        for i, (rect, value) in enumerate(zip(plt.bar(ind, values, width, bottom=bottoms, color=colors[len(data) - idx - 1]), values)):
            plt.text(rect.get_x() + rect.get_width() / 2,
                     bottoms[i] + value / 2, f'{value}', ha='center', va='bottom')

        bottoms = np.add(bottoms, values)

    # 添加 x 轴标签
    pic_name = "S_"+qcode+"_"+pic_name
    if is_percent:
        plt.title(pic_name + "%")
    else:
        plt.title(pic_name)

    plt.xticks(ind, x_labels)
    max_high = int(np.max(bottoms))

    min_high = 0

    step = 1

    if all(x > 0 for x in bottoms):
        min_high = 0
        step = round((max_high)/10)
    else:
        int(np.min(bottoms))
        step=1


    plt.yticks(np.arange(min_high, max_high + 1, step))
    plt.legend(reversed(bars), reversed(data.keys()))

    # 显示图形
    # plt.show()

    file_name='draw/'+pic_name+".png"
    os.makedirs('draw/', exist_ok = True)
    print("Save Picture: " + file_name)
    plt.savefig(file_name, bbox_inches = 'tight')
