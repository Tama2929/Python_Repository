# Python3.5
import certifi
import folium
import urllib3
import numpy as np
import requests
import csv
from folium.plugins import HeatMap
import sys

# 再起呼び出しの最大数をセット
sys.setrecursionlimit(2000000000)

# 気象庁のデータ取得
http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where())

readdata = http.request(
        'GET',
        'https://www.data.jma.go.jp/obd/stats/data/mdrr/pre_rct/alltable/pre24h00_rct.csv',
        preload_content=False)

# Yhoo!サイト(緯度経度の取得)
payload = {'appid': '******************************************************', # YhooのAppID
           'output': 'json',
           'al': 2,
           'recursive': 'true'}

url = 'https://map.yahooapis.jp/geocode/V1/geoCoder'

# csv読み込み
cities_list = np.empty([0, 1296]) #1297の市町村をcsvファイルから取得し格納
csv_file = open("./cities.csv", "r", encoding="ms932", errors="", newline="" )
f = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\n", quotechar='"', skipinitialspace=True)
for row in f:
        cities_list = np.append(cities_list, np.array([row]))

# データ整形(byte型→str型)
data = str(readdata.data.decode('shift_jis')).split('\r\n')

# 不要なデータの削除
data.pop(0)
data.pop()

# 整形後のデータを格納
list_data = np.empty((0, 9), str)

# データの整形
for line in range(len(data)):
        address = ''
        array_data = data[line].split(',')

        # 不要なデータの削除
        del array_data[10:]
        del array_data[0]

        address = cities_list[line]
        array_data[0] = array_data[0] + address
        try:
                payload["query"] = address
                r = requests.get(url, params=payload)
                res = r.json()

                for i in res["Feature"]:
                        coordinates= i["Geometry"]["Coordinates"].split(',')
                array_data[8] = float(array_data[8])
                array_data[1] = coordinates[1]
                array_data[2] = coordinates[0]

                if len(array_data) == 9:
                        list_data = np.append(list_data, np.array([array_data]), axis=0)
        except:
                print('error：'+ address)

print('データの整形完了')

# ヒートマップ作成
coordinates_plus = []

long = list(list_data[:,2])
lat = list(list_data[:,1])
precipitation = list(list_data[:,8])

for k, i, ic in zip(long, lat, precipitation):
        coordinates_plus.append((float(i), float(k), float(ic)))

Heat_map = folium.Map(location=[37.6441550, 139.0175760], zoom_start=6)

for x in range(len(coordinates_plus)):
        folium.Map([coordinates_plus[x][0],coordinates_plus[x][1]]).add_to(Heat_map)

Heat_map.add_child(HeatMap(coordinates_plus, radius=12))

Heat_map.save("Heat_map.html")