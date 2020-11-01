from math import sqrt

import speed as s
import distance as d


WEIGHT = 1200.0


# Вычисление Е(t)
def calculate_e(weight, speed):
    return (weight * (speed ** 2)) / 2.0


# Вычисление расстояния
def calculate_distance(distance, speed):
    return distance - speed


# База знаний
def calculate_brake_e(distance, speed):
    return [
        [0.0, 10.0 * speed + 25.0 * distance, 45.0 * speed + 80.0 * distance],
        [20.0 * speed + 2.0 * distance, 40.0 * speed + 16.0 * distance, 15.0 * speed + 50.0 * distance],
        [0.0, 15.0 * speed + 11.0 * distance, 22.0 * speed + 28.0 * distance]
    ]


# Нечеткий контроллер
def controller(speed, distance):
    # Фаззификация скорости
    speed_membership_function = {
        s.Terms.FAST: s.calculate(speed, s.Terms.FAST),
        s.Terms.MODERATE: s.calculate(speed, s.Terms.MODERATE),
        s.Terms.SLOW: s.calculate(speed, s.Terms.SLOW)
    }

    # Фаззификация расстояния
    distance_membership_function = {
        d.Terms.FAR: d.calculate(distance, d.Terms.FAR),
        d.Terms.CLOSE: d.calculate(distance, d.Terms.CLOSE),
        d.Terms.VERY_CLOSE: d.calculate(distance, d.Terms.VERY_CLOSE)
    }

    brake = calculate_brake_e(distance, speed)

    # Нахождение уровней отсечения для каждого правила
    cutoff_levels = []
    for fuzzy_speed in speed_membership_function.values():
        values = []
        for fuzzy_distance in distance_membership_function.values():
            values.append(min(fuzzy_speed, fuzzy_distance))
        cutoff_levels.append(values)

    # Вычисление значений выходной переменной
    sugeno = []
    for i in range(len(cutoff_levels)):
        for j in range(len(brake)):
            sugeno.append(cutoff_levels[i][j] * brake[i][j])

    # Агрегация
    cutoff_levels_sum = 0
    for l in cutoff_levels:
        cutoff_levels_sum += sum(l)
    sugeno_sum = sum(sugeno) / cutoff_levels_sum

    return 0.0 if (sugeno_sum <= 0) else sugeno_sum


if __name__ == "__main__":
    speed = 14.0
    distance = 300.0

    new_speed = speed
    new_distance = distance - speed * 1
    e = calculate_e(WEIGHT, new_speed)

    i = 1
    while True:
        brake_e = controller(new_speed, new_distance)
        new_e = calculate_e(WEIGHT, new_speed)
        print(f'Шаг {i}. Cкорость {new_speed}, расстояние - {new_distance}. '
              f'Энергия торможения - {brake_e}. Кинетическая энергия {new_e}')

        new_e_with_brake = 0.0 if (new_e - brake_e <= 0.0) else new_e - brake_e
        new_distance = calculate_distance(new_distance, new_speed)
        new_speed = 0.0 if (sqrt((2.0 * new_e_with_brake) / WEIGHT) <= 0.0) else sqrt((2.0 * new_e_with_brake) / WEIGHT)

        if new_distance <= 0.0:
            print(f'Произошло столкновение. Скорость - {new_speed}, расстояние - {new_distance}')
            break
        elif new_speed <= 0.0:
            print(f'Произошла остановка. Скорость - {new_speed}, расстояние - {new_distance}')
            break

        i += 1

