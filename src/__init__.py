from src.common import Constants, FileUtils, ImageUtils
from src.dataset import DatasetDownloader
from src.video import VideoReader
from src.model import Predictor


def start_app():
    # read file
    file_path = str(input("Enter the file path : "))
    scene_width = int(input("Enter scene width in meter : "))
    # check file type
    if FileUtils.get_file_type(file_path) == FileUtils.FILE_TYPE_NOT_SUPPORTED:
        print('\n The file type not supported!!\n')
        return
    # init predictor
    predictor = Predictor()
    if FileUtils.get_file_type(file_path) == FileUtils.FILE_TYPE_IMAGE:
        img = predictor.predict_image(file_path, scene_width)
        ImageUtils.save_image(file_path, img)
    elif FileUtils.get_file_type(file_path) == FileUtils.FILE_TYPE_VIDEO:
        video = predictor.predict_video(file_path, scene_width)


if __name__ == '__main__':
    start_app()
