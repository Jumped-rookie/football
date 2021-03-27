#!/usr/bin/env python
# -*- coding:utf-8 -*-
from selenium.webdriver.chrome.options import Options
from datetime import datetime, date, timedelta
from selenium import webdriver
from lxml import etree
import requests
import re, csv
import time
from selenium.webdriver.chrome.service import Service

def _write_log(name, txt, s, log_path, len_data=0):
    with open('./logs/{}/{}.txt'.format(log_path, name), 'a', encoding='utf-8') as f:
        if s == 1:
            f.write('采集开始'+txt+'\n')
        elif s == 2:
            f.write('结束采集,满足条件计入数据\n')
            f.write('剩余'+str(len_data)+'场比赛\n')
        elif s == 3:
            f.write('结束采集,比赛75分钟前没有发生6个进球\n')
            f.write('剩余' + str(len_data) + '场比赛\n')
        elif s == 4:
            f.write('该链接抓取失败,尝试重抓\n')
            f.write('剩余' + str(len_data) + '场比赛\n')
        elif s == 5:
            f.write('没有详细事件\n')
            f.write('剩余' + str(len_data) + '场比赛\n')


def _get_page(new_url):
    """打开页面，返回html"""
    # 实现无可视化界面的操作
    c_service = Service(r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
    c_service.command_line_args()
    c_service.start()
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('blink-settings=imagesEnabled=false')
    driver = webdriver.Chrome(chrome_options=chrome_options)  # 参数添加
    driver.set_page_load_timeout(10)
    driver.get(new_url)
    time.sleep(1)
    page_text = driver.page_source
    driver.quit()
    c_service.stop()
    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 SaWfari/537.36'}
    # r = requests.get(new_url, timeout=10)
    # r.encoding = r.apparent_encoding
    # page_text = r.text
    return page_text


def _go_daxiaoqiu(id):
    zcdxp = ''
    zcdqsw = ''
    sjq = ''
    url = 'http://vip.win007.com/changeDetail/overunder.aspx?id={}&companyID=3&l=0'.format(id)
    html = etree.HTML(_get_page(url))
    tr_list3 = html.xpath('//*[@id="odds2"]/table//tr')
    sj = html.xpath('//*[@id="odds2"]/table//tr/td[1]/text()')
    if tr_list3:
        if '中场' in sj:
            zcdxp, zcdqsw, sjq = _get_zcdata(tr_list3)
            if not zcdxp:
                if '45' in sj:
                    zcdxp, zcdqsw, sjq = _get_45data(tr_list3)
                    if not zcdxp:
                        if '46' in sj:
                            zcdxp, zcdqsw, sjq = _get_46data(tr_list3)
                elif '46' in sj:
                    zcdxp, zcdqsw, sjq = _get_46data(tr_list3)
        elif '45' in sj:
            zcdxp, zcdqsw, sjq = _get_45data(tr_list3)
            if not zcdxp:
                if '46' in sj:
                    zcdxp, zcdqsw, sjq = _get_46data(tr_list3)
        elif '46' in sj:
            zcdxp, zcdqsw, sjq = _get_46data(tr_list3)
        return [zcdxp, zcdqsw, sjq]
    else:
        print('无大小球变化表')
        return ['无大小球变化表', '无大小球变化表', '无大小球变化表']


def _get_zcdata(tr_list3):
    zcdxp = ''
    zcdqsw = ''
    sjq = ''
    for tr in tr_list3:
        if tr.xpath('./td[1]/text()') == ['中场']:
            if tr.xpath('./td[3]//b/text()') != ['封']:
                # 中场大小盘
                zcdxp = tr.xpath('./td[4]/font/text()')[0]
                # print(zcdxp)
                # 中场大球水位
                zcdqsw = tr.xpath('./td[3]//b/text()')[0] + '/' + tr.xpath('./td[5]//b/text()')[0]
                # 上半场进球
                sjq = tr.xpath('./td[2]/text()')[0].split('-')
                sjq = int(sjq[0]) + int(sjq[1])
                break
    return [zcdxp, zcdqsw, sjq]


def _get_45data(tr_list3):
    zcdxp = ''
    zcdqsw = ''
    sjq = ''
    for tr in tr_list3:
        if tr.xpath('./td[1]/text()') == ['45']:
            if tr.xpath('./td[3]//b/text()') != ['封']:
                # 中场大小盘
                zcdxp = tr.xpath('./td[4]/font/text()')[0]
                # print(zcdxp)
                # 中场大球水位
                zcdqsw = tr.xpath('./td[3]//b/text()')[0] + '/' + tr.xpath('./td[5]//b/text()')[0]
                # 上半场进球
                sjq = tr.xpath('./td[2]/text()')[0].split('-')
                sjq = int(sjq[0]) + int(sjq[1])
                break
    return [zcdxp, zcdqsw, sjq]


def _get_46data(tr_list3):
    zcdxp = ''
    zcdqsw = ''
    sjq = ''
    for tr in tr_list3:
        if tr.xpath('./td[1]/text()') == ['46']:
            if tr.xpath('./td[3]//b/text()') != ['封']:
                # 中场大小盘
                zcdxp = tr.xpath('./td[4]/font/text()')[0]
                # print(zcdxp)
                # 中场大球水位
                zcdqsw = tr.xpath('./td[3]//b/text()')[0] + '/' + tr.xpath('./td[5]//b/text()')[0]
                # 上半场进球
                sjq = tr.xpath('./td[2]/text()')[0].split('-')
                sjq = int(sjq[0]) + int(sjq[1])
    return [zcdxp, zcdqsw, sjq]


def _go_xiangxishijian(id):
    notimeurl = 'http://live.win007.com/detail/{}cn.htm'.format(id)
    eh = etree.HTML(_get_page(notimeurl))
    trs = eh.xpath('.//*[@id="teamEventDiv_detail"]//tr')
    if len(trs) > 1:
        tr = trs[1]
        zzjqs = int(tr.xpath('./td[1]//text()')[0]) + int(tr.xpath('./td[3]//text()')[0])
        sjq = 0  # 上半场进球数
        jqs80 = 0  # 80分钟后进球
        jqs75 = 0  # 75分钟后进球
        for i in trs[2:]:
            if i.xpath('./td[2]/text()') == ['点球']:
                break
            elif i.xpath('./td[2]/text()') == ['时间']:
                continue
            else:
                jq = i.xpath('./td[2]/img/@title')
                jq2 = i.xpath('./td[4]/img/@title')
                if jq == ['入球'] or jq == ['点球'] or jq == ['乌龙'] or \
                        jq2 == ['入球'] or jq2 == ['点球'] or jq2 == ['乌龙']:
                    jqtime = i.xpath('./td[3]//text()')[0][:-1]
                    if '+' not in jqtime:
                        jqtime = int(jqtime)
                    elif '+' in jqtime:
                        jqtime = int(jqtime.split('+')[0])
                    if jqtime <= 45:
                        sjq += 1
                    if jqtime >= 75:
                        jqs75 += 1
                    if jqtime >= 80:
                        jqs80 += 1
        return [sjq, zzjqs, jqs75, jqs80]
    else:
        print('没有详细事件')
        return ['没有详细事件', '没有详细事件', '没有详细事件', '没有详细事件']


def _daxiaoqiu_get_jinqiushuju(id):
    zzjqs = ''
    jqs80 = ''
    jqs75 = ''
    after80 = ''
    after75 = ''
    url = 'http://vip.win007.com/changeDetail/overunder.aspx?id={}&companyID=3&l=0'.format(id)
    html = etree.HTML(_get_page(url))
    tr_list3 = html.xpath('//*[@id="odds2"]/table//tr')
    tr = tr_list3[1]
    if tr.xpath('./td[2]/text()') and int(tr.xpath('./td[1]/text()')[0]) > 80:
        zzjqs = tr.xpath('./td[2]/text()')[0].split('-')
        zzjqs = int(zzjqs[0]) + int(zzjqs[1])
        # 75分钟80分钟后进球数
        s = True
        for tr in tr_list3:
            if tr.xpath('./td[1]/text()'):
                if int(tr.xpath('./td[1]/text()')[0]) <= 79 and s:
                    # 80分钟进球数
                    s = False
                    jqs80 = tr.xpath('./td[2]/text()')[0].split('-')
                    jqs80 = int(jqs80[0]) + int(jqs80[1])
                if int(tr.xpath('./td[1]/text()')[0]) <= 74:
                    # 75分钟进球数
                    jqs75 = tr.xpath('./td[2]/text()')[0].split('-')
                    jqs75 = int(jqs75[0]) + int(jqs75[1])
                    after80 = zzjqs - jqs80
                    after75 = zzjqs - jqs75
                    break
    return [zzjqs, after75, after80]


def _write_csv(data, csv_path):
    """将数据写入csv"""
    with open(csv_path, 'a', encoding='utf_8_sig', newline='') as f:
        data = [str(i) + '\t' for i in data]
        w = csv.writer(f)
        w.writerow(data)


def create_csv(csv_path):
    """创建存储数据的csv"""
    with open(csv_path, 'w', encoding='utf_8_sig', newline='') as f:
        f.write(
            '当日链接,比赛详情链接,日期,联赛名,主队,客队,初盘亚盘,终盘亚盘,终盘亚盘水位,初盘大球盘口,终盘大球盘口,终盘大球水位,中场大小盘,中场大球水位,上半场进球数,最终进球数,下半场75前进球数,75分钟后进球数,80分钟后进球数\n')


def _get_75data(html):
    before75 = 0
    html = etree.HTML(html)
    trs = html.xpath('.//*[@id="teamEventDiv_detail"]//tr')
    if len(trs) > 1:
        for i in trs[1:]:
            if i.xpath('./td[2]/text()') == ['点球']:
                break
            elif i.xpath('./td[2]/text()') == ['时间']:
                continue
            else:
                jq = i.xpath('./td[2]/img/@title')
                jq2 = i.xpath('./td[4]/img/@title')
                if jq == ['入球'] or jq == ['点球'] or jq == ['乌龙'] or \
                        jq2 == ['入球'] or jq2 == ['点球'] or jq2 == ['乌龙']:
                    jqtime = i.xpath('./td[3]//text()')[0][:-1]
                    if '+' not in jqtime:
                        jqtime = int(jqtime)
                    elif '+' in jqtime:
                        jqtime = int(jqtime.split('+')[0])
                    if jqtime < 75:
                        before75 += 1
        return before75
    else:
        print('没有详细事件')
        return '没有详细事件'


def _get_yz(url):
    html = _get_page(url)
    if html != '<html><head></head><body></body></html>':
        tree = etree.HTML(html)
        # 时间
        time1 = tree.xpath('//div[@class="vs"]/div[1]/text()')
        time1 = ''.join(time1).strip().split(' ')[0].replace('-','.')
        # 联赛名
        LName = tree.xpath('//a[@class="LName"]/text()')[0].strip()
        # 主场球队
        home = tree.xpath('//*[@class="header"]//*[@class="home"]/a/text()')[0]
        home = home.split(' ')[0]
        # 客场球队
        guest = tree.xpath('//*[@class="header"]//*[@class="guest"]/a/text()')[0]
        guest = guest.strip()
        cpyp, zpyp, zpypsw = ['没有Crown','没有Crown','没有Crown']
        tr_list = tree.xpath('//*[@id="odds"]//tr')
        for tr in tr_list:
            # print(tr.xpath('./td[1]/text()'))
            if tr.xpath('./td[1]/text()') == ['Crown']:
                cpyp = tr.xpath('./td[4]/text()')[0]  # 初盘亚盘
                zpyp = tr.xpath('./td[10]/text()')[0]  # 终盘亚盘
                # 终盘亚盘水位
                zpypsw = tr.xpath('./td[9]/text()')[0] + '/' + tr.xpath('./td[11]/text()')[0]
                break
        return [time1, LName, home, guest, cpyp, zpyp, zpypsw]
    else:
        print('亚指页面为无内容')
        return ['亚指页面为无内容', '亚指页面为无内容', '亚指页面为无内容', '亚指页面为无内容', '亚指页面为无内容', '亚指页面为无内容', '亚指页面为无内容']


def _get_dx(url):
    html = _get_page(url)
    if html != '<html><head></head><body></body></html>':
        tree = etree.HTML(html)
        tr_list = tree.xpath('//*[@id="odds"]//tr')
        cp, zp, zpdqsw = ['没有Crown', '没有Crown', '没有Crown']
        for tr in tr_list:
            if tr.xpath('./td[1]/text()') == ['Crown']:
                cp = tr.xpath('./td[4]/text()')[0]  # 初盘大球盘口
                zp = tr.xpath('./td[10]/text()')[0]  # 终盘大球盘口
                # 终盘大球水位
                zpdqsw = tr.xpath('./td[9]/text()')[0] + '/' + tr.xpath('./td[11]/text()')[0]
                break
        return [cp, zp, zpdqsw]
    else:
        print('大小页面为无内容')
        return ['大小页面为无内容', '大小页面为无内容', '大小页面为无内容']


def first_login(url, csv_path, log_path):
    log_name = url[-12:-4]
    print("开始采集{}数据".format(log_name))
    with open('./logs/{}/{}.txt'.format(log_path, log_name), 'w', encoding='utf-8') as f:
        f.write("开始采集{}数据{}\n".format(url, str(datetime.now())))
    page_text = _get_page(url)
    # print(page_text)
    reobj = re.compile(
        r'<tr height="18" align="center" bgcolor="[\d\D]*?" id="tr1_\d+" name="\d+,\d+" infoid="\d+">[\d\D]*?<a href="javascript:" onclick="AsianOdds\(([\d\D]*?)\)"[\d\D]*?>亚</a>[\d\D]*?</tr>',re.MULTILINE)
    num_list = reobj.findall(page_text)
    # print(num_list)
    num_list2 = ['http://live.win007.com/detail/{}cn.htm'.format(i)\
                for i in num_list]  # 单场比赛详细事件页面
    # print(len(num_list2))
    # print(num_list2)
    _second_login(num_list2, url, log_name, csv_path, log_path)
    with open('./logs/{}/{}.txt'.format(log_path, log_name), 'a', encoding='utf-8') as f:
        f.write("结束采集{}\n".format(str(datetime.now())))
    return None


def _second_login(num_list2, date_url, log_name, csv_path, log_path):
    boolen = False
    while num_list2:
        url = num_list2.pop(0)
        _write_log(log_name, url, 1, log_path)
        data = [date_url, url]
        try:
            html = _get_page(url)
            before75 = _get_75data(html)
            if before75 == '没有详细事件':
                print('没有详细事件')
                _write_log(log_name, url, 5, log_path, len(num_list2))
            elif before75 == 6:
                # 发生了6个进球，收集数据
                id = url[-13:-6]
                yzurl = 'http://vip.win007.com/AsianOdds_n.aspx?id={}'.format(id)
                # print(yzurl)
                time1, LName, home, guest, cpyp, zpyp, zpypsw = _get_yz(yzurl)
                # print(time1, LName, home, guest, cpyp, zpyp, zpypsw)
                data += [time1, LName, home, guest, cpyp, zpyp, zpypsw]
                # print(data)
                dxurl = 'http://vip.win007.com/OverDown_n.aspx?id={}&l=0'.format(id)
                cp, zp, zpdqsw = _get_dx(dxurl)
                data += [cp, zp, zpdqsw]
                zcdxp, zcdqsw, sjq = _go_daxiaoqiu(id)
                if zcdxp == '无大小球变化表':
                    # 没有大小球变化表
                    sjq, zzjqs, jqs75, jqs80 = _go_xiangxishijian(id)
                    data.append(zcdxp)
                    data.append(zcdqsw)
                    data.append(sjq)
                    data.append(zzjqs)
                    if zzjqs != '没有详细事件':
                        before75_sjq = before75 - sjq
                        data.append(before75_sjq)
                    else:
                        data.append('无大小球变化表也没有详细事件')
                    data.append(jqs75)
                    data.append(jqs80)
                elif not zcdxp and not zcdqsw and not sjq:
                    # 没有中场或45或46
                    sjq, zzjqs, jqs75, jqs80 = _go_xiangxishijian(id)
                    data.append('没有中场或45或46')
                    data.append('没有中场或45或46')
                    data.append(sjq)
                    data.append(zzjqs)
                    if zzjqs != '没有详细事件':
                        before75_sjq = before75 - sjq
                        data.append(before75_sjq)
                    else:
                        data.append('没有中场或45或46也没有详细事件')
                    data.append(jqs75)
                    data.append(jqs80)
                else:
                    data.append(zcdxp)
                    data.append(zcdqsw)
                    data.append(sjq)
                    sjq, zzjqs, jqs75, jqs80 = _go_xiangxishijian(id)
                    data.append(zzjqs)
                    if zzjqs != '没有详细事件':
                        before75_sjq = before75 - sjq
                        data.append(before75_sjq)
                    else:
                        data.append('没有详细事件')
                    data.append(jqs75)
                    data.append(jqs80)
                _write_csv(data, csv_path)
                _write_log(log_name, url, 2, log_path, len(num_list2))
            else:
                print('比赛75分钟前没有发生6个进球')
                _write_log(log_name, url, 3, log_path, len(num_list2))
            print(data)
            print(len(num_list2))
            time.sleep(1)
        except Exception as e:
            print(e)
            num_list2.insert(0, url)
            print(len(num_list2))
            print(url, '该链接抓取失败')
            _write_log(log_name, url, 4, log_path, len(num_list2))
            time.sleep(60)
    return None


# _second_login([
# 'http://vip.win007.com/AsianOdds_n.aspx?id=1825699',
#                ], 'a','a','a.csv','a2.csv')




def main(url_list, csv_path, log_path):
    #create_csv(csv_path)
    for url in url_list:
        first_login(url, csv_path, log_path)

