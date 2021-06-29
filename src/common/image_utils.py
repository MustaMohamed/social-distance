import cv2


class ImageUtils:
    @staticmethod
    def read_image(img_path):
        return cv2.imread(img_path)

    @staticmethod
    def save_image(img_path, img):
        return cv2.imwrite(img_path, img)

    @staticmethod
    def get_image_width(img):
        h, w, d = img.shape
        return w

    @staticmethod
    def get_image_height(img):
        h, w, d = img.shape
        return h

    @staticmethod
    def display_image(img_path, parent = None):
        from PIL import ImageTk, Image  
        import tkinter
        if parent is None:
            parent = tkinter.Tk()
        img = Image.open(img_path)
        img = img.resize((550, 650), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)

        panel = tkinter.Label(parent, image = img)
        panel.pack(side = "bottom", fill = "both", expand = "yes")
        parent.mainloop()
