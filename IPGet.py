# -*- coding:utf-8 -*-
import urllib.request as urllib2
import gc
import socket
import functools
import ssl
import sys
import random
import requests
from bs4 import BeautifulSoup
# import Crawler

default_encoding = 'utf-8'
# if sys.getdefaultencoding() != default_encoding:
#     reload(sys)

# sys.setdefaultencoding(default_encoding)
#
# reload(sys)

agent_arr = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E) ",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400) ",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E) ",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE) ",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E) ",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E) ",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E) ",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E) ",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E) ",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0) ",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:16.0) Gecko/20121026 Firefox/16.0",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-CN; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
    "Mozilla/5.0 (Linux; U; Android 2.2.1; zh-cn; HTC_Wildfire_A3333 Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"
]

sys.path.append("..")
socket.setdefaulttimeout(20.0)
urllib2.socket.setdefaulttimeout(20)
urllib2.disable_warnings = True



def cb_print(str):
    print(str)
    # pass

# 强制ssl使用TLSv1
def sslwrap(func):
    @functools.wraps(func)
    def bar(*args, **kw):
        kw['ssl_version'] = ssl.PROTOCOL_TLSv1
        return func(*args, **kw)
    return bar

ssl.wrap_socket = sslwrap(ssl.wrap_socket)

ip_arr = []

def get_ip_arr():
    gc.enable()
    try:
        url = 'http://vtp.daxiangdaili.com/ip/?tid=559609709731038&num=2000&delay=1&protocol=https'
        headers = {"User-Agent": "Mozilla/5.0"}
        req = urllib2.Request(url, headers=headers)
        res = urllib2.urlopen(req, timeout=20)
        res = res.read()
        ips_arr = res.split('\r\n')
        return ips_arr
    except Exception as e:
        cb_print('ip_arr_error:{}'.format(e))
    gc.collect()

def get_66_ip(index):
    gc.enable()
    try:
        url = 'http://www.66ip.cn/'+str(index)
        headers = {"User-Agent": "Mozilla/5.0"}
        req = urllib2.Request(url, headers=headers)
        res = urllib2.urlopen(req, timeout=20)
        res = res.read()
        # print res
        soup = BeautifulSoup(res, "html.parser")
        table_arr = soup('table')
        ip_soup_arr = table_arr[len(table_arr)-1]('tr')
        ips_arr = []
        for it in ip_soup_arr:
            if it != ip_soup_arr[0]:
                ip = it('td')[0].string
                port = it('td')[1].string
                ip_port = ip + ':' + port
                ips_arr.append(ip_port)
        return ips_arr
    except Exception as e:
        cb_print('ip_arr_error:{}'.format(e))
    gc.collect()


def get_xici_ip():
    gc.enable()
    try:
        url = 'http://www.xicidaili.com/wn/'
        headers = {"User-Agent": "Mozilla/5.0"}
        req = urllib2.Request(url, headers=headers)
        res = urllib2.urlopen(req, timeout=20)
        res = res.read()
        soup = BeautifulSoup(res, "html.parser")
        table_arr = soup('table')
        ip_soup_arr = table_arr[len(table_arr) - 1]('tr')
        ips_arr = []
        for it in ip_soup_arr:
            if it != ip_soup_arr[0]:
                ip = it('td')[1].string
                port = it('td')[2].string
                ip_port = ip + ':' + port
                ips_arr.append(ip_port)
        return ips_arr
    except Exception as e:
        cb_print('ip_arr_error:{}'.format(e))
    gc.collect()

def get_kuaidaili_ip(maxpage):
    ips_arr_all = []
    for i in range(1,maxpage+1):
        url = 'https://www.kuaidaili.com/free/inha/%d/' % i
        gc.enable()
        try:
            req = urllib2.Request(url, headers={"User-Agent":agent_arr[0]})
            res = urllib2.urlopen(req, timeout=20)
            res = res.read()
            soup = BeautifulSoup(res, "html.parser")
            # soup.find_all()
            table_arr = soup('table')
            ip_soup_arr = table_arr[len(table_arr) - 1]('tr')
            ips_arr = []
            for it in ip_soup_arr:
                if it != ip_soup_arr[0]:
                    ip = it('td')[0].string
                    port = it('td')[1].string
                    ip_port = ip + ':' + port
                    ips_arr.append(ip_port)
            ips_arr_all += ips_arr


        except Exception as e:
            cb_print('ip_arr_error:{}'.format(e))
            gc.collect()
            continue
    return ips_arr_all



def test_ip(ips, num):
    gc.enable()
    useful_ip = []
    for ip in ips:
        cb_print(ip)
        y = random.randint(0, len(agent_arr) - 1)
        agent = agent_arr[y]
        try:
            # proxy = urllib2.ProxyHandler({'http': ip})
            # opener = urllib2.build_opener(proxy)
            # urllib2.install_opener(opener)
            # url = 'https://api.douban.com/v2/book/' + str(num)
            url = "https://www.baidu.com/"
            headers = {"User-Agent": agent}
            # req = urllib2.Request(url, headers=headers)
            # res = urllib2.urlopen(req, timeout=5)
            # res = res.read()
            response = requests.get(url, headers = headers, proxies = {'http': ip})
            print ('结果是'+response.text)
            if response.status_code == 200:
                useful_ip.append({'http': ip})
        except Exception as e:
            if not e:
                cb_print('e = can not get e!')
            elif isinstance(e, urllib2.URLError):
                if format(e) == 'HTTP Error 404: Not Found':
                    print ('404 Not Found')
                    # SqlOperation.insert_none_book_id(num)
                    continue
                else:
                    cb_print('urllib2.URLError = ' + format(e))
            else:
                print ('insert_error_book_id')
                # SqlOperation.insert_error_book_id(num)
                continue
        finally:
            gc.collect()
    cb_print('end!')
    return useful_ip

# 测试id为10554308 的可用性
# test_ip(10554308)
# 测试方法
ips = get_kuaidaili_ip(10)
print (ips)
# ips = ['111.20.225.148:8080']
useful_ip = test_ip(ips, 10554308)
print(useful_ip)