import customtkinter
from PIL import Image
from meteo_db import *
from def_file import *
import webbrowser
import time
from tkinter import ttk
from datetime import datetime
from tkcalendar import DateEntry


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Meteo Helper v0.9.1")
        self.iconbitmap('img/icon.ico')
        self.geometry(
            "1150x690+{}+{}".format(self.winfo_screenwidth() // 2 - 600, self.winfo_screenheight() // 2 - 340))
        self.resizable(width=False, height=False)

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "img")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "offshore-rig-logo.png")),
                                                 size=(40, 40))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")),
                                                       size=(20, 20))
        self.window_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "icon.ico")),
                                                        size=(20, 20))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(
                                                     image_path, "home_light.png")),
                                                 size=(20, 20))
        self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(
                                                     image_path, "chat_light.png")),
                                                 size=(20, 20))
        self.add_user_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(
                image_path, "add_user_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(7, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  Лунская-А",
                                                             image=self.logo_image,
                                                             compound="left",
                                                             font=customtkinter.CTkFont(size=22, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        ###
        ###
        ###

        self.date_label = customtkinter.CTkLabel(self.navigation_frame, text="Дата",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.date_label.grid(row=1, column=0, sticky="ew")
        self.time_label = customtkinter.CTkLabel(self.navigation_frame, text="Время",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.time_label.grid(row=2, column=0, pady=(0, 20), sticky="ew")

        ###
        ###
        ###

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
                                                   text="Погода",
                                                   fg_color="transparent", text_color=("gray10", "gray90"),
                                                   hover_color=(
                                                       "gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=3, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                      border_spacing=10, text="История",
                                                      fg_color="transparent", text_color=("gray10", "gray90"),
                                                      hover_color=(
                                                          "gray70", "gray30"),
                                                      image=self.chat_image, anchor="w",
                                                      command=self.frame_2_button_event)
        self.frame_2_button.grid(row=4, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                      border_spacing=10, text="Дополнительно",
                                                      fg_color="transparent", text_color=("gray10", "gray90"),
                                                      hover_color=(
                                                          "gray70", "gray30"),
                                                      image=self.add_user_image, anchor="w",
                                                      command=self.frame_3_button_event)
        self.frame_3_button.grid(row=5, column=0, sticky="ew")

        self.frame_about_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                          border_spacing=10, text="О программе",
                                                          fg_color="transparent", text_color=("gray10", "gray90"),
                                                          hover_color=(
                                                              "gray70", "gray30"),
                                                          image=self.add_user_image, anchor="w",
                                                          command=self.frame_about_button_event)
        self.frame_about_button.grid(row=6, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame,
                                                                values=[
                                                                    "Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(
            row=7, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(
            self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        # Направление ветра (град)
        self.wind_dir_label = customtkinter.CTkLabel(self.home_frame, text="Направление ветра (град)",
                                                     font=customtkinter.CTkFont(size=14, weight="bold"))
        self.wind_dir_entry = customtkinter.CTkEntry(master=self.home_frame,
                                                     placeholder_text="000", width=60, text_color="#36719F",
                                                     font=customtkinter.CTkFont(size=14, weight="bold"))
        # "Средняя скорость ветра (м/c)"
        self.wind_label = customtkinter.CTkLabel(self.home_frame,
                                                 text="Средняя скорость ветра (м/c)",
                                                 font=customtkinter.CTkFont(size=14, weight="bold"), anchor='w')
        self.wind_entry = customtkinter.CTkEntry(master=self.home_frame,
                                                 placeholder_text="м/с", width=60, text_color="#36719F",
                                                 font=customtkinter.CTkFont(size=14, weight="bold"))
        # Максимальный порыв ветра (м/с)
        self.windgust_label = customtkinter.CTkLabel(self.home_frame, text="Максимальный порыв ветра (м/с)",
                                                     font=customtkinter.CTkFont(size=14, weight="bold"))
        self.windgust_entry = customtkinter.CTkEntry(master=self.home_frame,
                                                     placeholder_text="м/с", width=60, text_color="#36719F",
                                                     font=customtkinter.CTkFont(size=14, weight="bold"))

        # Горизонтальная видимость (км)
        self.visibility_label = customtkinter.CTkLabel(self.home_frame, text="Горизонтальная видимость (м)",
                                                       font=customtkinter.CTkFont(size=14, weight="bold"))
        self.visibility_entry = customtkinter.CTkEntry(master=self.home_frame,
                                                       placeholder_text="0000", width=60, text_color="#36719F",
                                                       font=customtkinter.CTkFont(size=14, weight="bold"))
        # Атмосферное явление
        self.weather_conditions_label = customtkinter.CTkLabel(self.home_frame, text="Атмосферное явление",
                                                               font=customtkinter.CTkFont(size=14, weight="bold"))
        # Выбор значения атмосферного явления
        self.optionmenu_var = customtkinter.StringVar(
            value="явлений не наблюдается")
        self.weather_conditions_optionmenu = customtkinter.CTkOptionMenu(self.home_frame,
                                                                         dynamic_resizing=False,
                                                                         values=weather_conditions_types, width=87,
                                                                         command=self.change_state_wc2,
                                                                         variable=self.optionmenu_var)
        self.optionmenu_var2 = customtkinter.StringVar(
            value="явлений не наблюдается")
        self.weather_conditions_optionmenu2 = customtkinter.CTkOptionMenu(self.home_frame,
                                                                          dynamic_resizing=False,
                                                                          values=weather_conditions_types, width=87,
                                                                          command=self.change_state_wc3,
                                                                          variable=self.optionmenu_var2)
        self.optionmenu_var3 = customtkinter.StringVar(
            value="явлений не наблюдается")
        self.weather_conditions_optionmenu3 = customtkinter.CTkOptionMenu(self.home_frame,
                                                                          dynamic_resizing=False,
                                                                          values=weather_conditions_types, width=87,
                                                                          command=self.change_state_wc3,
                                                                          variable=self.optionmenu_var3)
        # Температура воздуха(град)
        self.temperature_label = customtkinter.CTkLabel(self.home_frame, text="Температура воздуха(град)",
                                                        font=customtkinter.CTkFont(size=14, weight="bold"))
        self.temperature_entry = customtkinter.CTkEntry(master=self.home_frame,
                                                        placeholder_text="00.0", width=60, text_color="#36719F",
                                                        font=customtkinter.CTkFont(size=14, weight="bold"))
        # Температура точки росы(град)
        self.dew_point_temperature_label = customtkinter.CTkLabel(self.home_frame,
                                                                  text="Температура точки росы(град)",
                                                                  font=customtkinter.CTkFont(size=14, weight="bold"))
        self.dew_point_temperature_entry = customtkinter.CTkEntry(master=self.home_frame,
                                                                  placeholder_text="00.0", width=60,
                                                                  text_color="#36719F",
                                                                  font=customtkinter.CTkFont(size=14, weight="bold"))
        # Влажность воздуха (%)
        self.humidity_label = customtkinter.CTkLabel(self.home_frame, text="Влажность воздуха (%)",
                                                     font=customtkinter.CTkFont(size=14, weight="bold"))
        self.humidity_entry = customtkinter.CTkEntry(master=self.home_frame, placeholder_text="", width=60,
                                                     text_color="#36719F",
                                                     font=customtkinter.CTkFont(size=14, weight="bold"))

        # Общее количество облачности (октанты)
        self.total_clouds_label = customtkinter.CTkLabel(self.home_frame,
                                                         text="Общее количество облачности (октанты)",
                                                         font=customtkinter.CTkFont(size=14, weight="bold"))
        self.total_clouds_optionmenu = customtkinter.CTkOptionMenu(self.home_frame, dynamic_resizing=False,
                                                                   values=[
                                                                       '0', '1', '2', '3', '4', '5', '6', '7', '8'],
                                                                   width=87)
        # Количество нижнего яруса (октанты)
        self.quantity_clouds_label = customtkinter.CTkLabel(self.home_frame,
                                                            text="Количество нижнего яруса (октанты)",
                                                            font=customtkinter.CTkFont(size=14, weight="bold"))
        self.quantity_clouds_optionmenu = customtkinter.CTkOptionMenu(self.home_frame, dynamic_resizing=False,
                                                                      values=[
                                                                          '0', '1', '2', '3', '4', '5', '6', '7', '8'],
                                                                      width=87)
        # Высота НГО (м)
        self.cloud_base_lower_label = customtkinter.CTkLabel(self.home_frame, text="Высота НГО (м)",
                                                             font=customtkinter.CTkFont(size=14, weight="bold"))
        self.cloud_base_lower_entry = customtkinter.CTkEntry(master=self.home_frame,
                                                             placeholder_text="000", width=60, text_color="#36719F",
                                                             font=customtkinter.CTkFont(size=14, weight="bold"))
        # Форма облачности
        self.cloud_form_label = customtkinter.CTkLabel(self.home_frame, text="Форма облачности",
                                                       font=customtkinter.CTkFont(size=14, weight="bold"))
        self.cloud_form_optionmenu_var = customtkinter.StringVar(value="")
        self.cloud_form_optionmenu = customtkinter.CTkOptionMenu(self.home_frame, dynamic_resizing=False,
                                                                 values=clouds_type, width=87,
                                                                 command=self.change_state_cloud2,
                                                                 variable=self.cloud_form_optionmenu_var)
        self.cloud_form_optionmenu2_var = customtkinter.StringVar(value="")
        self.cloud_form_optionmenu2 = customtkinter.CTkOptionMenu(self.home_frame, dynamic_resizing=False,
                                                                  values=clouds_type, width=87,
                                                                  command=self.change_state_cloud3,
                                                                  variable=self.cloud_form_optionmenu2_var)
        self.cloud_form_optionmenu3_var = customtkinter.StringVar(value="")
        self.cloud_form_optionmenu3 = customtkinter.CTkOptionMenu(self.home_frame, dynamic_resizing=False,
                                                                  values=clouds_type, width=87,
                                                                  command=self.change_state_cloud3,
                                                                  variable=self.cloud_form_optionmenu3_var)
        # Давление на уровне вертолетной площадки (мм.рт.ст.)
        self.pressure_helideck_label = customtkinter.CTkLabel(self.home_frame,
                                                              text="Давление на уровне вертолетной площадки\n(мм.рт.ст.)",
                                                              font=customtkinter.CTkFont(size=14, weight="bold"))
        self.pressure_helideck_entry = customtkinter.CTkEntry(master=self.home_frame, placeholder_text="000.0",
                                                              width=60, text_color="#36719F",
                                                              font=customtkinter.CTkFont(size=14, weight="bold"))
        # Давление на уровне моря(гПа)
        self.pressure_sea_level_label = customtkinter.CTkLabel(self.home_frame, text="Давление на уровне моря(гПа)",
                                                               font=customtkinter.CTkFont(size=14, weight="bold"))
        self.pressure_sea_level_entry = customtkinter.CTkEntry(master=self.home_frame,
                                                               placeholder_text="0000", width=60, text_color="#36719F",
                                                               font=customtkinter.CTkFont(size=14, weight="bold"))
        # Высота преобладающих волн (cм)
        self.wave_height_label = customtkinter.CTkLabel(self.home_frame, text="Высота преобладающих волн (cм)",
                                                        font=customtkinter.CTkFont(size=14, weight="bold"))
        self.wave_height_entry = customtkinter.CTkEntry(master=self.home_frame, placeholder_text="000", width=60,
                                                        text_color="#36719F",
                                                        font=customtkinter.CTkFont(size=14, weight="bold"))

        ##############################    Расположение элементов     ####################################
        # левая колонка данных
        self.wind_dir_label.grid(row=2, column=0, padx=(
            0, 10), pady=(20, 0), sticky='E')
        self.wind_dir_entry.configure(justify='center')
        self.wind_dir_entry.grid(
            row=2, column=1, padx=0, pady=(20, 0), sticky="W")
        self.wind_label.grid(row=3, column=0, padx=(0, 0),
                             pady=(5, 0), sticky='E')
        self.wind_entry.configure(justify='center')
        self.wind_entry.grid(row=3, column=1, padx=(0, 0),
                             pady=(5, 0), sticky="w")
        self.windgust_label.grid(row=4, column=0, padx=(
            0, 10), pady=(5, 0), sticky='E')
        self.windgust_entry.configure(justify='center')
        self.windgust_entry.grid(
            row=4, column=1, padx=(0, 0), pady=(5, 0), sticky="W")
        self.weather_conditions_label.grid(
            row=6, column=0, padx=(0, 10), pady=(5, 0), sticky='E')
        self.visibility_label.grid(
            row=5, column=0, padx=(0, 10), pady=(5, 0), sticky='E')
        self.visibility_entry.configure(justify='center')
        self.visibility_entry.grid(
            row=5, column=1, padx=(0, 0), pady=(5, 0), sticky="W")
        self.weather_conditions_optionmenu.grid(
            row=6, column=1, padx=(0, 10), pady=(5, 0), sticky="w")
        self.weather_conditions_optionmenu2.grid(
            row=7, column=1, padx=0, pady=(5, 0), sticky="w")
        self.weather_conditions_optionmenu3.grid(
            row=8, column=1, padx=0, pady=(5, 0), sticky="w")
        self.weather_conditions_optionmenu3.grid(
            row=8, column=1, padx=0, pady=(5, 0), sticky="w")
        self.temperature_label.grid(
            row=9, column=0, padx=(0, 10), pady=(5, 0), sticky='E')
        self.temperature_entry.configure(justify='center')
        self.temperature_entry.grid(
            row=9, column=1, padx=(0, 0), pady=(5, 0), sticky="W")
        self.temperature_entry.bind("<KeyRelease>", self.update_humid)
        self.dew_point_temperature_label.grid(
            row=10, column=0, padx=(0, 10), pady=(5, 0), sticky='E')
        self.dew_point_temperature_entry.configure(justify='center')
        self.dew_point_temperature_entry.grid(
            row=10, column=1, padx=(0, 0), pady=(5, 0), sticky="W")
        self.dew_point_temperature_entry.bind(
            "<KeyRelease>", self.update_humid)
        self.humidity_label.grid(row=11, column=0, padx=(
            0, 10), pady=(5, 0), sticky='E')
        self.humidity_entry.configure(justify='center')
        self.humidity_entry.grid(
            row=11, column=1, padx=(0, 0), pady=(5, 0), sticky="W")
        # правая колонка данных
        self.total_clouds_label.grid(
            row=2, column=2, padx=(0, 0), pady=(20, 0), sticky='E')
        self.total_clouds_optionmenu.grid(
            row=2, column=3, padx=(0, 50), pady=(20, 0), sticky='W')
        self.quantity_clouds_label.grid(
            row=3, column=2, padx=(0, 10), pady=(5, 0), sticky='E')
        self.quantity_clouds_optionmenu.grid(
            row=3, column=3, padx=(0, 30), pady=(5, 0), sticky='W')
        self.cloud_base_lower_label.grid(
            row=4, column=2, padx=(0, 10), pady=(5, 0), sticky='E')
        self.cloud_base_lower_entry.configure(justify='center')
        self.cloud_base_lower_entry.grid(
            row=4, column=3, padx=(0, 30), pady=(5, 0), sticky="W")
        self.cloud_form_label.grid(
            row=6, column=2, padx=(0, 10), pady=(5, 0), sticky='E')
        self.cloud_form_optionmenu.grid(
            row=6, column=3, padx=0, pady=(5, 0), sticky='W')
        self.cloud_form_optionmenu2.grid(
            row=7, column=3, padx=0, pady=(5, 0), sticky='W')
        self.cloud_form_optionmenu2.grid(
            row=7, column=3, padx=0, pady=(5, 0), sticky='W')
        self.cloud_form_optionmenu3.grid(
            row=8, column=3, padx=0, pady=(5, 0), sticky='W')
        self.pressure_helideck_label.grid(
            row=9, column=2, padx=(0, 10), pady=(5, 0), sticky='E')
        self.pressure_helideck_entry.configure(justify='center')
        self.pressure_helideck_entry.grid(
            row=9, column=3, padx=(0, 0), pady=(5, 0), sticky="w")
        self.pressure_sea_level_label.grid(
            row=10, column=2, padx=(0, 10), pady=(5, 0), sticky='E')
        self.pressure_sea_level_entry.configure(justify='center')
        self.pressure_sea_level_entry.grid(
            row=10, column=3, padx=(0, 0), pady=(5, 0), sticky="W")
        self.wave_height_label.grid(
            row=11, column=2, padx=(0, 10), pady=(5, 0), sticky='E')
        self.wave_height_entry.configure(justify='center')
        self.wave_height_entry.grid(
            row=11, column=3, padx=(0, 0), pady=(5, 0), sticky="W")

        self.comments = customtkinter.CTkEntry(master=self.home_frame,
                                               placeholder_text="ЩЭФАП METAR UHSC 220500Z 35017G32MPS 0400 SN VV006 M10/M10 Q1006 RMK QBB180 QFE749 HSAUT000-")
        self.comments.grid(row=14, column=0, columnspan=4,
                           padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.checkbox_1 = customtkinter.CTkCheckBox(master=self.home_frame,
                                                    text='Включить комментарий в сводку')
        self.checkbox_1.grid(row=15, column=0, pady=(
            10, 10), padx=(20, 20), sticky="n")

        self.set_report_time_button_var = customtkinter.StringVar(
            value="1 час")  # set initial value
        self.set_report_time_button = customtkinter.CTkSegmentedButton(master=self.home_frame,
                                                                       values=[
                                                                           "1 час", "30 минут", "Фактическое"],
                                                                       variable=self.set_report_time_button_var)
        self.set_report_time_button.grid(
            row=15, column=2, columnspan=2, pady=(10, 10), padx=(10, 20), sticky="e")

        self.metar_button = customtkinter.CTkButton(master=self.home_frame,
                                                    command=self.check_user_name, text='METAR', width=900, height=35)
        self.metar_button.grid(row=17, column=0, columnspan=4, padx=0, pady=10)

        self.metar_output = customtkinter.CTkLabel(self.home_frame,
                                                   text="здесь будет код METAR",
                                                   font=customtkinter.CTkFont(size=16, weight="normal"))
        self.metar_output.configure(justify='center', width=200)
        self.metar_output.grid(row=18, column=0, columnspan=4, padx=(
            0, 0), pady=(20, 20), sticky="nsew")
        self.email_button = customtkinter.CTkButton(master=self.home_frame,
                                                    command=self.send_email, text='Отправить сводку', width=900,
                                                    height=35)
        self.email_button.grid(row=19, column=0, padx=0, pady=10, columnspan=4)
        #######################################################################################################################################
        #######################################################################################################################################
        # create second frame
        self.second_frame = customtkinter.CTkFrame(
            self, corner_radius=0, fg_color="transparent")
        self.history_date_frame = customtkinter.CTkFrame(self.second_frame, corner_radius=0, fg_color="transparent")
        self.history_date_frame.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        self.home_frame_button_2 = customtkinter.CTkButton(self.history_date_frame, text="Получить данные",
                                                           image=self.image_icon_image, compound="right",
                                                           command=self.history_table)
        self.home_frame_button_2.grid(row=1, column=0, padx=20, pady=0, sticky="w")

        self.day_history_OptionMenu = customtkinter.CTkOptionMenu(self.history_date_frame, dynamic_resizing=False,
                                                                  values= [], width=87)
        # Установка дат для отображения данных в окне

        self.history_from_date_picker_label = customtkinter.CTkLabel(self.history_date_frame, text="Начальная дата",
                                                          font=customtkinter.CTkFont(size=12, weight="normal"))
        self.history_from_date_picker_label.grid(row=0, column=1, padx=10, pady=0, sticky="we")
        self.history_from_date_picker_label.configure(justify='center')

        self.history_from_date_picker = DateEntry(self.history_date_frame, width=12,
                                     background='darkblue', foreground='white',
                                     font=('Arial', 10, 'bold'), borderwidth=2, date_pattern="yyyy-mm-dd")
        self.history_from_date_picker.grid(row=1, column=1, padx=10, pady=0, sticky="ew")
        self.history_from_date_picker.configure(justify='center')

        self.history_to_date_picker_label = customtkinter.CTkLabel(self.history_date_frame, text="Конечная дата",
                                                                     font=customtkinter.CTkFont(size=12,
                                                                                                weight="normal"))
        self.history_to_date_picker_label.grid(row=0, column=2, padx=10, pady=0, sticky="ew")
        self.history_to_date_picker_label.configure(justify='center')

        self.history_to_date_picker = DateEntry(self.history_date_frame, width=12,
                                                  background='darkblue', foreground='white',
                                                  font=('Arial', 10, 'bold'), borderwidth=2, date_pattern="yyyy-mm-dd")
        self.history_to_date_picker.grid(row=1, column=2, padx=10, pady=0, sticky="ew")
        self.history_to_date_picker.configure(justify='center')



        # Создание таблицы для вывода данных из базы данных
        self.tree = ttk.Treeview(self.second_frame, show='headings')
        self.tree.grid(row=3, column=0, pady=(20, 20), padx=(20, 20), sticky="nsew")
        self.second_frame.grid_columnconfigure(0, weight=1, minsize=100)
        self.second_frame.grid_rowconfigure(3, weight=1)
        self.tb_heads = ["Дата", "Время", "Направление", "Ветер", "Порыв", "Видимость", "Явления", "Темп", "Точка росы",
                         "Влажность", "Кол.облаков", "Кол.нижний", "НГО", "Тип облаков", "P вп", "Р море", "Волнение"]
        self.tree["columns"] = self.tb_heads
        for header in self.tb_heads:
            self.tree.heading(header, text=header, anchor='center')
            self.tree.column(header, anchor='center')
            self.tree.column(header, width=50, anchor='center')

        # create third frame
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.additional_func_tab = customtkinter.CTkTabview(self.third_frame, width=900)
        self.additional_func_tab.grid(row=0, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.additional_func_tab.add("Экспорт в excel")
        self.additional_func_tab.add("Дополнительная опция 1")
        self.additional_func_tab.add("Дополнительная опция 2")
        ### Выбор начальной даты для экспорта в excel
        self.date_from_label = customtkinter.CTkLabel(self.additional_func_tab.tab("Экспорт в excel"),
                                                      text="Введите начальную дату:",
                                                      font=customtkinter.CTkFont(size=14, weight="bold"))
        self.date_from_label.grid(row=0, column=0, pady=(10, 0), padx=10, sticky='W')

        self.for_excel_from_date_picker = DateEntry(self.additional_func_tab.tab("Экспорт в excel"), width=12,
                                                  background='darkblue', foreground='white',
                                                  font=('Arial', 10, 'bold'), borderwidth=2, date_pattern="yyyy-mm-dd")
        self.for_excel_from_date_picker.grid(row=0, column=2, pady=(10, 0), padx=10, sticky='EW')
        self.for_excel_from_date_picker.configure(justify='center')


        ### Выбор конечной даты для экспорта в excel
        self.date_to_label = customtkinter.CTkLabel(self.additional_func_tab.tab("Экспорт в excel"),
                                                    text="Введите конечную дату:",
                                                    font=customtkinter.CTkFont(size=14, weight="bold"))
        self.date_to_label.grid(row=1, column=0, pady=(10, 0), padx=10, sticky='W')

        self.for_excel_to_date_picker = DateEntry(self.additional_func_tab.tab("Экспорт в excel"), width=12,
                                                    background='darkblue', foreground='white',
                                                    font=('Arial', 10, 'bold'), borderwidth=2,
                                                    date_pattern="yyyy-mm-dd")
        self.for_excel_to_date_picker.grid(row=1, column=2, pady=(10, 0), padx=10, sticky='EW')
        self.for_excel_to_date_picker.configure(justify='center')

        # Кнопка для экспорта данных из базы данных в файл excel
        self.history_to_excel_button = customtkinter.CTkButton(self.additional_func_tab.tab("Экспорт в excel"),
                                                               command=self.data_to_excel_period, text='Экспорт данных',
                                                               width=100,
                                                               height=35)
        self.history_to_excel_button.grid(row=2, column=1, padx=0, pady=10, columnspan=3)



        # Создание фрейма "О программе"
        self.about_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.dev_label = customtkinter.CTkLabel(self.about_frame, text=f"Разработчик: Писанко Пётр Фёдорович",
                                                font=customtkinter.CTkFont(size=14, weight="bold"))
        self.dev_label.grid(row=0, column=0, pady=(10, 0), padx=10, sticky='W')
        self.expert_label = customtkinter.CTkLabel(self.about_frame,
                                                   text=f"Главный консультант: Сухоручкин Валерий Валерьевич",
                                                   font=customtkinter.CTkFont(size=14, weight="bold"))
        self.expert_label.grid(row=1, column=0, pady=(0, 0), padx=10, sticky='W')
        # self.thanks_label = customtkinter.CTkLabel(self.about_frame,
        #                                            text=f"Отдельная благодарность: Кармадонову Сергею Викторовичу",
        #                                            font=customtkinter.CTkFont(size=14, weight="bold"))
        # self.thanks_label.grid(row=2, column=0, pady=(10, 0), padx=10, sticky='W')

        # select default frame
        self.select_frame_by_name("home")

        self.update_clock()  # Запускаем функцию для обновления времени

        ########
        # Значения по умолчанию
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
        # self.dew_point_temperature_entry.insert(0, -22.9)
        #
        self.wave_height_entry.insert(0, 0)
        self.weather_conditions_optionmenu.set("явлений не наблюдается")
        self.weather_conditions_optionmenu2.set("")
        self.weather_conditions_optionmenu2.grid_remove()
        self.weather_conditions_optionmenu3.set("")
        self.weather_conditions_optionmenu3.grid_remove()
        self.cloud_form_optionmenu2.grid_remove()
        self.cloud_form_optionmenu3.grid_remove()
        self.quantity_clouds_optionmenu.set("0")
        self.total_clouds_optionmenu.set("0")
        self.cloud_form_optionmenu.set("Облачность отсутствует")
        self.cloud_form_optionmenu2.set("")
        self.cloud_form_optionmenu3.set("")
        ######
        ######

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(
            fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(
            fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(
            fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")
        self.frame_about_button.configure(
            fg_color=("gray75", "gray25") if name == "frame_about" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()
        if name == "frame_about":
            self.about_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.about_frame.grid_forget()


    def data_to_excel_period(self):
        data_to_excel_period(self.for_excel_from_date_picker.get_date(),
                             self.for_excel_to_date_picker.get_date())

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

    def frame_about_button_event(self):
        self.select_frame_by_name("frame_about")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    #####################################
    #####################################
    #####################################
    def update_humid(self, *args):
        """RH = (e / e_s) * 100 где:
            e = (6.11 * 10^((7.5 * Td) / (237.7 + Td))) * (10^(2) / (T + 273.15)) - абсолютная влажность воздуха
            e_s = (6.11 * 10^((7.5 * T) / (237.7 + T))) * (10^(2) / (T + 273.15)) - абсолютная влажность воздуха при сухом воздухе
            RH - относительная влажность воздуха в процентах
            """

        T = float(self.temperature_entry.get())
        Td = float(self.dew_point_temperature_entry.get())
        e = (6.11 * 10 ** ((7.5 * Td) / (237.7 + Td))) * \
            (10 ** (2) / (T + 273.15))
        e_s = (6.11 * 10 ** ((7.5 * T) / (237.7 + T))) * \
              (10 ** (2) / (T + 273.15))
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

    def change_state_cloud2(self, event):
        if self.cloud_form_optionmenu_var.get() == "Облачность отсутствует":
            self.cloud_form_optionmenu2.set("")
            self.cloud_form_optionmenu2.grid_remove()
            self.cloud_form_optionmenu3.set("")
            self.cloud_form_optionmenu3.grid_remove()
        elif self.cloud_form_optionmenu_var.get() != "Облачность отсутствует":
            self.cloud_form_optionmenu2.grid()

    def change_state_cloud3(self, event):
        print('1', self.cloud_form_optionmenu_var.get(), '2', self.cloud_form_optionmenu2_var.get(),
              self.cloud_form_optionmenu3_var.get())
        if self.cloud_form_optionmenu2_var.get() == "Облачность отсутствует":
            self.cloud_form_optionmenu2.set("")
            self.cloud_form_optionmenu2.grid_remove()
            self.cloud_form_optionmenu3.set("")
            self.cloud_form_optionmenu3.grid_remove()

        elif self.cloud_form_optionmenu2_var.get() != "Облачность отсутствует":
            print(self.cloud_form_optionmenu2_var.get())
            self.cloud_form_optionmenu3.grid()

        if self.cloud_form_optionmenu3_var.get() == "Облачность отсутствует":
            self.cloud_form_optionmenu3.set("")
            self.cloud_form_optionmenu3.grid_remove()

    def update_clock(self):
        current_time = time.strftime("%H:%M:%S")
        current_time_utc = datetime.utcnow().time().strftime("UTC %H:%M")
        current_date = time.strftime("%Y-%m-%d")
        current_date_utc = datetime.utcnow().date()
        self.time_label.configure(text=current_time_utc)
        # self.local_time_label.configure(text=current_time)
        # self.local_date_label.configure(text=current_date)
        self.date_label.configure(text=current_date_utc)
        self.after(1000, self.update_clock)

    def set_report_time(self):
        if self.set_report_time_button_var.get() == "1 час":
            return 0
        elif self.set_report_time_button_var.get() == "30 минут":
            return 1
        elif self.set_report_time_button_var.get() == "Фактическое":
            return 2

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
        datetime_utc = str(datetime.utcnow().strftime("%d/%m/%Y %H:%M"))
        set_report_time = self.set_report_time_button_var.get()
        local_datetime = str(time.strftime("%Y/%m/%d %H:%M:%S"))
        dt_metar, date_utc, time_utc = date_time_cod(datetime_utc, set_report_time)
        local_date_for_db, local_time_for_db = local_date_time_cod(local_datetime, set_report_time)

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
        self.metar_output.configure(text=metar_all)  # #
        print(self.metar_output.cget('text'))
        if self.metar_output.cget('text') != 'Укажи атмосферное явление!':
            self.db_insert(date_utc, time_utc, local_date_for_db, local_time_for_db)
            print('dt_metar', dt_metar)
            print('date_utc', date_utc)
            print('time_utc', time_utc)

    def send_email(self):
        data = self.metar_output.cget('text')
        if self.checkbox_1.get() == 1:
            data += ' ' + self.comments.get() + ' -'
        else:
            data += ' -'
        recipient = ['pogoda10@sakhugms.ru']
        cc = ['METAR']
        bcc = []
        subject = 'METAR'
        recipient_string = ";".join(recipient)
        cc_string = ";".join(cc)
        bcc_string = ";".join(bcc)
        webbrowser.open(
            'mailto:' + recipient_string +
            '?cc=' + cc_string +
            '&subject=' + subject +
            '&body=' + data)

    def check_user_name(self):
        import socket
        user_name = ['petrp1', 'valery.sukhoruchkin', 'dmitry.koryagin']
        comp_name = ['Mybook', 'YUZCHE-D-99672']
        if os.getlogin() in user_name or socket.gethostname() in comp_name:
            self.click_metar()
        else:
            metar_data = 'На работу в Гидрометеоцентр требуется метеоролог. ' \
                         'Зарплата 15 тыс. рублей, ощущается как 45 тыс.'
            self.metar_output.configure(text=metar_data)

    def db_insert(self, date_utc, time_utc, local_date_for_db, local_time_for_db):
        wind_direction = int(wind_direction_cod(self.wind_dir_entry.get()))
        wind_speed = wind_speed_cod(self.wind_entry.get())
        wind_gust = wind_gust_cod(self.windgust_entry.get())
        visibility = self.visibility_entry.get()
        weather_condition = weather_conditions_cod([self.weather_conditions_optionmenu.get(),
                                                    self.weather_conditions_optionmenu2.get(),
                                                    self.weather_conditions_optionmenu3.get()])
        temperature = self.temperature_entry.get()
        dew_point = self.dew_point_temperature_entry.get()
        humidity = self.humidity_entry.get()
        qt_clouds = self.total_clouds_optionmenu.get()
        qt_lower_clouds = self.quantity_clouds_optionmenu.get()
        cloud_base = self.cloud_base_lower_entry.get()
        clouds_type_cod = clouds_form(self.cloud_form_optionmenu.get(),
                                      self.cloud_form_optionmenu2.get(),
                                      self.cloud_form_optionmenu3.get())
        pressure_heli = self.pressure_helideck_entry.get()
        pressure_sea_level = self.pressure_sea_level_entry.get()
        wave = self.wave_height_entry.get()
        comments = self.comments.get()
        metar_cod_cod = self.metar_output.cget('text')

        insert_data(local_date_for_db, local_time_for_db, date_utc, time_utc, wind_direction, wind_speed, wind_gust,
                    visibility, weather_condition, temperature, dew_point, humidity, qt_clouds, qt_lower_clouds,
                    cloud_base, clouds_type_cod, pressure_heli, pressure_sea_level, wave, comments, metar_cod_cod)

    def history_table(self):
        data = select_from_db(self.history_from_date_picker.get_date(),
                              self.history_to_date_picker.get_date())

        for i in self.tree.get_children():
            self.tree.delete(i)

        for row in data:
            print(row)
            self.tree.insert("", 'end', values=row)



if __name__ == "__main__":
    app = App()
    app.mainloop()
