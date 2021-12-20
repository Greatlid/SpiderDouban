#对已经爬取到的书籍链接，获取书籍的各类信息
from time import sleep
import random
import pandas as pd
import os
import requests
from lxml import etree
import re

Cookie = ['bid=IA7RHZwAenQ; gr_user_id=2c1182b4-ae6a-465c-b45f-14c2112e1e3a; _vwo_uuid_v2=D1FAFC514A19B6F1A156AB13F79B140CB|445393e78f93b43449eb0fa7d9099996; dbcl2="249872952:5wMQFpSZ0WA"; ck=SqW6; __utma=30149280.902413818.1639186997.1639294032.1639999092.3; __utmc=30149280; __utmz=30149280.1639999092.3.3.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmt_douban=1; __utmb=30149280.1.10.1639999092; __utma=81379588.1841239901.1639186997.1639294032.1639999092.3; __utmc=81379588; __utmz=81379588.1639999092.3.3.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmt=1; __utmb=81379588.1.10.1639999092; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=1001c1c8-4982-4612-a6ab-7ec074210242; gr_cs1_1001c1c8-4982-4612-a6ab-7ec074210242=user_id:1; _pk_ref.100001.3ac3=["","",1639999093,"https://accounts.douban.com/"]; _pk_id.100001.3ac3=9554397d8a20fdff.1639186997.3.1639999093.1639294032.; _pk_ses.100001.3ac3=*; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03_1001c1c8-4982-4612-a6ab-7ec074210242=true; push_noty_num=0; push_doumail_num=0',
          'bid=aStoRYrwXN8; gr_user_id=f6e3cf9e-51b4-46de-bdd1-aabf8dca6f5c; _vwo_uuid_v2=D39390021B192FF773CE01FE15106C244|8292a37f118f517dbf88b53aee9f1327; push_doumail_num=0; push_noty_num=0; __gads=ID=3d649453488db278-22505defa0ce00a6:T=1636601693:RT=1636601693:S=ALNI_MavR0SyFTy1-Yr4N2ekWQyfER8C2A; __yadk_uid=iZfrfGVY99nwC0UMxIkFaDq6Gjpi1XLS; ll="118371"; _ga=GA1.1.2122267463.1636888206; douban-fav-remind=1; ct=y; _ga_RXNMP372GL=GS1.1.1639545224.3.1.1639545297.0; dbcl2="251664765:Z1TykKtHnrE"; __utmv=30149280.25166; __utmz=30149280.1639889452.34.19.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; ck=nE8Q; ap_v=0,6.0; __utmc=30149280; __utmc=81379588; __utma=30149280.2122267463.1636888206.1639992038.1639998336.38; __utma=81379588.1633473874.1636601563.1639992045.1639998340.43; __utmz=81379588.1639998340.43.25.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/misc/sorry; _pk_ref.100001.3ac3=["","",1639998340,"https://www.douban.com/misc/sorry?original-url=https%3A%2F%2Fbook.douban.com%2Ftag%2F"]; _pk_ses.100001.3ac3=*; __utmt_douban=1; __utmb=30149280.4.10.1639998336; __utmt=1; __utmb=81379588.2.10.1639998340; _pk_id.100001.3ac3=ae28e8ef85c97326.1636601565.43.1639999168.1639993459.']

headers = {
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
'Cache-Control': 'max-age=0',
'Connection': 'keep-alive',
'Cookie': 'bid=aStoRYrwXN8; gr_user_id=f6e3cf9e-51b4-46de-bdd1-aabf8dca6f5c; _vwo_uuid_v2=D39390021B192FF773CE01FE15106C244|8292a37f118f517dbf88b53aee9f1327; push_doumail_num=0; push_noty_num=0; __gads=ID=3d649453488db278-22505defa0ce00a6:T=1636601693:RT=1636601693:S=ALNI_MavR0SyFTy1-Yr4N2ekWQyfER8C2A; __yadk_uid=iZfrfGVY99nwC0UMxIkFaDq6Gjpi1XLS; ll="118371"; _ga=GA1.1.2122267463.1636888206; douban-fav-remind=1; ct=y; _ga_RXNMP372GL=GS1.1.1639545224.3.1.1639545297.0; dbcl2="251664765:Z1TykKtHnrE"; __utmv=30149280.25166; __utmz=30149280.1639889452.34.19.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; ck=nE8Q; ap_v=0,6.0; __utma=30149280.2122267463.1636888206.1639922126.1639992038.37; __utmc=30149280; __utmt=1; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=bb65d49b-53b7-4541-b26e-a44d70021a8a; gr_cs1_bb65d49b-53b7-4541-b26e-a44d70021a8a=user_id:1; __utmt_douban=1; __utma=81379588.1633473874.1636601563.1639922125.1639992045.42; __utmc=81379588; __utmz=81379588.1639992045.42.24.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/misc/sorry; _pk_ref.100001.3ac3=["","",1639992046,"https://www.douban.com/misc/sorry?original-url=https%3A%2F%2Fbook.douban.com%2F"]; _pk_ses.100001.3ac3=*; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03_bb65d49b-53b7-4541-b26e-a44d70021a8a=true; __utmb=30149280.6.10.1639992038; __utmb=81379588.2.10.1639992045; _pk_id.100001.3ac3=ae28e8ef85c97326.1636601565.42.1639992210.1639922125.',
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
    # url = 'https://music.douban.com/'
    try:
        bookname, author, info, pub, score, scorenum, price, ISBN, content, catalogue, label, simbook, comment, userid, bookimageurl = [[None]] * 15
        for i in range(len(Cookie)):
            headers['Cookie'] = Cookie[i]
            response = requests.get(url, headers = headers, timeout = 60)
            print('请求状态：',response.status_code)
            if response.status_code != 200:
                continue
            else: break
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
        score = tree.xpath('//strong[@class="ll rating_num "]/text()')
        scorenum = tree.xpath('//span[@property="v:votes"]/text()')
        userid = tree.xpath('//span[@class="comment-info"]/a/@href')
        userid = list(set(userid))
        bookimageurl = tree.xpath('//a[@class="nbg"]/@href')
    except Exception as e:
        flag = 2
        if re.findall('Read timed out|Max retries exceeded', str(e)): flag = 1
        print('error:%s, url: %s' % (e, url))
        return None, flag
    return (url, bookname, author, info, pub, score, scorenum, price, ISBN, content, catalogue, label, simbook, comment, userid, bookimageurl), flag

def RmDup(listin):
    # 去重
    temp = listin
    listin = list(set(temp))
    listin.sort(key=temp.index)
    return listin


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
                url_queue = url_queue + urllist
        cnt = 0
        bookres = pd.DataFrame(columns=['url', 'bookname', 'author', 'info', 'pub', 'score', 'scorenum', 'price', 'ISBN', 'content', 'catalogue', 'label', 'simbook', 'comment', 'userid', 'bookimageurl'])
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
            _, bookname, author, info, pub, score, scorenum, price, ISBN, content, catalogue, label, simbook, comment, userid, bookimageurl = res
            if not bookname:
                print('无书籍信息')
                url_queue.pop(0)
                continue
            url_list = url_list+[cururl]
            url_queue.pop(0)   #去除当前爬取的书籍信息
            url_queue = url_queue + simbook  #添加待爬取的书籍信息
            isbn_set = isbn_set+ISBN  #添加当前书籍的isbn号

            bookres.loc[cnt] = res
            cnt += 1


            if cnt % save_freq == 0:
                print(bookres.tail())
                print('booknum:', cnt)
                print('booklist:', len(url_list))
                print('queue:', len(url_queue))
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
            sleep(random.random()/4+1)
        else:url_queue.pop(0)
