###########################
#数据预处理，提取人名，去掉无书名信息

import pandas as pd
import re

bookinfor = pd.read_csv('./data/书籍信息精简版.csv', delimiter=',',  encoding=u'gbk')
bookinfor_new = bookinfor.copy(deep=True)
bookinfor_new = bookinfor_new.drop_duplicates(subset = ['题名', '作者', '出版社'])
bookinfor_new = bookinfor_new.dropna(subset = ['题名'])
bookinfor_new = bookinfor_new.reset_index(drop=True)
# idx = []
# for i in range(len(bookinfor_new)):
#     if not isinstance(bookinfor_new.iloc[i,0], str):
#         idx.append(i)
# bookinfor_new = bookinfor_new.drop(idx)
for i in range(len(bookinfor_new)):
    if isinstance(bookinfor_new.iloc[i,1], str):
        bookinfor_new.iloc[i, 1] = re.split('[,\s，]', bookinfor_new.iloc[i, 1])[0]
# bookinfor_new = bookinfor_new.fillna('-1')
print(bookinfor_new.head())
bookinfor_new.to_csv('./data/bookinfor.csv', index=0)