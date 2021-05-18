
class HumanUtils:
    # compute center
    @staticmethod
    def get_human_bottom_center_point(person) -> (int, int):
        x1, y1, x2, y2 = person
        x_center = int((x1 + x2) / 2)
        y_bottom = int(y2)
        bottom_center = (x_center, y_bottom)
        return bottom_center

    @staticmethod
    def get_human_height(person) -> int:
        x1, y1, x2, y2 = person
        return int(y2 - y1)

    @staticmethod
    def get_human_width(person) -> int:
        x1, y1, x2, y2 = person
        return int(x2 - x1)

    @staticmethod
    def get_humans_mid_points(persons):
        mid_points = [HumanUtils.get_human_bottom_center_point(persons[i]) for i in range(len(persons))]
        return mid_points
