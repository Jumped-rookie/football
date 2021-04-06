#!/usr/bin/env python
# -*- coding:utf-8 -*-
from selenium.webdriver.chrome.options import Options
from datetime import datetime, date, timedelta
from selenium import webdriver
from lxml import etree
import requests
import re, csv
import time, os
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select


def _get_page(new_url):
    """打开页面，返回html"""
    c_service = Service(r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
    c_service.command_line_args()
    c_service.start()
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('blink-settings=imagesEnabled=false')
    driver = webdriver.Chrome(chrome_options=chrome_options)  # 参数添加
    driver.set_page_load_timeout(10)
    try:
        driver.get(new_url)
        time.sleep(1)
        try:
            sel = driver.find_element_by_xpath('//*[@id="sel_showType"]')
            Select(sel).select_by_value('1')
            time.sleep(2)
        except:
            pass
        page_text = driver.page_source
        driver.quit()
        c_service.stop()
        return page_text
    except:
        print('访问超时')
        driver.quit()
        c_service.stop()


def _write_log(name, txt, s, log_path, len_data=0):
    with open('./logs/{}/{}.txt'.format(log_path, name), 'a', encoding='utf-8') as f:
        if s == 1:
            f.write('采集开始'+txt+'\n')
        elif s == 2:
            f.write('结束采集,满足条件计入数据\n')
            f.write('剩余'+str(len_data)+'场比赛\n')
        elif s == 3:
            f.write('结束采集,无竞彩官方\n')
            f.write('剩余' + str(len_data) + '场比赛\n')
        elif s == 4:
            f.write('该链接抓取失败,尝试重抓\n')
            f.write('剩余' + str(len_data) + '场比赛\n')
        elif s == 5:
            f.write('欧指页面为无内容\n')
            f.write('剩余' + str(len_data) + '场比赛\n')
        elif s == 6:
            f.write('结束采集,本场没符合条件\n')
            f.write('剩余' + str(len_data) + '场比赛\n')
        elif s == 7:
            f.write('结束采集,本场没有欧指页面\n')
            f.write('剩余' + str(len_data) + '场比赛\n')


def create_csv(csv_path):
    """创建存储数据的csv"""
    with open(csv_path, 'w', encoding='utf_8_sig', newline='') as f:
        f.write('当日链接,比赛详情链接,日期,联赛名,主队,客队,竞彩主胜初赔,竞彩平局初赔,竞彩客胜初赔,竞彩主胜终赔,竞彩平局终赔,竞彩客胜终赔,Crown初盘让球,Crown初盘让球主赔,Crown初盘让球客赔,Crown终盘让球,Crown终盘让球主赔,Crown终盘让球客赔,赛果,首先进球球队\n')


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
    num_list2 = ['http://op1.win007.com/oddslist/{}.htm'.format(i)\
                for i in num_list]  # 单场比赛详细事件页面
    # print(len(num_list2))
    # print(num_list2)
    _second_login(num_list2, url, log_name, csv_path, log_path)
    with open('./logs/{}/{}.txt'.format(log_path, log_name), 'a', encoding='utf-8') as f:
        f.write("结束采集{}\n".format(str(datetime.now())))
    return None


def _pd_yz(yz_url):
    """判断有没有亚指页面"""
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}
    r = requests.get(yz_url, headers=header)
    if r.text:
        return True
    else:
        return False


def _second_login(num_list2, date_url, log_name, csv_path, log_path):
    while num_list2:
        url = num_list2.pop(0)
        _write_log(log_name, url, 1, log_path)
        data = [date_url, url]
        try:
            id = re.search(r"http://op1\.win007\.com/oddslist/([\d\D]*?)\.htm", url).group(1)
            yz_url = 'http://vip.win007.com/AsianOdds_n.aspx?id={}'.format(id)
            if not _pd_yz(yz_url):
                # 没有亚指页面，所以欧指页面也没有
                print('该页面无法访问')
                _write_log(log_name, url, 7, log_path, len(num_list2))
            else:
                html = _get_page(url)
                Date, LName, Home, Guest, Saiguo = _get_base(html)
                if Date == '欧指页面为无内容':
                    _write_log(log_name, url, 5, log_path, len(num_list2))
                    print(data)
                    print(len(num_list2))
                    time.sleep(1)
                    continue
                data += [Date, LName, Home, Guest]
                jincai_data = _get_jincai(html)
                if jincai_data == '无竞彩官方':
                    print('无竞彩官方')
                    _write_log(log_name, url, 3, log_path, len(num_list2))
                else:
                    if jincai_data:
                        data += jincai_data
                        yz_data = _get_yz(yz_url)
                        data += yz_data
                        xx_url = 'http://live.win007.com/detail/{}cn.htm'.format(id)
                        if Saiguo != '无比分':
                            data.append(Saiguo)
                        else:
                            Saiguo = _go_xxsj_saiguo(xx_url)
                            data.append(Saiguo)
                        first_jq = _get_xiangshishijian(xx_url)
                        data.append(first_jq)
                        _write_log(log_name, url, 2, log_path, len(num_list2))
                        _write_csv(data, csv_path)
                    else:
                        print('没满足条件')
                        _write_log(log_name, url, 6, log_path, len(num_list2))
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


def _go_xxsj_saiguo(url):
    html = _get_page(url)
    tree = etree.HTML(html)
    trs = tree.xpath('.//*[@id="teamEventDiv_detail"]//tr')
    if len(trs) > 1:
        td = trs[1]
        try:
            L_saiguo = int(td.xpath('./td[1]//text()')[0])
            R_saiguo = int(td.xpath('./td[3]//text()')[0])
            if L_saiguo > R_saiguo:
                Saiguo = '3'
            elif L_saiguo < R_saiguo:
                Saiguo = '0'
            else:
                Saiguo = '1'
        except:
            Saiguo = '找不到比分'
        return Saiguo
    else:
        print('没有详细事件,找不到比分')
        return '找不到比分'


def _get_xiangshishijian(url):
    """到详细事件，获取首先进球方"""
    eh = etree.HTML(_get_page(url))
    trs = eh.xpath('.//*[@id="teamEventDiv_detail"]//tr')
    if len(trs) > 1:
        td = trs[1]
        L_bf = int(td.xpath('./td[1]//text()')[0])
        R_bf = int(td.xpath('./td[3]//text()')[0])

        first_jq = '1'
        for i in trs:
            L_jq = i.xpath('./td[2]/img/@title')
            R_jq = i.xpath('./td[4]/img/@title')
            if L_jq == ['入球'] or L_jq == ['点球'] or L_jq == ['乌龙']:
                first_jq = '3'
                return first_jq
            elif R_jq == ['入球'] or R_jq == ['点球'] or R_jq == ['乌龙']:
                first_jq = '0'
                return first_jq
        if first_jq == '1' and L_bf + R_bf == 0:
            return first_jq
        else:
            return '找不到首先进球方'
    else:
        print('没有详细事件')
        return '没有详细事件'


def _get_yz(url):
    """获得亚指中的数据"""
    html = _get_page(url)
    if html != '<html><head></head><body></body></html>':
        tree = etree.HTML(html)
        # 初盘让球 初盘让球主赔 初盘让球客赔
        cprq, cprqzp, cprqkp = ['没有Crown', '没有Crown', '没有Crown']
        # 终盘让球 终盘让球主赔 终盘让球客赔
        zprq, zprqzp, zprqkp = ['没有Crown', '没有Crown', '没有Crown']
        tr_list = tree.xpath('//*[@id="odds"]//tr')
        for tr in tr_list:
            # print(tr.xpath('./td[1]/text()'))
            if tr.xpath('./td[1]/text()') == ['Crown']:
                cprq = tr.xpath('./td[4]/text()')[0]
                cprqzp = tr.xpath('./td[3]/text()')[0]
                cprqkp = tr.xpath('./td[5]/text()')[0]
                zprq = tr.xpath('./td[10]/text()')[0]
                zprqzp = tr.xpath('./td[9]/text()')[0]
                zprqkp = tr.xpath('./td[11]/text()')[0]
                break
        return [cprq, cprqzp, cprqkp, zprq, zprqzp, zprqkp]
    else:
        print('亚指页面为无内容')
        return ['亚指页面为无内容']


def _get_base(html):
    """获取比赛的时间，联赛名，主队，客队"""
    if html != '<html><head></head><body></body></html>':
        tree = etree.HTML(html)
        time1 = tree.xpath('//div[@class="vs"]/div[1]/text()')
        # 日期
        Date = ''.join(time1).strip().split(' ')[0].replace('-','.')
        # 联赛名
        LName = tree.xpath('//a[@class="LName"]/text()')[0].strip()
        # 主场球队
        Home = tree.xpath('//*[@class="header"]//*[@class="home"]/a/text()')[0]
        Home = Home.split(' ')[0]
        # 客场球队
        Guest = tree.xpath('//*[@class="header"]//*[@class="guest"]/a/text()')[0]
        Guest = Guest.strip()
        # 赛果
        L_saiguo, R_saiguo = ['无比分', '无比分']
        try:
            L_saiguo = int(tree.xpath('//*[@id="headVs"]/div/div[1]/text()')[0])
            R_saiguo = int(tree.xpath('//*[@id="headVs"]/div/div[3]/text()')[0])
        except:
            pass
        if L_saiguo != '无比分':
            if L_saiguo > R_saiguo:
                Saiguo = '3'
            elif L_saiguo < R_saiguo:
                Saiguo = '0'
            else:
                Saiguo = '1'
        else:
            Saiguo = '无比分'
        return [Date, LName, Home, Guest, Saiguo]
    else:
        print('欧指页面为无内容')
        return ['欧指页面为无内容','','','','']


def _get_jincai(html):
    """获取金竞彩官方的数据"""
    #竞彩主胜初赔 竞彩平局初赔 竞彩客胜初赔
    zscp, pjcp, kscp = ['无竞彩官方', '无竞彩官方', '无竞彩官方']
    #竞彩主胜终赔 竞彩平局终赔 竞彩客胜终赔
    zszp, pjzp, kszp = ['无竞彩官方', '无竞彩官方', '无竞彩官方']
    tree = etree.HTML(html)
    table = tree.xpath('//*[@id="oddsList_tab"]//tr')
    company = ''
    for tr in table:
        if company == '竞彩官方':
            zszp = tr.xpath('./td[1]//text()')[0]
            pjzp = tr.xpath('./td[2]//text()')[0]
            kszp = tr.xpath('./td[3]//text()')[0]
            break
        if tr.xpath('./@id'):
            company = tr.xpath('./td[2]/a/text()')[0]
            if company == '竞彩官方':
                zscp = tr.xpath('./td[3]//text()')[0]
                pjcp = tr.xpath('./td[4]//text()')[0]
                kscp = tr.xpath('./td[5]//text()')[0]
    # 判断是否满足条件
    if zscp == '无竞彩官方':
        return '无竞彩官方'
    result = _pd(zscp, pjcp, kscp, zszp, pjzp, kszp)
    if result:
        return [zscp, pjcp, kscp, zszp, pjzp, kszp]
    else:
        return False


def _pd(zscp, pjcp, kscp, zszp, pjzp, kszp):
    """判断是否满足条件"""
    if '\xa0' == zscp or '\xa0' == pjcp or '\xa0' == kscp or \
            '\xa0' == zszp or '\xa0' == pjzp or '\xa0' == kszp:
        return False
    if eval(zscp) > eval(kscp) and eval(zszp) > eval(zscp) and eval(zszp)-eval(kszp) >= -0.2:
        return True
    else:
        return False


def _write_csv(data, csv_path):
    """将数据写入csv"""
    with open(csv_path, 'a', encoding='utf_8_sig', newline='') as f:
        data = [str(i) + '\t' for i in data]
        w = csv.writer(f)
        w.writerow(data)


def main(url_list, csv_path, log_path):
    isExists = os.path.exists(csv_path)
    if not isExists:
        create_csv(csv_path)
    for url in url_list:
        first_login(url, csv_path, log_path)



# _second_login([
#                'http://op1.win007.com/oddslist/1839363.htm',
#
#                ], '1', 'log_name', 'csv_path', 'log_path')


