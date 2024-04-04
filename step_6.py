# підключення необхідних бібліотек
import cv2
import numpy as np

sources = {'video1': "C:/Users/User/PycharmProjects/oop/video/bunnies.mp4", 'video2':  "web"}


# Фільтр Гауса
def gaussian_filtration(image, kernel_size=3):
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)



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
        frame_changed = gaussian_filtration(frame, kernel_size=11)


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
        frame_changed = gaussian_filtration(frame, kernel_size=11)

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
