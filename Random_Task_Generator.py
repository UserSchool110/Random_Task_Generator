import random
import json
import os
from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime

# Константы
history_file = "task_history.json"
tasks_file = "tasks.json"

# Предопределённые задачи
default_tasks = [
    {"text": "Прочитать статью", "category": "Учёба"},
    {"text": "сделать зарядку", "category": "Спорт"},
    {"text": "Написать отчёт", "category": "Работа"}
]

# Переменные
tasks = []
history = []
filter_var = None
history_listbox = None
current_task_label = None
new_task_entry = None
root = None


# Функции работы с файлами
def load_tasks():
    global tasks
    if os.path.exists(tasks_file):
        try:
            with open(tasks_file, 'r', encoding='utf-8') as f:
                tasks = json.load(f)
                return
        except:
            pass
    tasks = default_tasks.copy()
    save_tasks()


def save_tasks():
    with open(tasks_file, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


def load_history():
    global history
    if os.path.exists(history_file):
        try:
            with open(history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
                return
        except:
            pass
    history = []
    save_history()


def save_history():
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def generate_task():
    global current_task

    if not tasks:
        messagebox.showwarning("ошибка", "сначала добавьте задачу!")
        return

    task = random.choice(tasks)
    current_task = task.copy()
    current_task["timestamp"] = get_timestamp()

    history.append(current_task)
    save_history()

    current_task_label.config(text=f"{task['text']} ({task['category']})")
    update_history_display()


def update_history_display():
    history_listbox.delete(0, END)

    current_filter = filter_var.get()

    filtered_history = history
    if current_filter != "все":
        filtered_history = [item for item in history
                            if item.get("category") == current_filter]

    for item in reversed(filtered_history):
        display_text = f"{item['text']} [{item['category']}]"
        history_listbox.insert(END, display_text)

    if not filtered_history:
        history_listbox.insert(0, "история пуста")


def apply_filter():
    update_history_display()


def add_new_task():
    task_text = new_task_entry.get().strip()

    if not task_text:
        messagebox.showwarning("ошибка", "введите задачу!")
        return

    tasks.append({"text": task_text, "category": filter_var.get()})
    save_tasks()
    new_task_entry.delete(0, END)
    messagebox.showinfo("успех", f"задача '{task_text}' добавлена!")


def clear_history():
    if messagebox.askyesno("подтверждение", "очистить всю историю?"):
        global history
        history = []
        save_history()
        update_history_display()
        current_task_label.config(text="история очищена")


def on_closing():
    save_history()
    save_tasks()
    root.destroy()


# Интерфейс
def create_ui():
    global filter_var, history_listbox, current_task_label, new_task_entry, root

    root = Tk()
    root.title("генератор задач")
    root.geometry("500x500")

    Button(root, text="сгенерировать задачу", command=generate_task,
           font=("arial", 14, "bold"), pady=10).pack(pady=10)

    # Текущая задача
    current_task_label = Label(root, text="нажмите кнопку", font=("arial", 12))
    current_task_label.pack(pady=5)

    Frame(root, height=2, relief=SUNKEN).pack(fill=X, pady=10)

    # Фильтрация
    filter_frame = Frame(root)
    filter_frame.pack(pady=5)
    Label(filter_frame, text="фильтр:").pack(side=LEFT)
    filter_var = StringVar(value="все")
    for cat in ["все", "учёба", "спорт", "работа"]:
        Radiobutton(filter_frame, text=cat, variable=filter_var,
                    value=cat, command=apply_filter).pack(side=LEFT, padx=5)

    #Добавление задачи
    add_frame = Frame(root)
    add_frame.pack(pady=10, fill=X, padx=20)
    new_task_entry = Entry(add_frame, width=30)
    new_task_entry.pack(side=LEFT, padx=5)
    Button(add_frame, text="добавить", command=add_new_task).pack(side=LEFT)

    #История
    Label(root, text="история:", font=("arial", 10, "bold")).pack(anchor=W, padx=20)

    history_frame = Frame(root)
    history_frame.pack(fill=BOTH, expand=True, padx=20, pady=5)

    scrollbar = Scrollbar(history_frame)
    scrollbar.pack(side=RIGHT, fill=Y)

    history_listbox = Listbox(history_frame, yscrollcommand=scrollbar.set, font=("arial", 9))
    history_listbox.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.config(command=history_listbox.yview)

    #Удаление
    Button(root, text="очистить историю", command=clear_history).pack(pady=10)

    return root


# Запуск прилдожения
load_tasks()
load_history()
root = create_ui()
update_history_display()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()