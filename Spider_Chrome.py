#-- coding: utf-8 --
#爬取豆瓣网页
import os
from multiprocessing import Pool
from time import sleep
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ChromeOptions
import re
import numpy as np
from msedge.selenium_tools import EdgeOptions, Edge

def GetHTML(brochoice):
    ################################################
    #设置无头浏览器
    if brochoice:
        #chrome
        chrome_options = ChromeOptions()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        # chrome_options.add_argument("--proxy-server=http://111.231.86.149:7890")
        options = Options()
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # options.add_argument("--proxy-server=http://183.247.211.151:30001")
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")
        executable_path = r'./chromedriver.exe'
        bro = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options, options=options)
        bro.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
          """
        })

    else:
        #edge
        edge_options = EdgeOptions()
        edge_options.add_argument('--headless')
        edge_options.add_argument('--disable-gpu')
        edge_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # options.add_argument("--proxy-server=http://183.247.211.151:30001")
        edge_options.add_experimental_option('useAutomationExtension', False)
        edge_options.add_argument("--disable-blink-features")
        edge_options.add_argument("--disable-blink-features=AutomationControlled")
        executable_path = r'./msedgedriver.exe'
        bro = Edge(executable_path=executable_path, options=edge_options)
        bro.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
          """
        })
    ###################################################
    #对每本书依次爬取信息
    bro.minimize_window()
    bookinfor = pd.read_csv('./data/bookinfor.csv')
    files = os.listdir('./html')
    files = [eval(t.split('.')[0]) for t in files]
    for i in range(max(files)+1, len(bookinfor)):
        try:
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
            # 开始爬取
            bro.get(url)
            pagetext = bro.page_source
            if re.findall('有异常请求从你的', pagetext):
                print('ip异常， 第%d本书' % i)
                break
            with open('./html/%d.html' % i, 'wb') as f:
                f.write(pagetext.encode("utf-8", "ignore"))
                f.close()
            sleep(2)
        except Exception as e:
            # with open('./data/%d.html' % i, 'wb') as f:
            #     f.write(pagetext.encode("utf-8", "ignore"))
            #     f.close()
            bro.quit()
            print('error: %s', e)
            break

    bro.quit()

brochoice = 1  #1:chrome  0:edge
while 1:
    brochoice = 1
    GetHTML(brochoice)
    sleep(180)
    brochoice = 0
    GetHTML(brochoice)
    sleep(180)