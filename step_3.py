# підключення необхідних бібліотек
import cv2
import numpy as np

sources = {'video1': "C:/Users/User/PycharmProjects/oop/video/bunnies.mp4", 'video2':  "web"}

# функція дзеркального відображення зображення (стор. 135)
def mirror(image):
    rows, cols = image.shape[:2]
    src_points = np.float32([[0, 0], [cols - 1, 0], [0, rows - 1]])
    dst_points = np.float32([[cols - 1, 0], [0, 0], [cols - 1, rows - 1]])
    affine_matrix = cv2.getAffineTransform(src_points, dst_points)
    img_output = cv2.warpAffine(image, affine_matrix, (cols, rows))
    return img_output

def main():
    cap = cv2.VideoCapture(sources.get('video1'))
    # Перевірка готовності веб-камери
    while cap.isOpened():
        # Запис фреймів
        ret, frame = cap.read()
        # При виникненні помилці запису
        if not ret:
            print("Помилка запису фрейму!")
            break

        # Геометричні перетворення зображення (фрейму)
        frame_mirror = mirror(frame)

        # Відображення результату
        cv2.imshow('frame', frame)
        cv2.imshow('frame_mirrored', frame_mirror)
        if cv2.waitKey(25) == ord('q'):
            break
    # Завершуємо запис у кінці роботи
    cap.release()
    cv2.destroyAllWindows()
    # зчитування відно з веб-камери
    cap = cv2.VideoCapture(0)
    # перевірка готовності веб-камери
    while cap.isOpened():
        # Запис фреймів
        ret, frame = cap.read()
        # при виникненні помилки запису
        if not ret:
            print("Помилка запису файлу")
            break

        # Геометричні перетворення зображення (фрейму)
        frame_mirror = mirror(frame)

        # Відображення результату
        cv2.imshow('frame', frame)
        cv2.imshow('frame_mirrored', frame_mirror)
        if cv2.waitKey(25) == ord('q'):
            break
    # Завершуємо запис у кінці роботи
    cap.release()
    cv2.destroyAllWindows()

# при запуску як головного файлу
if __name__ == '__main__':
    main()
