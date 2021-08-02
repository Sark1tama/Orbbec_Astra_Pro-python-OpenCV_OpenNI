import cv2
import numpy as np
from OpenNIClass import OpenniClass

astra = OpenniClass("/home/sark1tama/软件/OpenNI-Linux-Arm64-2.3.0.66/Redist")

def mousecallback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        print(y, x, depthImg[y, x])

if __name__ == "__main__":

    cv2.namedWindow('depth')
    cv2.setMouseCallback('depth', mousecallback)

    while True:

        colorImg  = astra.color_read()

        # 原始深度图像
        depthImg = astra.depth_read()

        #  保留特定深度值范围
        # depthImg  = astra.depth_read_range(5000,12000)

        # 标准化到uint8格式以便运行cv算法
        # depthImg = astra.depth_read_format()
        # edge = cv2.Canny(depthImg, 100, 200)
        # cv2.imshow('edge', edge)

        cv2.imshow('color', colorImg)
        cv2.imshow('depth', depthImg)


        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break

    astra.destroy()
