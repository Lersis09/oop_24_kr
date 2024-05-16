import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk

class TaskWindow(tk.Frame):
    """Класс MainWindow, наследующий Frame"""

    def __init__(self, parent):
        """Настройка графического интерфейса"""
        super().__init__(parent)
        # Растянуть фрейм
        self.pack(fill=tk.BOTH, expand=1)
        # Растянуть сетку
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # Создание виджетов (4 командные кнопки)
        self.but1 = tk.Button(self, text="Геометричне перетворення(дзеркальне відображення)", command=self.show_video1)
        self.but2 = tk.Button(self, text="Операція над зображенням(детекція кутів Ши-Томасі)", command=self.show_video2)
        self.but3 = tk.Button(self, text="Кольорове перетворення(YUV)", command=self.show_video3)
        self.but4 = tk.Button(self, text="Фільтрація зображення(Гаусів фільтр)", command=self.show_video4)
        # Создание метки для отображения видео
        self.label_video = tk.Label(self)
        self.label_video.grid(row=0, column=0, sticky="nsew")
        # Размещение виджетов в сетке основного окна
        self.but1.grid(row=1, column=0, sticky="nsew")
        self.but2.grid(row=1, column=1, sticky="nsew")
        self.but3.grid(row=1, column=2, sticky="nsew")
        self.but4.grid(row=1, column=3, sticky="nsew")

    def show_video1(self):
        self.show_video_from_file("step_3.py")

    def show_video2(self):
        self.show_video_from_file("step_6.py")

    def show_video3(self):
        self.show_video_from_file("step_4.py")

    def show_video4(self):
        self.show_video_from_file("step_5.py")

    def show_video_from_file(self, filename):
        cap = cv2.VideoCapture(filename)
        if not cap.isOpened():
            print(f"Помилка: не вдається відкрити файл {filename}")
            return

        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                img = ImageTk.PhotoImage(image=img)
                self.label_video.img = img
                self.label_video.config(image=img)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            else:
                print(f"Помилка: не вдається прочитати кадр з файлу {filename}")
                break

        cap.release()
        cv2.destroyAllWindows()


