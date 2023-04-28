```
create: 2023/04/27
update: 2023/04/27
author: zendu
descri: 计算Choice导出的报表，并生成相关图像
```

# show
![](./imgs/L_600436_%E5%88%A9%E6%B6%A6%E7%9B%B8%E5%85%B3.png)
![](./imgs/L_600436_%E8%A7%84%E6%A8%A1%E5%A2%9E%E9%95%BF.png)
![](./imgs/L_600436_%E8%B4%B9%E7%94%A8%E7%9B%B8%E5%85%B3.png)
![](./imgs/S_600436_%E8%B5%84%E4%BA%A7%E7%BB%86%E5%88%86.png)


# step
1. 从choice里导出三张财务报表年表，按年排序
2. 放入xls文件夹
3. 执行`run.bat(windows)`文件
4. 在`config.py`中配置计算公式，公式的字面量是excel的第一列的值
5. 在`draw/`文件夹中查看效果图，会合并一个干净的xlsx文件在根目录下




# explain

1. 将Choice导出的xls文件处理，导出为xlsx文件
    1. 过滤不必要的字段，如`公告日期`
    2. 删除不需要的内容，如`(亿元)`、`年年报`
2. 将多个xlsx合并为一个
    3. 选择第一列和最后N列（排除三表年不同步的情况）
    4. 不同文件之间用空行隔开
    5. 垂直堆叠合并
3. 计算Excel
    1. 读取合并的xlxs文件，转化为map的形式，如`{year: [1999,2000],data: [0,-1]}`
    2. 对象的加减乘除和常熟运算，如列出公式：
        `毛利率=营业总收入/营业成本`，计算对象:`{营业总收入：[...],营业成本:[...]}`中两数组相除
    3. 将运算结果绘制成图标并保存为图片







### RUN

配置config.py

-   CODE是股票代码，也是最后生成的xlsx文件名
-   FIELDS_To_REMOVE 是需要过滤的Excel行元素
-   SHEETS是需要处理的报表
-   Limit_Year是需要截取的时间长度，有些报表存在比如：资产负债表时间区间为`1990~2023`，但利润表的时间区间可能是`1993~2023`，不重叠，需要截取
-   FORMULAS是核心功能，用于计算Excel数据，等号右边是CODE.xlsx里的第一列的值



```
pip3 install -r requirements
python3 main.py
```

