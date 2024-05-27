import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk


class VideoApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Застосування фільтрів")

        self.video_source = None
        self.cap = None
        self.video_width = 640
        self.video_height = 480

        self.create_widgets()

    def create_widgets(self):
        self.video_label = tk.Label(self)
        self.video_label.pack()

        self.open_file_button = tk.Button(self, text="Вибрати файл", command=self.open_file)
        self.open_file_button.pack()

        self.filter_buttons = []
        filters = ["Віддзеркалення", "Ши-Томасі", "Кольорове перетворення", "Гаусів фільтр"]
        for filter_name in filters:
            button = tk.Button(self, text=filter_name, command=lambda f=filter_name: self.apply_filter(f))
            button.pack()
            self.filter_buttons.append(button)

        self.open_camera_button = tk.Button(self, text="Увімкнути веб-камеру", command=self.open_camera)
        self.open_camera_button.pack()

        self.stop_button = tk.Button(self, text="Стоп", command=self.stop_video)
        self.stop_button.pack()

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi")])
        if file_path:
            self.video_source = file_path
            self.cap = cv2.VideoCapture(file_path)
            self.play_video()

    def open_camera(self):
        self.video_source = 0
        self.cap = cv2.VideoCapture(self.video_source)
        self.play_video()

    def play_video(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (self.video_width, self.video_height))
            img = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=img)
            self.video_label.img = img
            self.video_label.config(image=img)
            self.video_label.after(10, self.play_video)
        else:
            self.stop_video()

    def stop_video(self):
        if self.cap:
            self.cap.release()
            self.video_source = None
            cv2.destroyAllWindows()

    def apply_filter(self, filter_name):
        if self.cap:
            ret, frame = self.cap.read()
            if ret:
                if filter_name == "Віддзеркалення":
                    frame = self.apply_mirror(frame)
                elif filter_name == "Ши-Томасі":
                    frame = self.apply_corner_detection(frame,max_corners=20, quality_level=0.01, min_dist=50)
                elif filter_name == "Кольорове перетворення":
                    frame = self.apply_colorspace_change(frame,'YUV')
                elif filter_name == "Гаусів фільтр":
                    frame = self.apply_gaussian_filter(frame, kernel_size=11)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                img = ImageTk.PhotoImage(image=img)
                self.video_label.img = img
                self.video_label.config(image=img)

    def apply_mirror(self, frame):
        rows, cols = frame.shape[:2]
        src_points = np.float32([[0, 0], [cols - 1, 0], [0, rows - 1]])
        dst_points = np.float32([[cols - 1, 0], [0, 0], [cols - 1, rows - 1]])
        affine_matrix = cv2.getAffineTransform(src_points, dst_points)
        img_output = cv2.warpAffine(frame, affine_matrix, (cols, rows))
        return img_output

    def apply_corner_detection(self, frame, max_corners=5, quality_level=0.01, min_dist=20):
        new_frame = frame.copy()
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners = cv2.goodFeaturesToTrack(gray_frame, max_corners, quality_level, min_dist)
        corners = np.int0(corners)
        for item in corners:
            x, y = item.ravel()
            cv2.circle(new_frame, (x, y), 5, (255, 255, 255), -1)
        return new_frame

    def apply_colorspace_change(self, frame, colorspace_index=cv2.COLOR_BGR2GRAY):
        return cv2.cvtColor(frame, colorspace_index)

    def apply_gaussian_filter(self, frame, kernel_size=3):
        return cv2.GaussianBlur(frame, (kernel_size, kernel_size), 0)


if __name__ == "__main__":
    app = VideoApp()
    app.mainloop()
