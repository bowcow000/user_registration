import sqlite3
import hashlib
import tkinter as tk
from tkinter import messagebox

def create_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hash_password(password)))
        conn.commit()
        messagebox.showinfo("Успех", "Пользователь успешно зарегистрирован.")
    except sqlite3.IntegrityError:
        messagebox.showerror("Ошибка", "Пользователь с таким логином уже существует.")
    conn.close()

def login_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, hash_password(password)))
    user = cursor.fetchone()
    conn.close()
    return user

def open_register_window():
    register_window = tk.Toplevel(root)
    register_window.title("Регистрация")

    tk.Label(register_window, text="Логин").pack(padx=10, pady=5)
    entry_register_username = tk.Entry(register_window)
    entry_register_username.pack(padx=10, pady=5)

    tk.Label(register_window, text="Пароль").pack(padx=10, pady=5)
    entry_register_password = tk.Entry(register_window, show="*")
    entry_register_password.pack(padx=10, pady=5)

    def on_register():
        username = entry_register_username.get()
        password = entry_register_password.get()
        if username and password:
            register_user(username, password)
            register_window.destroy()
        else:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены.")

    tk.Button(register_window, text="Зарегистрироваться", command=on_register).pack(pady=10)

root = tk.Tk()
root.title("Авторизация")

tk.Label(root, text="Логин").pack(padx=10, pady=5)
entry_username = tk.Entry(root)
entry_username.pack(padx=10, pady=5)

tk.Label(root, text="Пароль").pack(padx=10, pady=5)
entry_password = tk.Entry(root, show="*")
entry_password.pack(padx=10, pady=5)

def on_login():
    username = entry_username.get()
    password = entry_password.get()
    if username and password:
        user = login_user(username, password)
        if user:
            messagebox.showinfo("Успех", f"Добро пожаловать, {username}!")
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль.")
    else:
        messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля.")

tk.Button(root, text="Авторизоваться", command=on_login).pack(pady=10)
tk.Button(root, text="Зарегистрироваться", command=open_register_window).pack(pady=10)

create_db()

root.mainloop()
