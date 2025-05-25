import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from database import get_connection, load_user_tasks
from AI_description import get_description

class TaskManagerApp:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        self.root.title("Task Manager")

        # Загрузка задач из базы данных
        self.tasks = load_user_tasks(user_id)

        # Создание интерфейса
        self.create_widgets()

        # Обновление списка задач
        self.update_task_listbox()

    def create_widgets(self):
        # Кнопка для открытия окна создания задачи
        self.add_button = tk.Button(self.root, text="Создать задачу", command=self.open_create_task_window)
        self.add_button.grid(row=0, column=0, columnspan=2, pady=10)

        # Прокручиваемый список задач
        self.task_listbox = tk.Listbox(self.root, width=70, height=10)
        self.task_listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        # Управление статусом задач
        self.complete_button = tk.Button(self.root, text="Отметить как выполнено", command=self.mark_completed)
        self.complete_button.grid(row=2, column=0, columnspan=2, pady=5)

        # Фильтрация задач
        self.filter_label = tk.Label(self.root, text="Фильтр:")
        self.filter_label.grid(row=3, column=0, padx=10, pady=5)
        self.filter_var = tk.StringVar(value="Все")
        self.filter_menu = ttk.Combobox(self.root, textvariable=self.filter_var, values=["Все", "Текущие", "Выполненные"])
        self.filter_menu.grid(row=3, column=1, padx=10, pady=5)
        self.filter_menu.bind("<<ComboboxSelected>>", self.apply_filter)

        # Редактирование задач
        self.edit_button = tk.Button(self.root, text="Редактировать задачу", command=self.edit_task)
        self.edit_button.grid(row=4, column=0, columnspan=2, pady=5)

        # Удаление задач
        self.delete_button = tk.Button(self.root, text="Удалить задачу", command=self.delete_task)
        self.delete_button.grid(row=5, column=0, columnspan=2, pady=5)

    def open_create_task_window(self):
        # Создание нового окна для добавления задачи
        create_window = tk.Toplevel(self.root)
        create_window.title("Создать задачу")

        # Заголовок задачи
        tk.Label(create_window, text="Заголовок задачи:").grid(row=0, column=0, padx=10, pady=5)
        task_entry = tk.Entry(create_window, width=50)
        task_entry.grid(row=0, column=1, padx=10, pady=5)

        # Поле для отображения возможного описания (только для чтения)
        tk.Label(create_window, text="Возможное описание:").grid(row=1, column=0, padx=10, pady=5)
        possible_description_var = tk.StringVar()
        possible_description_label = tk.Label(create_window, textvariable=possible_description_var, width=50, anchor="w", relief="groove")
        possible_description_label.grid(row=1, column=1, padx=10, pady=5)

        def confirm_title():
            title = task_entry.get()
            if title:
                print(f"Подтвержденный заголовок: {title}")  # Вывод заголовка в консоль
                task_entry.config(state=tk.DISABLED)  # Блокировка поля заголовка
                confirm_button.config(state=tk.DISABLED)  # Блокировка кнопки подтверждения

                # Разблокировка поля описания
                desc_entry.config(state=tk.NORMAL)

                # Добавляем пример описания (будущая функциональность)
                possible_description = get_description(title)
                possible_description_var.set(possible_description)

                # Разблокировка кнопки "Использовать предложенное описание"
                enable_use_description_button()
            else:
                messagebox.showwarning("Ошибка", "Заполните заголовок!")




        confirm_button = tk.Button(create_window, text="Подтвердить заголовок", command=confirm_title)
        confirm_button.grid(row=0, column=2, padx=10, pady=5)

        # Описание задачи (изначально заблокировано)
        tk.Label(create_window, text="Описание задачи:").grid(row=2, column=0, padx=10, pady=5)
        desc_entry = tk.Entry(create_window, width=50, state=tk.DISABLED)
        desc_entry.grid(row=2, column=1, padx=10, pady=5)

        # Кнопка "Использовать предложенное описание"
        def use_description():
            selected_description = possible_description_var.get()
            if selected_description:
                desc_entry.delete(0, tk.END)
                desc_entry.insert(0, selected_description)
            else:
                messagebox.showwarning("Ошибка", "Нет доступных описаний!")

        use_description_button = tk.Button(create_window, text="Использовать предложенное описание", command=use_description, state=tk.DISABLED)
        use_description_button.grid(row=1, column=2, padx=10, pady=5)

        # Логика разблокировки кнопки "Использовать предложенное описание"
        def enable_use_description_button():
            use_description_button.config(state=tk.NORMAL)

        # Дата выполнения
        tk.Label(create_window, text="Дата выполнения:").grid(row=3, column=0, padx=10, pady=5)
        date_entry = DateEntry(create_window, width=12, background='darkblue', foreground='white', borderwidth=2)
        date_entry.grid(row=3, column=1, padx=10, pady=5)

        # Приоритет
        tk.Label(create_window, text="Приоритет:").grid(row=4, column=0, padx=10, pady=5)
        priority_var = tk.StringVar(value="Средний")
        priority_menu = ttk.Combobox(create_window, textvariable=priority_var, values=["Высокий", "Средний", "Низкий"])
        priority_menu.grid(row=4, column=1, padx=10, pady=5)

        # Кнопка добавления задачи
        def add_task_from_window():
            title = task_entry.get()
            description = desc_entry.get()
            priority = priority_var.get()
            date = date_entry.get_date()
            if title and description:
                task = {
                    "title": title,
                    "description": description,
                    "priority": priority,
                    "date": date,
                    "status": "Текущая"
                }
                self.tasks.append(task)
                self.save_tasks()
                self.update_task_listbox()
                create_window.destroy()
            else:
                messagebox.showwarning("Ошибка", "Заполните все поля!")

        tk.Button(create_window, text="Добавить задачу", command=add_task_from_window).grid(row=5, column=0, columnspan=2, pady=10)

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            status = "[Выполнено] " if task["status"] == "Выполнена" else ""
            task_text = f"{status}{task['title']} - {task['description']} (Приоритет: {task['priority']}, Дата: {task['date']})"
            self.task_listbox.insert(tk.END, task_text)

    def mark_completed(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            self.tasks[selected_index]["status"] = "Выполнена"
            self.save_tasks()
            self.update_task_listbox()
        except IndexError:
            messagebox.showwarning("Ошибка", "Выберите задачу!")

    def apply_filter(self, event):
        filter_type = self.filter_var.get()
        filtered_tasks = []
        for task in self.tasks:
            if filter_type == "Все":
                filtered_tasks.append(task)
            elif filter_type == "Текущие" and task["status"] == "Текущая":
                filtered_tasks.append(task)
            elif filter_type == "Выполненные" and task["status"] == "Выполнена":
                filtered_tasks.append(task)
        self.task_listbox.delete(0, tk.END)
        for task in filtered_tasks:
            status = "[Выполнено] " if task["status"] == "Выполнена" else ""
            task_text = f"{status}{task['title']} - {task['description']} (Приоритет: {task['priority']}, Дата: {task['date']})"
            self.task_listbox.insert(tk.END, task_text)

    def edit_task(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            task = self.tasks[selected_index]
            # Открытие окна для редактирования
            edit_window = tk.Toplevel(self.root)
            edit_window.title("Редактирование задачи")

            tk.Label(edit_window, text="Заголовок:").grid(row=0, column=0, padx=10, pady=5)
            title_entry = tk.Entry(edit_window, width=50)
            title_entry.grid(row=0, column=1, padx=10, pady=5)
            title_entry.insert(0, task["title"])

            tk.Label(edit_window, text="Описание:").grid(row=1, column=0, padx=10, pady=5)
            desc_entry = tk.Entry(edit_window, width=50)
            desc_entry.grid(row=1, column=1, padx=10, pady=5)
            desc_entry.insert(0, task["description"])

            tk.Label(edit_window, text="Приоритет:").grid(row=2, column=0, padx=10, pady=5)
            priority_var = tk.StringVar(value=task["priority"])
            priority_menu = ttk.Combobox(edit_window, textvariable=priority_var, values=["Высокий", "Средний", "Низкий"])
            priority_menu.grid(row=2, column=1, padx=10, pady=5)

            tk.Label(edit_window, text="Дата выполнения:").grid(row=3, column=0, padx=10, pady=5)
            date_entry = DateEntry(edit_window, width=12, background='darkblue', foreground='white', borderwidth=2)
            date_entry.grid(row=3, column=1, padx=10, pady=5)
            date_entry.set_date(task["date"])

            def save_changes():
                task["title"] = title_entry.get()
                task["description"] = desc_entry.get()
                task["priority"] = priority_var.get()
                task["date"] = date_entry.get_date()
                self.save_tasks()
                self.update_task_listbox()
                edit_window.destroy()

            tk.Button(edit_window, text="Сохранить изменения", command=save_changes).grid(row=4, column=0, columnspan=2, pady=10)
        except IndexError:
            messagebox.showwarning("Ошибка", "Выберите задачу!")

    def delete_task(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            del self.tasks[selected_index]
            self.save_tasks()
            self.update_task_listbox()
        except IndexError:
            messagebox.showwarning("Ошибка", "Выберите задачу!")

    def save_tasks(self):
        conn = get_connection()
        c = conn.cursor()
        c.execute("DELETE FROM tasks WHERE user_id=?", (self.user_id,))
        for task in self.tasks:
            c.execute("""
                INSERT INTO tasks (user_id, title, description, priority, date, status)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                self.user_id,
                task['title'],
                task['description'],
                task['priority'],
                task['date'],
                task['status']
            ))
        conn.commit()
        conn.close()

def run_main_app(user_id):
    root = tk.Tk()
    app = TaskManagerApp(root, user_id)
    root.mainloop()