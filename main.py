import tkinter as tk
import tkinter.messagebox
import customtkinter
from datetime import datetime
import time
import os
from test_cod import *
import subprocess
import win32com.client
from def_file import *
import webbrowser

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Meteo Helper")
        self.geometry(
            "1340x690+{}+{}".format(self.winfo_screenwidth() // 2 - 700, self.winfo_screenheight() // 2 - 340))

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew", rowspan=20)
        self.sidebar_frame.grid_rowconfigure(5, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Лунская-А",
                                                 font=customtkinter.CTkFont(size=24, weight="bold", underline=True))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.date_label = customtkinter.CTkLabel(self.sidebar_frame, text="Дата",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.date_label.grid(row=1, column=0, padx=20, pady=10)
        self.time_label = customtkinter.CTkLabel(self.sidebar_frame, text="Время",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.time_label.grid(row=2, column=0, padx=20, pady=10)

        self.weather_button = customtkinter.CTkButton(master=self.sidebar_frame, command=self.weather_frame_visibility,
                                                      text='Сводка', width=120, height=30)
        self.weather_button.grid(row=3, column=0, padx=0, pady=(10, 0), sticky='n')
        self.history_button = customtkinter.CTkButton(master=self.sidebar_frame, command=self.history_frame_visibility,
                                                      text='История', width=120, height=30)
        self.history_button.grid(row=4, column=0, padx=0, pady=(10, 0), sticky='n')
        self.history_button.grid_remove()
        self.about_button = customtkinter.CTkButton(master=self.sidebar_frame, command=self.about_frame_visibility,
                                                    text='О программе', width=120, height=30)
        self.about_button.grid(row=5, column=0, padx=0, pady=(10, 0), sticky='n')
        self.about_button.grid_remove()

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Цветовая схема:", anchor="w")
        self.appearance_mode_label.grid(row=8, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                                       values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=9, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="Масштаб интерфейса:", anchor="w")
        self.scaling_label.grid(row=17, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                               values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=18, column=0, padx=20, pady=(10, 20))

        # Создаём Frame weather
        self.weather_frame = customtkinter.CTkFrame(self, width=1000, height=600, corner_radius=0)
        self.weather_frame.grid(row=0, column=1, rowspan=20, sticky='NS', padx=(20, 20), pady=(10, 10))

        # Создаём Frame history
        self.history_frame = customtkinter.CTkFrame(self, width=1000, height=700, corner_radius=0)
        self.history_frame.grid(row=0, column=1, rowspan=20, sticky="NS", padx=(20, 20), pady=(10, 10))
        self.test_label = customtkinter.CTkLabel(self.history_frame,
                                                 text="Переданные сводки",
                                                 font=customtkinter.CTkFont(size=14, weight="bold"), width=930)
        self.test_label.grid(row=0, column=0, padx=0, pady=(0, 0), sticky='NSEW')
        #
        # Создаём Frame about
        self.about_frame = customtkinter.CTkFrame(self, width=1000, height=600, corner_radius=0)
        self.about_frame.grid(row=0, column=1, rowspan=19, sticky="NS", padx=(20, 20), pady=(10, 10))
        self.test_label_about = customtkinter.CTkLabel(self.about_frame,
                                                       text="О программе",
                                                       font=customtkinter.CTkFont(size=14, weight="bold"), width=930)
        self.test_label_about.grid(row=0, column=0, padx=0, pady=(0, 0), sticky='NSEW')
        #
        #

        # Окно "Текущая погода"
        self.test_label_weather = customtkinter.CTkLabel(self.weather_frame, text="Текущая погода",
                                                         font=customtkinter.CTkFont(size=14, weight="bold"),
                                                         width=930)
        self.test_label_weather.grid(row=0, column=0, padx=(0, 10), pady=(5, 0), sticky='NSEW', columnspan=4)

        # "Средняя скорость ветра (м/c)"
        self.wind_label = customtkinter.CTkLabel(self.weather_frame,
                                                 text="Средняя скорость ветра (м/c)",
                                                 font=customtkinter.CTkFont(size=14, weight="bold"), anchor='w')
        self.wind_entry = customtkinter.CTkEntry(master=self.weather_frame,
                                                 placeholder_text="м/с", width=60, text_color="#36719F",
                                                 font=customtkinter.CTkFont(size=14, weight="bold"))
        # Максимальный порыв ветра (м/с)
        self.windgust_label = customtkinter.CTkLabel(self.weather_frame, text="Максимальный порыв ветра (м/с)",
                                                     font=customtkinter.CTkFont(size=14, weight="bold"))
        self.windgust_entry = customtkinter.CTkEntry(master=self.weather_frame,
                                                     placeholder_text="м/с", width=60, text_color="#36719F",
                                                     font=customtkinter.CTkFont(size=14, weight="bold"))
        # Направление ветра (град)
        self.wind_dir_label = customtkinter.CTkLabel(self.weather_frame, text="Направление ветра (град)",
                                                     font=customtkinter.CTkFont(size=14, weight="bold"))
        self.wind_dir_entry = customtkinter.CTkEntry(master=self.weather_frame,
                                                     placeholder_text="000", width=60, text_color="#36719F",
                                                     font=customtkinter.CTkFont(size=14, weight="bold"))
        # Горизонтальная видимость (км)
        self.visibility_label = customtkinter.CTkLabel(self.weather_frame, text="Горизонтальная видимость (м)",
                                                       font=customtkinter.CTkFont(size=14, weight="bold"))
        self.visibility_entry = customtkinter.CTkEntry(master=self.weather_frame,
                                                       placeholder_text="0000", width=60, text_color="#36719F",
                                                       font=customtkinter.CTkFont(size=14, weight="bold"))
        # Атмосферное явление
        self.weather_conditions_label = customtkinter.CTkLabel(self.weather_frame, text="Атмосферное явление",
                                                               font=customtkinter.CTkFont(size=14, weight="bold"))
        # Выбор значения атмосферного явления
        self.optionmenu_var = customtkinter.StringVar(value="явлений не наблюдается")
        self.weather_conditions_optionmenu = customtkinter.CTkOptionMenu(self.weather_frame,
                                                                         dynamic_resizing=False,
                                                                         values=weather_conditions_types, width=87,
                                                                         command=self.change_state_wc2,
                                                                         variable=self.optionmenu_var)
        self.optionmenu_var2 = customtkinter.StringVar(value="явлений не наблюдается")
        self.weather_conditions_optionmenu2 = customtkinter.CTkOptionMenu(self.weather_frame,
                                                                          dynamic_resizing=False,
                                                                          values=weather_conditions_types, width=87,
                                                                          command=self.change_state_wc3,
                                                                          variable=self.optionmenu_var2)
        self.optionmenu_var3 = customtkinter.StringVar(value="явлений не наблюдается")
        self.weather_conditions_optionmenu3 = customtkinter.CTkOptionMenu(self.weather_frame,
                                                                          dynamic_resizing=False,
                                                                          values=weather_conditions_types, width=87,
                                                                          command=self.change_state_wc3,
                                                                          variable=self.optionmenu_var3)
        # Температура воздуха(град)
        self.temperature_label = customtkinter.CTkLabel(self.weather_frame, text="Температура воздуха(град)",
                                                        font=customtkinter.CTkFont(size=14, weight="bold"))
        self.temperature_entry = customtkinter.CTkEntry(master=self.weather_frame,
                                                        placeholder_text="00.0", width=60, text_color="#36719F",
                                                        font=customtkinter.CTkFont(size=14, weight="bold"))
        # Температура точки росы(град)
        self.dew_point_temperature_label = customtkinter.CTkLabel(self.weather_frame,
                                                                  text="Температура точки росы(град)",
                                                                  font=customtkinter.CTkFont(size=14, weight="bold"))
        self.dew_point_temperature_entry = customtkinter.CTkEntry(master=self.weather_frame,
                                                                  placeholder_text="00.0", width=60,
                                                                  text_color="#36719F",
                                                                  font=customtkinter.CTkFont(size=14, weight="bold"))
        # Влажность воздуха (%)
        self.humidity_label = customtkinter.CTkLabel(self.weather_frame, text="Влажность воздуха (%)",
                                                     font=customtkinter.CTkFont(size=14, weight="bold"))
        self.humidity_entry = customtkinter.CTkEntry(master=self.weather_frame, placeholder_text="", width=60,
                                                     text_color="#36719F",
                                                     font=customtkinter.CTkFont(size=14, weight="bold"))

        # Общее количество облачности (октанты)
        self.total_clouds_label = customtkinter.CTkLabel(self.weather_frame,
                                                         text="Общее количество облачности (октанты)",
                                                         font=customtkinter.CTkFont(size=14, weight="bold"))
        self.total_clouds_optionmenu = customtkinter.CTkOptionMenu(self.weather_frame, dynamic_resizing=False,
                                                                   values=['0', '1', '2', '4', '5', '6', '7', '8'],
                                                                   width=87)
        # Количество нижнего яруса (октанты)
        self.quantity_clouds_label = customtkinter.CTkLabel(self.weather_frame,
                                                            text="Количество нижнего яруса (октанты)",
                                                            font=customtkinter.CTkFont(size=14, weight="bold"))
        self.quantity_clouds_optionmenu = customtkinter.CTkOptionMenu(self.weather_frame, dynamic_resizing=False,
                                                                      values=['0', '1', '2', '4', '5', '6', '7', '8'],
                                                                      width=87)
        # Высота НГО (м)
        self.cloud_base_lower_label = customtkinter.CTkLabel(self.weather_frame, text="Высота НГО (м)",
                                                             font=customtkinter.CTkFont(size=14, weight="bold"))
        self.cloud_base_lower_entry = customtkinter.CTkEntry(master=self.weather_frame,
                                                             placeholder_text="000", width=60, text_color="#36719F",
                                                             font=customtkinter.CTkFont(size=14, weight="bold"))
        # Форма облачности
        self.cloud_form_label = customtkinter.CTkLabel(self.weather_frame, text="Форма облачности",
                                                       font=customtkinter.CTkFont(size=14, weight="bold"))
        self.cloud_form_optionmenu = customtkinter.CTkOptionMenu(self.weather_frame, dynamic_resizing=False,
                                                                 values=clouds_type, width=87)
        self.cloud_form_optionmenu2 = customtkinter.CTkOptionMenu(self.weather_frame, dynamic_resizing=False,
                                                                  values=clouds_type, width=87)
        self.cloud_form_optionmenu3 = customtkinter.CTkOptionMenu(self.weather_frame, dynamic_resizing=False,
                                                                  values=clouds_type, width=87)
        # Давление на уровне вертолетной площадки (мм.рт.ст.)
        self.pressure_helideck_label = customtkinter.CTkLabel(self.weather_frame,
                                                              text="Давление на уровне вертолетной площадки\n(мм.рт.ст.)",
                                                              font=customtkinter.CTkFont(size=14, weight="bold"))
        self.pressure_helideck_entry = customtkinter.CTkEntry(master=self.weather_frame, placeholder_text="000.0",
                                                              width=60, text_color="#36719F",
                                                              font=customtkinter.CTkFont(size=14, weight="bold"))
        # Давление на уровне моря(гПа)
        self.pressure_sea_level_label = customtkinter.CTkLabel(self.weather_frame, text="Давление на уровне моря(гПа)",
                                                               font=customtkinter.CTkFont(size=14, weight="bold"))
        self.pressure_sea_level_entry = customtkinter.CTkEntry(master=self.weather_frame,
                                                               placeholder_text="0000", width=60, text_color="#36719F",
                                                               font=customtkinter.CTkFont(size=14, weight="bold"))
        # Высота преобладающих волн (cм)
        self.wave_height_label = customtkinter.CTkLabel(self.weather_frame, text="Высота преобладающих волн (cм)",
                                                        font=customtkinter.CTkFont(size=14, weight="bold"))
        self.wave_height_entry = customtkinter.CTkEntry(master=self.weather_frame, placeholder_text="000", width=60,
                                                        text_color="#36719F",
                                                        font=customtkinter.CTkFont(size=14, weight="bold"))

        ##############################    Расположение элементов     ####################################
        # левая колонка данных
        self.wind_dir_label.grid(row=2, column=0, padx=(0, 10), pady=(20, 0), sticky='E')
        self.wind_dir_entry.configure(justify='center')
        self.wind_dir_entry.grid(row=2, column=1, padx=0, pady=(20, 0), sticky="W")
        self.wind_label.grid(row=3, column=0, padx=(0, 0), pady=(5, 0), sticky='E')
        self.wind_entry.configure(justify='center')
        self.wind_entry.grid(row=3, column=1, padx=(0, 0), pady=(5, 0), sticky="w")
        self.windgust_label.grid(row=4, column=0, padx=(0, 10), pady=(5, 0), sticky='E')
        self.windgust_entry.configure(justify='center')
        self.windgust_entry.grid(row=4, column=1, padx=(0, 0), pady=(5, 0), sticky="W")
        self.weather_conditions_label.grid(row=6, column=0, padx=(0, 10), pady=(5, 0), sticky='E')
        self.visibility_label.grid(row=5, column=0, padx=(0, 10), pady=(5, 0), sticky='E')
        self.visibility_entry.configure(justify='center')
        self.visibility_entry.grid(row=5, column=1, padx=(0, 0), pady=(5, 0), sticky="W")
        self.weather_conditions_optionmenu.grid(row=6, column=1, padx=(0, 10), pady=(5, 0), sticky="w")
        self.weather_conditions_optionmenu2.grid(row=7, column=1, padx=0, pady=(5, 0), sticky="w")
        self.weather_conditions_optionmenu3.grid(row=8, column=1, padx=0, pady=(5, 0), sticky="w")
        self.weather_conditions_optionmenu3.grid(row=8, column=1, padx=0, pady=(5, 0), sticky="w")
        self.temperature_label.grid(row=9, column=0, padx=(0, 10), pady=(5, 0), sticky='E')
        self.temperature_entry.configure(justify='center')
        self.temperature_entry.grid(row=9, column=1, padx=(0, 0), pady=(5, 0), sticky="W")
        self.temperature_entry.bind("<KeyRelease>", self.update_humid)
        self.dew_point_temperature_label.grid(row=10, column=0, padx=(0, 10), pady=(5, 0), sticky='E')
        self.dew_point_temperature_entry.configure(justify='center')
        self.dew_point_temperature_entry.grid(row=10, column=1, padx=(0, 0), pady=(5, 0), sticky="W")
        self.dew_point_temperature_entry.bind("<KeyRelease>", self.update_humid)
        self.humidity_label.grid(row=11, column=0, padx=(0, 10), pady=(5, 0), sticky='E')
        self.humidity_entry.configure(justify='center')
        self.humidity_entry.grid(row=11, column=1, padx=(0, 0), pady=(5, 0), sticky="W")
        ### правая колонка данных
        self.total_clouds_label.grid(row=2, column=2, padx=(0, 10), pady=(20, 0), sticky='E')
        self.total_clouds_optionmenu.grid(row=2, column=3, padx=0, pady=(20, 0), sticky='W')
        self.quantity_clouds_label.grid(row=3, column=2, padx=(0, 10), pady=(5, 0), sticky='E')
        self.quantity_clouds_optionmenu.grid(row=3, column=3, padx=0, pady=(5, 0), sticky='W')
        self.cloud_base_lower_label.grid(row=4, column=2, padx=(0, 10), pady=(5, 0), sticky='E')
        self.cloud_base_lower_entry.configure(justify='center')
        self.cloud_base_lower_entry.grid(row=4, column=3, padx=(0, 0), pady=(5, 0), sticky="W")
        self.cloud_form_label.grid(row=6, column=2, padx=(0, 10), pady=(5, 0), sticky='E')
        self.cloud_form_optionmenu.grid(row=6, column=3, padx=0, pady=(5, 0), sticky='W')
        self.cloud_form_optionmenu2.grid(row=7, column=3, padx=0, pady=(5, 0), sticky='W')
        self.cloud_form_optionmenu2.grid(row=7, column=3, padx=0, pady=(5, 0), sticky='W')
        self.cloud_form_optionmenu3.grid(row=8, column=3, padx=0, pady=(5, 0), sticky='W')
        self.pressure_helideck_label.grid(row=9, column=2, padx=(0, 10), pady=(5, 0), sticky='E')
        self.pressure_helideck_entry.configure(justify='center')
        self.pressure_helideck_entry.grid(row=9, column=3, padx=(0, 0), pady=(5, 0), sticky="w")
        self.pressure_sea_level_label.grid(row=10, column=2, padx=(0, 10), pady=(5, 0), sticky='E')
        self.pressure_sea_level_entry.configure(justify='center')
        self.pressure_sea_level_entry.grid(row=10, column=3, padx=(0, 0), pady=(5, 0), sticky="W")
        self.wave_height_label.grid(row=11, column=2, padx=(0, 10), pady=(5, 0), sticky='E')
        self.wave_height_entry.configure(justify='center')
        self.wave_height_entry.grid(row=11, column=3, padx=(0, 0), pady=(5, 0), sticky="W")

        #######################
        self.comments = customtkinter.CTkEntry(master=self.weather_frame,
                                               placeholder_text="ЩЭФАП METAR UHSC 220500Z 35017G32MPS 0400 SN VV006 M10/M10 Q1006 RMK QBB180 QFE749 HSAUT000-")
        self.comments.grid(row=14, column=0, columnspan=4, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.checkbox_1 = customtkinter.CTkCheckBox(master=self.weather_frame,
                                                    text='Включить комментарий в сводку')
        self.checkbox_1.grid(row=15, column=0, pady=(10, 10), padx=0, sticky="n")

        self.metar_button = customtkinter.CTkButton(master=self.weather_frame,
                                                    command=self.check_user_name, text='METAR', width=900, height=35)
        self.metar_button.grid(row=17, column=0, columnspan=4, padx=0, pady=10)
        self.email_button = customtkinter.CTkButton(master=self.weather_frame,
                                                    command=self.send_email, text='Отправить сводку', width=900,
                                                    height=35)
        self.email_button.grid(row=19, column=0, padx=0, pady=10, columnspan=4)
        self.metar_output = customtkinter.CTkLabel(self.weather_frame,
                                                   text="здесь будет код METAR",
                                                   font=customtkinter.CTkFont(size=16, weight="normal"))
        self.metar_output.configure(justify='center', width=200)
        self.metar_output.grid(row=18, column=0, columnspan=4, padx=(0, 0), pady=(20, 20), sticky="nsew")

        # Создаём фрейм для местного времени
        self.local_time_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.local_time_frame.grid(row=0, column=2, rowspan=20, sticky="nsew")
        self.local_time_text = customtkinter.CTkLabel(self.local_time_frame, text="Местное время",
                                                      font=customtkinter.CTkFont(size=16, weight="bold"))
        self.local_time_text.grid(row=1, column=0, padx=20, pady=10)
        self.local_date_label = customtkinter.CTkLabel(self.local_time_frame, text="Местное Время",
                                                       font=customtkinter.CTkFont(size=20, weight="bold"))
        self.local_date_label.grid(row=2, column=0, padx=20, pady=10)
        self.local_time_label = customtkinter.CTkLabel(self.local_time_frame, text="Местное Время",
                                                       font=customtkinter.CTkFont(size=20, weight="bold"))
        self.local_time_label.grid(row=3, column=0, padx=20, pady=10)
        self.update_clock()  # Запускаем функцию для обновления времени

        # set default values
        # self.wind_entry.insert(0, 12)
        # self.windgust_entry.insert(0, 37)
        # self.visibility_entry.insert(0, 1500)
        # self.wind_dir_entry.insert(0, 250)
        # self.temperature_entry.insert(0, -21.6)
        # self.humidity_entry.insert(0, 0)
        # self.cloud_base_lower_entry.insert(0, 700)
        # self.pressure_helideck_entry.insert(0, 747.7)
        # self.pressure_sea_level_entry.insert(0, 1012.4)
        self.wave_height_entry.insert(0, 0)
        # self.dew_point_temperature_entry.insert(0, -22.9)
        self.weather_conditions_optionmenu.set("явлений не наблюдается")
        self.weather_conditions_optionmenu2.set("")
        self.weather_conditions_optionmenu2.grid_remove()
        self.weather_conditions_optionmenu3.set("")
        self.weather_conditions_optionmenu3.grid_remove()
        self.quantity_clouds_optionmenu.set("0")
        self.total_clouds_optionmenu.set("0")
        self.cloud_form_optionmenu.set("")
        self.cloud_form_optionmenu2.set("")
        self.cloud_form_optionmenu3.set("")

        self.history_frame.grid_remove()
        self.about_frame.grid_remove()

        self.appearance_mode_optionemenu.set("Light")
        self.scaling_optionemenu.set("100%")

        self.wc_option = self.weather_conditions_optionmenu.get()
        self.wc_option2 = self.weather_conditions_optionmenu2.get()
        self.wc_option3 = self.weather_conditions_optionmenu3.get()

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="Всплывающее окно ввода данных")
        print("Всплывающее окно ввода данных:", dialog.get_input())

    def update_humid(self, *args):
        '''RH = (e / e_s) * 100 где:
            e = (6.11 * 10^((7.5 * Td) / (237.7 + Td))) * (10^(2) / (T + 273.15)) - абсолютная влажность воздуха
            e_s = (6.11 * 10^((7.5 * T) / (237.7 + T))) * (10^(2) / (T + 273.15)) - абсолютная влажность воздуха при сухом воздухе
            RH - относительная влажность воздуха в процентах
            '''

        T = float(self.temperature_entry.get())
        Td = float(self.dew_point_temperature_entry.get())
        e = (6.11 * 10 ** ((7.5 * Td) / (237.7 + Td))) * (10 ** (2) / (T + 273.15))
        e_s = (6.11 * 10 ** ((7.5 * T) / (237.7 + T))) * (10 ** (2) / (T + 273.15))
        RH = int((e / e_s) * 100)
        self.humidity_entry.delete(0, 'end')
        self.humidity_entry.insert('end', RH)

    def change_state_wc2(self, event):
        if self.optionmenu_var.get() == "явлений не наблюдается":
            self.weather_conditions_optionmenu2.set("")
            self.weather_conditions_optionmenu2.grid_remove()
            self.weather_conditions_optionmenu3.set("")
            self.weather_conditions_optionmenu3.grid_remove()
        elif self.optionmenu_var.get() != "явлений не наблюдается":
            self.weather_conditions_optionmenu2.grid()

    def change_state_wc3(self, event):
        if self.optionmenu_var2.get() == "явлений не наблюдается":
            self.weather_conditions_optionmenu2.set("")
            self.weather_conditions_optionmenu2.grid_remove()
            self.weather_conditions_optionmenu3.set("")
            self.weather_conditions_optionmenu3.grid_remove()
        elif self.optionmenu_var2.get() != "явлений не наблюдается":
            self.weather_conditions_optionmenu3.grid()
        if self.optionmenu_var3.get() == "явлений не наблюдается":
            self.weather_conditions_optionmenu3.set("")
            self.weather_conditions_optionmenu3.grid_remove()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")

    def update_clock(self):
        current_time = time.strftime("%H:%M:%S")
        current_time_utc = datetime.utcnow().time().strftime("UTC %H:%M")
        current_date = time.strftime("%Y-%m-%d")
        current_date_utc = datetime.utcnow().date()
        self.time_label.configure(text=current_time_utc)
        self.local_time_label.configure(text=current_time)
        self.local_date_label.configure(text=current_date)
        self.date_label.configure(text=current_date_utc)
        self.after(1000, self.update_clock)

    def click_metar(self):  # формирование кода метар
        self.metar_output.configure(text='проверь введённые данные')
        global dt_metar
        clouds_metar = [self.visibility_entry.get(),
                        self.total_clouds_optionmenu.get(),
                        self.quantity_clouds_optionmenu.get(),
                        self.cloud_base_lower_entry.get()]
        wc = [self.weather_conditions_optionmenu.get(),
              self.weather_conditions_optionmenu2.get(),
              self.weather_conditions_optionmenu3.get()]
        dt_metar = date_time_cod(str(datetime.utcnow().strftime("%d/%m/%Y %H:%M")))
        metar_all = metar_cod(self.wind_entry.get(),
                              self.windgust_entry.get(),
                              self.wind_dir_entry.get(),
                              self.visibility_entry.get(),
                              wc,
                              self.pressure_helideck_entry.get(),
                              self.pressure_sea_level_entry.get(),
                              self.temperature_entry.get(),
                              self.dew_point_temperature_entry.get(),
                              self.humidity_entry.get(),
                              clouds_metar,
                              self.quantity_clouds_optionmenu.get(),
                              self.cloud_base_lower_entry.get(),
                              self.cloud_form_optionmenu.get(),
                              self.wave_height_entry.get()
                              )
        # metar_data = f'ЩЭФАП METAR UHSC {metar_all}'
        # if self.checkbox_1.get() == 1:
        #     metar_data += ' ' + self.comments.get() + ' -'
        # else:
        #     metar_data += ' -'
        self.metar_output.configure(text=metar_all)  # #

    def send_email(self):
        data = self.metar_output.cget('text')
        if self.checkbox_1.get() == 1:
            data += ' ' + self.comments.get() + ' -'
        else:
            data += ' -'
        recipient = ['pogoda10@sakhugms.ru']
        # pogoda10@sakhugms.ru SELLC-LUNA-Radio-Room@sakhalin2.ru
        cc = ['METAR', 'SELLC-LUNA-Radio-Room@sakhalin2.ru']
        bcc = ['SELLC-LUNA-Radio-Room@sakhalin2.ru', 'SELLC-LUNA-Weather-Observer@sakhalin2.ru']
        subject = 'METAR'
        recipient_string = ";".join(recipient)
        cc_string = ";".join(cc)
        bcc_string = ";".join(bcc)
        webbrowser.open(
            'mailto:' + recipient_string +
            '?cc=' + cc_string +
            '&bcc=' + bcc_string +
            '&subject=' + subject +
            '&body=' + data)

    def check_user_name(self):
        import socket
        user_name = ['petrp1', 'valery.sukhoruchkin']
        comp_name = ['Mybook', 'YUZCHE-D-99672']
        if os.getlogin() in user_name or socket.gethostname() in comp_name:
            self.click_metar()
        else:
            metar_data = 'На работу в Гидрометеоцентр требуется метеоролог. ' \
                         'Зарплата 15 тыс. рублей, ощущается как 45 тыс.'
            self.metar_output.configure(text=metar_data)

    def weather_frame_visibility(self):
        self.history_frame.grid_remove()
        self.about_frame.grid_remove()
        self.weather_frame.grid()

    def history_frame_visibility(self):
        self.history_frame.grid()
        self.about_frame.grid_remove()
        self.weather_frame.grid_remove()

    def about_frame_visibility(self):
        self.history_frame.grid_remove()
        self.weather_frame.grid_remove()
        self.about_frame.grid()


if __name__ == "__main__":
    app = App()
    app.mainloop()
