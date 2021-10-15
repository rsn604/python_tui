#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# bookoff.py
#
from selenium import webdriver
from bs4 import BeautifulSoup
import time

categories = []
rows = []

def get_category(address):
    if address[:len('東京都')] != '東京都':
        return
    pos = address.find('区')
    if pos == -1:
        pos = address.find('市')
        if pos == -1:
            return
    category = address[len('東京都'):pos+1]
    if category not in categories:
        categories.append(category)
    return category

def put_shop(html):
    bs = BeautifulSoup(html, "html.parser")
    shops = bs.find('div', class_="shop-detail-lists").find_all('div', class_="shop-detail-item")
    for shop in shops:
        shop_name = shop.find('a').get_text()
        ss = shop.find_all('dd')
        shop_address = ss[0].get_text()
        category = get_category(shop_address)
        del ss[0]
        row = category+","+shop_name+","+shop_address
        for s in ss:
            t = s.get_text().strip()
            if len(t) > 0:
                row += ","+t
        rows.append(row)

#driver = webdriver.PhantomJS()
driver = webdriver.Chrome()
driver.get("https://www.bookoff.co.jp/shop/search-result.html#opt_prefecture=13_%E6%9D%B1%E4%BA%AC%E9%83%BD/opt_and_or=and")
time.sleep(1)

while True:
    put_shop(driver.page_source)
    try:
        element = driver.find_element_by_link_text("次のページ")
    except :
        break
    element.click()
    time.sleep(3)
driver.quit()
#
print("ブックオフ店舗情報(東京都),name,address", end="")
for category in categories:
    print(","+category, end="")
print()
for row in rows:
    print(row)

