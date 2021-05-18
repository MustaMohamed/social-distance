import os
from tqdm import tqdm
from src import VideoReader
from src.common import ImageUtils, DrawerHelper
from src.distance.distance import DistanceCalculator
from src.model.model import HumanDetector
import cv2


class Predictor:
    def __init__(self):
        self.model = HumanDetector()
        self.persons = []
        self.scene_width = 0

    def predict_image(self, img_path, image_width_in_meters):
        self.scene_width = image_width_in_meters
        img = cv2.imread(img_path)
        self.persons = self.model.get_persons_from_model(img)
        img = self.__highlight_person(img)
        img = self.__highlight_risky(img)
        return img

    def predict_video(self, video_path, image_width_in_meters):
        video = VideoReader(video_path)
        frames = video.read()
        for idx, img in enumerate(frames):
            ImageUtils.save_image(os.path.splitext(video_path)[0] + '/' + str(idx) + '.png',
                                  self.predict_image(img, image_width_in_meters))

        res_vid = VideoReader.save_frames_as_video(video_path, frames)
        print("Your result video is under this path: ", res_vid)
        return res_vid


    def __highlight_person(self, img):
        for idx in tqdm(range(len(self.persons))):
            img = DrawerHelper.highlight_person_rectangle_center_circle(img, self.persons[idx], 10, 20)
        return img

    def __highlight_risky(self, img):
        h, img_width, c = img.shape
        dist = DistanceCalculator.compute_distance(self.persons)
        thresh = DistanceCalculator.convert_meters2pixels(1, img_width, 3)
        closest = DistanceCalculator.find_closest(dist, len(self.persons), thresh)
        img = DistanceCalculator.mark_risky_person_with_red(img, self.persons,
                                                            closest[0], closest[1], closest[2], self.scene_width)
        return img
