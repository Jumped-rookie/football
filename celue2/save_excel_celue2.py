#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from lxml import etree
import re, csv
import time
import xlwt




def walkFile(file):
    data = []
    work_book = xlwt.Workbook()
    work_sheet = work_book.add_sheet('Test')
    
    for root, dirs, files in os.walk(file):
        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list      
        
        # 遍历文件
        for f in files:
            csv_file = os.path.join(root, f)
            with open(csv_file, encoding='utf-8') as f:
                for line in f.readlines()[1:]:
                    l = [i for i in line.split(',')]
                    # print(line)
                    data.append(line)
    # 写入第一行
    a = ['当日链接', '比赛详情链接', '日期', '开赛时间', '联赛名', '主队', '客队', '威廉希尔凯利胜', '威廉希尔凯利平', '威廉希尔凯利负', '威廉希尔初盘返还率', '威廉希尔终盘返还率', '威廉希尔变化时间', '伟德凯利胜', '伟德凯利平', '伟德凯利负', '伟德初盘返还率', '伟德终盘返还率', '伟德变化时间', '易胜博凯利胜', '易胜博凯利平', '易胜博凯利负', '易胜博初盘返还率', '易胜博终盘返还率', '易胜博变化时间', 'interwetten凯利胜', 'interwetten凯利平', 'interwetten凯利负', 'interwetten初盘返还率', 'interwetten终盘返还率', 'interwetten变化时间', '伟德主胜初赔', '伟德主胜终赔', '伟德平赔初赔', '伟德平赔终赔', '伟德客胜初赔', '伟德客胜终赔', '最终赛果', '初盘亚盘（Crown）', '终盘亚盘（Crown）', '首先进球方']
    for i in range(len(a)):
        work_sheet.write(0,i,a[i])
    # 写入数据
    x = 1  # 行 从第二行开始
    for info in range(len(data)):
        y = 0  # 列
        line = data[info].split(',')
        for i in range(len(line)):
            # print(line[i])
            work_sheet.write(x, y, line[i].strip().strip(r'\t'))
            y += 1
        x += 1
    work_book.save('celue2.xls')
file = './data'
walkFile(file)





