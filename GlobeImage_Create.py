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
