# підключення необхідних бібліотек
import cv2

sources = {'video1': "C:/Users/User/PycharmProjects/oop/video/bunnies.mp4", 'video2': "web"}


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
        # обробка поточного фрейму
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # відображення результату
        cv2.imshow('frame', gray)
        if cv2.waitKey(1) == ord('q'):
            break
    # Завершуємо запис у кінці роботи
    cap.release()
    cv2.destroyAllWindows()

# при запуску як головного файлу
if __name__ == '__main__':
    main()
