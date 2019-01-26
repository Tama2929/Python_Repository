import cv2

#  ファイルパス
folderName = './Image Folder/globe/'

# 動画作成
fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
video = cv2.VideoWriter('./Image Folder/video.mp4', fourcc, 20.0, (640, 480))

for i in range(360):
    img = cv2.imread(folderName+'fig_{:04}'.format(i)+'.png')
    img = cv2.resize(img, (640,480))
    video.write(img)

video.release()