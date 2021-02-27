#!/usr/bin/env python
# -*- coding:utf-8 -*-
from selenium.webdriver.chrome.options import Options
from datetime import datetime, date, timedelta
from selenium.webdriver import ChromeOptions
from multiprocessing.dummy import Pool
from selenium import webdriver
from lxml import etree
import requests
import re, csv
import time


def time_day():
    """一年的url"""
    url_list = []
    for i in range(1,366+31+26):  #
        yesterday = str(date.today() + timedelta(days = -i-1))
        yesterdays = yesterday.replace('-','')
        urls = "http://bf.win007.com/football/Over_"+yesterdays+".htm"
        url_list.append(urls)
    print(url_list)
    return url_list


def _write_log(name, txt, s, log_path, len_data=0):
    with open('./logs/{}/{}.txt'.format(log_path, name), 'a', encoding='utf-8') as f:
        if s == 1:
            f.write('采集开始'+txt+'\n')
        elif s == 2:
            f.write('结束采集,满足条件计入数据\n')
            f.write('剩余'+str(len_data)+'场比赛\n')
        elif s == 3:
            f.write('结束采集,未满足条件\n')
            f.write('剩余' + str(len_data) + '场比赛\n')
        elif s == 4:
            f.write('该链接抓取失败,尝试重抓\n')
            f.write('剩余' + str(len_data) + '场比赛\n')
        elif s == 5:
            f.write('该链接页面为空白\n')
            f.write('剩余' + str(len_data) + '场比赛\n')


def _get_page(new_url):
    """打开页面，返回html"""
    # driver = webdriver.Chrome()
    # driver.set_page_load_timeout(10)
    # driver.get(new_url)
    # page_text = driver.page_source
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'}
    r = requests.get(new_url, timeout=10)
    r.encoding = r.apparent_encoding
    page_text = r.text
    print(page_text)
    if page_text:
        print(1)
    else:
        print(2)
    return page_text
_get_page('http://vip.win007.com/AsianOdds_n.aspx?id=1838246')

def first_login(url, csv_path, log_path):
    log_name = url[-12:-4]
    print("开始采集{}数据".format(log_name))
    with open('./logs/{}/{}.txt'.format(log_path, log_name), 'w', encoding='utf-8') as f:
        f.write("开始采集{}数据{}\n".format(log_name, str(datetime.now())))
    page_text = _get_page(url)
    # print(page_text)
    # reobj = re.compile(
    #     r'<tr height="18" align="center" bgcolor="[\d\D]*?" id="tr1_\d+" name="\d+,\d+" infoid="\d+">[\d\D]*?<a href="javascript:" onclick="AsianOdds\(([\d\D]*?)\)"[\d\D]*?>亚</a>[\d\D]*?</tr>',re.MULTILINE)
    reobj = re.compile(
        r"<tr height=18 align=center bgColor=[\d\D]*? id='tr1_\d+' name='\d+,\d+' infoid='\d+'>[\d\D]*?<a href=javascript: onclick='AsianOdds\(([\d\D]*?)\)' style='margin-left:3px;'>亚</a>[\d\D]*?</tr>", re.MULTILINE)
    num_list = reobj.findall(page_text)
    # print(num_list)
    num_list2 = ['http://vip.win007.com/AsianOdds_n.aspx?id={}'.format(i)\
                  for i in num_list]  # 单场比赛页面
    # print(len(num_list2))
    _second_login(num_list2, url, log_name, csv_path, log_path)
    with open('./logs/{}/{}.txt'.format(log_path, log_name), 'a', encoding='utf-8') as f:
        f.write("结束采集{}\n".format(str(datetime.now())))
    return None


def _second_login(num_list2, date_url, log_name, csv_path, log_path):
    boolen = False
    while num_list2:
        url = num_list2.pop(0)
        _write_log(log_name, url, 1, log_path)
        try:
            html = _get_page(url)
            if html:
                tree = etree.HTML(html)
                time1 = tree.xpath('//div[@class="vs"]/div[1]/text()')
                time1 = ''.join(time1).strip().split(' ')[0].replace('-','.')
                data = [date_url, url, time1]
                tr_list = tree.xpath('//*[@id="odds"]/tr')
                for tr in tr_list:
                    # print(tr.xpath('./td[1]/text()'))
                    if tr.xpath('./td[1]/text()') == ['Crown']:
                        cpyp = tr.xpath('./td[4]/text()')  # 初盘亚盘
                        zpyp = tr.xpath('./td[10]/text()')  # 终盘亚盘
                        if cpyp == ['平手'] or cpyp == ['平手/半球'] or cpyp == ['受让平手/半球']:
                            boolen = True
                            # 联赛名
                            LName = tree.xpath('//a[@class="LName"]/text()')[0].strip()
                            data.append(LName)
                            # 主场球队
                            home = tree.xpath('//*[@class="header"]//*[@class="home"]/a/text()')[0]
                            home = home.split(' ')[0]
                            data.append(home)
                            # 客场球队
                            guest = tree.xpath('//*[@class="header"]//*[@class="guest"]/a/text()')[0]
                            guest = guest.strip()
                            data.append(guest)
                            # 终盘亚盘水位
                            zpypsw = tr.xpath('./td[9]/text()')[0] + '/' + tr.xpath('./td[11]/text()')[0]
                            data.append(cpyp[0])
                            data.append(zpyp[0])
                            data.append(zpypsw)
                            break
                if boolen:
                    boolen = False
                    size = tree.xpath('//*[@id="odds_menu"]/li[3]/a/@href')[0]
                    new_url = 'http://vip.win007.com' + size  # 转到大小页面
                    size_html = _get_page(new_url)
                    size_tree = etree.HTML(size_html)
                    tr_list2 = size_tree.xpath('//*[@id="odds"]/tr')
                    for tr in tr_list2:
                        if tr.xpath('./td[1]/text()') == ['Crown']:
                            cp = tr.xpath('./td[4]/text()')  # 初盘大球盘口
                            zp = tr.xpath('./td[10]/text()')  # 终盘大球盘口
                            if cp == ['2.5'] and zp == ['2.5/3'] or \
                                    cp == ['2.5/3'] and zp == ['3']:
                                boolen = True
                                # 终盘大球水位
                                zpdqsw = tr.xpath('./td[9]/text()')[0] + '/' + tr.xpath('./td[11]/text()')[0]
                                data.append(cp[0])
                                data.append(zp[0])
                                data.append(zpdqsw)
                                break
                if boolen:
                    """满足两个条件后记录数据"""
                    boolen = False
                    id = re.search(r'http://vip\.win007\.com/AsianOdds_n\.aspx\?id=(.*)', url).group(1)
                    new_url2 = 'http://vip.win007.com/changeDetail/overunder.aspx?id={}&companyID=3&l=0'.format(id)
                    # 进到大小球变化表
                    new_html = etree.HTML(_get_page(new_url2))
                    tr_list3 = new_html.xpath('//*[@id="odds2"]/table/tr')
                    fen = False
                    for tr in tr_list3:
                        if tr.xpath('./td[1]/text()') == ['中场']:
                            if tr.xpath('./td[3]//b/text()') != ['封']:
                                # 中场大小盘
                                zcdxp = tr.xpath('./td[4]/font/text()')[0]
                                # 中场大球水位
                                zcdqsw = tr.xpath('./td[3]//b/text()')[0] + '/' + tr.xpath('./td[5]//b/text()')[0]
                                # 上半场进球
                                if not fen:
                                    sjq = tr.xpath('./td[2]/text()')[0].split('-')
                                    sjq = int(sjq[0]) + int(sjq[1])
                                data.append(zcdxp)
                                data.append(zcdqsw)
                                data.append(sjq)
                                break
                            else:
                                # 上半场进球
                                fen = True
                                sjq = tr.xpath('./td[2]/text()')[0].split('-')
                                sjq = int(sjq[0]) + int(sjq[1])
                    # 最终进球数
                    tr = tr_list3[1]
                    if tr.xpath('./td[2]/text()'):
                        zzjqs = tr.xpath('./td[2]/text()')[0].split('-')
                        zzjqs = int(zzjqs[0]) + int(zzjqs[1])
                    else:
                        zzjqs = '大小球变化表没有时间和比分'
                    data.append(zzjqs)
                    # 75分钟80分钟后进球数
                    s = True
                    for tr in tr_list3:
                        if tr.xpath('./td[1]/text()'):
                            if int(tr.xpath('./td[1]/text()')[0]) <= 80 and s:
                                # 80分钟进球数
                                s = False
                                jqs80 = tr.xpath('./td[2]/text()')[0].split('-')
                                jqs80 = int(jqs80[0]) + int(jqs80[1])
                            if int(tr.xpath('./td[1]/text()')[0]) <= 75:
                                # 75分钟进球数
                                jqs75 = tr.xpath('./td[2]/text()')[0].split('-')
                                jqs75 = int(jqs75[0]) + int(jqs75[1])
                                after80 = zzjqs - jqs80
                                after75 = zzjqs - jqs75
                                data.append(after75)
                                data.append(after80)
                                break
                    _write_csv(data, csv_path)
                    _write_log(log_name, url, 2, log_path, len(num_list2))
                else:
                    print('没满足条件')
                    _write_log(log_name, url, 3, log_path, len(num_list2))
                print(data)
                print(len(num_list2))
                time.sleep(1)
            else:
                print('该页面为无内容')
                _write_log(log_name, url, 5, log_path, len(num_list2))
        except Exception as e:
            print(e)
            num_list2.insert(0, url)
            print(len(num_list2))
            print(url, '该链接抓取失败')
            _write_log(log_name, url, 4, log_path, len(num_list2))
            time.sleep(60)
    return None


def _write_csv(data, csv_path):
    """将数据写入csv"""
    with open(csv_path, 'a', encoding='utf_8_sig', newline='') as f:
        data = [str(i)+'\t' for i in data]
        w = csv.writer(f)
        w.writerow(data)


def create_csv(csv_path):
    """创建存储数据的csv"""
    with open(csv_path, 'w', encoding='utf_8_sig', newline='') as f:
        f.write('当日链接,比赛详情链接,日期,联赛名,主队,客队,初盘亚盘,终盘亚盘,终盘亚盘水位,初盘大球盘口,终盘大球盘口,终盘大球水位,中场大小盘,中场大球水位,上半场进球数,最终进球数,75分钟后进球数,80分钟后进球数\n')


def main(url_list, csv_path, log_path):
    create_csv(csv_path)
    for url in url_list:
        first_login(url, csv_path, log_path)



