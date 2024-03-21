# підключення необхідних бібліотек
import cv2

sources = {'video1': "C:/Users/User/PycharmProjects/oop/video/bunnies.mp4", 'video2':  "web"}
colorspaces = {'YUV': cv2.COLOR_BGR2YUV}


def colorspace_change(input_frame, colorspace_index):
    return cv2.cvtColor(input_frame, colorspaces.get(colorspace_index))


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

        # Зміна колірного простору зображення (фрейму)
        frame_YUV = colorspace_change(frame, 'YUV')

        # Відображення результату
        cv2.imshow('frame', frame)
        cv2.imshow('frame YUV', frame_YUV)
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

        # Зміна колірного простору зображення (фрейму)
        frame_YUV = colorspace_change(frame, 'YUV')

        # Відображення результату
        cv2.imshow('frame', frame)
        cv2.imshow('frame YUV', frame_YUV)
        if cv2.waitKey(25) == ord('q'):
            break
    # Завершуємо запис у кінці роботи
    cap.release()
    cv2.destroyAllWindows()

# при запуску як головного файлу
if __name__ == '__main__':
    main()
