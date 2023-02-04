
import sqlite3
from tkinter import messagebox
import pandas as pd


def create_db_luna():  # Создание базы данных
    db = sqlite3.connect('C:/Apps/luna.db')
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
    db = sqlite3.connect('C:/Apps/luna.db')
    c = db.cursor()
    c.execute(" DELETE FROM meteo ")
    db.commit()
    db.close()


def check_data(date, time):
    # Creating a connection to the database
    conn = sqlite3.connect('C:/Apps/luna.db')
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
    # Checking if data already exists for the specified time and date
    if check_data(date_utc, time_utc):
        # Displaying a messagebox asking the user if they want to overwrite the data
        result = messagebox.askyesno("Данные уже существуют",
                                     "Информация на выбранную дату и время уже существует в базе данных и будет перезаписана.")
        # If the user chooses to overwrite the data, proceed with the insertion
        if result:
            # Creating a connection to the database
            conn = sqlite3.connect('C:/Apps/luna.db')
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
            messagebox.showinfo("Data Inserted", "Data inserted successfully!")

    else:
        # Creating a connection to the database
        conn = sqlite3.connect('C:/Apps/luna.db')

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
        messagebox.showinfo("Информация внесена в базу данных", "Data inserted successfully!")


def select_from_db(day_history, month_history, year_history):
    date_for_select = f'{day_history}.{month_history}.{year_history}'
    db = sqlite3.connect('C:/Apps/luna.db')
    c = db.cursor()
    query = "SELECT date_utc, time_utc, wind_direction, wind_speed, wind_gust, visibility, weather_condition," \
            "temperature,dew_point, humidity, qt_clouds, qt_lower_clouds, cloud_base, clouds_type, pressure_heli, " \
            "pressure_sea_level, wave FROM meteo WHERE local_date_for_db = ?"
    c.execute(query, (date_for_select,))
    items = c.fetchall()
    db.commit()
    db.close()
    return items


def select_from_db_test():
    db = sqlite3.connect('C:/Apps/luna.db')
    c = db.cursor()

    c.execute("SELECT * FROM meteo")
    items = c.fetchall()

    db.commit()
    db.close()
    return items


def read_csv():
    """Функция считывает данные из файла csv"""

    df = pd.read_excel('C:/Apps/2022.xlsx')

    df['date_utc'] = pd.to_datetime(df['date_utc'], format='%Y-%m-%d').dt.strftime('%d.%m.%Y')
    df['local_date_for_db'] = pd.to_datetime(df['local_date_for_db'], format='%Y-%m-%d').dt.strftime('%d.%m.%Y')
    df['time_utc'] = pd.to_datetime(df['time_utc'], format='%H:%M:%S').dt.strftime('%H:%M')
    df['local_time_for_db'] = pd.to_datetime(df['local_time_for_db'], format='%H:%M:%S').dt.strftime('%H:%M')

    insert_additional_data(df)


def insert_additional_data(data):
    """Функция добавляет данные в базу данных"""
    conn = sqlite3.connect('C:/Apps/luna.db')
    data.to_sql('meteo', conn, if_exists='append', index=False)
    conn.close()

def data_to_excel_period(month_from, year_from):
    import os
    if len(str(month_from)) < 2 or len(str(year_from)) > 4:
        messagebox.showwarning("Проверь дату", "Месяц - 2 цифры. Год - 4 цифры.")
    elif not month_from.isdigit() or not year_from.isdigit():
        messagebox.showwarning("Проверь дату", "Допускается ввод только цифр")
    else:
        start_date = f'{month_from}.{year_from}'
        print(start_date)
        conn = sqlite3.connect('C:/Apps/luna.db')
        df = pd.read_sql_query("SELECT date_utc, time_utc, wind_direction, wind_speed, wind_gust, visibility, weather_condition," \
                "temperature,dew_point, humidity, qt_clouds, qt_lower_clouds, cloud_base, clouds_type, pressure_heli, " \
                "pressure_sea_level, wave FROM meteo WHERE local_date_for_db LIKE '%{}%'".format(start_date), conn)

        # Save DataFrame to Excel file
        file_name = f'LUNA {start_date}'
        df.to_excel(f"C:/Apps/{file_name}.xlsx", index=False)

        conn.close()
        result = messagebox.askquestion(title='Данные',
                                        message=f"В папке C:/Apps/ создан отчёт {file_name}\nОткрыть?")
        if result == 'yes':
            os.startfile(f"C:/Apps/{file_name}.xlsx")


# create_db_luna()
# delete_all_data()
# read_csv()
# print(select_from_db_test())
