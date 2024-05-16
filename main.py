import tkinter
from task import TaskWindow

# словник для швидкого доступу до відповідної функції виконання
task_window_dict = {
    "1": (TaskWindow, "Методи обробки відеозображень в системах управління з ТЗ", "600x300")
}


# Основна функція
def main():
    choice = input("Please, choose the task 1 (0-EXIT): ")
    while choice != "0":
        # якщо даний ключ є у словнику
        if choice in task_window_dict.keys():
            # Створення відповідного вікна
            application = tkinter.Tk()
            window_class, window_name, window_size = task_window_dict.get(choice)
            window = window_class(application)
            application.geometry(window_size)
            application.title(window_name)
            application.mainloop()
        else:
            print("Wrong task number!")
        choice = input("Please, choose the task again (0-EXIT): ")


if __name__ == '__main__':
    main()
