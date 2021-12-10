#获取每个标签下的书籍编号
import requests
from lxml import etree
import re
import pandas as pd
from time import sleep
import os
headers = {
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
'Cache-Control': 'max-age=0',
'Connection': 'keep-alive',
'Cookie': 'bid=aStoRYrwXN8; dbcl2="249872952:UGW8oDqEQLE"; gr_user_id=f6e3cf9e-51b4-46de-bdd1-aabf8dca6f5c; _vwo_uuid_v2=D39390021B192FF773CE01FE15106C244|8292a37f118f517dbf88b53aee9f1327; push_doumail_num=0; push_noty_num=0; __gads=ID=3d649453488db278-22505defa0ce00a6:T=1636601693:RT=1636601693:S=ALNI_MavR0SyFTy1-Yr4N2ekWQyfER8C2A; __yadk_uid=iZfrfGVY99nwC0UMxIkFaDq6Gjpi1XLS; ll="118371"; _ga=GA1.1.2122267463.1636888206; __utmv=30149280.24987; _ga_RXNMP372GL=GS1.1.1636888561.1.1.1636889953.0; douban-fav-remind=1; ct=y; ck=VD4Z; __utmc=30149280; __utmc=81379588; ap_v=0,6.0; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=c54d8691-92ac-4424-a3c0-6626fc5f25c0; gr_cs1_c54d8691-92ac-4424-a3c0-6626fc5f25c0=user_id:1; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03_c54d8691-92ac-4424-a3c0-6626fc5f25c0=true; _pk_ref.100001.3ac3=["","",1639149612,"https://www.baidu.com/link?url=gh2PceqhGr8lDb2scDE32V6ZDWbHAW1A9GZWHkOppLn27n42uViGytdscxFC0Cjn&wd=&eqid=bea7bce6001a218b0000000261b37027"]; _pk_ses.100001.3ac3=*; __utma=30149280.2122267463.1636888206.1639146148.1639149612.13; __utmz=30149280.1639149612.13.11.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utma=81379588.1633473874.1636601563.1639146148.1639149612.17; __utmz=81379588.1639149612.17.13.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmt=1; __utmt_douban=1; __utmb=30149280.5.10.1639149612; __utmb=81379588.3.10.1639149612; _pk_id.100001.3ac3=ae28e8ef85c97326.1636601565.18.1639150403.1639147028.',
'Host': 'book.douban.com',
'Referer': 'https://www.douban.com/misc/sorry?original-url=https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4?start=0&type=T',
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

def GetBookList(tag, pagenum, unit, bookinfor):
    curpage = len(bookinfor) // unit
    cnt = len(bookinfor)
    try:
        for start in range(curpage, pagenum*unit, unit):
            url = 'https://book.douban.com/tag/%s?start=%d&type=T' % (tag, start)
            response = requests.get(url, headers = headers, timeout = 20)
            tree = etree.HTML(response.text)
            booklist = tree.xpath('//li[@class="subject-item"]')
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
                    bookinfor.loc[cnt] = [tag, bookname, bookurl, infor, introduction, score, cmtnum]
                    cnt += 1
                except:
                    continue
            print(bookinfor.tail())
            sleep(1)
            if response.status_code != 200:
                print(response.status_code)
                return bookinfor
    except Exception as e:
        print('ERROR:%s' % e)
        return bookinfor
    return bookinfor

with open('./DoubanData/tag.txt', 'r', encoding='utf-8') as f:
    taglist = f.read()
    taglist = eval(taglist)

tag = '小说'
pagenum = 100
unit = 20
if not os.path.isfile('./DoubanData/booklist_%s.csv'%tag): bookinfor = pd.DataFrame(columns=['tag', 'bookname', 'url', 'infor', 'introduction', 'score', 'cntnum'])
else: bookinfor = pd.read_csv('./DoubanData/booklist_%s.csv'%tag)
bookinfor = GetBookList(tag, pagenum, unit, bookinfor)
bookinfor.to_csv('./DoubanData/booklist_%s.csv'%tag,index=False, encoding='utf_8_sig')