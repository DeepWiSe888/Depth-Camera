import sys
import pyzed.sl as sl
import numpy as np
import cv2
from pathlib import Path
import enum
import scipy.io as sio
import time


def progress_bar(percent_done, bar_length=50):
    done_length = int(bar_length * percent_done / 100)
    bar = '=' * done_length + '-' * (bar_length - done_length)
    sys.stdout.write('[%s] %f%s\r' % (bar, percent_done, '%'))
    sys.stdout.flush()

def main():
    # Create a ZED camera object
    
    zed = sl.Camera()
    
    
    
    # Set SVO path for playback
    
    input_path = sys.argv[1]
    output_path = Path(sys.argv[2])
    init_parameters = sl.InitParameters()
    init_parameters.set_from_svo_file(input_path)
    
    
    
    # Open the ZED
    
    zed = sl.Camera()
    err = zed.open(init_parameters)
    
    
    # Prepare single image containers
    left_image = sl.Mat()
    right_image = sl.Mat()
    depth_image = sl.Mat()
    point_cloud = sl.Mat()
    timesp1 = []
    R_data = []
    G_data = []
    B_data = []
    D_data = []
    FNO = []
    fps = 0
    data_file = time.strftime('%Y%m%d%H%M%S',time.localtime()) + '.mat'
    nb_frames = zed.get_svo_number_of_frames()
    while True:
        if zed.grab() == sl.ERROR_CODE.SUCCESS:
            # Read side by side frames stored in the SVO
            timestamp = zed.get_timestamp(sl.TIME_REFERENCE.IMAGE)
            tp = timestamp.get_milliseconds()
            svo_position = zed.get_svo_position();    
            ## RGBD
            zed.retrieve_image(left_image, sl.VIEW.LEFT)
            img_L = left_image.get_data()
            zed.retrieve_image(right_image, sl.VIEW.RIGHT)
            img_R = right_image.get_data()
            zed.retrieve_image(depth_image,sl.VIEW.DEPTH)
            dep_map = depth_image.get_data()
            
            # save 
            
            FNO.append(svo_position)
            timesp1.append(int(tp))
            # R_data.append(dep_map[:,:,0])
            # G_data.append(dep_map[:,:,1])
            # B_data.append(dep_map[:,:,2])
            # D_data.append(dep_map[:,:,3])
            timesp =np.array(timesp1)
            fno =np.array(FNO)
            # RD = np.array(R_data)
            # GD = np.array(G_data)
            # BD = np.array(B_data)
            # DD = np.array(D_data)

        progress_bar((svo_position - 1 ) / nb_frames * 100, 30)
        # Check if we have reached the end of the video
        if svo_position >= (nb_frames - 2 ):  # End of SVO    
                print('p',svo_position)
                print('f',nb_frames)
                print("SVO end has been reached. Looping back to first frame")
                break

    zed.close()
    # sio.savemat(data_file,{'time':timesp,'frame':FNO,'R_data':R_data,'G_data':G_data,'B_data':B_data,'D_data':D_data})  # 保存RGBD  数据量很大慎用
    sio.savemat(data_file,{'time':timesp,'frame':FNO})                                                                    # 保存帧号与时间戳
    print('over')
    return 0
if  __name__ == "__main__":
    main()
