# Python3.5
# HTMLデータを取得
import requests

URL = 'http://traininfo.jreast.co.jp/train_info/kanto.aspx'
res = requests.get(URL)
content = res.text

# table 要素を取得
from bs4 import BeautifulSoup as BS

bs = BS(content, "lxml")
tables = bs.find_all("table")

import numpy as np


def get_element(table):
    # tbodyタグの取得
    tbody = table.find("tbody")

    # 取得した要素の格納配列
    rows = [1]
    alts = [1]

    # 路線名の要素取得
    trs = tbody.find_all("tr")
    for tr in trs:
        # th要素が空なのか判定
        if tr.find('th') is not None:
            row = [td.text for td in tr.find_all(["th"])]
            rows.append(row)

    # 不要な要素の削除
    del rows[0]

    # 運行状況の要素取得
    article = tbody.find_all(class_="acess_i")
    for x in article:
        img = x.find("img")
        alt = [img["alt"]]
        if alt != '':
            alts.append(alt)

    # 不要な要素の削除
    del alts[0]

    # 配列結合
    re_rows = np.hstack([rows, alts])

    return re_rows

# 格納する配列
route = np.array([])

# 配列の結合
for x in range(len(tables)):
    table = tables[x]
    result = get_element(table)
    route = np.append(route, result)

print(route)