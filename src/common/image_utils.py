import cv2


class ImageUtils:
    @staticmethod
    def read_image(img_path):
        return cv2.imread(img_path)

    @staticmethod
    def save_image(img_path, img):
        return cv2.imwrite(img_path, img)