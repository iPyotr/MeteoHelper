import sqlite3
from tkinter import messagebox
import pandas as pd
import os
import openpyxl
from openpyxl.styles import Alignment

db_dir_name = f"C:/Apps/MeteoHelperData/"
def create_db_luna():  # Создание базы данных
    global db_dir_name
    db = sqlite3.connect(f'{db_dir_name}luna.db')
    c = db.cursor()

    c.execute("""CREATE TABLE meteo (
                local_date_for_db TEXT, 
                local_time_for_db TEXT,
                date_utc TEXT, 
                time_utc TEXT, 
                wind_direction INTEGER, 
                wind_speed INTEGER, 
                wind_gust INTEGER, 
                visibility INTEGER, 
                weather_condition TEXT, 
                temperature REAL,
                dew_point REAL, 
                humidity INTEGER, 
                qt_clouds INTEGER, 
                qt_lower_clouds INTEGER,
                cloud_base INTEGER, 
                clouds_type TEXT, 
                pressure_heli REAL, 
                pressure_sea_level REAL, 
                wave INTEGER,
                comments TEXT, 
                metar_cod TEXT
               
              )""")
    db.close()


def delete_all_data():  # Удаление всех данных из базы
    global db_dir_name
    db = sqlite3.connect(f'{db_dir_name}luna.db')
    c = db.cursor()
    c.execute(" DELETE FROM meteo ")
    db.commit()
    db.close()


def check_data(date, time):
    # Creating a connection to the database
    global db_dir_name
    conn = sqlite3.connect(f'{db_dir_name}luna.db')
    # Creating a cursor object
    cursor = conn.cursor()

    # Selecting data by time and date
    cursor.execute("SELECT * FROM meteo WHERE time_utc = ? and date_utc = ?", (time, date))

    # Fetching the results
    results = cursor.fetchall()

    # Closing the connection
    conn.close()

    # If data already exists, return True, else return False
    if len(results) > 0:
        return True
    else:
        return False


def insert_data(local_date_for_db, local_time_for_db, date_utc, time_utc, wind_direction, wind_speed, wind_gust,
                visibility, weather_condition, temperature,
                dew_point, humidity, qt_clouds, qt_lower_clouds, cloud_base, clouds_type, pressure_heli,
                pressure_sea_level,
                wave, comments, metar_cod):
    global db_dir_name

    # Checking if data already exists for the specified time and date
    if check_data(date_utc, time_utc):
        # Displaying a messagebox asking the user if they want to overwrite the data
        result = messagebox.askyesno("Данные уже существуют",
                                     "Информация на выбранную дату и время уже существует в базе данных и будет перезаписана.")
        # If the user chooses to overwrite the data, proceed with the insertion
        if result:
            # Creating a connection to the database
            conn = sqlite3.connect(f'{db_dir_name}luna.db')
            # Creating a cursor object
            cursor = conn.cursor()

            # Inserting data into the table
            cursor.execute("""UPDATE meteo SET local_date_for_db = ?, local_time_for_db = ?, wind_direction = ?, wind_speed = ?, wind_gust = ?, visibility = ?, 
                                                weather_condition = ?, temperature = ?, dew_point = ?, humidity = ?, 
                                                qt_clouds = ?, qt_lower_clouds = ?, cloud_base = ?, clouds_type = ?, pressure_heli = ?, 
                                                pressure_sea_level = ?, wave = ?, comments = ?, metar_cod = ? WHERE time_utc = ? and date_utc = ?""",
                           (local_date_for_db, local_time_for_db, wind_direction, wind_speed, wind_gust, visibility,
                            weather_condition,
                            temperature, dew_point, humidity, qt_clouds, qt_lower_clouds, cloud_base, clouds_type,
                            pressure_heli, pressure_sea_level, wave, comments, metar_cod, time_utc, date_utc))
            # Committing the changes
            conn.commit()

            # Closing the connection
            conn.close()

            # Displaying a messagebox to confirm the insertion
            messagebox.showinfo("Сохранение данных", "Данные успешно сохранены!")

    else:
        # Creating a connection to the database
        conn = sqlite3.connect(f'{db_dir_name}luna.db')

        # Creating a cursor object
        cursor = conn.cursor()

        # Inserting data into the table
        cursor.execute("INSERT INTO meteo VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?, ?)",
                       (local_date_for_db, local_time_for_db, date_utc, time_utc, wind_direction, wind_speed, wind_gust,
                        visibility, weather_condition,
                        temperature, dew_point, humidity,
                        qt_clouds, qt_lower_clouds, cloud_base, clouds_type, pressure_heli, pressure_sea_level, wave,
                        comments, metar_cod))

        # Committing the changes
        conn.commit()

        # Closing the connection
        conn.close()

        # Displaying a messagebox to confirm the insertion
        messagebox.showinfo("Информация внесена в базу данных", "Данные успешно сохранены!")


def select_from_db(from_date, to_date):
    global db_dir_name
    from_db = str(from_date)
    to_db = str(to_date)

    db = sqlite3.connect(f'{db_dir_name}luna.db')
    c = db.cursor()
    query = "SELECT date_utc, time_utc, wind_direction, wind_speed, wind_gust, visibility, weather_condition," \
            "temperature,dew_point, humidity, qt_clouds, qt_lower_clouds, cloud_base, clouds_type, pressure_heli, " \
            "pressure_sea_level, wave FROM meteo WHERE local_date_for_db BETWEEN ? AND ?"
    c.execute(query, (from_db, to_db))
    items = c.fetchall()
    db.commit()
    db.close()
    return items


def select_from_db_test():
    global db_dir_name
    db = sqlite3.connect(f'{db_dir_name}luna.db')
    c = db.cursor()

    c.execute("SELECT * FROM meteo")
    items = c.fetchall()

    db.commit()
    db.close()
    return items


def insert_additional_data(data):
    """Функция добавляет данные в базу данных"""
    global db_dir_name
    conn = sqlite3.connect(f'{db_dir_name}luna.db')
    data.to_sql('meteo', conn, if_exists='append', index=False)
    conn.close()


def data_to_excel_month(month_from, year_from):
    global db_dir_name
    if len(str(month_from)) < 2 or len(str(year_from)) > 4:
        messagebox.showwarning("Проверь дату", "Месяц - 2 цифры. Год - 4 цифры.")
    elif not month_from.isdigit() or not year_from.isdigit():
        messagebox.showwarning("Проверь дату", "Допускается ввод только цифр")
    else:
        start_date = f'{year_from}-{month_from}'
        print(start_date)
        conn = sqlite3.connect(f'{db_dir_name}luna.db')
        df = pd.read_sql_query(
            "SELECT date_utc, time_utc, wind_direction, wind_speed, wind_gust, visibility, weather_condition," \
            "temperature,dew_point, humidity, qt_clouds, qt_lower_clouds, cloud_base, clouds_type, pressure_heli, " \
            "pressure_sea_level, wave FROM meteo WHERE local_date_for_db LIKE '%{}%'".format(start_date), conn)
        # df = df.applymap(lambda x: x.replace(",", ".") if isinstance(x, str) else x)
        # Save DataFrame to Excel file
        file_name = f'LUNA {start_date}'
        df.to_excel(f"C:/Apps/{file_name}.xlsx", engine='openpyxl', index=False)

        # Load the Excel file with openpyxl
        book = openpyxl.load_workbook(f"C:/Apps/{file_name}.xlsx")
        sheet = book.active

        # Iterate over cells and set the number format
        for row in sheet.iter_rows():
            for cell in row:
                if isinstance(cell.value, int):
                    cell.number_format = '0'
                elif isinstance(cell.value, float):
                    cell.number_format = '0.0'
        # Set the number format for the specific columns
        for col in ["temperature", "dew_point", "pressure_heli", "pressure_sea_level"]:
            column_index = df.columns.get_loc(col) + 1
            for row in sheet.iter_rows(min_row=2, min_col=column_index, max_col=column_index):
                for cell in row:
                    cell.number_format = '0.0'

        # Save the Excel file
        book.save(f"C:/Apps/{file_name}.xlsx")

        conn.close()
        result = messagebox.askquestion(title='Данные',
                                        message=f"В папке C:/Apps/ создан отчёт {file_name}\nОткрыть?")
        if result == 'yes':
            os.startfile(f"C:/Apps/{file_name}.xlsx")


def data_to_excel_period(from_date, to_date):
    global db_dir_name
    start_date = from_date
    end_date = to_date

    print(start_date)
    conn = sqlite3.connect(f'{db_dir_name}luna.db')

    # Формируем параметризованный запрос
    query = "SELECT date_utc, time_utc, wind_direction, wind_speed, wind_gust, visibility, " \
            "weather_condition, temperature, dew_point, humidity, qt_clouds, qt_lower_clouds, " \
            "cloud_base, clouds_type, pressure_heli, pressure_sea_level, wave " \
            "FROM meteo " \
            "WHERE local_date_for_db " \
            "BETWEEN :start_date AND :end_date"

    # Выполняем запрос с использованием параметров
    df = pd.read_sql_query(query, params={"start_date": start_date, "end_date": end_date}, con=conn)
    print(df)
    dic_col = {'date_utc': 'Дата UTC', 'time_utc': 'Время UTC', 'wind_direction': 'Направление ветра',
               'wind_speed': 'Скорость ветра', 'wind_gust': 'Порыв ветра', 'visibility': 'Горизонтальная видимость',
               'weather_condition': 'Атмосферные явления', 'temperature': 'Температура воздуха',
               'dew_point': 'Точка росы', 'humidity': 'Влажность воздуха', 'qt_clouds': 'Общее воличество облаков',
               'qt_lower_clouds': 'Количество облаков нижнего яруса', 'cloud_base': 'Нижняя граница облачности',
               'clouds_type': 'Тип облачности', 'pressure_heli': 'Давление на уровне вертолётной площадки',
               'pressure_sea_level': 'Давление на уровне моря', 'wave': 'Высота волн'}
    df = df.rename(columns=dic_col)
    print(df)
    # Save DataFrame to Excel file
    dir_name = f"C:/Apps/MeteoHelperData/Excel/"
    file_name = f"LUNA_выгрузка данных за период {start_date} - {end_date}.xlsx"
    df.to_excel(f"{dir_name}{file_name}", engine='openpyxl', index=False)

    # Load the Excel file with openpyxl
    book = openpyxl.load_workbook(f"{dir_name}{file_name}")
    sheet = book.active

    # Iterate over cells and set the number format
    for row in sheet.iter_rows():
        for cell in row:
            if isinstance(cell.value, int):
                cell.number_format = '0'
            elif isinstance(cell.value, float):
                cell.number_format = '0.0'
    # Set the number format for the specific columns
    for col in ["Температура воздуха",
                "Точка росы",
                "Давление на уровне вертолётной площадки",
                "Давление на уровне моря"]:
        column_index = df.columns.get_loc(col) + 1
        for row in sheet.iter_rows(min_row=2, min_col=column_index, max_col=column_index):
            for cell in row:
                cell.number_format = '0.0'

    # Установка высоты первой строки
    sheet.row_dimensions[1].height = 60

    # Включение переноса слов и выравнивание текста
    for row in sheet.iter_rows(min_row=1, max_row=1):
        for cell in row:
            cell.alignment = Alignment(wrapText=True, horizontal='center', vertical='center')

    # Установка ширины столбцов
    for column in sheet.columns:
        column_letter = column[0].column_letter
        sheet.column_dimensions[column_letter].width = 14

    # Save the Excel file
    book.save(f"{dir_name}{file_name}")

    conn.close()
    result = messagebox.askquestion(title='Данные',
                                    message=f"В папке {dir_name} создан отчёт {file_name}\nОткрыть?")
    if result == 'yes':
        os.startfile(f"{dir_name}{file_name}")

# create_db_luna()
# delete_all_data()
# read_csv()
# print(select_from_db_test())
