#获取每个标签下的书籍编号
import requests
from lxml import etree
import re
import pandas as pd
from time import sleep
import os
from multiprocessing import Pool

headers = {
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
'Cache-Control': 'max-age=0',
'Connection': 'keep-alive',
'Cookie': 'bid=aStoRYrwXN8; gr_user_id=f6e3cf9e-51b4-46de-bdd1-aabf8dca6f5c; _vwo_uuid_v2=D39390021B192FF773CE01FE15106C244|8292a37f118f517dbf88b53aee9f1327; push_doumail_num=0; push_noty_num=0; __gads=ID=3d649453488db278-22505defa0ce00a6:T=1636601693:RT=1636601693:S=ALNI_MavR0SyFTy1-Yr4N2ekWQyfER8C2A; __yadk_uid=iZfrfGVY99nwC0UMxIkFaDq6Gjpi1XLS; ll="118371"; _ga=GA1.1.2122267463.1636888206; __utmv=30149280.24987; douban-fav-remind=1; ct=y; __utmz=30149280.1639149612.13.11.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmz=81379588.1639149612.17.13.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmc=30149280; __utmc=81379588; _ga_RXNMP372GL=GS1.1.1639187231.2.1.1639187380.0; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=5c1d1236-bd23-41ea-a65f-c78d48d1e75c; gr_cs1_5c1d1236-bd23-41ea-a65f-c78d48d1e75c=user_id:1; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03_5c1d1236-bd23-41ea-a65f-c78d48d1e75c=true; __utma=30149280.2122267463.1636888206.1639189832.1639194080.16; __utma=81379588.1633473874.1636601563.1639189847.1639194080.20; _pk_ref.100001.3ac3=["","",1639194080,"https://www.baidu.com/link?url=gh2PceqhGr8lDb2scDE32V6ZDWbHAW1A9GZWHkOppLn27n42uViGytdscxFC0Cjn&wd=&eqid=bea7bce6001a218b0000000261b37027"]; _pk_ses.100001.3ac3=*; ap_v=0,6.0; __utmt=1; dbcl2="249872952:GiPLHj5z6aE"; ck=7O-S; __utmt_douban=1; __utmb=30149280.4.10.1639194080; __utmb=81379588.3.10.1639194080; _pk_id.100001.3ac3=ae28e8ef85c97326.1636601565.21.1639195220.1639191868.',
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

def GetBookList(tag, pagenum, unit, bookinfor, restart):
    curpage = restart
    cnt = len(bookinfor)
    try:
        for start in range(curpage*unit, (pagenum+curpage)*unit, unit):
            url = 'https://book.douban.com/tag/%s?start=%d&type=T' % (tag, start)
            response = requests.get(url, headers = headers, timeout = 60)
            tree = etree.HTML(response.text)
            booklist = tree.xpath('//li[@class="subject-item"]')
            if response.status_code != 200:
                print(response.status_code)
                return bookinfor
            if re.findall('没有找到符合条件的图书', response.text):
                print('没有找到符合条件的图书')
                bookinfor.loc[cnt] = [-1] *len(bookinfor.columns)
                return bookinfor
            for book in booklist:
                try:
                    bookname = book.xpath('.//a/@title')[0]
                    bookurl =book.xpath('.//div[@class="info"]//a/@href')[0]
                    infor = re.sub('\n', '', book.xpath('.//div[@class="pub"]//text()')[0])
                    infor = infor.replace(' ', '')
                    introduction = book.xpath('.//p/text()')[0]
                    score = book.xpath('.//span[@class="rating_nums"]/text()')[0]
                    cmtnum = book.xpath('.//span[@class="pl"]/text()')[0]
                    cmtnum = re.sub('\n', '', cmtnum)
                    cmtnum = cmtnum.replace(' ', '')
                    bookinfor.loc[cnt] = [tag, bookname, bookurl, infor, introduction, score, cmtnum, url]
                    cnt += 1

                except:
                    continue
            print(bookinfor.tail())
            sleep(2)
    except Exception as e:
        print('ERROR:%s' % e)
        return bookinfor
    return bookinfor


def GetAllBookList(tag):
    while 1:
        # tag = '小说'
        pagenum = 50
        unit = 20
        try:
            bookinfor = pd.read_csv('./DoubanData/booklist_%s.csv'%tag)
            restart_web = bookinfor['pageurl'].iloc[-1]
            restart = int(re.findall(r"\d+\.?\d*", restart_web)[0])//unit + 1
            if bookinfor.iloc[-1, 0] == '-1':
                break
            print('已有文件，从第%d页开始' % restart)
        except:
            bookinfor = pd.DataFrame(columns=['tag', 'bookname', 'url', 'infor', 'introduction', 'score', 'cntnum', 'pageurl'])
            restart = 0
            print('无文件 %s，创建文件' % tag)
        bookinfor = GetBookList(tag, pagenum, unit, bookinfor, restart)
        bookinfor.to_csv('./DoubanData/booklist_%s.csv'%tag,index=False, encoding='utf_8_sig')
        print('写入成功:', tag)
        sleep(10)


if __name__ == '__main__':
    with open('./DoubanData/tag.txt', 'r', encoding='utf-8') as f:
        taglist = f.read()
        taglist = eval(taglist)
    # pool = Pool(5)
    # pool.map(GetAllBookList, taglist)

    for i, tag in enumerate(taglist):
        print('第%d个tag, 总共%d个tag' % (i, len(taglist)))
        GetAllBookList(tag)
