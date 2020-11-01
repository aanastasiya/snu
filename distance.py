import enum


# Список термов
class Terms(enum.IntEnum):
    FAR = 1
    CLOSE = 2
    VERY_CLOSE = 3


# Преобразование значения расстояния в степень принадлежности терма лингвистической переменной "расстояние"
# Расстояние указано в метрах
def calculate(distance, term):
    if term == Terms.FAR:
        if distance <= 500: return 0.0
        elif 500 < distance <= 800: return (distance - 500) / 300.0
        elif distance > 800: return 1.0
    elif term == Terms.CLOSE:
        if distance >= 700: return 0.0
        elif 300 <= distance < 700: return (700 - distance) / 400.0
        elif distance < 300: return 1.0
    elif term == Terms.VERY_CLOSE:
        if distance <= 100: return 1.0
        elif 100 < distance <= 300: return (300 - distance) / 200.0
        elif distance > 300: return 0.0
