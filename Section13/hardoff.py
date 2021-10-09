#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# hardoff.py
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
    store_lists =  bs.find('ul', class_="store_list2")
    shops = store_lists.find_all('h3', class_="store_list2_ttl")
    data = store_lists.find_all('div', class_="store_list2_data")
    for i, shop in enumerate(shops):
        shop_name = shop.get_text()
        details = data[i].find_all('p')
        shop_address = details[0].get_text().split()[1]
        category = get_category(shop_address)
        del details[0]
        row = category+","+shop_name+","+shop_address
        for detail in details:
            t = detail.get_text().strip()
            if len(t) > 0:
                row += ","+t
        rows.append(row)

driver = webdriver.Chrome()
driver.get("https://www.hardoff.co.jp/shop/list/?a=13&w=&t1=on&t3=on&t8=on&t5=on&t4=on&t6=on&t2=on&t9=on")
time.sleep(1)
while True:
    put_shop(driver.page_source)
    try:
        element = driver.find_element_by_link_text("»")
    except :
        break
    element.click()
    time.sleep(3)
driver.quit()

#
print("ハードオフ店舗情報(東京都),name,address", end="")
for category in categories:
    print(","+category, end="")
print()
for row in rows:
    print(row)

