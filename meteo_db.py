from config import host_cnf, user_cnf, password_cnf, db_name_cnf
import sqlite3
import tkinter as tk
from tkinter import messagebox
import datetime
import time
from dateutil.parser import parse

def create_db_luna(): # Создание базы данных
    db = sqlite3.connect('C:/Apps/luna.db')
    c = db.cursor()
    
    c.execute("""CREATE TABLE meteo (
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


def delete_all_data(): # Удаление всех данных из базы
    db = sqlite3.connect('C:/Apps/luna.db')
    c = db.cursor()
    c.execute(" DELETE FROM meteo# ")
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


def insert_data(date_utc, time_utc, wind_direction, wind_speed, wind_gust, visibility, weather_condition, temperature, 
                dew_point, humidity, qt_clouds, qt_lower_clouds, cloud_base, clouds_type, pressure_heli, pressure_sea_level, 
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
            cursor.execute("""UPDATE meteo SET wind_direction = ?, wind_speed = ?, wind_gust = ?, visibility = ?, 
                                                weather_condition = ?, temperature = ?, dew_point = ?, humidity = ?, 
                                                qt_clouds = ?, qt_lower_clouds = ?, cloud_base = ?, clouds_type = ?, pressure_heli = ?, 
                                                pressure_sea_level = ?, wave = ?, comments = ?, metar_cod = ? WHERE time_utc = ? and date_utc = ?""",
                           (wind_direction, wind_speed, wind_gust, visibility, weather_condition,
                            temperature, dew_point, humidity, qt_clouds, qt_lower_clouds, cloud_base, clouds_type, pressure_heli,
                            pressure_sea_level, wave, comments, metar_cod, time_utc, date_utc))
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
        cursor.execute("INSERT INTO meteo VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?, ?)",
                       (date_utc, time_utc, wind_direction, wind_speed, wind_gust, visibility, weather_condition, temperature, dew_point, humidity, 
                        qt_clouds, qt_lower_clouds, cloud_base, clouds_type, pressure_heli, pressure_sea_level, wave, comments, metar_cod))

        # Committing the changes
        conn.commit()

        # Closing the connection
        conn.close()

        # Displaying a messagebox to confirm the insertion
        messagebox.showinfo("Информация внесена в базу данных", "Data inserted successfully!")


def select_from_db():
    db = sqlite3.connect('C:/Apps/luna.db')
    c = db.cursor()

    c.execute("""SELECT date_utc, time_utc, wind_direction, wind_speed, wind_gust, visibility, weather_condition, temperature, 
                dew_point, humidity, qt_clouds, qt_lower_clouds, cloud_base, clouds_type, pressure_heli, pressure_sea_level, 
                wave FROM meteo""")
    
    items = c.fetchall()
    
    # for i in range(len(items)): # Форматирование даты для вывода в окне программы только даты и месяца
    #     date = parse(items[i][0])
    #     formatted_date = date.strftime('%d/%m')
    #     items[i] = items[i][:0] + (formatted_date,) + items[i][1:]
    

    db.commit()
    db.close()
    return items

# create_db_luna()
# delete_all_data()
# select_from_db()

