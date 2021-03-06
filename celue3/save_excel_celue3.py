import os
import re, csv
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
    a = ['当日链接', '比赛详情链接', '日期', '联赛名', '主队', '客队', '初盘亚盘', '终盘亚盘', '终盘亚盘水位', '初盘大球盘口', '终盘大球盘口', '终盘大球水位', '中场大小盘', '中场大球水位', '上半场进球数', '最终进球数', '下半场75前进球数', '75分钟后进球数', '80分钟后进球数']
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
    work_book.save('celue3.xls')
file = './data'
walkFile(file)