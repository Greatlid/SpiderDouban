#获取豆瓣分类标签
import requests
from lxml import etree
import re

headers = {
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
'Cache-Control': 'max-age=0',
'Connection': 'keep-alive',
'Cookie': 'bid=aStoRYrwXN8; dbcl2="249872952:UGW8oDqEQLE"; gr_user_id=f6e3cf9e-51b4-46de-bdd1-aabf8dca6f5c; _vwo_uuid_v2=D39390021B192FF773CE01FE15106C244|8292a37f118f517dbf88b53aee9f1327; push_doumail_num=0; push_noty_num=0; __gads=ID=3d649453488db278-22505defa0ce00a6:T=1636601693:RT=1636601693:S=ALNI_MavR0SyFTy1-Yr4N2ekWQyfER8C2A; __yadk_uid=iZfrfGVY99nwC0UMxIkFaDq6Gjpi1XLS; ll="118371"; _ga=GA1.1.2122267463.1636888206; __utmv=30149280.24987; _ga_RXNMP372GL=GS1.1.1636888561.1.1.1636889953.0; douban-fav-remind=1; ct=y; ck=VD4Z; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=f14d8598-9c18-4726-a4eb-0127d41c1d70; gr_cs1_f14d8598-9c18-4726-a4eb-0127d41c1d70=user_id:1; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03_f14d8598-9c18-4726-a4eb-0127d41c1d70=true; _pk_ref.100001.3ac3=["","",1639139188,"https://www.baidu.com/link?url=cVjiKNRAe37JgfpiJZHMwt2fh8oPLSP3VBxQ0RS0IxGxbRijkKnFyuKByArl5CKN&wd=&eqid=cf0fd61500036eed0000000661b3476b"]; _pk_ses.100001.3ac3=*; __utma=30149280.2122267463.1636888206.1639118634.1639139188.11; __utmc=30149280; __utmz=30149280.1639139188.11.10.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utma=81379588.1633473874.1636601563.1639118634.1639139188.15; __utmc=81379588; __utmz=81379588.1639139188.15.12.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmb=30149280.3.10.1639139188; __utmb=81379588.3.10.1639139188; _pk_id.100001.3ac3=ae28e8ef85c97326.1636601565.16.1639139267.1639119956.',
'Host': 'book.douban.com',
'Referer': 'https://book.douban.com/',
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
url = 'https://book.douban.com/tag/?icn=index-nav'

response = requests.get(url, headers = headers)
print(response.status_code)

pagetext = response.text
tree = etree.HTML(pagetext)
res = tree.xpath('//div[@class="grid-16-8 clearfix"]//a/@href')
res = [re.sub(r'/tag/', '', t) for t in res]
print(res)
with open('./DoubanData/tag.txt', 'w', encoding='utf-8') as f:
    f.write(str(res[1:]))

