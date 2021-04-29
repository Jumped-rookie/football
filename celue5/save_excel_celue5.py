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
    a = ['当日链接', '比赛详情链接', '日期', '联赛名', '主队', '客队', '竞彩主胜初赔', '竞彩平局初赔', '竞彩客胜初赔', '竞彩主胜终赔', '竞彩平局终赔', '竞彩客胜终赔', 'inter主胜初赔', 'inter平局初赔', 'inter客胜初赔', 'inter主胜终赔', 'inter平局终赔', 'inter客胜终赔', '主胜是否有凯利≥1', '客胜是否有凯利≥1', 'Crown终盘让球', 'Crown终盘让球主赔', 'Crown终盘让球客赔', '赛果', '首先进球球队', '比分']
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
    work_book.save('celue5.xls')
file = './data'
walkFile(file)





