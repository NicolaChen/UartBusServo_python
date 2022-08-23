import cv2
import numpy as np

mtx = np.load('Cali_params/mtx.npy')
dist = np.load('Cali_params/dist.npy')

cap = cv2.VideoCapture(0)  # 创建一个 VideoCapture 对象
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2000)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2000)
while (cap.isOpened()):  # 循环读取每一帧0
    ret_flag, img = cap.read()
    cv2.imshow('ori', img)
    h, w = img.shape[:2]
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))

# undistort
    dst = cv2.undistort(img, mtx, dist, None)
    
# crop the image
    # x,y,w,h = roi
    # dst = dst[y:y+h, x:x+w]
    cv2.imshow('dst', dst)

    k = cv2.waitKey(1)
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()


