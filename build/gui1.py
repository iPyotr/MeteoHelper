
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\petrp\PycharmProjects\WeatherAssistant\build\assets\frame1")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("1000x800")
window.configure(bg = "#7AEA78")


canvas = Canvas(
    window,
    bg = "#7AEA78",
    height = 34,
    width = 1000,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_text(
    0.0,
    0.0,
    anchor="nw",
    text="Лунское-А",
    fill="#000000",
    font=("Inter ExtraBold", 16 * -1)
)

canvas.create_rectangle(
    0.0,
    34.0,
    1000.0,
    80.0,
    fill="#000000",
    outline="")
window.resizable(False, False)
window.mainloop()
