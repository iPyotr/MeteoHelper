from datetime import datetime, timedelta
import math

clouds_type = ['Кучево дождевые', 'кучевые плоские', 'слоисто-дождевые', 'разорванно-дождевые', 'слоистые',
               'слоисто-кучевые', 'высокослоистые', 'высококучевые', 'пересто-кучевые', 'перистые']

weather_conditions_types = ['явлений не наблюдается',
                            'дымка',
                            'туман',
                            'туман в пределах 8 км',
                            'поземный туман',
                            'дождь',
                            'снег',
                            'морось',
                            'ливневый дождь',
                            'ливневой снег',
                            'туман местами',
                            'град',
                            'ледяная крупа',
                            'переохлажденный дождь',
                            'переохлажденная морось',
                            'гроза',
                            'шквал',
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
                 '':' '
                 }


def date_time_cod(date_time_string):  # Дата и время передачи сводки
    '''Дата и время передачи сводки
    Принимает значение даты и времени формирования сводки и возвращает код METAR'''
    date_time_obj = datetime.strptime(date_time_string, "%d/%m/%Y %H:%M")
    minute = date_time_obj.minute
    if 15 <= minute <= 44:
        date_time_obj = date_time_obj.replace(minute=30)
    elif minute < 30:
        date_time_obj = date_time_obj.replace(minute=0)
    else:
        date_time_obj = date_time_obj.replace(minute=0, hour=date_time_obj.hour + 1)
    global date_time_for_metar
    date_time_for_metar = date_time_obj.strftime("%d%H%M")
    return date_time_for_metar


def metar_cod(ws, wg, wd, v, wc, ph, psl, t, dpt, h, tc, qc, cbl, cf, wh):
    wind_speed = wind_speed_cod(ws)
    wind_gust = wind_gust_cod(wg)
    wind_direction = wind_direction_cod(wd)
    visibility = visibility_cod(v)
    weather_conditions = weather_conditions_cod(wc)
    pressure_helideck = pressure_helideck_cod(ph)
    pressure_sea_level = pressure_sea_level_cod(psl)
    temperature = temperature_cod(t)
    dew_point_temperature = dew_point_temperature_cod(dpt)
    humidity = humidity_cod(h)
    total_clouds = total_clouds_cod(tc)
    quantity_clouds = quantity_clouds_cod(qc)
    cloud_base_lower = cloud_base_lower_cod(cbl)
    cloud_form = cloud_form_cod(cf)
    wave_height = wave_height_cod(wh)
    metar_data = f'{date_time_for_metar}Z ' \
                 f'{str(wind_direction)}' \
                 f'{str(wind_speed)}' \
                 f'G{str(wind_gust)}MPS ' \
                 f'{str(visibility)} ' \
                 f'{str(weather_conditions)} ' \
                 f'{str(temperature)}/' \
                 f'{str(dew_point_temperature)} ' \
                 f'{str(pressure_helideck)} ' \
                 f'{str(pressure_sea_level)} ' \
                 f'{str(humidity)} ' \
                 f'{str(total_clouds)} ' \
                 f'{str(quantity_clouds)} ' \
                 f'{str(cloud_base_lower)} ' \
                 f'{str(cloud_form)} ' \
                 f'{str(wave_height)}'
    return metar_data



def wind_speed_cod(data):  # Средняя скорость ветра (м/c)
    '''Максимальный порыв ветра (м/с)
    Принимает значение скорости ветра в м/с и возвращает код METAR'''
    data = int(data)
    if 0 <= data < 10:
        return '0' + str(data)
    else:
        return str(data)


def wind_gust_cod(data):  # Максимальный порыв ветра (м/с)
    '''Средняя скорость ветра (м/c)
    Принимает значение максимальной скорости ветра в м/с и возвращает код METAR'''
    data = int(data)
    if data == 0:
        return ''
    else:
        return str(data)


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
        # return '0' + str((x // 50) * 50)
        return str((x // 50) * 50).zfill(4)
    elif x < 5000:
        return (x // 100) * 100
    elif x < 10000:
        return (x // 1000) * 1000
    else:
        return 9999


def weather_conditions_cod(wc1):  # Атмосферное явление. Может принимать несколько явлений
    '''Атмосферное явление
    Принимает значение погодных явлений(может быть указано несколько явлений) и возвращает код METAR'''
    wc_all = wc_dictionary[wc1[0]]
    if len(wc1) > 1:
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
    n = int(float(data))
    if n < 0:
        n = abs(n)
        n = "M" + str(n).zfill(2)
    else:
        n = str(n).zfill(2)
    return n


def dew_point_temperature_cod(data):  # Температура точки росы(град)
    '''Температура точки росы(град)
    Принимает значение температуры точки росы в градусах и возвращает код METAR'''
    n = int(float(data))
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


def total_clouds_cod(data):  # Общее количество облачности (октанты)
    '''Общее количество облачности (октанты)
    Принимает значение количества облачности в октантах и возвращает код METAR'''
    pass


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


def cloud_form_cod(data):  # Форма облачности
    ''' Форма облачности
    Принимает значение формы облаков и возвращает код METAR'''
    cloud_forms = {'Cb': 'Кучево дождевые',
                   'Сu': 'кучевые плоские',
                   'Ns': 'слоисто-дождевые',
                   'Frnb': 'разорванно-дождевые',
                   'St': 'слоистые',
                   'Sc': 'слоисто-кучевые',
                   'As': 'высокослоистые',
                   'Ас': 'высококучевые',
                   'Cc': 'пересто-кучевые',
                   'Сi ': 'перистые'}
    pass


def wave_height_cod(data):  # Высота преобладающих волн (м)
    ''' Высота преобладающих волн (м) с точностью до 0.1 метра
    Принимает значение высоты преобладающих волн в метрах и возвращает код METAR'''
    pass
