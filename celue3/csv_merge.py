import os
import re, csv
import time

def walkFile(file):
    data = []
    for root, dirs, files in os.walk(file):

        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list
        with open('celue3.csv', 'w', encoding='utf_8_sig', newline='') as fc:
            fc.write(
            '当日链接,比赛详情链接,日期,联赛名,主队,客队,初盘亚盘,终盘亚盘,终盘亚盘水位,初盘大球盘口,终盘大球盘口,终盘大球水位,中场大小盘,中场大球水位,上半场进球数,最终进球数,下半场75前进球数,75分钟后进球数,80分钟后进球数\n')
            # 遍历文件
            for f in files:
                csv_file = os.path.join(root, f)
                with open(csv_file, encoding='utf-8') as f:
                    for line in f.readlines()[1:]:
                        # print([i for i in line.split(',')])
                        # print(line)
                        fc.write(line)
file = './data'
walkFile(file)