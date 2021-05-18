import cv2
from src.common.human_utils import HumanUtils
from src.common.constants import Constants


class DrawerHelper:

    def __init__(self):
        pass

    @staticmethod
    def draw_rectangle(img, position: (float, float, float, float), rectangle_line_width: int = 10, box_color=Constants.BOX_COLOR):
        x1, y1, x2, y2 = position
        img = cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), box_color, rectangle_line_width)
        return img

    @staticmethod
    def draw_circle(img, center: (int, int), diameter: int, circle_color=Constants.CIRCLE_COLOR):
        img = cv2.circle(img, center, int(diameter), circle_color, -1)
        return img

    @staticmethod
    def draw_line(img, start, end, line_width: int = 10, line_color=Constants.BOX_COLOR):
        img = cv2.line(img, start, end, line_color, line_width)
        return img

    @staticmethod
    def put_text(img, text, pos, size=1, color=Constants.FONT_COLOR_GREEN):
        font = cv2.FONT_HERSHEY_DUPLEX
        x, y = pos
        img = cv2.putText(img, text, (int(x), int(y)), font, size, color, 2, cv2.LINE_AA)
        return img

    @staticmethod
    def highlight_person_rectangle(img, person, box_line_width: int = 10, box_color=Constants.BOX_COLOR):
        x1, y1, x2, y2 = person
        img = DrawerHelper.draw_rectangle(img, (x1, y1, x2, y2), box_line_width, box_color)
        return img

    @staticmethod
    def highlight_person_risky(img, person, box_line_width: int = 10):
        x1, y1, x2, y2 = person
        img = DrawerHelper.highlight_person_rectangle(img, (x1, y1, x2, y2), box_line_width, Constants.DANGER_BOX_COLOR)
        wid = HumanUtils.get_human_width(person)
        img = DrawerHelper.draw_rectangle(img, (x1, y1, x1 + wid, y1 - 100), -1, Constants.DANGER_BOX_COLOR)
        img = DrawerHelper.put_text(img, 'Violation!!', (x1 + 20, y1 - 25), 2, Constants.FONT_COLOR_WHITE)
        return img

    @staticmethod
    def highlight_person_rectangle_center_circle(img, person, rectangle_line_width: int = 10,
                                                 box_color=Constants.BOX_COLOR,
                                                 circle_diameter: int = 5,
                                                 circle_color=Constants.CIRCLE_COLOR):
        person_mid = HumanUtils.get_human_bottom_center_point(person)
        img = DrawerHelper.highlight_person_rectangle(img, person, rectangle_line_width, box_color)
        img = DrawerHelper.draw_circle(img, person_mid, circle_diameter, circle_color)
        return img
