import cv2
import shutil
import os
import re
from tqdm import tqdm

from src.common import Constants


class VideoReader:
    __video_path: str = ''
    frames_path = ''

    def __init__(self, video_path: str):
        self.__video_path = video_path
        self.frames_path = os.path.splitext(video_path)[0] + '-frames/'
        self.__init_frames_folder(self.frames_path)

    def read(self):
        frames_count = 0
        frames_names = []
        # capture video
        capture_reader = cv2.VideoCapture(self.__video_path)

        # Check if video file is opened successfully
        if not capture_reader.isOpened():
            print("Error opening video stream or file")

        ret, first_frame = capture_reader.read()

        # Read until video is completed
        while capture_reader.isOpened():
            # Capture frame-by-frame
            ret, frame = capture_reader.read()

            if ret:
                # save each frame to folder
                cv2.imwrite(self.frames_path + str(frames_count) + '.png', frame)
                frames_names.append(self.frames_path + str(frames_count) + '.png')
                frames_count = frames_count + 1
                # if(frames_count==1500):
                #   break
            # Break the loop
            else:
                break
        # frame rate of a video
        fps = capture_reader.get(cv2.CAP_PROP_FPS)
        print('Frames rate fps: ' + str(fps))
        return frames_names

    def play(self):
        cap = cv2.VideoCapture(self.__video_path)

        while cap.isOpened():
            ret, frame = cap.read()
            # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            cv2.imshow(self.__video_path, frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

    @staticmethod
    def save_frames_as_video(video_name, frames_path):
        frames = os.listdir(frames_path)
        frames.sort(key=lambda f: int(re.sub('\D', '', f)))
        frame_array = []
        size = (100, 100)
        for i in tqdm(range(len(frames))):
            # reading each files
            img = cv2.imread(frames_path + frames[i])
            if img is None:
                continue
            # img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            height, width, layers = img.shape
            size = (width, height)
            # inserting the frames into an image array
            frame_array.append(img)

        # fourcc = cv2.VideoWriter_fourcc(*'DIVX')
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_out = Constants.LOCAL_DATASET_PATH + '{}-out.mp4'.format(video_name)
        out = cv2.VideoWriter(video_out,
                              fourcc, 25, size)

        for i in tqdm(range(len(frame_array))):
            # writing to a image array
            out.write(frame_array[i])
        out.release()
        return video_out

    def __init_frames_folder(self, frames_path):
        if os.path.exists(frames_path):
            shutil.rmtree(frames_path)
        os.mkdir(frames_path)
