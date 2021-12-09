#根据ISBN号获取书籍信息
import requests
from Headers import *
ISBN = '9787567596825'
# ISBN = '9787530212004'
apikey = '11519.2e1d8a82e29922b23633bc65e10cf5f1.9f6d5de1b464fc1e03db4fe721d1ffdd'
url = 'https://api.jike.xyz/situ/book/isbn/%s?apikey=%s' % (ISBN, apikey)

response = requests.get(url, headers = {"User-Agent":agent_arr[0]})
print(response)
res = response.json()
print(res)


