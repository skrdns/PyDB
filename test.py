import tkinter as tk
from tkinter import messagebox, scrolledtext
from pymongo import MongoClient

# --- Параметри підключення до MongoDB ---
uri = "mongodb+srv://sikora:20050411@db1.gyaftca.mongodb.net/?retryWrites=true&w=majority&appName=DB1"
client = MongoClient(uri)
db = client.mydatabase  # Замініть на назву вашої бази даних
collection = db.mycollection  # Замініть на назву вашої колекції

def insert_data():
    """Отримує дані з полів введення та вставляє їх у MongoDB."""
    name = entry_name.get()
    age_str = entry_age.get()
    if name and age_str.isdigit():
        age = int(age_str)
        data = {"name": name, "age": age}
        try:
            result = collection.insert_one(data)
            messagebox.showinfo("Успіх", f"Документ успішно вставлено з ID: {result.inserted_id}")
            entry_name.delete(0, tk.END)
            entry_age.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Помилка", f"Помилка вставки: {e}")
    else:
        messagebox.showerror("Помилка", "Будь ласка, введіть ім'я та коректний вік.")

def view_data():
    """Отримує всі дані з MongoDB та відображає їх у текстовому полі."""
    text_area.delete(1.0, tk.END)
    try:
        documents = collection.find()
        for doc in documents:
            text_area.insert(tk.END, f"Ім'я: {doc['name']}, Вік: {doc['age']}\n")
    except Exception as e:
        messagebox.showerror("Помилка", f"Помилка отримання даних: {e}")

def clear_fields():
    """Очищає поля вводу."""
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)

# --- Створення головного вікна ---
window = tk.Tk()
window.title("Інтерфейс MongoDB")

# --- Елементи керування для вставки даних ---
label_name = tk.Label(window, text="Ім'я:")
label_name.grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_name = tk.Entry(window)
entry_name.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

label_age = tk.Label(window, text="Вік:")
label_age.grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_age = tk.Entry(window)
entry_age.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

button_insert = tk.Button(window, text="Вставити дані", command=insert_data)
button_insert.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

# --- Елемент керування для перегляду даних ---
label_view = tk.Label(window, text="Дані з MongoDB:")
label_view.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="w")
text_area = scrolledtext.ScrolledText(window, width=40, height=10)
text_area.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

button_view = tk.Button(window, text="Оновити дані", command=view_data)
button_view.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

# --- Кнопка для очищення полів ---
button_clear = tk.Button(window, text="Очистити поля", command=clear_fields)
button_clear.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

# --- Налаштування сітки для розтягування елементів ---
window.grid_columnconfigure(1, weight=1)
window.grid_rowconfigure(4, weight=1)

# --- Запуск головного циклу Tkinter ---
window.mainloop()

# --- Закриття підключення до MongoDB після завершення роботи ---
client.close()
