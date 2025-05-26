from auth_app import TaskManagerApp
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()