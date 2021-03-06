#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from lxml import etree
import re, csv
import time

def walkFile(file):
    data = []
    for root, dirs, files in os.walk(file):

        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list
        with open('data2.csv', 'w', encoding='utf_8_sig', newline='') as fc:
            fc.write(
                '当日链接,比赛详情链接,日期,联赛名,主队,客队,初盘亚盘,终盘亚盘,终盘亚盘水位,初盘大球盘口,终盘大球盘口,终盘大球水位,中场大小盘,中场大球水位,上半场进球数,最终进球数,75分钟后进球数,80分钟后进球数\n')
            # 遍历文件
            for f in files:
                csv_file = os.path.join(root, f)
                with open(csv_file, encoding='utf-8') as f:
                    for line in f.readlines()[1:]:
                        print([i for i in line.split(',')])
                        print(line)
                        fc.write(line)
# file = './data'
# walkFile(file)
def _get_page(new_url):
    """打开页面，返回html"""
    # 实现无可视化界面的操作
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(chrome_options=chrome_options)  # 参数添加
    driver.set_page_load_timeout(10)
    driver.get(new_url)
    page_text = driver.page_source
    driver.quit()
    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'}
    # r = requests.get(new_url, timeout=10)
    # r.encoding = r.apparent_encoding
    # page_text = r.text
    return page_text

def _second_login(num_list2, date_url):
    boolen = False
    while num_list2:
        url = num_list2.pop(0)
        try:
            html = _get_page(url)
            if html != '<html><head></head><body></body></html>':
                tree = etree.HTML(html)
                time1 = tree.xpath('//div[@class="vs"]/div[1]/text()')
                time1 = ''.join(time1).strip().split(' ')[0].replace('-','.')
                data = [date_url, url, time1]
                tr_list = tree.xpath('//*[@id="odds"]//tr')
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
                    tr_list2 = size_tree.xpath('//*[@id="odds"]//tr')
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
                    tr_list3 = new_html.xpath('//*[@id="odds2"]/table//tr')
                    nozc = True
                    zcdxp = ''
                    zcdqsw= ''
                    sjq = ''
                    if tr_list3:
                        fen = False
                        for tr in tr_list3:
                            # print(tr.xpath('./td[1]/text()'))
                            if tr.xpath('./td[1]/text()') == ['中场']:
                                if tr.xpath('./td[3]//b/text()') != ['封']:
                                    # 中场大小盘
                                    zcdxp = tr.xpath('./td[4]/font/text()')[0]
                                    # print(zcdxp)
                                    # 中场大球水位
                                    zcdqsw = tr.xpath('./td[3]//b/text()')[0] + '/' + tr.xpath('./td[5]//b/text()')[0]
                                    # 上半场进球
                                    if not fen:
                                        sjq = tr.xpath('./td[2]/text()')[0].split('-')
                                        sjq = int(sjq[0]) + int(sjq[1])
                                    nozc = False
                                    break
                                else:
                                    # 上半场进球
                                    fen = True
                                    sjq = tr.xpath('./td[2]/text()')[0].split('-')
                                    sjq = int(sjq[0]) + int(sjq[1])
                        if nozc:
                            no45 = True
                            for tr in tr_list3:
                                if tr.xpath('./td[1]/text()'):
                                    if tr.xpath('./td[1]/text()') != ['中场'] and int(tr.xpath('./td[1]/text()')[0]) == 45:
                                        if tr.xpath('./td[3]//b/text()') != ['封']:
                                            # 中场大小盘
                                            zcdxp = tr.xpath('./td[4]/font/text()')[0]
                                            # print(zcdxp)
                                            # 中场大球水位
                                            zcdqsw = tr.xpath('./td[3]//b/text()')[0] + '/' + tr.xpath('./td[5]//b/text()')[0]
                                            # 上半场进球
                                            if not fen:
                                                sjq = tr.xpath('./td[2]/text()')[0].split('-')
                                                sjq = int(sjq[0]) + int(sjq[1])
                                            data.append(zcdxp)
                                            data.append(zcdqsw)
                                            data.append(sjq)
                                            no45 = False
                                            break
                        else:
                            data.append(zcdxp)
                            data.append(zcdqsw)
                            data.append(sjq)
                        if nozc and no45:
                            data.append('没有中场和45')
                        # 最终进球数
                        tr = tr_list3[1]
                        if tr.xpath('./td[2]/text()'):
                            zzjqs = tr.xpath('./td[2]/text()')[0].split('-')
                            zzjqs = int(zzjqs[0]) + int(zzjqs[1])
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
                        else:
                            data.append('没有中场和45')
                            zzjqs = '大小球变化表没有时间和比分'
                            notimeurl = 'http://live.win007.com/detail/{}cn.htm'.format(id)
                            eh = etree.HTML(_get_page(notimeurl))
                            trs = eh.xpath('.//*[@id="teamEventDiv_detail"]//tr')
                            # 最终进球数
                            if len(trs) > 1:
                                tr = trs[1]
                                zzjqs = int(tr.xpath('./td[1]//text()')[0]) + int(tr.xpath('./td[3]//text()')[0])
                                sjq = 0  # 上半场进球数
                                jqs80 = 0  # 80分钟后进球
                                jqs75 = 0  # 75分钟后进球
                                for i in trs[2:]:
                                    if i.xpath('./td[2]/text()') == ['点球']:
                                        break
                                    else:
                                        jq = i.xpath('./td[2]/img/@title')
                                        jq2 = i.xpath('./td[4]/img/@title')
                                        if jq == ['入球'] or jq == ['点球'] or jq == ['乌龙'] or\
                                        jq2 == ['入球'] or jq2 == ['点球'] or jq2 == ['乌龙']:
                                            jqtime = i.xpath('./td[3]//text()')[0][:-1]
                                            if '+' not in jqtime:
                                                jqtime = int(jqtime)
                                            elif '+' in jqtime:
                                                jqtime = int(jqtime.split('+')[0])
                                            if jqtime <= 45:
                                                sjq += 1
                                            if jqtime > 75:
                                                jqs75 += 1
                                            if jqtime > 80:
                                                jqs80 += 1
                                data.append(sjq)
                                data.append(zzjqs)
                                data.append(jqs75)
                                data.append(jqs80)
                            else:
                                print('没有详细事件')
                                data.append('没有详细事件')

                    else:
                        print('无大小球变化表')
                else:
                    print('没满足条件')
                print(data)
                print(len(num_list2))
                time.sleep(1)
                return data
            else:
                print('该页面为无内容')
        except Exception as e:
            print(e)
            num_list2.insert(0, url)
            print(len(num_list2))
            print(url, '该链接抓取失败')
            time.sleep(60)


# _second_login(['http://vip.win007.com/AsianOdds_n.aspx?id=1793722'],'http://vip.win007.com/AsianOdds_n.aspx?id=1793722')
with open('data2.csv', 'r', encoding='utf_8_sig') as fr:
    with open('data6.csv', 'w', encoding='utf_8_sig', newline='') as fw:
        data = []
        for line in fr.readlines():
            l = [i for i in line.split(',')]
            if len(l) == 15 or len(l) == 13:
                print(l)
                date_url = l[0]
                url = [l[1].strip()]
                result = _second_login(url, date_url)
                result2 = [str(i) + '\t' for i in result]
                w = csv.writer(fw)
                w.writerow(result2)
            elif len(l) == 18:
                fw.write(line)





