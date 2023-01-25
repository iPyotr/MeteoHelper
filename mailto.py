import tkinter as tk

def create_new_window():
    new_window = tk.Toplevel(root)
    new_window.title("New Window")
    tk.Label(new_window, text="This is a new window").pack()
    tk.Button(new_window, text="Close", command=new_window.destroy).pack()

root = tk.Tk()
root.title("Main Window")
tk.Button(root, text="Open new window", command=create_new_window).pack()
root.mainloop()