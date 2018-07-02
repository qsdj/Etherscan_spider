#!/usr/bin/env python3
#encoding:utf-8
# author qsdj

import requests
import re
import time
from datetime import datetime
from pyquery import PyQuery as pq


def get_code(address=""):
    token_url = address
    print("//spider token_url\t"+token_url+"\n")
    # just pq(token_url) throw timeout error sometime
    html = requests.get(url=token_url).text
    html_dom = pq(html)
    token_code = html_dom("pre#editor").html()  # .encode("utf8",'ignore')
    print("//parser token_url\t"+token_url+"\n")
    if token_code != None and token_code != "":
        token_name = html_dom(
            "#ContentPlaceHolder1_tr_tokeninfo > td:nth-child(2) > a").text().replace(" ", "_")
        token_Transactions = html_dom(
            "#ContentPlaceHolder1_divSummary > div:nth-child(1) > table  > tr:nth-child(4) > td >span").text()
        token_price = html_dom(
            "#balancelistbtn > span.pull-left").text().split(" ")
        token_price = token_price[1] if len(token_price) == 2 else ""
        spider_time = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        token_contact = html_dom(
        "#ContentPlaceHolder1_tr_tokeninfo > td:nth-child(2) > a").attr('href').replace("/token/", "")
        with open("./tokens_code/"+token_contact+"_"+token_name+".sol", 'w') as fp:
            fp.write("//token_name\t"+token_contact+"_"+token_name+"\n")
            fp.write("//token_url\t"+token_url+"\n")
            fp.write("//spider_time\t"+spider_time+"\n")
            fp.write("//token_Transactions\t"+token_Transactions+"\n")
            fp.write("//token_price\t"+token_price+"\n\n")
            fp.write(token_code)
            print("write down\n")
        print("//token_name\t"+token_contact+"_"+token_name+"\n")
        print("//spider_time\t"+spider_time+"\n")
        print("//token_Transactions\t"+token_Transactions+"\n")
        print("//token_price\t"+token_price+"\n")
        print("\n"+token_code+"\n")


for x in 'abcdefghijklmnopqrstuvwxyz0123456789':
    domain = "https://etherscan.io/searchHandler?term=%s" % x
    r = requests.get(domain)
    pattern = re.compile('0x[a-fA-F0-9]{32,42}', re.S)
    items = re.findall(pattern, r.text)
    for i in tuple(items):
        a = 'https://etherscan.io/address/'+i+'#code'
        print("正在处理链接:"+a+"\n")
        try:
            time.sleep(5)
            get_code(a)
        except AttributeError:
            print(a+"该合约没有contact"+"\n")
