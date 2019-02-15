# Python3.5
import urllib3
import certifi
import datetime


# CSVファイル読込関数
def getprecipitation():
    http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where())

    readdata = http.request(
        'GET',
        'https://www.data.jma.go.jp/obd/stats/data/mdrr/pre_rct/alltable/pre24h00_rct.csv',
        preload_content=False)

    return readdata


# ファイル出力関数
def createfile():
    # ファイル名の生成
    now_time = datetime.datetime.now()
    year = str(now_time.year)
    month = str(now_time.month)
    day = str(now_time.day)
    hour = str(now_time.hour)
    minute = str(now_time.minute)
    filename = './Image Folder/map/' + year + month + day + hour + minute + '.png'

    return filename


# 配列格納関数
def storearray(csv_data):
    # 二次元配列の初期化
    precipitation_list = np.empty((0, 29), str)

    # bytes型からstr型への変換
    a = str(csv_data.data.decode('shift_jis'))

    # 配列を行別に分割(空白、改行削除)
    row = a.split("\r\n")

    # 配列格納処理
    for i in range(len(row)):  # 横のライン
        # 配列を列別に分割
        data_list = row[i].split(',')

        if len(data_list) == 29:
            precipitation_list = np.append(precipitation_list, np.array([data_list]), axis=0)

    return precipitation_list


# 要素抽出関数
def deleteelement(storearray):
    # 二次元配列の初期化
    precipitation_list = np.empty((0, 29), str)

    precipitation_list = storearray[:, [1, 11]]

    return precipitation_list


Prefectures_list = [
    '北海道', '青森県', '岩手県', '宮城県', '秋田県', '山形県', '福島県',
    '茨城県', '栃木県', '群馬県', '埼玉県', '千葉県', '東京都', '神奈川県',
    '新潟県', '富山県', '石川県', '福井県', '山梨県', '長野県', '岐阜県', '静岡県', '愛知県',
    '三重県', '滋賀県', '京都府', '大阪府', '兵庫県', '奈良県', '和歌山県',
    '鳥取県', '島根県', '岡山県', '広島県', '山口県',
    '徳島県', '香川県', '愛媛県', '高知県',
    '福岡県', '佐賀県', '長崎県', '熊本県', '大分県', '宮崎県', '鹿児島県', '沖縄県'
]

# 地図作成関数
from japanmap import *
import matplotlib.pyplot as plt


def precipitation(precipitation_list):
    # 色を塗る都道府県の配列
    color_map = list(range(1))

    # 降水量データの内容確認
    for x in range(len(precipitation_list)):

        # 降水量データの0番目、空白の箇所をスキップ
        if x != 0 and precipitation_list[x, 1] != '':

            # String型→Float型
            num = float(precipitation_list[x, 1])

            # 雨の降ってる箇所を抽出
            result = extractdata(num, x, precipitation_list)

            # color_map内を検索
            a = result in color_map

            # 検索結果で色を塗る都道府県を抽出
            if a == False and color_map[0] == 0:
                color_map[0] = result

            elif result != '' and a != True:
                color_map.append(result)

    # 辞書型データの作成
    dicdata = dictionarydata(color_map)

    return dicdata


# データ抽出関数
def extractdata(num, x, precipitation_list):
    if num != 0.0:
        for i in range(len(Prefectures_list)):
            if precipitation_list[x, 0].startswith(Prefectures_list[i]):
                result = Prefectures_list[i]
    else:
        result = ''

    return result


# 辞書型データの作成
def dictionarydata(color_map):
    # 色の配列
    color = list(range(1))

    # 色の配列作成
    for x in range(len(color_map)):
        if x == 0:
            color[0] = 'blue'
        else:
            color.append('blue')

    # dict型データの作成
    dic = dict(zip(color_map, color))

    return dic


if __name__ == '__main__':
    # CSVファイル読込関数
    dfgetprecipitation = getprecipitation()

    # 配列格納関数
    dfstorearray = storearray(dfgetprecipitation)

    # 要素抽出関数
    dfdeleteelement = deleteelement(dfstorearray)

    # 地図作成関数
    dfprecipitation = precipitation(dfdeleteelement)

    # ファイル名作成関数
    dffilename = createfile()

    plt.imshow(picture(dfprecipitation))
    plt.show(dfprecipitation)
