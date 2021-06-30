from tkinter import filedialog, messagebox
from tkinter import *
from PIL import ImageTk, Image
from src.common import Constants, FileUtils, ImageUtils
from src.model import Predictor
import cv2
from tkvideo import tkvideo


class UIComponent(object):
    pass


class Window:

    components = UIComponent()

    def __init__(self):
        self.progress = None
        self.window = Tk()
        self.init_window()
        self.predictor = Predictor()

    def init_window(self):
        self.window.title("COVID-19 Protocol")
        self.window.geometry("840x950")
        Window.components.browse_file_label = Label(self.window, text="Please select the file to work on")
        Window.components.browse_file_label.place(x=20, y=20)
        Window.components.browse_btn = Button(self.window, text="Browse", command=self.read_file)
        Window.components.browse_btn.place(x=650, y=47)
        Window.components.file_path_read_only = Text(self.window, height=1, width=60)
        Window.components.file_path_read_only.place(x=20, y=50)
        Window.components.file_path_read_only.configure(state=DISABLED)
        Window.components.file_path_read_only.bind("<1>", lambda event: self.components.file_path_read_only.focus_set())
        # meter to pixels scene width
        scene_label = Label(self.window, text="Please enter the scene width of the image in meters")
        scene_label.place(x=20, y=80)
        Window.components.scene_width_text = Text(self.window, height=1, width=10)
        Window.components.scene_width_text.place(x=400, y=80)

        # covid protocol distance in meters
        threshold_label = Label(self.window, text="Please enter covid protocol threshold distance")
        threshold_label.place(x=20, y=130)
        Window.components.threshold_distance_text = Text(self.window, height=1, width=10)
        Window.components.threshold_distance_text.place(x=400, y=130)
        # Start
        Window.components.start_btn = Button(self.window, text="Start", command=self.start_model)
        Window.components.start_btn.place(x=350, y=170)
        # Canvas for result
        Window.components.canvas = Canvas(self.window, width=820, height=720)
        Window.components.canvas.place(x=10, y=220)

    def start(self):
        self.window.mainloop()

    def read_file(self):
        file_path = filedialog.askopenfilename(parent=self.window)
        Window.components.file_path_read_only.configure(state=NORMAL)
        Window.components.file_path_read_only.delete('1.0', END)
        Window.components.file_path_read_only.insert('1.0', file_path)
        Window.components.file_path_read_only.configure(state=DISABLED)
        return file_path

    def display_image(self, img_path):
        h, w, d = cv2.imread(img_path).shape
        if w > 820:
            h = 820 * h / w
            w = 820

        if h > 720:
            w = 720 * w / h
            h = 720
        img = Image.open(img_path)
        img = img.resize((int(w), int(h)), Image.ANTIALIAS)
        Window.components.canvas.res_img = img = ImageTk.PhotoImage(img)
        Window.components.canvas.create_image((0, 0), anchor=NW, image=Window.components.canvas.res_img)
        Window.components.canvas.image = Window.components.canvas.res_img

    def validate_input(self, file_path, scene_width, threshold_distance):
        if FileUtils.get_file_type(file_path) == FileUtils.FILE_TYPE_NOT_SUPPORTED:
            messagebox.showerror("Input Error", "File should be an image or video!")
            return False

        if not self.validate_number(scene_width):
            messagebox.showerror("Input Error", "Scene width should be a number!")
            return False

        if not self.validate_number(threshold_distance):
            messagebox.showerror("Input Error", "Threshold distance should be a number!")
            return False

        return True

    def validate_number(self, val):
        if val.isdigit():
            return True
        try:
            float(val)
            return True
        except ValueError:
            return False

    def start_model(self):
        Window.components.file_path_read_only.configure(state=NORMAL)
        file_path = Window.components.file_path_read_only.get("1.0", END).strip()
        Window.components.file_path_read_only.configure(state=DISABLED)
        scene_width = Window.components.scene_width_text.get("1.0", END)
        threshold_dist = Window.components.threshold_distance_text.get("1.0", END)
        if self.validate_input(file_path, scene_width, threshold_dist):
            if FileUtils.get_file_type(file_path) == FileUtils.FILE_TYPE_IMAGE:
                self.predict_image(file_path, float(scene_width), float(threshold_dist))
            elif FileUtils.get_file_type(file_path) == FileUtils.FILE_TYPE_VIDEO:
                self.predict_video(file_path, float(scene_width), float(threshold_dist))

    def predict_image(self, file_path, scene_width, threshold_distance):
        img = self.predictor.predict_image(file_path, scene_width, threshold_distance)
        print('\nFinish prediction\n')
        img_name = FileUtils.get_out_image_path(file_path)
        print('Output image in ' + img_name)
        ImageUtils.save_image(img_name, img)
        self.display_image(img_name)

    def predict_video(self, file_path, scene_width, threshold_distance):
        video = self.predictor.predict_video(file_path, scene_width, threshold_distance)
        my_label = Label(self.window)
        my_label.place(x=10, y=220)
        player = tkvideo.tkvideo(video, my_label, loop=1, size=(820, 720))
        player.play()








