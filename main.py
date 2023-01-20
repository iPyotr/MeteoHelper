import tkinter as tk
import datetime
from tkinter import ttk

root = tk.Tk()
root.geometry("1000x800+{}+{}".format(root.winfo_screenwidth()//2-500, root.winfo_screenheight()//2-400))
root.title("My window")

# надпись "Лунское-А"
title_label = tk.Label(root, text="Лунское-А", font=("Arial", 22), anchor="center")
title_label.pack(pady=20)

# фрейм для даты и времени
time_frame = tk.Frame(root)
time_frame.pack(pady=10)

# текущая дата
date_label = tk.Label(time_frame, text="", font=("Arial", 14), anchor="w")
date_label.pack(side="left", anchor="w", padx=10)

# текущее время
time_label = tk.Label(time_frame, text="", font=("Arial", 14), anchor="e")
time_label.pack(side="right", anchor="e", padx=10)

def update_time():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    current_date = datetime.datetime.now().strftime("%d/%m/%Y")
    time_label.config(text=current_time)
    date_label.config(text=current_date)
    root.after(1000, update_time)

# линия разделения
separator = ttk.Separator(root)
separator.pack(fill="x", padx=5, pady=5)

# вкладки
notebook = ttk.Notebook(root)
summary_tab = ttk.Frame(notebook)
weather_tab = ttk.Frame(notebook)
notebook.add(summary_tab, text="Сводки")
notebook.add(weather_tab, text="Текущая погода")
notebook.pack(expand=1, fill="both")

# таблица на вкладке "Сводки"
table = ttk.Treeview(summary_tab, columns=("col1", "col2", "col3", "col4", "col5", "col6", "col7", "col8", "col9", "col10"))
table.heading("#0", text="Столбец 1")
table.heading("col1", text="Столбец 2")
table.heading("col2", text="Столбец 3")
table.heading("col3", text="Столбец 4")
table.heading("col4", text="Столбец 5")
table.heading("col5", text="Столбец 6")
table.heading("col6", text="Столбец 7")
table.heading("col7", text="Столбец 8")
table.heading("col8", text="Столбец 9")
table.heading("col9", text="Столбец 10")
table.column("#0", width=100)
table.column("col1", width=100)
table.column("col2", width=100)
table.column("col3", width=100)
table.column("col4", width=100)
table.column("col5", width=100)
table.column("col6", width=100)
table.column("col7", width=100)
table.column("col8", width=100)
table.column("col9", width=100)
table.pack(expand=1, fill="both")

update_time()
root.mainloop()
