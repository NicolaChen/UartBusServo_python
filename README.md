# UartBusServo_python
Python codes for control Feetech&amp;Hiwonder UART bus servo.

## myCheckSum.py
（通信领域8位）累加和取反校验的python实现

## Camera Calibration
1. 运行VideoMatGen.py，弹出棋盘识别框后，移动棋盘至多种不同角度，移动完成后按`esc`键退出，将生成畸变矫正所需的矩阵文件mtx3.npy和dist3.npy
2. 运行VidCalib.py，可以看到矫正前后的视频画面对比。