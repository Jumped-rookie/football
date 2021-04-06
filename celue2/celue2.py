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


def _write_log(name, txt, s, log_path, len_data=0):
    with open('./logs/{}/{}.txt'.format(log_path, name), 'a', encoding='utf-8') as f:
        if s == 1:
            f.write('采集开始'+txt+'\n')
        elif s == 2:
            f.write('结束采集,满足条件计入数据\n')
            f.write('剩余'+str(len_data)+'场比赛\n')
        elif s == 3:
            f.write('结束采集,暂时没有本场比赛的欧指\n')
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



def create_csv(csv_path):
    """创建存储数据的csv"""
    with open(csv_path, 'w', encoding='utf_8_sig', newline='') as f:
        f.write('当日链接,比赛详情链接,日期,开赛时间,联赛名,主队,客队,' +\
                '威廉希尔凯利胜,威廉希尔凯利平,威廉希尔凯利负,威廉希尔初盘返还率,威廉希尔终盘返还率,威廉希尔变化时间,' +\
                '伟德凯利胜,伟德凯利平,伟德凯利负,伟德初盘返还率,伟德终盘返还率,伟德变化时间,' +\
                '易胜博凯利胜,易胜博凯利平,易胜博凯利负,易胜博初盘返还率,易胜博终盘返还率,易胜博变化时间,' +\
                'interwetten凯利胜,interwetten凯利平,interwetten凯利负,interwetten初盘返还率,interwetten终盘返还率,interwetten变化时间,' +\
                '伟德主胜初赔,伟德主胜终赔,伟德平赔初赔,伟德平赔终赔,伟德客胜初赔,伟德客胜终赔,' +\
                '最终赛果,初盘亚盘（Crown）,终盘亚盘（Crown）,首先进球方\n'
                )


def _write_csv(data, csv_path):
    """将数据写入csv"""
    with open(csv_path, 'a', encoding='utf_8_sig', newline='') as f:
        data = [str(i) + '\t' for i in data]
        w = csv.writer(f)
        w.writerow(data)


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


def _get_base(html):
    """获取比赛的时间，联赛名，主队，客队"""
    if html != '<html><head></head><body></body></html>':
        tree = etree.HTML(html)
        time1 = tree.xpath('//div[@class="vs"]/div[1]/text()')
        # 日期
        Date = ''.join(time1).strip().split(' ')[0].replace('-','.')
        # 时间
        Time = ''.join(time1).strip().split(' ')[1][:5]
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
        return [Date, Time, LName, Home, Guest, Saiguo]
    else:
        print('欧指页面为无内容')
        return ['欧指页面为无内容','','','','','']


def _judgment(html):
    """判断是否满足条件"""
    tree = etree.HTML(html)
    table = tree.xpath('//*[@id="oddsList_tab"]//tr')
    if table:
        """有本场比赛的欧指"""
        jieguo = False
        for tr in table:
            if tr.xpath('./@id'):
                company = tr.xpath('./td[2]/a/text()')[0]
                if '(' in company:
                    company = company.split('(')[0]
                if '威廉希尔' == company or '伟德' == company or\
                    '易胜博' == company or 'Interwetten' == company:
                    # print(company)
                    L_kl = eval(tr.xpath('./td[10]//text()')[0])  # 左边凯利指数
                    R_kl = eval(tr.xpath('./td[12]//text()')[0])  # 右边
                    # print(L_kl,R_kl)
                    if L_kl >= 1 or R_kl >= 1:
                        jieguo = True
                        return jieguo
        return jieguo
    else:
        print('暂时没有本场比赛的欧指。')
        return '暂时没有本场比赛的欧指'


def _get_data(html):
    """满足条件记录数据"""
# 威廉希尔凯利胜 威廉希尔凯利平 威廉希尔凯利负 威廉希尔初盘返还率 威廉希尔终盘返还率
    weil_L, weil_C, weil_R, weil_cp, weil_zp, weil_time  = ['','','','','','']
# 韦德凯利胜 韦德凯利平 韦德凯利负 韦德初盘返还率 韦德终盘返还率
    wd_L, wd_C, wd_R, wd_cp, wd_zp, wd_time = ['', '', '', '', '', '']
# 易胜博凯利胜 易胜博凯利平 易胜博凯利负 易胜博初盘返还率 易胜博终盘返还率
    yisb_L, yisb_C, yisb_R, yisb_cp, yisb_zp, yisb_time = ['','','','','','']
# interwetten凯利胜 interwetten凯利平 interwetten凯利负 interwetten初盘返还率 interwetten终盘返还率
    inter_L, inter_C, inter_R, inter_cp, inter_zp, inter_time = ['','','','','','']
# 韦德主胜初赔 韦德主胜终赔 韦德平赔初赔 韦德平赔终赔 韦德客胜初赔 韦德客胜终赔
    wd_zs_cp, wd_zs_zp, wd_pp_cp, wd_pp_zp, wd_ks_cp, wd_ks_zp = ['','','','','','']
    tree = etree.HTML(html)
    table = tree.xpath('//*[@id="oddsList_tab"]//tr')
    comp = ''
    for tr in table:
        if comp == '威廉希尔':
            comp = ''
            weil_zp = tr.xpath('./td[7]//text()')[0]
        elif comp == '伟德':
            comp = ''
            wd_zp = tr.xpath('./td[7]//text()')[0]
            wd_zs_zp = tr.xpath('./td[1]//text()')[0]
            wd_pp_zp = tr.xpath('./td[2]//text()')[0]
            wd_ks_zp = tr.xpath('./td[3]//text()')[0]
        elif comp == '易胜博':
            comp = ''
            yisb_zp = tr.xpath('./td[7]//text()')[0]
        elif comp == 'Interwetten':
            comp = ''
            inter_zp = tr.xpath('./td[7]//text()')[0]
        if tr.xpath('./@id'):
            company = tr.xpath('./td[2]/a/text()')[0]
            if '(' in company:
                company = company.split('(')[0]
            if '威廉希尔' == company:
                comp = '威廉希尔'
                weil_L = tr.xpath('./td[10]//text()')[0]
                weil_C = tr.xpath('./td[11]//text()')[0]
                weil_R = tr.xpath('./td[12]//text()')[0]
                weil_cp = tr.xpath('./td[9]//text()')[0]
                if eval(weil_L) >= 1 or eval(weil_R) >= 1:
                    weil_time = tr.xpath('./td[13]//text()')[0]
            elif '伟德' == company:
                comp = '伟德'
                wd_L = tr.xpath('./td[10]//text()')[0]
                wd_C = tr.xpath('./td[11]//text()')[0]
                wd_R = tr.xpath('./td[12]//text()')[0]
                wd_cp = tr.xpath('./td[9]//text()')[0]
                wd_zs_cp = tr.xpath('./td[3]//text()')[0]
                wd_pp_cp = tr.xpath('./td[4]//text()')[0]
                wd_ks_cp = tr.xpath('./td[5]//text()')[0]
                if eval(wd_L) >= 1 or eval(wd_R) >= 1:
                    wd_time = tr.xpath('./td[13]//text()')[0]
            elif '易胜博' == company:
                comp = '易胜博'
                yisb_L = tr.xpath('./td[10]//text()')[0]
                yisb_C = tr.xpath('./td[11]//text()')[0]
                yisb_R = tr.xpath('./td[12]//text()')[0]
                yisb_cp =tr.xpath('./td[9]//text()')[0]
                if eval(yisb_L) >= 1 or eval(yisb_R) >= 1:
                    yisb_time = tr.xpath('./td[13]//text()')[0]
            elif 'Interwetten' == company:
                comp = 'Interwetten'
                inter_L = tr.xpath('./td[10]//text()')[0]
                inter_C = tr.xpath('./td[11]//text()')[0]
                inter_R = tr.xpath('./td[12]//text()')[0]
                inter_cp =tr.xpath('./td[9]//text()')[0]
                if eval(inter_L) >= 1 or eval(inter_R) >= 1:
                    inter_time = tr.xpath('./td[13]//text()')[0]
    data1 = [weil_L, weil_C, weil_R, weil_cp, weil_zp, weil_time,
             wd_L, wd_C, wd_R, wd_cp, wd_zp, wd_time,
             yisb_L, yisb_C, yisb_R, yisb_cp, yisb_zp, yisb_time,
             inter_L, inter_C, inter_R, inter_cp, inter_zp, inter_time,
             wd_zs_cp, wd_zs_zp, wd_pp_cp, wd_pp_zp, wd_ks_cp, wd_ks_zp
             ]
    return data1


def _get_yz(url):
    """获得初盘亚盘和中盘亚盘"""
    html = _get_page(url)
    if html != '<html><head></head><body></body></html>':
        tree = etree.HTML(html)
        cpyp, zpyp = ['没有Crown', '没有Crown']
        tr_list = tree.xpath('//*[@id="odds"]//tr')
        for tr in tr_list:
            # print(tr.xpath('./td[1]/text()'))
            if tr.xpath('./td[1]/text()') == ['Crown']:
                cpyp = tr.xpath('./td[4]/text()')[0]  # 初盘亚盘
                zpyp = tr.xpath('./td[10]/text()')[0]  # 终盘亚盘
                break
        return [cpyp, zpyp]
    else:
        print('亚指页面为无内容')
        return ['亚指页面为无内容', '亚指页面为无内容']


def _get_xiangshishijian_saiguo(url):
    """到详细事件，获取赛果"""
    eh = etree.HTML(_get_page(url))
    trs = eh.xpath('.//*[@id="teamEventDiv_detail"]//tr')
    if len(trs) > 1:
        td = trs[1]
        L_saiguo = int(td.xpath('./td[1]//text()')[0])
        R_saiguo = int(td.xpath('./td[3]//text()')[0])
        if L_saiguo > R_saiguo:
            Saiguo = '3'
        elif L_saiguo < R_saiguo:
            Saiguo = '0'
        else:
            Saiguo = '1'
        return Saiguo
    else:
        print('没有详细事件')
        return '没有详细事件'


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


def _second_login(num_list2, date_url, log_name, csv_path, log_path):
    while num_list2:
        url = num_list2.pop(0)
        _write_log(log_name, url, 1, log_path)
        data = [date_url, url]
        try:
            id = re.search(r"http://op1\.win007\.com/oddslist/([\d\D]*?)\.htm", url).group(1)
            none = _get_yz('http://vip.win007.com/AsianOdds_n.aspx?id={}'.format(id))[0]
            if none != '亚指页面为无内容':
                html = _get_page(url)
                Date, Time, LName, Home, Guest, Saiguo = _get_base(html)
                # print(Date, Time, LName, Home, Guest, Saiguo)
                if Date == '欧指页面为无内容':
                    _write_log(log_name, url, 5, log_path, len(num_list2))
                    print(data)
                    print(len(num_list2))
                    time.sleep(1)
                    continue
                data += [Date, Time, LName, Home, Guest]
                # print(data)
                jieguo = _judgment(html)
                if jieguo == '暂时没有本场比赛的欧指':
                    _write_log(log_name, url, 3, log_path, len(num_list2))
                    print(data)
                    print(len(num_list2))
                    time.sleep(1)
                    continue
                if jieguo:
                    # 满足条件
                    print('本场符合条件')
                    data1 = _get_data(html)
                    data += data1
                    if Saiguo != '无比分':
                        data.append(Saiguo)
                    else:
                        Saiguo = _get_xiangshishijian_saiguo('http://live.win007.com/detail/{}cn.htm'.format(id))
                        if Saiguo != '没有详细事件':
                            data.append(Saiguo)
                        else:
                            data.append('找不到比分')
                    yz_url = 'http://vip.win007.com/AsianOdds_n.aspx?id={}'.format(id)
                    cpyp, zpyp = _get_yz(yz_url)
                    data.append(cpyp)
                    data.append(zpyp)
                    xx_url = 'http://live.win007.com/detail/{}cn.htm'.format(id)
                    first_jq = _get_xiangshishijian(xx_url)
                    data.append(first_jq)
                    # print(data)
                    _write_csv(data, csv_path)
                    _write_log(log_name, url, 2, log_path, len(num_list2))
                else:
                    # 没满足条件
                    print('本场没符合条件')
                    _write_log(log_name, url, 6, log_path, len(num_list2))
            else:
                print('该页面无法访问')
                _write_log(log_name, url, 7, log_path, len(num_list2))
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


# _second_login(['http://op1.win007.com/oddslist/1836674.htm'], '1', '1', '1', '1')


def main(url_list, csv_path, log_path):
    isExists = os.path.exists(csv_path)
    if not isExists:
        create_csv(csv_path)
    for url in url_list:
        first_login(url, csv_path, log_path)
