from lxml import etree
import re
import pandas as pd
import numpy as np

#################################################
#define constant
INF = 100
MAXFILE = 5
NONEFLAG = '-1'

###########################
#匹配最佳的书
res_df = pd.DataFrame(columns=('题名', '信息', '网址'))
res_all = {}
bookinfor = pd.read_csv('./data/bookinfor.csv')
for i in range(0, len(bookinfor)):
    print('当前匹配书籍为%d' % i)
    try:
        booktitle = bookinfor.iloc[i, 0]
        bookauthor = bookinfor.iloc[i, 1]
        bookpublisher = bookinfor.iloc[i, 2]
        if not isinstance(booktitle, str): booktitle = ''
        if not isinstance(bookauthor, str): bookauthor = ''
        if not isinstance(bookpublisher, str): bookpublisher = ''

        tree = etree.parse('./html/%d.html' % i, etree.HTMLParser())
        bookdetail = tree.xpath('//div[@class="detail"]')
        # bookdetail = tree.xpath('//div[@id="wrapper"]//div[@class="item-root"]')
        res_url, res_title, res_infor = [], [], []
        for detail in bookdetail:
            url_temp = detail.xpath('.//a/@href')
            title_temp = detail.xpath('.//a/text()')

            if url_temp: res_url += url_temp
            else: res_url += [NONEFLAG]
            if title_temp: res_title += title_temp
            else:  res_title += [NONEFLAG]
            infor_temp = detail.xpath('.//div[@class="meta abstract"]/text()')
            if infor_temp: res_infor += infor_temp
            else: res_infor += [NONEFLAG]

        # res_url = tree.xpath('//div[@class="title"]/a/@href')
        # res_title = tree.xpath('//div[@class="title"]/a/text()')
        # res_infor = tree.xpath('//div[@class="meta abstract"]/text()')


        matchdegree_title = []

        for title in res_title:
            booktitle = booktitle.replace('+', '\+')
            title = title.replace('+', '\+')
            matchres = re.match(booktitle, title)
            if matchres != None:
                matchrange = matchres.span()
                matchdegree_title.append(len(title) - matchrange[1] + matchrange[0])
            else:
                matchdegree_title.append(INF)

        matchdegree_author = []
        for infor in res_infor:
            matchres = re.findall(bookauthor, infor)
            if matchres:
                matchdegree_author.append(0)
                # matchrange = matchres.span()
                # matchdegree_author.append(len(infor[0]) - matchrange[1] + matchrange[0])
            else:
                matchdegree_author.append(INF)

        matchdegree_pub = []
        for infor in res_infor:
            matchres = re.findall(bookpublisher, infor)
            if matchres:
                matchdegree_pub.append(0)
                # matchrange = matchres.span()
                # matchdegree_pub.append(len(infor[1]) - matchrange[1] + matchrange[0])
            else:
                matchdegree_pub.append(INF)

        match_ind = np.lexsort((matchdegree_pub, matchdegree_title, matchdegree_author))
        if len(match_ind) > 0:
            useful_infor = [res_title[match_ind[0]], res_infor[match_ind[0]], res_url[match_ind[0]]]
        else: useful_infor = [NONEFLAG]*3
        print('找到的书为%s' % (str(useful_infor)))
        res_all['i'] = useful_infor
        res_df.loc[i] = useful_infor
    except Exception as e:
        print('error: %s' % e)
        res_df.to_csv('./data/bookurl.csv',index=False)
        break

res_df.to_csv('./data/bookurl.csv',index=False)



