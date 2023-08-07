from cx_Freeze import setup, Executable
from main import App

## запуск скрипта
#### python setup.py build

cls = App()
version_n = cls.vers_n.get()

base = "Win32GUI"

# Настройки исполняемого файла
executable_name = 'MeteoHelper.exe'
executables = [
    Executable("main.py", base=base,
               target_name=executable_name,
               icon='img/icon.ico',
               copyright='©Petr Pisanko, 2023')]

output_directory = 'build/MeteoHelper/'  # Папка вывода
root_folder = 'img/'  # Папка для размещения в корне
root_file = 'default.ini'  # Файл для размещения в корне

build_exe_options = {
    'build_exe': output_directory,  # Папка вывода
    'include_files': [
        (root_folder, root_folder),  # Папка для размещения в корне
        (root_file, root_file)  # Файл для размещения в корне
    ]
}

setup(
    name="Meteo Helper",
    version=version_n,
    description="Лёгкое кодирование погоды в METAR",
    options={'build_exe': build_exe_options},
    executables=executables
)
