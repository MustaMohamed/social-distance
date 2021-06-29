from src.common import Constants, FileUtils, ImageUtils
from src.dataset import DatasetDownloader
from src.video import VideoReader
from src.model import Predictor
import os
import cv2
from tkinter import filedialog as fd, simpledialog as sd, Tk
import tkinter


def start_app():
    # read file
    # file_path = str(input("Enter the file path : "))
    root = tkinter.Tk()
    file_path = fd.askopenfilename(parent=root)
    scene_width = sd.askfloat("Scene Width", "Please enterimage scene width?", parent=root)
    print(file_path, scene_width)
    # scene_width = float(input("Enter scene width in meter : "))
    # check file type
    if FileUtils.get_file_type(file_path) == FileUtils.FILE_TYPE_NOT_SUPPORTED:
        print('\n The file type not supported!!\n')
        return
    # init predictor
    predictor = Predictor()
    if FileUtils.get_file_type(file_path) == FileUtils.FILE_TYPE_IMAGE:
        print('\nStart prediction\n')
        img = predictor.predict_image(file_path, scene_width)
        print('\nFinish prediction\n')
        img_name = FileUtils.get_out_image_path(file_path)
        print('Output image in ' + img_name)
        ImageUtils.save_image(img_name, img)
        ImageUtils.display_image(img_name, root)
  
    elif FileUtils.get_file_type(file_path) == FileUtils.FILE_TYPE_VIDEO:
        video = predictor.predict_video(file_path, scene_width)


if __name__ == '__main__':
    start_app()
