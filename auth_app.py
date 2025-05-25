import tkinter as tk
from tkinter import messagebox
import sqlite3
from database import get_connection, init_db
from main_app import run_main_app

class TaskManagerApp:
    def __init__(self, root):
        init_db()  # Инициализация БД
        self.root = root
        self.root.title("Вход")
        self.root.geometry('300x150')

        self.login_name = tk.Label(root, text="Логин: ")
        self.login_name.grid(row=0, column=0, padx=10, pady=5)
        self.login_name_input = tk.Entry(root, width=30)
        self.login_name_input.grid(row=0, column=1, padx=10, pady=5)

        self.password_name = tk.Label(root, text=f"Пароль: ")
        self.password_name.grid(row=1, column=0, padx=10, pady=5)
        self.password_name_input = tk.Entry(root, width=30, show='*')
        self.password_name_input.grid(row=1, column=1, padx=10, pady=5)

        self.entrance_button = tk.Button(root, text="Вход", command=self.Entrance)
        self.entrance_button.grid(row=2, column=1, padx=10, pady=5)

        self.registration_button = tk.Button(root, text="Регистрация", command=self.Registration_window)
        self.registration_button.grid(row=3, column=1, padx=10, pady=5)
    
        self.registration_window = None

        self.users = {'qwerty' : '12345'}

    def Entrance(self):
        login = self.login_name_input.get()
        password = self.password_name_input.get()
        if not login or not password:
            messagebox.showerror(title='Ошибка', message='Заполните все поля!')
            return
            
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE login=? AND password=?", (login, password))
        user = c.fetchone()
        conn.close()
        
        if user:
            self.root.destroy()
            run_main_app(user[0])  # Передаем ID пользователя
        else:
            messagebox.showerror(title='Ошибка', message='Неверный логин или пароль!')

    def Registration_window(self):
        if self.registration_window is None or not self.registration_window.winfo_exists():
            self.registration_window = tk.Toplevel(self.root)
            self.registration_window.title('Регистрация')
            self.registration_window.geometry('400x150')

            self.registration_window_login = tk.Label(self.registration_window, text="Логин:")
            self.registration_window_login.grid(row=0, column=0, padx=10, pady=5)
            self.registration_window_login_input = tk.Entry(self.registration_window, width=30)
            self.registration_window_login_input.grid(row=0, column=1, padx=10, pady=5)

            self.registration_window_password1 = tk.Label(self.registration_window, text="Пароль:")
            self.registration_window_password1.grid(row=1, column=0, padx=10, pady=5)
            self.registration_window_password1_input = tk.Entry(self.registration_window, width=30, show='*')
            self.registration_window_password1_input.grid(row=1, column=1, padx=10, pady=5)

            self.registration_window_password2 = tk.Label(self.registration_window, text="Подтверждение пароля:")
            self.registration_window_password2.grid(row=2, column=0, padx=10, pady=5)
            self.registration_window_password2_input = tk.Entry(self.registration_window, width=30, show='*')
            self.registration_window_password2_input.grid(row=2, column=1, padx=10, pady=5)

            self.registration_window_reg_button = tk.Button(self.registration_window, text="Зарегистрироваться", command=self.registration)
            self.registration_window_reg_button.grid(row=3, column=1, padx=10, pady=5)
        else:
            messagebox.showinfo(title='Предупреждение', message='Окно регистрации уже открыто')
   
    def registration(self):
        login = self.registration_window_login_input.get()
        password = self.registration_window_password1_input.get()
        confirm_password = self.registration_window_password2_input.get()

        if not login or not password or not confirm_password:
            messagebox.showerror(title='Ошибка', message='Заполните все поля')
        elif self.registration_window_password1_input.get() != confirm_password:
            messagebox.showerror(title='Ошибка', message='Пароли должны совпадать')
        elif login in self.users:
            messagebox.showwarning(title='Ошибка', message='Аккаунт с таким логином уже существует!')
        else:
            conn = get_connection()
            c = conn.cursor()
            try:
                c.execute("INSERT INTO users (login, password) VALUES (?, ?)", (login, password))
                conn.commit()
                messagebox.showinfo(title='Успех', message='Регистрация прошла успешно!')
            except sqlite3.IntegrityError:
                messagebox.showwarning(title='Ошибка', message='Аккаунт с таким логином уже существует!')
            finally:
                conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()