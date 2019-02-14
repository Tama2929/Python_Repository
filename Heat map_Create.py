import certifi
import folium
import urllib3
import numpy as np
import requests
import csv
from folium.plugins import HeatMap

http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where())

readdata = http.request(
        'GET',
        'https://www.data.jma.go.jp/obd/stats/data/mdrr/pre_rct/alltable/pre24h00_rct.csv',
        preload_content=False)

# Yhoo!サイト(緯度経度の取得)
payload = {'appid': '******************************************************', # IDを入力
           'output': 'json',
           'al': 2,
           'recursive': 'true'}

url = 'https://map.yahooapis.jp/geocode/V1/geoCoder'

# csv読み込み
cities_list = np.empty([0, 1296]) #1297の市町村をcsvファイルから取得し格納
csv_file = open("./cities.csv", "r", encoding="ms932", errors="", newline="" )
f = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
for row in f:
        cities_list = np.append(cities_list, np.array([row]))


# データ整形(byte型→str型)
data = str(readdata.data.decode('shift_jis')).split('\r\n')

# 不要なデータの削除
data.pop(0)
data.pop()
list_data = np.empty((0, 9), str) # 整形後のデータを格納

cunt = 0 # エラーカウントの変数
table_name = ['地点名','緯度','経度','年','月','日','時','分','降水量']
list_data = np.append(list_data, np.array([table_name]), axis=0)
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
                array_data[8] = array_data[8]
                array_data[1] = coordinates[1]
                array_data[2] = coordinates[0]

                if len(array_data) == 9:
                        list_data = np.append(list_data, np.array([array_data]), axis=0)
        except:
                cunt += 1

coordinates_plus = []
print(list_data[:,2])
long = list(list_data['経度'])

lat = list(list_data['緯度'])
precipitation = list('降水量')

for k, i, ic in zip(long, lat, precipitation):
        coordinates_plus.append((i, k, float(ic)))

Heat_map = folium.Map(location=[37.6441550, 139.0175760], zoom_start=6)
for x in range(len(array_data)):
        Heat_map.add_child(HeatMap(coordinates_plus, radius=12))

# ヒートマップの作成
#


Heat_map.save("Heat_map.html")