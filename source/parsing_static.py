#!/usr/bin/python3
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from requests import get
def search(x):
    try:
        query=str(x)
        query = query.replace(" ", "+")
        url='https://www.google.com/search?q=' + query
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        html = get(url, headers=headers).text
        soup = BeautifulSoup(html, "html.parser")
        res = soup.find('span', attrs={'class': 'st'})
        res=res.get_text()
        return res
    except:
        res="Check your Internet connection"
        return res


# print (search("Україна"))