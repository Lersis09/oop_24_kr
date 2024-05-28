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
        self.video_width = 540
        self.video_height = 380
        self.create_widgets()
        self.create_filter_controls()

    def create_filter_controls(self):
        self.filter_controls = {}

        self.filter_params_frame = tk.Frame(self)
        self.filter_params_frame.pack()

        gaussian_label = tk.Label(self.filter_params_frame, text="Розмір ядра Гаусового фільтру:")
        gaussian_label.grid(row=0, column=0, padx=5, pady=5)
        self.gaussian_kernel_size_entry = tk.Entry(self.filter_params_frame)
        self.gaussian_kernel_size_entry.insert(0, "3")
        self.gaussian_kernel_size_entry.grid(row=0, column=1, padx=5, pady=5)

        mirror_label = tk.Label(self.filter_params_frame, text="Віддзеркалення (0/1):")
        mirror_label.grid(row=1, column=0, padx=5, pady=5)
        self.mirror_entry = tk.Entry(self.filter_params_frame)
        self.mirror_entry.insert(0, "0")
        self.mirror_entry.grid(row=1, column=1, padx=5, pady=5)

        shi_tomasi_label = tk.Label(self.filter_params_frame, text="Макс. к-ть кутів:")
        shi_tomasi_label.grid(row=2, column=0, padx=5, pady=5)
        self.shi_tomasi_max_corners_entry = tk.Entry(self.filter_params_frame)
        self.shi_tomasi_max_corners_entry.insert(0, "20")
        self.shi_tomasi_max_corners_entry.grid(row=2, column=1, padx=5, pady=5)

        yuv_label = tk.Label(self.filter_params_frame, text="Канал U кольорового простору YUV:")
        yuv_label.grid(row=3, column=0, padx=5, pady=5)
        self.yuv_u_channel_entry = tk.Entry(self.filter_params_frame)
        self.yuv_u_channel_entry.insert(0, "0")
        self.yuv_u_channel_entry.grid(row=3, column=1, padx=5, pady=5)

        apply_button = tk.Button(self.filter_params_frame, text="Застосувати параметри", command=self.apply_filters)
        apply_button.grid(row=4, columnspan=2, padx=5, pady=5)

        self.filter_controls["Гаусів фільтр"] = self.gaussian_kernel_size_entry
        self.filter_controls["Віддзеркалення"] = self.mirror_entry
        self.filter_controls["Ши-Томасі"] = self.shi_tomasi_max_corners_entry
        self.filter_controls["Кольорове перетворення"] = self.yuv_u_channel_entry

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
            frame = cv2.cvtColor(frame, 4)
            frame = cv2.resize(frame, (self.video_width, self.video_height))
            img = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=img)
            self.video_label.img = img
            self.video_label.config(image=img)
            self.video_label.after(30, self.play_video)
        else:
            self.stop_video()

    def stop_video(self):
        if self.cap:
            self.cap.release()
            self.video_source = None
            cv2.destroyAllWindows()

    def apply_filters(self):
        if self.cap:
            ret, frame = self.cap.read()
            if ret:
                for filter_name, entry in self.filter_controls.items():
                    if filter_name == "Віддзеркалення":
                        mirror_value = int(entry.get())
                        frame = self.apply_mirror(frame, mirror_value)
                    elif filter_name == "Ши-Томасі":
                        max_corners = int(entry.get())
                        frame = self.apply_corner_detection(frame, max_corners)
                    elif filter_name == "Кольорове перетворення":
                        colorspace_index = int(entry.get())
                        frame = self.apply_colorspace_change(frame, colorspace_index)
                    elif filter_name == "Гаусів фільтр":
                        kernel_size = int(entry.get())
                        frame = self.apply_gaussian_filter(frame, kernel_size)
                frame = cv2.cvtColor(frame, 4)
                img = Image.fromarray(frame)
                img = ImageTk.PhotoImage(image=img)
                self.video_label.img = img
                self.video_label.config(image=img)

    def apply_mirror(self, frame, mirror_value):
        rows, cols = frame.shape[:2]
        src_points = np.float32([[0, 0], [cols - 1, 0], [0, rows - 1]])
        dst_points = np.float32([[cols - 1, 0], [0, 0], [cols - 1, rows - 1]])
        affine_matrix = cv2.getAffineTransform(src_points, dst_points)
        img_output = cv2.warpAffine(frame, affine_matrix, (cols, rows))
        return img_output

    def apply_corner_detection(self, frame, max_corners, quality_level=0.01, min_dist=20):
        new_frame = frame.copy()
        gray_frame = cv2.cvtColor(frame, 6)
        corners = cv2.goodFeaturesToTrack(gray_frame, max_corners, quality_level, min_dist)
        corners = np.intp(corners)
        for item in corners:
            x, y = item.ravel()
            cv2.circle(new_frame, (x, y), 5, (255, 255, 255), -1)
        return new_frame

    def apply_colorspace_change(self, frame, colorspace_index=6):
        return cv2.cvtColor(frame, colorspace_index)

    def apply_gaussian_filter(self, frame, kernel_size):
        return cv2.GaussianBlur(frame, (kernel_size, kernel_size), 0)


if __name__ == "__main__":
    app = VideoApp()
    app.mainloop()
