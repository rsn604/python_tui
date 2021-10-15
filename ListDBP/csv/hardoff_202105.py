import time
import requests
from bs4 import BeautifulSoup

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

def put_shop(url):
    response = requests.get(url)
    bs = BeautifulSoup(response.text, 'html.parser')
    tr_tags = bs.find('div', class_="search__result__list__sp sp-only").find("table").find_all('tr')

    for tr in tr_tags:
        td = tr.find('td')
        if td != None:
            th = tr.find('th')
            shop_name = th.get_text().strip()
            ss = td.get_text().split()
            shop_address = ss[1]
            category = get_category(shop_address)
            del ss[0:2]
            row = category+","+shop_name+","+shop_address
            for s in ss:
                row += ","+s.strip()
            rows.append(row)

url = 'https://www.hardoff.co.jp/shop/kanto/tokyo/page/{}/'
for i in range(1,9):
    put_shop(url.format(i))
    time.sleep(1)

print("ハードオフ店舗情報(東京都),name,address", end="")
for category in categories:
    print(","+category, end="")
print()
for row in rows:
    print(row)
