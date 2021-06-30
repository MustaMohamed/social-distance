import os
from tqdm import tqdm
from src import VideoReader
from src.common import ImageUtils, DrawerUtils
from src.distance.distance import DistanceCalculator
from src.model.model import HumanDetector
import cv2


class Predictor:
    def __init__(self):
        self.model = HumanDetector()
        self.persons = []
        self.scene_width = 0
        self.threshold_dist = 0

    def predict_image(self, img_path, image_width_in_meters, threshold_dist):
        self.scene_width = image_width_in_meters
        self.threshold_dist = threshold_dist
        img = cv2.imread(img_path)
        h, w, d = img.shape
        if w > 820:
            h = int(820 * h / w)
            w = 820
        if h > 720:
            w = int(720 * w / h)
            h = 720
        img = cv2.resize(img, (w, h), interpolation=cv2.INTER_AREA)
        self.persons = self.model.get_persons_from_model(img)
        img = self.__highlight_person(img, image_width_in_meters)
        img = self.__highlight_risky(img)
        return img

    def predict_image_matrix(self, img, image_width_in_meters):
        self.scene_width = image_width_in_meters
        self.persons = self.model.get_persons_from_model(img)
        img = self.__highlight_person(img)
        img = self.__highlight_risky(img)
        return img

    def predict_video(self, video_path, image_width_in_meters, threshold_distance):
        video = VideoReader(video_path)
        print('\nReading video...\n')
        frames = video.read()
        print('\nPredicting video frames...\n')
        for idx in tqdm(range(len(frames))):
            img = frames[idx]
            ImageUtils.save_image(img, self.predict_image(img, image_width_in_meters, threshold_distance))

        res_vid = VideoReader.save_frames_as_video(video_path, frames)
        print("\nYour result video is under this path: ", res_vid)
        return res_vid

    def __highlight_person(self, img, image_width_in_meters):
        rectangle_line_width = DrawerUtils.get_suit_line_size(img, image_width_in_meters)
        font_scale = DrawerUtils.get_suit_font_size(img, image_width_in_meters)
        for per in self.persons:
            img = DrawerUtils.highlight_person_rectangle_center_circle(img, per, rectangle_line_width, circle_diameter=rectangle_line_width * 2)
        return img

    def __highlight_risky(self, img):
        h, img_width, c = img.shape
        dist = DistanceCalculator.compute_distance(self.persons)
        thresh = DistanceCalculator.convert_meters2pixels(self.threshold_dist, img_width, self.scene_width)
        closest = DistanceCalculator.find_closest(dist, len(self.persons), thresh)
        img = DistanceCalculator.mark_risky_person_with_red(img, self.persons,
                                                            closest[0], closest[1], closest[2], self.scene_width)
        return img
