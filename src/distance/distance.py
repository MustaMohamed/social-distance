from src.common import Constants, DrawerUtils, HumanUtils, ImageUtils
from scipy.spatial import distance
import numpy as np


class DistanceCalculator:
    def __init__(self):
        pass

    """# Compute the persons distance"""

    @staticmethod
    def compute_distance(persons):
        persons_count = len(persons)
        midpoints = HumanUtils.get_humans_mid_points(persons=persons)
        dist = np.zeros((persons_count, persons_count))
        for i in range(persons_count):
            for j in range(i + 1, persons_count):
                if i != j:
                    dst = distance.euclidean(midpoints[i], midpoints[j])
                    dist[i][j] = dst
        return dist

    @staticmethod
    def find_closest(dist, persons_count, thresh):
        p1 = []
        p2 = []
        d = []
        for i in range(persons_count):
            for j in range(i, persons_count):
                if (i != j) & (dist[i][j] <= thresh):
                    p1.append(i)
                    p2.append(j)
                    d.append(dist[i][j])
        return p1, p2, d

    @staticmethod
    def convert_pixels2meters(px: float, img_width: float, img_width_meters: float) -> float:
        return round(px * img_width_meters / img_width, 2)

    @staticmethod
    def convert_meters2pixels(mt: float, img_width: float, img_width_meters: float) -> float:
        return round(mt * img_width / img_width_meters, 2)

    @staticmethod
    def mark_risky_person_with_red(img, persons, p1, p2, dist, image_width_in_meters):
        risky = np.unique(p1 + p2)
        rectangle_line_width = DrawerUtils.get_suit_line_size(img, image_width_in_meters)
        font_scale = DrawerUtils.get_suit_font_size(img, image_width_in_meters)
        for i in risky:
            img = DrawerUtils.highlight_person_risky(img, persons[i], image_width_in_meters, rectangle_line_width)

        mid = []
        for i in range(len(p1)):
            md1 = HumanUtils.get_human_bottom_center_point(persons[p1[i]])
            md2 = HumanUtils.get_human_bottom_center_point(persons[p2[i]])
            mid.append((md1, md2))

        for i in range(len(mid)):
            md = mid[i]
            start, end = md
            img = DrawerUtils.draw_line(img, start, end, line_width=rectangle_line_width, line_color=Constants.DANGER_LINE_COLOR)
            h, w, c = img.shape
            real_dist = DistanceCalculator.convert_pixels2meters(dist[i], w, image_width_in_meters)
            img = DrawerUtils.put_text(img, 'distance: ' + str(real_dist) + ' m',
                                       (min(start[0], end[0]), min(start[1], end[1])), size=font_scale*1.5)

        return img
