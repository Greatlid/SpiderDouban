import requests
#################
#普通爬虫方式
headers = {
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
'Cache-Control': 'max-age=0',
'Connection': 'keep-alive',
'Cookie': 'bid=aStoRYrwXN8; dbcl2="249872952:UGW8oDqEQLE"; gr_user_id=f6e3cf9e-51b4-46de-bdd1-aabf8dca6f5c; push_doumail_num=0; push_noty_num=0; __gads=ID=3d649453488db278-22505defa0ce00a6:T=1636601693:RT=1636601693:S=ALNI_MavR0SyFTy1-Yr4N2ekWQyfER8C2A; ll="118371"; _ga=GA1.1.2122267463.1636888206; __utmv=30149280.24987; _ga_RXNMP372GL=GS1.1.1636888561.1.1.1636889953.0; douban-fav-remind=1; ck=VD4Z; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=3ae859a8-3a66-4599-8a09-7912d30b03fc; gr_cs1_3ae859a8-3a66-4599-8a09-7912d30b03fc=user_id%3A1; __utma=30149280.2122267463.1636888206.1638974242.1639024585.4; __utmc=30149280; __utmz=30149280.1639024585.4.4.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmt_douban=1; ap_v=0,6.0; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03_3ae859a8-3a66-4599-8a09-7912d30b03fc=true; _pk_ref.100001.2939=%5B%22%22%2C%22%22%2C1639024589%2C%22https%3A%2F%2Fbook.douban.com%2F%22%5D; _pk_id.100001.2939=78508f6f925daba6.1638545921.4.1639024589.1638975700.; _pk_ses.100001.2939=*; __utmt=1; __utmb=30149280.3.10.1639024585',
'Host': 'search.douban.com',
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


data = {
'search_text': '平凡的世界',
'cat': '1001',
'start': '15'
}
response = requests.get(url = url, headers = headers, proxies = {'http':'121.13.252.62'}, data = data)
pagetext = response.text
with open('./web.html', 'wb') as f:
    f.write(response.content)
    f.close()
tree = etree.HTML(pagetext)