# database.py
import sqlite3

def init_db():
    conn = sqlite3.connect('task_manager.db')
    c = conn.cursor()
    
    # Создание таблицы пользователей
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    # Создание таблицы задач
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            priority TEXT NOT NULL,
            date TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    conn.commit()
    conn.close()

def get_connection():
    return sqlite3.connect('task_manager.db')

def load_user_tasks(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM tasks WHERE user_id=?", (user_id,))
    rows = c.fetchall()
    tasks = []
    for row in rows:
        task = {
            "id": row[0],
            "title": row[2],
            "description": row[3],
            "priority": row[4],
            "date": row[5],
            "status": row[6]
        }
        tasks.append(task)
    conn.close()
    return tasks