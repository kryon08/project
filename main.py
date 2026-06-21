import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

DATA_FILE = 'data.json'

class TrainingPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")
        self.root.geometry("600x500")

        self.data = self.load_data()

        frame_input = tk.Frame(root)
        frame_input.pack(pady=10)

        tk.Label(frame_input, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, padx=5, pady=5)
        self.entry_date = tk.Entry(frame_input)
        self.entry_date.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_input, text="Тип тренировки:").grid(row=1, column=0, padx=5, pady=5)
        self.combo_type = ttk.Combobox(frame_input, values=["Бег", "Силовая", "Йога", "Плавание", "Кардио"])
        self.combo_type.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_input, text="Длительность (мин):").grid(row=2, column=0, padx=5, pady=5)
        self.entry_duration = tk.Entry(frame_input)
        self.entry_duration.grid(row=2, column=1, padx=5, pady=5)

        tk.Button(frame_input, text="Добавить тренировку", command=self.add_record,
                  bg="#4CAF50", fg="white", activebackground="#45a049",
                  font=("Arial", 10, "bold"), relief=tk.RAISED).grid(row=3, columnspan=2, pady=10)

        frame_filter = tk.Frame(root)
        frame_filter.pack(pady=5)

        tk.Label(frame_filter, text="Фильтр по типу:").grid(row=0, column=0, padx=5)
        self.filter_type = ttk.Combobox(frame_filter, values=["Все", "Бег", "Силовая", "Йога", "Плавание", "Кардио"])
        self.filter_type.current(0)
        self.filter_type.grid(row=0, column=1, padx=5)

        tk.Label(frame_filter, text="Фильтр по дате:").grid(row=0, column=2, padx=5)
        self.filter_date = tk.Entry(frame_filter, width=12)
        self.filter_date.grid(row=0, column=3, padx=5)

        tk.Button(frame_filter, text="Применить", command=self.apply_filter,
                  bg="#2196F3", fg="white", activebackground="#0b7dda", relief=tk.RAISED).grid(row=0, column=4, padx=5)

        tk.Button(frame_filter, text="Сбросить", command=self.reset_filter,
                  bg="#f44336", fg="white", activebackground="#da190b", relief=tk.RAISED).grid(row=0, column=5, padx=5)

        # --- Таблица ---
        columns = ("date", "type", "duration")
        self.tree = ttk.Treeview(root, columns=columns, show="headings")
        self.tree.heading("date", text="Дата")
        self.tree.heading("type", text="Тип тренировки")
        self.tree.heading("duration", text="Длительность (мин)")
        self.tree.pack(expand=True, fill='both', padx=10, pady=10)

        self.update_table(self.data)

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    def save_data(self):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def validate_date(self, date_text):
        try:
            datetime.strptime(date_text, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def add_record(self):
        date_val = self.entry_date.get()
        type_val = self.combo_type.get()
        duration_val = self.entry_duration.get()

        if not self.validate_date(date_val):
            messagebox.showerror("Ошибка", "Неверный формат даты. Используйте ГГГГ-ММ-ДД.")
            return

        if not type_val:
            messagebox.showerror("Ошибка", "Выберите тип тренировки.")
            return

        try:
            dur = float(duration_val)
            if dur <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Длительность должна быть положительным числом.")
            return

        record = {"date": date_val, "type": type_val, "duration": dur}
        self.data.append(record)
        self.save_data()
        self.update_table(self.data)

        self.entry_date.delete(0, tk.END)
        self.combo_type.set('')
        self.entry_duration.delete(0, tk.END)
        messagebox.showinfo("Успех", "Тренировка успешно добавлена!")

    def apply_filter(self):
        f_type = self.filter_type.get()
        f_date = self.filter_date.get()

        filtered = self.data
        if f_type != "Все" and f_type != "":
            filtered = [r for r in filtered if r["type"] == f_type]

        if f_date.strip() != "":
            filtered = [r for r in filtered if r["date"] == f_date.strip()]

        self.update_table(filtered)

    def reset_filter(self):
        self.filter_type.current(0)
        self.filter_date.delete(0, tk.END)
        self.update_table(self.data)

    def update_table(self, data_to_show):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for row in data_to_show:
            self.tree.insert("", tk.END, values=(row["date"], row["type"], row["duration"]))

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlannerApp(root)
    root.mainloop()