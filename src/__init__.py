from src.common import Constants
from src.dataset import DatasetDownloader
from src.video import VideoReader


def sample_test():
    # drive = DatasetDownloader()
    # dataset_files = drive.get_drive_dataset_files_names()
    # print(dataset_files)
    # print(drive.get_local_dataset_files_names())
    # file_path = drive.download_file_from_drive(dataset_files[2])
    # print(file_path)
    # video = VideoReader(file_path)
    # frames = video.read()
    VideoReader.save_frames_as_video('sample', Constants.LOCAL_DATASET_PATH + 'sample9-frames/')
