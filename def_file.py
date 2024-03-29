from datetime import datetime, timedelta

clouds_type = ['Облачность отсутствует',
               'Сi перистые',
               'Cc перисто-кучевые',
               'Cs перисто-слоистые',
               'Ac высококучевые',
               'As высокослоистые',
               'Sc слоисто-кучевые',
               'St слоистые',
               'Ns слоисто-дождевые',
               'Cu кучевые',
               'Cb кучево-дождевые',
               'Frnb разорванно-дождевые',
               'VV вертикальная видимость'
               ]

clouds_type_dictionary = {"Сi перистые": "Сi",
                          "Cc перисто-кучевые": "Cc",
                          "Cs перисто-слоистые": "Cs",
                          "Ac высококучевые": "Ac",
                          "As высокослоистые": "As",
                          "Sc слоисто-кучевые": "Sc",
                          "St слоистые": "St",
                          "Ns слоисто-дождевые": "Ns",
                          "Cu кучевые": "Cu",
                          "Cb кучево-дождевые": "Cb",
                          "Frnb разорванно-дождевые": "Frnb",
                          "VV вертикальная видимость": "VV",
                          '': ' '
                          }

weather_conditions_types = ['явлений не наблюдается',
                            'дымка',
                            'туман',
                            'туман в пределах 8 км',
                            'туман переохлажденный',
                            'туман просвечивающий',
                            'туман местами',
                            'поземный туман',
                            'дождь',
                            'дождь со снегом обложной',
                            'ливневый дождь',
                            'переохлажденный дождь',
                            'снег',
                            'снег с дождем обложной',
                            'ливневой снег',
                            'морось',
                            'переохлажденная морось',
                            'град',
                            'ледяная крупа',
                            'гроза',
                            'гроза с дождем',
                            'шквал'
                            ]

wc_dictionary = {'явлений не наблюдается': 'NSW',
                 'дымка': 'BR',
                 'туман': 'FG',
                 'туман в пределах 8 км': 'VCFG',
                 'поземный туман': 'MIFG',
                 'дождь': 'RA',
                 'снег': 'SN',
                 'морось': 'DZ',
                 'ливневый дождь': 'SHRA',
                 'ливневой снег': 'SHSN',
                 'туман местами': 'BCFG',
                 'град': 'GR',
                 'ледяная крупа': 'PL',
                 'переохлажденный дождь': 'FZRA',
                 'переохлажденная морось': 'FZDZ',
                 'гроза': 'TS',
                 'шквал': 'SQ',
                 'туман просвечивающий': 'PRFG',
                 'гроза с дождем': 'TSRA',
                 'туман переохлажденный': 'FZFG',
                 'снег с дождем обложной': 'SNRA',
                 'дождь со снегом обложной': 'RASN',
                 '': ' '
                 }


def date_time_cod(date_time_string, set_report_time):  # Дата и время передачи сводки
    """Дата и время передачи сводки
    Принимает значение даты и времени формирования сводки и возвращает код METAR"""
    date_time_obj = datetime.strptime(date_time_string, "%d/%m/%Y %H:%M")
    minute = date_time_obj.minute
    global date_time_for_metar, date_time_for_db, date_time_for_db
    ####
    if set_report_time == "1 час":
        if minute < 30:
            date_time_obj = date_time_obj.replace(minute=0)
        elif date_time_obj.hour == 23 and date_time_obj.minute >= 30:
            date_time_obj = date_time_obj.replace(hour=0, minute=0) + timedelta(days=1)
        else:
            date_time_obj = date_time_obj.replace(minute=0, hour=date_time_obj.hour + 1)

        date_time_for_metar = date_time_obj.strftime("%d%H%M")
        date_for_db = date_time_obj.strftime("%Y-%m-%d")
        time_for_db = date_time_obj.strftime("%H:%M")
        return date_time_for_metar, date_for_db, time_for_db

    elif set_report_time == "30 минут":
        if 15 <= minute <= 44:
            date_time_obj = date_time_obj.replace(minute=30)
        elif minute < 30:
            date_time_obj = date_time_obj.replace(minute=0)
        elif date_time_obj.hour == 23 and date_time_obj.minute > 44:
            date_time_obj = date_time_obj.replace(hour=0, minute=0) + timedelta(days=1)
        else:
            date_time_obj = date_time_obj.replace(minute=0, hour=date_time_obj.hour + 1)

        date_time_for_metar = date_time_obj.strftime("%d%H%M")
        date_for_db = date_time_obj.strftime("%Y-%m-%d")
        time_for_db = date_time_obj.strftime("%H:%M")
        return date_time_for_metar, date_for_db, time_for_db

    elif set_report_time == "Фактическое":
        date_time_for_metar = date_time_obj.strftime("%d%H%M")
        date_for_db = date_time_obj.strftime("%Y-%m-%d")
        time_for_db = date_time_obj.strftime("%H:%M")
        return date_time_for_metar, date_for_db, time_for_db


def local_date_time_cod(date_time_string, set_report_time):  # Дата и время передачи сводки
    '''Дата и время передачи сводки в формате местного времени
    Принимает значение даты и времени формирования сводки и возвращает дату и время'''

    local_date_time_obj = datetime.strptime(date_time_string, "%Y/%m/%d %H:%M:%S")
    minute = local_date_time_obj.minute
    ####
    if set_report_time == "1 час":
        if minute < 30:
            local_date_time_obj = local_date_time_obj.replace(minute=0)
        elif local_date_time_obj.hour == 23 and local_date_time_obj.minute >= 30:
            local_date_time_obj = local_date_time_obj.replace(hour=0, minute=0) + timedelta(days=1)
        else:
            local_date_time_obj = local_date_time_obj.replace(minute=0, hour=local_date_time_obj.hour + 1)

        local_date_for_db = local_date_time_obj.strftime("%Y-%m-%d")
        local_time_for_db = local_date_time_obj.strftime("%H:%M")
        return local_date_for_db, local_time_for_db

    elif set_report_time == "30 минут":
        if 15 <= minute <= 44:
            local_date_time_obj = local_date_time_obj.replace(minute=30)
        elif minute < 30:
            local_date_time_obj = local_date_time_obj.replace(minute=0)
        elif local_date_time_obj.hour == 23 and local_date_time_obj.minute > 44:
            local_date_time_obj = local_date_time_obj.replace(hour=0, minute=0) + timedelta(days=1)
        else:
            local_date_time_obj = local_date_time_obj.replace(minute=0, hour=local_date_time_obj.hour + 1)

        local_date_for_db = local_date_time_obj.strftime("%Y-%m-%d")
        local_time_for_db = local_date_time_obj.strftime("%H:%M")
        return local_date_for_db, local_time_for_db

    elif set_report_time == "Фактическое":
        local_date_for_db = local_date_time_obj.strftime("%Y-%m-%d")
        local_time_for_db = local_date_time_obj.strftime("%H:%M")
        return local_date_for_db, local_time_for_db


def metar_cod(ws, wg, wd, v, wc, ph, psl, t, dpt, h, tc, qc, cbl, cf, wh):
    wind_direction = wind_direction_cod(wd)
    wind_speed = wind_speed_cod(ws)
    wind_gust = wind_gust_cod(wg)

    if wind_speed == 0:
        wind_metar = '00000MPS'
    elif int(wg) - int(ws) < 3:
        wind_metar = f'{wind_direction}{wind_speed}MPS'
    else:
        wind_metar = f'{wind_direction}{wind_speed}G{wind_gust}MPS'

    visibility = visibility_cod(v)
    weather_conditions = weather_conditions_cod(wc)
    pressure_helideck = pressure_helideck_cod(ph)
    pressure_sea_level = pressure_sea_level_cod(psl)
    temperature = temperature_cod(t)
    dew_point_temperature = dew_point_temperature_cod(dpt)
    total_clouds = total_clouds_cod(tc)
    cloud_form = clouds_form(cf, cf, cf)
    wave_height = wave_height_cod(wh)
    rmk = f' {str(pressure_helideck)} {str(wave_height)}'
    cbl_round = str((int(cbl) // 10) * 10).zfill(3)

    if int(visibility) < 8000 and weather_conditions == 'NN':
        return 'Укажи атмосферное явление!'
    if int(cbl) < 200:
        rmk = f' QBB{cbl_round} {str(pressure_helideck)} {str(wave_height)}'
    if weather_conditions == 'NN':
        metar_data = f'{date_time_for_metar}Z ' \
                     f'{str(wind_metar)} ' \
                     f'{str(visibility)} ' \
                     f'{str(total_clouds)} ' \
                     f'{str(temperature)}/' \
                     f'{str(dew_point_temperature)} ' \
                     f'{str(pressure_sea_level)} RMK' \
                     f'{rmk}'

    else:
        metar_data = f'{date_time_for_metar}Z ' \
                     f'{str(wind_metar)} ' \
                     f'{str(visibility)} ' \
                     f'{str(weather_conditions)} ' \
                     f'{str(total_clouds)} ' \
                     f'{str(temperature)}/' \
                     f'{str(dew_point_temperature)} ' \
                     f'{str(pressure_sea_level)} RMK' \
                     f'{rmk}'

    return f'ЩЭФАП METAR UHSC {metar_data}'


def wind_speed_cod(data):  # Средняя скорость ветра (м/c)
    '''Максимальный порыв ветра (м/с)
    Принимает значение скорости ветра в м/с и возвращает код METAR'''
    data = int(data)
    if 1 <= data < 10:
        return str(data).zfill(2)
    elif data < 1:
        return 0
    else:
        return str(data)


def wind_gust_cod(data):  # Максимальный порыв ветра (м/с)
    '''Средняя скорость ветра (м/c)
    Принимает значение максимальной скорости ветра в м/с и возвращает код METAR'''
    data = int(data)
    if data == 0:
        return ''
    else:
        return str(data).zfill(2)


def wind_direction_cod(n):  # Направление ветра (град)
    '''Направление ветра (град)
    Принимает значение направления ветра в градусах(кратное 10) и возвращает код METAR'''
    n = round(int(n), -1)
    if n > 360:
        n = 360
    elif n < 0:
        n = 0
    return "{:03d}".format(n)


def visibility_cod(data):  # Горизонтальная видимость (км)
    '''Горизонтальная видимость (км)
    Принимает значение видимости в километрах и возвращает код METAR
    менее 800 указывается кратно 50
    от 800 до 5000 кратно 100
    от 5000 до 9999 кратно 1000
    от 10000 значение равно 9999
    '''
    x = int(data)
    if x < 800:
        return str((x // 50) * 50).zfill(4)
    elif x < 5000:
        return str((x // 100) * 100).zfill(4)
    elif x < 10000:
        return (x // 1000) * 1000
    else:
        return 9999


def weather_conditions_cod(wc1):  # Атмосферное явление. Может принимать несколько явлений
    '''Атмосферное явление
    Принимает значение погодных явлений(может быть указано несколько явлений) и возвращает код METAR'''
    wc_all = wc_dictionary[wc1[0]]
    if wc1[0] == 'явлений не наблюдается':
        return 'NN'
    elif len(wc1) > 1:
        for i in range(1, len(wc1)):
            wc_all += " " + wc_dictionary[wc1[i]]
    return wc_all.strip()


def pressure_helideck_cod(data):  # Давление на уровне вертолетной площадки (мм.рт.ст.)
    '''Давление на уровне вертолетной площадки (мм.рт.ст.) фактическое значение
    Принимает значение атмосферного давления в мм.р.ст.(фактическое значение) на уровне вертолётной площадки и возвращает код METAR'''

    return 'QFE' + str(int(float(data)))


def pressure_sea_level_cod(data):  # Давление на уровне моря(гПа)
    '''Давление на уровне моря(гПа)
    Принимает значение атмосферного давления в гПа на уровне моря и возвращает код METAR'''
    return 'Q' + str(int(float(data))).zfill(4)


def temperature_cod(data):  # Температура воздуха(град)
    '''Температура воздуха(град)
    Принимает значение температуры воздуха в градусах и возвращает код METAR'''
    num = float(data)
    if int(str(num)[-1]) == 5:
        num += 0.1
    n = round(num)
    if n < 0:
        n = abs(n)
        n = "M" + str(n).zfill(2)
    else:
        n = str(n).zfill(2)
    return n


def dew_point_temperature_cod(data):  # Температура точки росы(град)
    '''Температура точки росы(град)
    Принимает значение температуры точки росы в градусах и возвращает код METAR'''
    num = float(data)
    if int(str(num)[-1]) == 5:
        num += 0.1
    n = round(num)
    if n < 0:
        n = abs(n)
        n = "M" + str(n).zfill(2)
    else:
        n = str(n).zfill(2)
    return n


def humidity_cod(data):  # Влажность воздуха (%)
    '''Влажность воздуха (%)
    e=E-A(t-t_1)P,
    где E — давление насыщения при температуре смоченного термометра,
    A — постоянная психрометра, принимаемая равной 0.0007947,
    P — атмосферное давление, принимается равным 1000 гПа
    t — показания сухого термометра
    t_1 — показания смоченного термометра
    '''
    pass


def total_clouds_cod(data):  # Общее количество облачности в сводку метар
    '''Общее количество облачности (октанты)
    Принимает значение количества облачности в октантах
    количество нижнего яруса в октантах
    горизонтальную видимость в метрах
    высоту нижней границы облачности в метрах
    и возвращает код METAR'''
    visibility_h = int(data[0])
    qt_clouds = int(data[1])
    qt_lower = int(data[2])
    ngo = int(data[3])

    if ngo > 1500:
        return 'NSC'
    elif visibility_h < 1000:
        return 'VV' + str(ngo // 30).zfill(3)
    elif visibility_h >= 1000 and qt_lower < 3:
        return 'FEW' + str(ngo // 30).zfill(3)
    elif visibility_h >= 1000 and 3 <= qt_lower <= 4:
        return 'SCT' + str(ngo // 30).zfill(3)
    elif visibility_h >= 1000 and 5 <= qt_lower <= 7:
        return 'BKN' + str(ngo // 30).zfill(3)
    elif visibility_h >= 1000 and qt_lower == 8:
        return 'OVC' + str(ngo // 30).zfill(3)


def quantity_clouds_cod(data):  # Количество нижнего яруса (октанты)
    '''Количество нижнего яруса (октанты)
    Принимает значение количества нижнего яруса облачности в октантах и возвращает код METAR'''
    pass


def cloud_base_lower_cod(data):  # Высота НГО (м)
    ''' Высота НГО (м)
    Принимает значение высоты облаков нижнего яруса в метрах и возвращает код METAR
    если меньше 1500 то в базу данныx идёт число кратное 10 с округлением в меньшую сторону, а в сводку идёт //30
    если более 1500, то в базу и в сводку идёт буквенный код NSC
    '''
    pass


def clouds_form(cf1, cf2, cf3):
    cf_all = []
    if cf1 == 'Облачность отсутствует':
        return 'SKC'
    else:
        cf_all = clouds_type_dictionary[cf1] + " " + clouds_type_dictionary[cf2] + " " + clouds_type_dictionary[cf3]
    return cf_all.strip()


def wave_height_cod(data):  # Высота преобладающих волн (см)
    ''' Высота преобладающих волн (см) с точностью до 1 сантиметра
    Принимает значение высоты преобладающих волн в сантиметрах и возвращает код METAR'''
    x = int(data)
    if x > 999:
        result = 999
    else:
        result = str((x // 10) * 10).zfill(3)
    return f"HSAUT{result}"
