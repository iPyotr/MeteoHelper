import tkinter
import tkinter.messagebox
import customtkinter
from datetime import datetime
import time
import os
from mailto import *
import subprocess
import win32com.client
from def_file import *

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Meteo Helper")
        self.geometry(f"{1285}x{700}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Лунская-А", font=customtkinter.CTkFont(size=24, weight="bold", underline=True))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.date_label = customtkinter.CTkLabel(self.sidebar_frame, text="Дата", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.date_label.grid(row=1, column=0, padx=20, pady=10)
        self.time_label = customtkinter.CTkLabel(self.sidebar_frame, text="Время", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.time_label.grid(row=2, column=0, padx=20, pady=10)

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Цветовая схема:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="Масштаб интерфейса:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))


        # Создаём группу вкладок weather
        self.tabview_weather = customtkinter.CTkTabview(self, width=350)
        self.tabview_weather.grid(row=0, column=1, padx=(20, 20), pady=(10, 10), sticky="nsew")
        self.tabview_weather.add("Текущая погода")
        self.tabview_weather.add("История наблюдений")
        self.tabview_weather.add("Процедура")
        self.tabview_weather.tab("Текущая погода").grid_columnconfigure(1, weight=1)# configure grid of individual tabs
        self.tabview_weather.tab("История наблюдений").grid_columnconfigure(0, weight=1)
        self.tabview_weather.tab("Процедура").grid_columnconfigure(1, weight=1)
        self.font_table = customtkinter.CTkFont(size=14, weight="bold")
        # Средняя скорость ветра (м/c)#
        self.wind_label = customtkinter.CTkLabel(self.tabview_weather.tab("Текущая погода"),
                                                     text="Средняя скорость ветра (м/c)",
                                                     font=customtkinter.CTkFont(size=14, weight="bold"), anchor='w')
        self.wind_label.grid(row=2, column=0, padx=20, pady=(20, 0), sticky='E')
        self.wind_entry = customtkinter.CTkEntry(master=self.tabview_weather.tab("Текущая погода"),
                                                     placeholder_text="m/s", width=60)
        self.wind_entry.grid(row=2, column=1, padx=(20, 20), pady=(20, 0), sticky="W")

        # Максимальный порыв ветра (м/с)
        self.windgust_label = customtkinter.CTkLabel(self.tabview_weather.tab("Текущая погода"), text="Максимальный порыв ветра (м/с)",
                                                 font=customtkinter.CTkFont(size=14, weight="bold"))
        self.windgust_label.grid(row=3, column=0, padx=20, pady=(0, 0), sticky='E')
        self.windgust_entry = customtkinter.CTkEntry(master=self.tabview_weather.tab("Текущая погода"),
                                               placeholder_text="m/s", width=60)
        self.windgust_entry.grid(row=3, column=1, padx=(20, 20), pady=(0, 0), sticky="W")


        # Направление ветра (град)
        self.wind_dir_label = customtkinter.CTkLabel(self.tabview_weather.tab("Текущая погода"),
                                                     text="Направление ветра (град)",
                                                     font=customtkinter.CTkFont(size=14, weight="bold"))
        self.wind_dir_label.grid(row=4, column=0, padx=20, pady=(0, 10), sticky='E')
        self.wind_dir_entry = customtkinter.CTkEntry(master=self.tabview_weather.tab("Текущая погода"),
                                                     placeholder_text="", width=60)
        self.wind_dir_entry.grid(row=4, column=1, padx=(20, 20), pady=(0, 10), sticky="W")

        # Горизонтальная видимость (км)
        self.visibility_label = customtkinter.CTkLabel(self.tabview_weather.tab("Текущая погода"),
                                                     text="Горизонтальная видимость (км)",
                                                     font=customtkinter.CTkFont(size=14, weight="bold"))
        self.visibility_label.grid(row=5, column=0, padx=20, pady=(0, 0), sticky='E')
        self.visibility_entry = customtkinter.CTkEntry(master=self.tabview_weather.tab("Текущая погода"),
                                                     placeholder_text="", width=60)
        self.visibility_entry.grid(row=5, column=1, padx=(20, 20), pady=(0, 0), sticky="W")
        # Атмосферное явление
        self.weather_conditions_label = customtkinter.CTkLabel(self.tabview_weather.tab("Текущая погода"),
                                                         text="Атмосферное явление",
                                                         font=customtkinter.CTkFont(size=14, weight="bold"))
        self.weather_conditions_label.grid(row=6, column=0, padx=20, pady=(0, 0), sticky='E')
        self.weather_conditions_optionmenu = customtkinter.CTkOptionMenu(self.tabview_weather.tab("Текущая погода"),
                                                                   dynamic_resizing=False,
                                                                   values=["Дождь", "Град", "Снег"], width=87)
        self.weather_conditions_optionmenu.grid(row=6, column=1, padx=20, pady=(0, 0), sticky="w")
        # Температура воздуха(град)
        self.temperature_label = customtkinter.CTkLabel(self.tabview_weather.tab("Текущая погода"),
                                                       text="Температура воздуха(град)",
                                                       font=customtkinter.CTkFont(size=14, weight="bold"))
        self.temperature_label.grid(row=7, column=0, padx=20, pady=(0, 0), sticky='E')
        self.temperature_entry = customtkinter.CTkEntry(master=self.tabview_weather.tab("Текущая погода"),
                                                       placeholder_text="", width=60)
        self.temperature_entry.grid(row=7, column=1, padx=(20, 20), pady=(0, 0), sticky="W")
        # Температура точки росы(град)
        self.dew_point_temperature_label = customtkinter.CTkLabel(self.tabview_weather.tab("Текущая погода"),
                                                        text="Температура точки росы(град)",
                                                        font=customtkinter.CTkFont(size=14, weight="bold"))
        self.dew_point_temperature_label.grid(row=8, column=0, padx=20, pady=(0, 0), sticky='E')
        self.dew_point_temperature_entry = customtkinter.CTkEntry(master=self.tabview_weather.tab("Текущая погода"),
                                                        placeholder_text="", width=60)
        self.dew_point_temperature_entry.grid(row=8, column=1, padx=(20, 20), pady=(0, 0), sticky="W")
        # Влажность воздуха (%)
        self.humidity_label = customtkinter.CTkLabel(self.tabview_weather.tab("Текущая погода"),
                                                                  text="Влажность воздуха (%)",
                                                                  font=customtkinter.CTkFont(size=14, weight="bold"))
        self.humidity_label.grid(row=9, column=0, padx=20, pady=(0, 0), sticky='E')
        self.humidity_entry = customtkinter.CTkEntry(master=self.tabview_weather.tab("Текущая погода"),
                                                                  placeholder_text="", width=60)
        self.humidity_entry.grid(row=9, column=1, padx=(20, 20), pady=(0, 0), sticky="W")
        # Общее количество облачности (октанты)
        self.total_clouds_label = customtkinter.CTkLabel(self.tabview_weather.tab("Текущая погода"),
                                                 text="Общее количество облачности (октанты)",
                                                 font=customtkinter.CTkFont(size=14, weight="bold"))
        self.total_clouds_label.grid(row=2, column=3, padx=0, pady=(20, 0), sticky='E')
        self.total_clouds_optionmenu = customtkinter.CTkOptionMenu(self.tabview_weather.tab("Текущая погода"),
                                                        dynamic_resizing=False,
                                                        values=['0', '1', '2', '4', '5', '6', '7', '8', '9'], width=87)
        self.total_clouds_optionmenu.grid(row=2, column=4, padx=20, pady=(20, 0))
        # Количество нижнего яруса (октанты)
        self.quantity_clouds_label = customtkinter.CTkLabel(self.tabview_weather.tab("Текущая погода"),
                                                         text="Количество нижнего яруса (октанты)",
                                                         font=customtkinter.CTkFont(size=14, weight="bold"))
        self.quantity_clouds_label.grid(row=3, column=3, padx=0, pady=(5, 0), sticky='E')
        self.quantity_clouds_optionmenu = customtkinter.CTkOptionMenu(self.tabview_weather.tab("Текущая погода"),
                                                                   dynamic_resizing=False,
                                                                   values=['0', '1', '2', '4', '5', '6', '7', '8', '9'], width=87)
        self.quantity_clouds_optionmenu.grid(row=3, column=4, padx=20, pady=(5, 0))
        # Высота НГО (м)
        self.cloud_base_lower_label = customtkinter.CTkLabel(self.tabview_weather.tab("Текущая погода"),
                                                            text="Высота НГО (м)",
                                                            font=customtkinter.CTkFont(size=14, weight="bold"))
        self.cloud_base_lower_label.grid(row=4, column=3, padx=0, pady=(0, 0), sticky='E')
        self.cloud_base_lower_entry = customtkinter.CTkEntry(master=self.tabview_weather.tab("Текущая погода"),
                                                     placeholder_text="", width=60)
        self.cloud_base_lower_entry.grid(row=4, column=4, padx=(20, 20), pady=(0, 0), sticky="W")
        # Форма облачности
        self.cloud_form_label = customtkinter.CTkLabel(self.tabview_weather.tab("Текущая погода"),
                                                            text="Форма облачности",
                                                            font=customtkinter.CTkFont(size=14, weight="bold"))
        self.cloud_form_label.grid(row=5, column=3, padx=0, pady=(0, 10), sticky='E')
        self.cloud_form_optionmenu = customtkinter.CTkOptionMenu(self.tabview_weather.tab("Текущая погода"),
                                                                      dynamic_resizing=False,
                                                                      values=['Кучево дождевые',
                                                                              'кучевые плоские',
                                                                              'слоисто-дождевые',
                                                                              'разорванно-дождевые',
                                                                              'слоистые',
                                                                              'слоисто-кучевые',
                                                                              'высокослоистые',
                                                                              'высококучевые',
                                                                              'пересто-кучевые',
                                                                              'перистые'], width=87)
        self.cloud_form_optionmenu.grid(row=5, column=4, padx=20, pady=(0, 10))
        # Давление на уровне вертолетной площадки (мм.рт.ст.)
        self.pressure_helideck_label = customtkinter.CTkLabel(self.tabview_weather.tab("Текущая погода"),
                                                             text="Давление на уровне вертолетной площадки\n(мм.рт.ст.)",
                                                             font=customtkinter.CTkFont(size=14, weight="bold"))
        self.pressure_helideck_label.grid(row=7, column=3, padx=0, pady=(0, 0), sticky='E')
        self.pressure_helideck_entry = customtkinter.CTkEntry(master=self.tabview_weather.tab("Текущая погода"),
                                                             placeholder_text="", width=60)
        self.pressure_helideck_entry.grid(row=7, column=4, padx=(20, 20), pady=(0, 0), sticky="w")
        # Давление на уровне моря(гПа)
        self.pressure_sea_level_label = customtkinter.CTkLabel(self.tabview_weather.tab("Текущая погода"),
                                                              text="Давление на уровне моря(гПа)",
                                                              font=customtkinter.CTkFont(size=14, weight="bold"))
        self.pressure_sea_level_label.grid(row=8, column=3, padx=0, pady=(0, 0), sticky='E')
        self.pressure_sea_level_entry = customtkinter.CTkEntry(master=self.tabview_weather.tab("Текущая погода"),
                                                              placeholder_text="", width=60)
        self.pressure_sea_level_entry.grid(row=8, column=4, padx=(20, 20), pady=(0, 0), sticky="W")
        # Высота преобладающих волн (м)
        self.wave_height_label = customtkinter.CTkLabel(self.tabview_weather.tab("Текущая погода"),
                                                               text="Высота преобладающих волн (м)",
                                                               font=customtkinter.CTkFont(size=14, weight="bold"))
        self.wave_height_label.grid(row=9, column=3, padx=0, pady=(0, 0), sticky='E')
        self.wave_height_entry = customtkinter.CTkEntry(master=self.tabview_weather.tab("Текущая погода"),
                                                               placeholder_text="", width=60)
        self.wave_height_entry.grid(row=9, column=4, padx=(20, 20), pady=(0, 0), sticky="W")

#######################
        self.comments = customtkinter.CTkEntry(master=self.tabview_weather.tab("Текущая погода"),
                                            placeholder_text="Ввести комментарий(если требуется)")
        self.comments.grid(row=14, column=0, columnspan=5, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.checkbox_1 = customtkinter.CTkCheckBox(master=self.tabview_weather.tab("Текущая погода"),
                                                    text='Включить комментарий в сводку')
        self.checkbox_1.grid(row=15, column=0, pady=(10, 10), padx=20, sticky="n")

        self.metar_button = customtkinter.CTkButton(master=self.tabview_weather.tab("Текущая погода"),
                                                    command=self.click_metar, text='METAR', width=100, height=35)
        self.metar_button.grid(row=17, column=0, padx=20, pady=10)
        self.email_button = customtkinter.CTkButton(master=self.tabview_weather.tab("Текущая погода"),
                                                    command=self.send_email, text='Отправить сводку', width=50, height=35)
        self.email_button.grid(row=19, column=0, padx=20, pady=10)
        self.metar_output = customtkinter.CTkLabel(self.tabview_weather.tab("Текущая погода"), text="здесь будет МЕТАР код",
                                                       font=customtkinter.CTkFont(size=20, weight="normal"), bg_color='light gray')
        self.metar_output.grid(row=18, column=0, columnspan=5, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.textbox_metar = customtkinter.CTkTextbox(self.tabview_weather.tab("Текущая погода"), height=0)
        self.textbox_metar.grid(row=20, column=0, columnspan=5, padx=(20, 0), pady=(20, 20), sticky="nsew")


        # create textbox
        self.textbox_tab3 = customtkinter.CTkTextbox(self.tabview_weather.tab("Процедура"))
        self.textbox_tab3.grid(row=0, column=1, padx=(00, 0), pady=(00, 0), sticky="nsew")

        # Создаём фрейм для местного времени
        self.local_time_frame = customtkinter.CTkFrame(self, width=240, corner_radius=0)
        self.local_time_frame.grid(row=0, column=3, rowspan=4, sticky="nsew")
        self.local_time_text = customtkinter.CTkLabel(self.local_time_frame, text="Местное время",
                                                       font=customtkinter.CTkFont(size=16, weight="bold"))
        self.local_time_text.grid(row=1, column=0, padx=20, pady=10)
        self.local_time_label = customtkinter.CTkLabel(self.local_time_frame, text="Местное Время", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.local_time_label.grid(row=2, column=0, padx=20, pady=10)
        self.update_clock() # Запускаем функцию для обновления времени


        # set default values
        # self.sidebar_button_3.configure(state="disabled", text="Disabled CTkButton")
        self.appearance_mode_optionemenu.set("Light")
        self.scaling_optionemenu.set("100%")
        self.textbox_tab3.insert("0.0", "Наставление по наблюдению за погодой\n\n" + "Результаты наблюдений и специальных сводок фиксируются в специальном журнале и передаются открытым текстом в установленные адреса (в случае недоступности сервиса передачи сообщений METAR). При передаче метеорологических данных в автоматическом режиме запись в журнал отменяется (фиксируются только данные об особых явлениях погоды и наличии кучево-дождевой и мощно-кучевой облачности)." * 20)


    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="Всплывающее окно ввода данных")
        print("Всплывающее окно ввода данных:", dialog.get_input())

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
        current_date = time.strftime("%d/%m/%Y")
        current_date_utc = datetime.utcnow().date()
        self.time_label.configure(text=current_time_utc)
        self.local_time_label.configure(text=current_time)
        self.date_label.configure(text=current_date_utc)
        self.after(1000, self.update_clock)

    def click_metar(self):
        date_time = date_time_cod(str(datetime.utcnow().strftime("%d/%m/%Y %H:%M")))

        metar_data = str(date_time)
        self.metar_output.configure(text=metar_data)




    def send_email(self):
        data = self.metar_output.cget('text')
        self.textbox_metar.delete('1.0', 'end')
        self.textbox_metar.insert('end', data)
        print(datetime.utcnow())

    def mail_outlook(self):
        print('ok')
        pass


if __name__ == "__main__":
    app = App()
    app.mainloop()