import cv2
import numpy as np

sources = {'video1': "C:/Users/User/PycharmProjects/oop/video/bunnies.mp4", 'video2':  "web"}


# клас обробки відео-даних
class VideoProcessing:

    # конструктор
    def __init__(self, filename):
        self.__filename = filename
        self.__mode = 0
        self.__mode_to_func = {1: VideoProcessing.colorspace_change, 2: VideoProcessing.mirror,
                               3: VideoProcessing.corner_detector, 4: VideoProcessing.gaussian_filtration}
        self.__mode_to_step = {0: "Basic", 1: "Colorspace", 2: "Geometric", 3: "Operation", 4: "Filtration"}
        self.__stop_flag = False

    def change_input(self, new_filename):
        self.__filename = new_filename

    def set_mode(self, mode_key):
        self.__mode = mode_key

    def get_current_mode_name(self):
        return self.__mode_to_step.get(self.__mode)

    @staticmethod
    def colorspace_change(input_frame):
        return cv2.cvtColor(input_frame, cv2.COLOR_BGR2YUV)

    @staticmethod
    def mirror(input_frame):
        rows, cols = input_frame.shape[:2]
        src_points = np.float32([[0, 0], [cols - 1, 0], [0, rows - 1]])
        dst_points = np.float32([[cols - 1, 0], [0, 0], [cols - 1, rows - 1]])
        affine_matrix = cv2.getAffineTransform(src_points, dst_points)
        img_output = cv2.warpAffine(input_frame, affine_matrix, (cols, rows))
        return img_output

    @staticmethod
    def corner_detector(input_frame, max_corners=5, quality_level=0.01, min_dist=20):
        new_image = input_frame.copy()
        gray_image = cv2.cvtColor(input_frame, cv2.COLOR_BGR2GRAY)
        corners = cv2.goodFeaturesToTrack(gray_image, max_corners, quality_level, min_dist)
        corners = np.float32(corners)
        for item in corners:
            x, y = item[0]
            cv2.circle(new_image, (int(x), int(y)), 5, 255, -1)
        return new_image

    @staticmethod
    def gaussian_filtration(input_frame, kernel_size=3):
        return cv2.GaussianBlur(input_frame, (kernel_size, kernel_size), 0)

    # методи класу
    def start_processing(self):
        cap = cv2.VideoCapture(self.__filename)
        self.__stop_flag = False
        # Перевірка готовності веб-камери
        while cap.isOpened() and not self.__stop_flag:
            # Запис фреймів
            ret, frame = cap.read()
            # При виникненні помилці запису
            if not ret:
                print("Помилка запису фрейму!")
                break

            frame_changed = self.__modify_frame(frame)

            # Відображення результату
            cv2.imshow('frame', frame)
            cv2.imshow('frame_changed', frame_changed)
            self.__state_check()
        # Завершуємо запис у кінці роботи
        cap.release()
        cv2.destroyAllWindows()
        # зчитування відео з веб-камери
        cap = cv2.VideoCapture(self.__filename)
        self.__stop_flag = False
        # перевірка готовності веб-камери
        while cap.isOpened() and not self.__stop_flag:
            # Запис фреймів
            ret, frame = cap.read()
            # при виникненні помилки запису
            if not ret:
                print("Помилка запису файлу")
                break

                # Відображення результату
                cv2.imshow('frame', frame)
                cv2.imshow('frame_changed', frame_changed)
                self.__state_check()
            # Завершуємо запис у кінці роботи
            cap.release()
            cv2.destroyAllWindows()

    def __state_check(self):
        key_code = cv2.waitKey(25)
        if key_code == ord('0'):
            self.set_mode(0)
        elif key_code == ord('1'):
            self.set_mode(1)
        elif key_code == ord('2'):
            self.set_mode(2)
        elif key_code == ord('3'):
            self.set_mode(3)
        elif key_code == ord('4'):
            self.set_mode(4)
        elif key_code == ord('q'):
            self.__stop_flag = True
        print(self.get_current_mode_name())


    def __modify_frame(self, input_frame):
        if self.__mode == 0:
            return input_frame
        elif self.__mode in self.__mode_to_func.keys():
            return self.__mode_to_func.get(self.__mode)(input_frame)


def main():
    video_processing = VideoProcessing(sources.get('video1'))
    video_processing.start_processing()

    video_processing.set_mode(3)
    video_processing.change_input(sources.get('video2'))
    video_processing.start_processing()


if __name__ == '__main__':
    main()
