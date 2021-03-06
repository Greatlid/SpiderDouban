from time import sleep
import random
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
'Cookie': 'bid=aStoRYrwXN8; gr_user_id=f6e3cf9e-51b4-46de-bdd1-aabf8dca6f5c; _vwo_uuid_v2=D39390021B192FF773CE01FE15106C244|8292a37f118f517dbf88b53aee9f1327; push_doumail_num=0; push_noty_num=0; __gads=ID=3d649453488db278-22505defa0ce00a6:T=1636601693:RT=1636601693:S=ALNI_MavR0SyFTy1-Yr4N2ekWQyfER8C2A; __yadk_uid=iZfrfGVY99nwC0UMxIkFaDq6Gjpi1XLS; ll="118371"; _ga=GA1.1.2122267463.1636888206; douban-fav-remind=1; ct=y; __utmz=30149280.1639545177.23.15.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmz=81379588.1639545177.27.17.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _ga_RXNMP372GL=GS1.1.1639545224.3.1.1639545297.0; ap_v=0,6.0; _pk_ref.100001.3ac3=["","",1639556524,"https://www.baidu.com/link?url=xsntIZ2zGU1zhJ4TSdBjU0ZVfEXc77y92Y6JeG9MSzozYxMNhrg7QyOo_McKcyBo&wd=&eqid=bc64c36f00074bda0000000561b97954"]; _pk_ses.100001.3ac3=*; __utma=30149280.2122267463.1636888206.1639545177.1639556524.24; __utmc=30149280; __utma=81379588.1633473874.1636601563.1639545177.1639556524.28; __utmc=81379588; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=823e75f7-6f2f-4f21-b3a8-db053f0620d4; gr_cs1_823e75f7-6f2f-4f21-b3a8-db053f0620d4=user_id:1; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03_823e75f7-6f2f-4f21-b3a8-db053f0620d4=true; dbcl2="251664765:Z1TykKtHnrE"; ck=nE8Q; __utmt=1; __utmv=30149280.25166; __utmt_douban=1; __utmb=30149280.7.10.1639556524; __utmb=81379588.5.10.1639556524; _pk_id.100001.3ac3=ae28e8ef85c97326.1636601565.29.1639557135.1639545281.',
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
ips = [{'http':'111.20.225.130'}, {'http':'192.168.1.101'}, {'http':'111.20.225.137'}]
def GetUserId(url):
    flag = 0
    try:
        booknam, ISBN, userid, bookimageurl = [[None]] * 4
        for i in range(len(ips)):
            # headers['User-Agent'] = agent_arr[random.randint(0, len(agent_arr)-1)]
            response = requests.get(url, headers = headers, timeout = 60, proxies = ips[i])
            print('???????????????',response.status_code)
            if response.status_code != 200:
                continue
            else: break
        if response.status_code != 200:
            flag = 1  #ip?????????????????????
            return None, flag
        tree = etree.HTML(response.text)
        bookname = tree.xpath('//span[@property="v:itemreviewed"]/text()')
        info = tree.xpath('//div[@id="info"]//text()')
        info = [t for t in info if not '\n' in t]
        for i, t in enumerate(info):
            if t == 'ISBN:': ISBN = [info[i + 1]]
        userid = tree.xpath('//span[@class="comment-info"]/a/@href')
        userid = list(set(userid))
    except Exception as e:
        flag = 2
        if re.findall('Read timed out|Max retries exceeded', str(e)): flag = 1
        print('error:%s, url: %s' % (e, url))
        return None, flag

    return (url, bookname, ISBN, userid), flag

if __name__ == '__main__':
    if os.path.isfile('./UserInfor/userid.csv'):
        with open('./UserInfor/userid_book_url_list.txt', 'r') as f:
            userid_book_url_list = f.read()
            userid_book_url_list = eval(userid_book_url_list)
            f.close()
        with open('./UserInfor/userid_url_list.txt', 'r') as f:
            userid_url_list = f.read()
            userid_url_list = eval(userid_url_list)
            f.close()
        useridres = pd.read_csv('./UserInfor/userid.csv')
        cnt = len(useridres)
        print('??????????????????')

    else:
        cnt = 0
        useridres = pd.DataFrame(columns=['url', 'bookname',  'ISBN', 'userid'])
        userid_book_url_list = []
        userid_url_list = []
        print('????????????')
    with open('./UserInfor/userid_url_queue.txt', 'r') as f:
        userid_url_queue = f.read()
        userid_url_queue = eval(userid_url_queue)
        f.close()

    save_freq = 10
    while 1:
        cururl = userid_url_queue[0]
        if not cururl in userid_book_url_list:
            res, flag = GetUserId(cururl)
            if flag == 1:  #ip??????
                print('ip??????')
                sleep(120)
                continue
            if flag == 2:  #????????????
                print('????????????')
                userid_url_queue.pop(0)
                continue
            url, bookname, ISBN, userid = res
            if not bookname:
                print('???????????????')
                userid_url_queue.pop(0)
                continue
            userid_book_url_list = userid_book_url_list + [url]
            userid_url_queue.pop(0)   #?????????????????????????????????
            useridres.loc[cnt] = res
            userid_url_list += userid
            cnt += 1


            if cnt % save_freq == 0:
                userid_url_list = list(set(userid_url_list))
                print(useridres.tail())
                print('curfilenum:', cnt)
                print('usernum:', len(userid_url_list))
                print('booknum:', len(userid_book_url_list))
                print('queue:', len(userid_url_queue))
                useridres.to_csv('./UserInfor/userid.csv', index=False, encoding='utf_8_sig')
                with open('./UserInfor/userid_book_url_list.txt', 'w') as f:
                    f.write(str(userid_book_url_list))
                    f.close()
                with open('./UserInfor/userid_url_queue.txt', 'w') as f:
                    f.write(str(userid_url_queue))
                    f.close()
                with open('./UserInfor/userid_url_list.txt', 'w') as f:
                    f.write(str(userid_url_list))
                    f.close()

            sleep(random.random()/4+1)
        else:userid_url_queue.pop(0)