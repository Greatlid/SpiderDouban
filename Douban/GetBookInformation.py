#对已经爬取到的书籍链接，获取书籍的各类信息
from time import sleep

import pandas as pd
import os
import requests
from lxml import etree
import re
headers = {
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
'Cache-Control': 'max-age=0',
'Connection': 'keep-alive',
'Cookie': 'bid=aStoRYrwXN8; gr_user_id=f6e3cf9e-51b4-46de-bdd1-aabf8dca6f5c; _vwo_uuid_v2=D39390021B192FF773CE01FE15106C244|8292a37f118f517dbf88b53aee9f1327; push_doumail_num=0; push_noty_num=0; __gads=ID=3d649453488db278-22505defa0ce00a6:T=1636601693:RT=1636601693:S=ALNI_MavR0SyFTy1-Yr4N2ekWQyfER8C2A; __yadk_uid=iZfrfGVY99nwC0UMxIkFaDq6Gjpi1XLS; ll="118371"; _ga=GA1.1.2122267463.1636888206; __utmv=30149280.24987; douban-fav-remind=1; ct=y; __utmz=30149280.1639149612.13.11.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmz=81379588.1639149612.17.13.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmc=30149280; __utmc=81379588; _ga_RXNMP372GL=GS1.1.1639187231.2.1.1639187380.0; __utma=30149280.2122267463.1636888206.1639189832.1639194080.16; __utma=81379588.1633473874.1636601563.1639189847.1639194080.20; _pk_ref.100001.3ac3=["","",1639194080,"https://www.baidu.com/link?url=gh2PceqhGr8lDb2scDE32V6ZDWbHAW1A9GZWHkOppLn27n42uViGytdscxFC0Cjn&wd=&eqid=bea7bce6001a218b0000000261b37027"]; ap_v=0,6.0; dbcl2="249872952:GiPLHj5z6aE"; ck=7O-S; _pk_id.100001.3ac3=ae28e8ef85c97326.1636601565.21.1639198051.1639191868.',
'Host': 'book.douban.com',
'Referer': 'https://accounts.douban.com/',
'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Microsoft Edge";v="96"',
'sec-ch-ua-mobile': '?0',
'sec-ch-ua-platform': '"Windows"',
'Sec-Fetch-Dest': 'document',
'Sec-Fetch-Mode': 'navigate',
'Sec-Fetch-Site': 'same-site',
'Sec-Fetch-User': '?1',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.43'
}


def GetBookInfor(url):
    flag = 0
    # url = 'https://book.douban.com/subject/4913064/'
    try:
        bookname, author, pub, price, ISBN, content, catalogue, label, simbook, comment = [[None]] * 10
        response = requests.get(url, headers = headers, timeout = 60)
        print('请求状态：',response.status_code)
        if response.status_code != 200:
            flag = 1  #ip异常或网络异常
            return None, flag
        tree = etree.HTML(response.text)
        bookname = tree.xpath('//span[@property="v:itemreviewed"]/text()')
        author = tree.xpath('//div[@id="info"]//a/text()')
        if len(author) > 0:author = author[0].replace('\n', '')
        info = tree.xpath('//div[@id="info"]//text()')
        info = [t for t in info if not '\n' in t]
        for i, t in enumerate(info):
            if t == '出版社:': pub = info[i + 1]
            if t == '定价:': price = info[i + 1]
            if t == 'ISBN:': ISBN = [info[i + 1]]
        content = tree.xpath('//div[@class="intro"]/p/text()')
        catalogue = tree.xpath('//div[@class="indent"]/text()')
        label = tree.xpath('//div[@id="db-tags-section"]/div[@class="indent"]//a/text()')
        simbook = tree.xpath('//div[@id="db-rec-section"]//a/@href')
        simbook = simbook[::2]
        comment = tree.xpath('//div[@class="review-list  "]//div[@class="short-content"]/text()')
    except Exception as e:
        flag = 2
        if re.findall('Read timed out', str(e)): flag = 1
        print('error:%s, url: %s' % (e, url))
        return None, flag
    return (url, bookname, author, pub, price, ISBN, content, catalogue, label, simbook, comment), flag

if __name__ == '__main__':
    if os.path.isfile('./BookInfor/book.csv'):
        with open('./BookInfor/url_list.txt', 'r') as f:
            url_list = f.read()
            url_list = eval(url_list)
            f.close()
        with open('./BookInfor/url_queue.txt', 'r') as f:
            url_queue = f.read()
            url_queue = eval(url_queue)
            f.close()
        with open('./BookInfor/isbn_set.txt', 'r') as f:
            isbn_set = f.read()
            isbn_set = eval(isbn_set)
            f.close()
        bookres = pd.read_csv('./BookInfor/book.csv')
        cnt = len(bookres)
        print('加载已有文件')

    else:
        with open('./DoubanData/tag.txt', 'r', encoding='utf-8') as f:
            taglist = f.read()
            taglist = eval(taglist)
        url_queue = []  #存储待爬取的书籍链接
        url_list = []   #存储已爬取的书籍链接，以防止重复爬取
        isbn_set = []   #存储已爬取书的isbn号
        for tag in taglist:
            path = './DoubanData/booklist_%s.csv' % tag
            if os.path.isfile(path):
                bookinfor = pd.read_csv(path)
                urllist = bookinfor['url'].to_list()
                url_queue = list(set(url_queue + urllist))
        cnt = 0
        bookres = pd.DataFrame(columns=['url', 'bookname', 'author', 'pub', 'price', 'ISBN', 'content', 'catalogue', 'label', 'simbook', 'comment'])
        print('新建文件')

    save_freq = 10
    while 1:
        cururl = url_queue[0]
        if not cururl in url_list:
            res, flag = GetBookInfor(cururl)
            if flag == 1:  #ip被封
                print('ip异常')
                sleep(120)
                continue
            if flag == 2:  #网页异常
                print('网页异常')
                url_queue.pop(0)
                continue
            _, bookname, author, pub, price, ISBN, content, catalogue, label, simbook, comment = res
            url_list = list(set(url_list+[cururl]))
            url_queue.pop(0)   #去除当前爬取的书籍信息
            url_queue = list(set(url_queue + simbook))  #添加待爬取的书籍信息
            isbn_set = list(set(isbn_set+ISBN))  #添加当前书籍的isbn号

            bookres.loc[cnt] = res
            cnt += 1
            if cnt % save_freq == 0:
                print(bookres.tail())
                print('booknum:', cnt)
                bookres.to_csv('./BookInfor/book.csv', index=False, encoding='utf_8_sig')
            with open('./BookInfor/url_list.txt', 'w') as f:
                f.write(str(url_list))
                f.close()
            with open('./BookInfor/url_queue.txt', 'w') as f:
                f.write(str(url_queue))
                f.close()
            with open('./BookInfor/isbn_set.txt', 'w') as f:
                f.write(str(isbn_set))
                f.close()
            # sleep(0.1)
