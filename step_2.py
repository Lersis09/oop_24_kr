# підключення необхідних бібліотек
import cv2

sources = {'video1': "data/Video/bunnies.mp4", 'video2': "data/Video/bunnies.mp4", "web": 0}


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


# при запуску як головного файлу
if __name__ == '__main__':
    main()
