import cv2
import numpy as np
import glob
# 找棋盘格角点
# 阈值
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# print(cv2.TERM_CRITERIA_EPS,'',cv2.TERM_CRITERIA_MAX_ITER)
#w h分别是棋盘格模板长边和短边规格（角点个数）
w = 9
h = 6

# 世界坐标系中的棋盘格点,例如(0,0,0), (1,0,0), (2,0,0) ....,(8,5,0)，去掉Z坐标，记为二维矩阵，认为在棋盘格这个平面上Z=0
objp = np.zeros((w*h,3), np.float32) #构造0矩阵，88行3列，用于存放角点的世界坐标
objp[:,:2] = np.mgrid[0:w,0:h].T.reshape(-1,2)# 三维网格坐标划分

# 储存棋盘格角点的世界坐标和图像坐标对
objpoints = [] # 在世界坐标系中的三维点
imgpoints = [] # 在图像平面的二维点

images = glob.glob('./test/*.jpeg')
timages = glob.glob('./CalibImages/*.png')
for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # 粗略找到棋盘格角点 这里找到的是这张图片中角点的亚像素点位置，共11×8 = 88个点，gray必须是8位灰度或者彩色图，（w,h）为角点规模
    ret, corners = cv2.findChessboardCorners(gray, (w,h))
    print(corners)
    # 如果找到足够点对，将其存储起来
    if ret == True:
        #精确找到角点坐标
        corners = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)

        #将正确的objp点放入objpoints中
        objpoints.append(objp)
        imgpoints.append(corners)
        # 将角点在图像上显示
        cv2.drawChessboardCorners(img, (w,h), corners, ret)
        cv2.imshow('findCorners',img)
        cv2.waitKey()
cv2.destroyAllWindows()

# 标定
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

# 去畸变
for tfname in timages:
    timg = cv2.imread(tfname)
    h,  w = timg.shape[:2]
    newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),0,(w,h)) # 自由比例参数
    dst = cv2.undistort(timg, mtx, dist, None, newcameramtx)
    # 根据前面ROI区域裁剪图片
    #x,y,w,h = roi
    #dst = dst[y:y+h, x:x+w]
    # dst = cv2.resize(dst,(400,400))
    cv2.imshow('fin',dst)
    # end = time.time() - s
    cv2.waitKey()
cv2.destroyAllWindows()

# 反投影误差
total_error = 0
for i in range(len(objpoints)):
    imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
    error = cv2.norm(imgpoints[i],imgpoints2, cv2.NORM_L2)/len(imgpoints2)
    total_error += error
print ("total error: ", total_error/len(objpoints))