import cv2 
import os
import numpy as np
import scipy.io as sio
import time
import sys

import ogl_viewer.viewer as gl 
import pyzed.sl as sl

def image_capture():
    zed = sl.Camera()
    # 设置相机的分辨率720和采集帧率30fps
    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.HD720  # Use HD1080 video mode
    init_params.camera_fps = 30  # fps可选：15、30、60、100
    err = zed.open(init_params)  # 根据自定义参数打开相机
    if err != sl.ERROR_CODE.SUCCESS:
        print('open error')
        exit(1)
    runtime_parameters = sl.RuntimeParameters()  # 设置相机获取参数
    runtime_parameters.sensing_mode = sl.SENSING_MODE.STANDARD  
    i = 0
    # 创建sl.Mat对象来存储图像（容器），Mat类可以处理1到4个通道的多种矩阵格式（定义储存图象的类型）
    image = sl.Mat()  # 图像
    disparity = sl.Mat()  # 视差值
    dep = sl.Mat()  # 深度图
    depth = sl.Mat()  # 深度值
    point_cloud = sl.Mat()  # 点云数据
    # 获取分辨率
    resolution = zed.get_camera_information().camera_resolution
    w, h = resolution.width , resolution.height
    x,y = int(w/2),int(h/2)  # 中心点
    timesp1 = []
    fno = []
    R_data = []
    G_data =[]
    B_data = []
    D_data = []
    data1 = []
    data2 = []
    data3 = []
    fps = 0
    FPS = 100000
    data_file = time.strftime('%Y%m%d%H%M%S',time.localtime()) + '.mat'
   
    while len(timesp1) < FPS:
        # 获取最新的图像，修正它们，并基于提供的RuntimeParameters(深度，点云，跟踪等)计算测量值。
        if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:  # 相机成功获取图象
            # 获取图像
            timestamp = zed.get_timestamp(sl.TIME_REFERENCE.CURRENT)  # 获取图像被捕获时的时间点
            zed.retrieve_image(image, sl.VIEW.LEFT)  # image：容器，sl.VIEW.LEFT：内容
            img_L = image.get_data()  # 转换成图像数组，便于后续的显示或者储存
            zed.retrieve_image(image, sl.VIEW.RIGHT)  
            img_R = image.get_data()  
            # 获取视差值
            zed.retrieve_measure(disparity,sl.MEASURE.DISPARITY,sl.MEM.CPU)
            dis_map = disparity.get_data()
            # 获取深度
            zed.retrieve_measure(depth,sl.MEASURE.DEPTH,sl.MEM.CPU)  # 深度值
            zed.retrieve_image(dep,sl.VIEW.DEPTH)  # 深度图
            depth_map = depth.get_data()
            dep_map = dep.get_data()
           ## 获取点云
           #  zed.retrieve_measure(point_cloud,sl.MEASURE.XYZBGRA,sl.MEM.CPU)
           #  point_map = point_cloud.get_data()
            #print('时间点',timestamp.get_seconds(),'中心点视差值',dis_map[x,y],'中心点深度值',depth_map[x,y],'中心点云数据',point_map[x,y])
            # 利用cv2.imshow显示视图，并对想要的视图进行保存
            view = np.concatenate((cv2.resize(img_L,(640,360)),cv2.resize(dep_map,(640,360))),axis=1)
            # view1 = cv2.resize(point_map,(640,360))
            tp = timestamp.get_milliseconds()
            print('view',view.shape)
            print('timesp',tp)
            print('imag',img_L.shape)
            print('depth',dep_map.shape)
            #print('point',point_map.shape)
            cv2.namedWindow('View',0)
            cv2.imshow("View", view)
            key = cv2.waitKey(1)
            if key & 0xFF == 27:  # esc退出
                break
            # if key & 0xFF == ord('s'):  # 图像保存
            #     savePath = os.path.join("./images", "V{:0>3d}.png".format(i))  # 注意根目录是否存在"./images"文件夹
            #     cv2.imwrite(savePath, view)
            i = i + 1
            fps += 1
            fno.append(int(fps))
            timesp1.append(int(tp))
            #   img 
            data1.append(img_L)
            data11 = np.array(data1)
            
            #   depth
            # cv2.resize(dep_map,(640,360))
            # data2.append(dep_map)
            # data22 = np.array(data2)
            # R_data.append(dep_map[:,:,0])
            # G_data.append(dep_map[:,:,1])
            # B_data.append(dep_map[:,:,2])
            # D_data.append(dep_map[:,:,3])
            
            ##   point cloud
            #data3.append(point_map)
            #data33 = np.array(data3)
            FNO = np.array(fno)
            timesp =np.array(timesp1)
            # RD = np.array(R_data)
            # GD = np.array(G_data)
            # BD = np.array(B_data)
            # DD = np.array(D_data)
    zed.close()
    print('over')

if __name__ =='__main__':
    image_capture()
