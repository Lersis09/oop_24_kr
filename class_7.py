import cv2
import numpy as np

sources = {'video1': "data/Video/Hourglass.mp4", 'video2': "data/Video/Hourglass.mp4", "web": 0}


# клас обробки відео-даних
class VideoProcessing:

    # конструктор
    def __init__(self, filename):
        self.__filename = filename
        self.__mode = 0
        self.__mode_to_func = {1: VideoProcessing.colorspace_change, 2: VideoProcessing.rotate_image,
                               3: VideoProcessing.binarization, 4: VideoProcessing.sharpening_filtration}
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
    def rotate_image(input_frame, angle=45):
        num_rows, num_cols = input_frame.shape[:2]
        rotation_matrix = cv2.getRotationMatrix2D((num_cols / 2, num_rows / 2), angle, 1)
        img_rotation = cv2.warpAffine(input_frame, rotation_matrix, (num_cols, num_rows))
        return img_rotation

    @staticmethod
    def binarization(input_frame, threshold=127):
        gray_frame = cv2.cvtColor(input_frame, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray_frame, threshold, 255, cv2.THRESH_BINARY)
        return thresh

    @staticmethod
    def sharpening_filtration(input_frame, kernel_size=3):
        kernel = np.ones((kernel_size, kernel_size), np.float32)
        center_index = int((kernel_size - 1) * 0.5)
        kernel[center_index][center_index] = (kernel_size * kernel_size - 2) * -1
        return cv2.filter2D(input_frame, -1, kernel)

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
