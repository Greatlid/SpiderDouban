#-- coding: utf-8 --
#爬取豆瓣网页
from multiprocessing import Pool
from time import sleep
import pandas as pd
from lxml import etree
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ChromeOptions
import re
import numpy as np
#################################################
#define var
INF = 100

################################################
#设置无头浏览器
chrome_options = Options()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
options = ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_argument("--proxy-server=http://60.167.21.129:1133")
executable_path = r'./chromedriver.exe'
bro = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options, options=options)

###################################################
#对每本书依次爬取信息
res_all = {}
bookinfor = pd.read_csv('./data/bookinfor.csv')
for i in range(27, len(bookinfor)):
    booktitle = bookinfor.iloc[i,0]
    bookauthor = bookinfor.iloc[i,1]
    bookpublisher = bookinfor.iloc[i,2]
    if not isinstance(booktitle, str): booktitle = ''
    if not isinstance(bookauthor, str): bookauthor = ''
    if not isinstance(bookpublisher, str): bookpublisher = ''
    book = booktitle+'+'+bookauthor+'+'+bookpublisher
    print('第%d本书, 需要的书为%s' % (i, book))
    url = 'https://search.douban.com/book/subject_search?search_text='+ book +'&cat=1001'

    ######################
    #开始爬取
    bro.get(url)
    pagetext = bro.page_source
    tree = etree.HTML(pagetext)
    res_url = tree.xpath('//div[@class="detail"]//a/@href')
    res_title = tree.xpath('//div[@class="detail"]//a/text()')
    res_infor = tree.xpath('//div[@class="detail"]//div[@class="meta abstract"]/text()')
    res_infor = [t.split('/') for t in res_infor]
    # print(res_title)
    # print(res_infor)

    matchdegree_title = []
    for title in res_title:
        matchres = re.match(booktitle, title)
        if matchres != None:
            matchrange = matchres.span()
            matchdegree_title.append(len(title) - matchrange[1] + matchrange[0])
        else:
            matchdegree_title.append(INF)

    matchdegree_author = []
    for infor in res_infor:
        matchres = re.match(bookauthor, infor[0])
        if matchres != None:
            matchrange = matchres.span()
            matchdegree_author.append(len(infor[0]) - matchrange[1] + matchrange[0])
        else:
            matchdegree_author.append(INF)

    matchdegree_pub = []
    for infor in res_infor:
        try:
            matchres = re.match(bookpublisher, infor[1])
        except:
            matchdegree_pub.append(INF)
            continue
        if matchres != None:
            matchrange = matchres.span()
            matchdegree_pub.append(len(infor[1]) - matchrange[1] + matchrange[0])
        else:
            matchdegree_pub.append(INF)

    match_ind = np.lexsort((matchdegree_pub, matchdegree_title, matchdegree_author))
    useful_infor = [res_title[match_ind[0]], res_infor[match_ind[0]][0], res_infor[match_ind[0]][1], res_url[match_ind[0]]]
    print('找到的书为%s' % (str(useful_infor)))
    res_all[book] = useful_infor
bro.quit()





