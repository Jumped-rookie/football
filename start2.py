#!/usr/bin/env python
# -*- coding:utf-8 -*-
from datetime import datetime, date, timedelta
import demo
import os


def time_day():
    """一年的url"""
    url_list = []
    for i in range(1,366+31+26):  #
        yesterday = str(date.today() + timedelta(days = -i-1))
        yesterdays = yesterday.replace('-','')
        # urls = "http://bf.win007.com/football/Over_"+yesterdays+".htm"
        url_list.append(yesterdays)
    print(url_list)
    return url_list

# time_day()
# 从2020年1.1到2021年2.28
url_list = ['20210228', '20210227', '20210226', '20210225', '20210224', '20210223', '20210222', '20210221', '20210220', '20210219', '20210218', '20210217', '20210216', '20210215', '20210214', '20210213', '20210212', '20210211', '20210210', '20210209', '20210208', '20210207', '20210206', '20210205', '20210204', '20210203', '20210202', '20210201', '20210131', '20210130', '20210129', '20210128', '20210127', '20210126', '20210125', '20210124', '20210123', '20210122', '20210121', '20210120', '20210119', '20210118', '20210117', '20210116', '20210115', '20210114', '20210113', '20210112', '20210111', '20210110', '20210109', '20210108', '20210107', '20210106', '20210105', '20210104', '20210103', '20210102', '20210101', '20201231', '20201230', '20201229', '20201228', '20201227', '20201226', '20201225', '20201224', '20201223', '20201222', '20201221', '20201220', '20201219', '20201218', '20201217', '20201216', '20201215', '20201214', '20201213', '20201212', '20201211', '20201210', '20201209', '20201208', '20201207', '20201206', '20201205', '20201204', '20201203', '20201202', '20201201', '20201130', '20201129', '20201128', '20201127', '20201126', '20201125', '20201124', '20201123', '20201122', '20201121', '20201120', '20201119', '20201118', '20201117', '20201116', '20201115', '20201114', '20201113', '20201112', '20201111', '20201110', '20201109', '20201108', '20201107', '20201106', '20201105', '20201104', '20201103', '20201102', '20201101', '20201031', '20201030', '20201029', '20201028', '20201027', '20201026', '20201025', '20201024', '20201023', '20201022', '20201021', '20201020', '20201019', '20201018', '20201017', '20201016', '20201015', '20201014', '20201013', '20201012', '20201011', '20201010', '20201009', '20201008', '20201007', '20201006', '20201005', '20201004', '20201003', '20201002', '20201001', '20200930', '20200929', '20200928', '20200927', '20200926', '20200925', '20200924', '20200923', '20200922', '20200921', '20200920', '20200919', '20200918', '20200917', '20200916', '20200915', '20200914', '20200913', '20200912', '20200911', '20200910', '20200909', '20200908', '20200907', '20200906', '20200905', '20200904', '20200903', '20200902', '20200901', '20200831', '20200830', '20200829', '20200828', '20200827', '20200826', '20200825', '20200824', '20200823', '20200822', '20200821', '20200820', '20200819', '20200818', '20200817', '20200816', '20200815', '20200814', '20200813', '20200812', '20200811', '20200810', '20200809', '20200808', '20200807', '20200806', '20200805', '20200804', '20200803', '20200802', '20200801', '20200731', '20200730', '20200729', '20200728', '20200727', '20200726', '20200725', '20200724', '20200723', '20200722', '20200721', '20200720', '20200719', '20200718', '20200717', '20200716', '20200715', '20200714', '20200713', '20200712', '20200711', '20200710', '20200709', '20200708', '20200707', '20200706', '20200705', '20200704', '20200703', '20200702', '20200701', '20200630', '20200629', '20200628', '20200627', '20200626', '20200625', '20200624', '20200623', '20200622', '20200621', '20200620', '20200619', '20200618', '20200617', '20200616', '20200615', '20200614', '20200613', '20200612', '20200611', '20200610', '20200609', '20200608', '20200607', '20200606', '20200605', '20200604', '20200603', '20200602', '20200601', '20200531', '20200530', '20200529', '20200528', '20200527', '20200526', '20200525', '20200524', '20200523', '20200522', '20200521', '20200520', '20200519', '20200518', '20200517', '20200516', '20200515', '20200514', '20200513', '20200512', '20200511', '20200510', '20200509', '20200508', '20200507', '20200506', '20200505', '20200504', '20200503', '20200502', '20200501', '20200430', '20200429', '20200428', '20200427', '20200426', '20200425', '20200424', '20200423', '20200422', '20200421', '20200420', '20200419', '20200418', '20200417', '20200416', '20200415', '20200414', '20200413', '20200412', '20200411', '20200410', '20200409', '20200408', '20200407', '20200406', '20200405', '20200404', '20200403', '20200402', '20200401', '20200331', '20200330', '20200329', '20200328', '20200327', '20200326', '20200325', '20200324', '20200323', '20200322', '20200321', '20200320', '20200319', '20200318', '20200317', '20200316', '20200315', '20200314', '20200313', '20200312', '20200311', '20200310', '20200309', '20200308', '20200307', '20200306', '20200305', '20200304', '20200303', '20200302', '20200301', '20200229', '20200228', '20200227', '20200226', '20200225', '20200224', '20200223', '20200222', '20200221', '20200220', '20200219', '20200218', '20200217', '20200216', '20200215', '20200214', '20200213', '20200212', '20200211', '20200210', '20200209', '20200208', '20200207', '20200206', '20200205', '20200204', '20200203', '20200202', '20200201', '20200131', '20200130', '20200129', '20200128', '20200127', '20200126', '20200125', '20200124', '20200123', '20200122', '20200121', '20200120', '20200119', '20200118', '20200117', '20200116', '20200115', '20200114', '20200113', '20200112', '20200111', '20200110', '20200109', '20200108', '20200107', '20200106', '20200105', '20200104', '20200103', '20200102', '20200101']

date_dict = {}
for i in url_list:
    key = i[:6]
    date_dict.setdefault(key, [])
    date_dict[key].append(i)

months = ['202010', '202011', '202012']  # 选择要爬取的月份,


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
    demo.main(urls, csv_path, i)

