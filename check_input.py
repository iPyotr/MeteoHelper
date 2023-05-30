
def wind_direction_check(data):
    if str(data).isnumeric() and 0 <= int(data) <= 360:
        return 1
    else:
        return 'Направление ветра: Только цифры!(от 0 до 360)'
def wind_speed_check(data):
    if str(data).isnumeric():
        return 1
    else:
        return 'Скорость ветра: Только цифры!'
def wind_gust_check(data):
    if str(data).isnumeric():
        return 1
    else:
        return 'Порыв ветра: Только цифры!'
def visibility_check(data):
    if str(data).isnumeric():
        return 1
    else:
        return 'Горизонтальная видимость: Только цифры!'
def temperature_check(data):
    if check_num_dot_minus(data) == 1:
        return 1
    else:
        return 'Температура воздуха: Цифры и разделитель " . "!'
def dew_point_check(data):
    if check_num_dot_minus(data) == 1:
        return 1
    else:
        return 'Точка росы: Цифры и разделитель " . "!'
def humidity_check(data):
    if str(data).isnumeric():
        return 1
    else:
        return 'Влажность воздуха: Только цифры!'
def cloud_base_check(data):
    if str(data).isnumeric():
        return 1
    else:
        return 'Нижняя граница облачности: Только цифры!'
def pressure_heli_check(data):
    if check_num_and_dot(data) == 1:
        return 1
    else:
        return 'Давление на уровне вертолётки: Цифры и разделитель " . "!'
def pressure_sea_level_check(data):
    if check_num_and_dot(data) == 1:
        return 1
    else:
        return 'Давление на уровне моря: Цифры и разделитель " . "!'
def wave_check(data):
    if str(data).isnumeric():
        return 1
    else:
        return 'Высота волны: Только цифры!'


def check_num_and_dot(data):
    ls = '1234567890.'
    for i in data:
        if i not in ls:
            return 0
    return 1

def check_num_dot_minus(data):
    ls = '1234567890.-'
    for i in data:
        if i not in ls:
            return 0
    return 1