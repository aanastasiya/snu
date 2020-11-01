import enum


# Список термов
class Terms(enum.IntEnum):
    SLOW = 1
    MODERATE = 2
    FAST = 3


# Преобразование значения скорости авто в степень принадлежности терма лингвистической переменной "скорость"
# Скорость указана в м/с
def calculate(speed, term):
    if term == Terms.SLOW:
        if speed <= 5: return 1.0
        elif 5 < speed <= 10: return (10 - speed) / 5.0
        elif speed > 10: return 0.0
    elif term == Terms.MODERATE:
        if speed >= 17: return 0.0
        elif 8 < speed <= 11: return (speed - 8) / 3.0
        elif 11 < speed < 17: return (17 - speed) / 6.0
        elif speed <= 8: return 0.0
    elif term == Terms.FAST:
        if speed <= 11: return 0.0
        elif 11 < speed < 17: return (speed - 11) / 6.0
        elif speed >= 17: return 1.0
