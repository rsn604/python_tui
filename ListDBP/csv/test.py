#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# test.py
#
from selenium import webdriver
from bs4 import BeautifulSoup
import time

driver = webdriver.Chrome()
driver.get("https://www.bookoff.co.jp/shop/search-result.html#opt_prefecture=13_%E6%9D%B1%E4%BA%AC%E9%83%BD/opt_and_or=and")

bs = BeautifulSoup(driver.page_source, "html.parser")
print(bs.prettify()) 
driver.quit()

