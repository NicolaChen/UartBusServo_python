import cv2
import numpy as np
import time
# 找棋盘格角点
# 阈值
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
#w h分别是棋盘格模板长边和短边规格（角点个数）
w = 7
h = 7

objp = np.zeros((w*h,3), np.float32) 
objp[:,:2] = np.mgrid[0:w,0:h].T.reshape(-1,2)

# 储存棋盘格角点的世界坐标和图像坐标对
objpoints = [] # 在世界坐标系中的三维点
imgpoints = [] # 在图像平面的二维点

cam = cv2.VideoCapture(0)
while(cam.isOpened()):
    retR, frame = cam.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    retF, corners = cv2.findChessboardCorners(gray, (w,h))
    if retF == True:
        #精确找到角点坐标
        corners = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)

        #将正确的objp点放入objpoints中
        objpoints.append(objp)
        imgpoints.append(corners)
         # 将角点在图像上显示
        cv2.drawChessboardCorners(frame, (w,h), corners, retF)
        cv2.imshow('findCorners', frame)
        print('Find one, hold 5s for adjust.')
        time.sleep(5)
    if cv2.waitKey(10) == 27:
        break
cv2.destroyAllWindows()

# 标定
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

np.save('./Cali_params/mtx.npy', mtx)
np.save('./Cali_params/dist.npy', dist)
print('done!')