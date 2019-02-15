# Python3.5
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

#  ファイルパス
folderName = './Image Folder/globe/'

#　地球儀の画像作成
for i in range(360):
    map = Basemap(projection='ortho', lat_0=20, lon_0=i,resolution='l', area_thresh=1000.0)
    map.drawcoastlines()
    map.drawcountries()
    map.fillcontinents(color='chartreuse')
    map.drawmeridians(np.arange(0, 360, 30))
    map.drawparallels(np.arange(-90, 90, 30))
    plt.savefig(folderName+'fig_{:04}'.format(i)+'.png')
    plt.close()

# 動画作成
import cv2

fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
video = cv2.VideoWriter('./Image Folder/video.mp4', fourcc, 20.0, (640, 480))

for i in range(360):
    img = cv2.imread(folderName+'fig_{:04}'.format(i)+'.png')
    img = cv2.resize(img, (640,480))
    video.write(img)

video.release()
