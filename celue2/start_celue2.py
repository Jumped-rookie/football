#!/usr/bin/env python
# -*- coding:utf-8 -*-
from datetime import datetime, date, timedelta
import celue2
import os

months = ['202001', '202002', '202003', '202004', '202005',
          '202006', '202007']  # 选择要爬取的月份,该月在url_list中存在

day31 = ['01','03','05','07','08','10','12']
day30 = ['04','06','09','11']

url_list = []

def create_day(month, days):
      url = []
      for i in range(1, days+1):
            if i < 10:
                  day = '0' + str(i)
            else:
                  day = str(i)
            url.append(month + day)
      return url


def pd_rn(year):
      """判断是不是闰年"""
      year = int(year)
      if (year % 4) == 0:
         if (year % 100) == 0:
             if (year % 400) == 0:
                 return True   # 整百年能被400整除的是闰年
             else:
                 return False
         else:
             return True       # 非整百年能被4整除的为闰年
      else:
         return False
      
for month in months:
      m = month[-2:]
      if m in day31:
            # 该月有31天
            url = create_day(month, 31)
            url_list += url
            pass
      elif m in day30:
            # 该月有30天
            url = create_day(month, 30)
            url_list += url
      else:
            # 2月
            year = month[:4]
            # 判断是不是闰年
            result = pd_rn(year)
            if result:
                 # 是闰年
                  url = create_day(month, 29)
                  url_list += url
            else:
                  # 不是闰年 
                  url = create_day(month, 28)
                  url_list += url
                  
date_dict = {}
for i in url_list:
    key = i[:6]
    date_dict.setdefault(key, [])
    date_dict[key].append(i)




for i in months:
    urls = []
    month = date_dict[i]
    for j in month:
        url = "http://bf.win007.com/football/Over_" + j + ".htm"
        urls.append(url)
    # print(urls)
    isExists = os.path.exists('./data')
    if not isExists:
        os.makedirs('./data')
    csv_path = './data/{}.csv'.format(i)
    # print(csv_path)
    isExists = os.path.exists('./logs/{}'.format(i))
    if not isExists:
        os.makedirs('./logs/{}'.format(i))
    celue2.main(urls, csv_path, i)
