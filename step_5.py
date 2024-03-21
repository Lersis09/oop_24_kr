# підключення необхідних бібліотек
import cv2
import numpy as np

sources = {'video1': "C:/Users/User/PycharmProjects/oop/video/bunnies.mp4", 'video2':  "web"}




# функція детектування кутів Ши-Томасі  (стор. 140)
def corner_detector(image, max_corners=5, quality_level=0.01, min_dist=20):
    new_image = image.copy()
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    corners = cv2.goodFeaturesToTrack(gray_image, max_corners, quality_level, min_dist)
    corners = np.float32(corners)
    for item in corners:
        x, y = item[0]
        cv2.circle(new_image, (int(x), int(y)), 5, 255, -1)
    return new_image


def main():
    # метод зчитування даних з відеофайлу (стор. 142 - 145)
    cap = cv2.VideoCapture(sources.get('video1'))
    # Перевірка готовності веб-камери
    while cap.isOpened():
        # Запис фреймів
        ret, frame = cap.read()
        # При виникненні помилці запису
        if not ret:
            print("Помилка запису фрейму!")
            break
        # Відображення результату
        cv2.imshow('frame', frame)
        if cv2.waitKey(25) == ord('q'):
            break

        # Виконання операції за варіантом
        frame_changed = corner_detector(frame, max_corners=20, quality_level=0.01, min_dist=50)

        # Відображення результату
        cv2.imshow('frame', frame)
        cv2.imshow('frame_changed', frame_changed)
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

        # Виконання операції за варіантом
        frame_changed = corner_detector(frame, max_corners=20, quality_level=0.01, min_dist=50)

        # Відображення результату
        cv2.imshow('frame', frame)
        cv2.imshow('frame_changed', frame_changed)
        if cv2.waitKey(25) == ord('q'):
            break
    # Завершуємо запис у кінці роботи
    cap.release()
    cv2.destroyAllWindows()

# при запуску як головного файлу
if __name__ == '__main__':
    main()
