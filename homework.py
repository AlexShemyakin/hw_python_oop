class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type: str, duration: float,
                 distance: float, speed: float, calories: float):
        self.duration = duration
        self.training_type = training_type
        self.speed = speed
        self.calories = calories
        self.distance = distance

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    M_IN_KM = 1000
    LEN_STEP = 0.65
    H_IN_M = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        training_type = self.__class__.__name__
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        return InfoMessage(training_type, self.duration, distance,
                           speed, calories)


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def __init__(self, action, duration, weight):
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM * self.duration * self.H_IN_M)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    H_IN_M = 60.0
    COEF_WEIGHT_1 = 0.035
    COEF_WEIGHT_2 = 0.029
    KM_H_IN_M_S = 0.278
    SM_IN_M = 100

    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.height: float = height

    def get_spent_calories(self) -> float:
        return ((self.COEF_WEIGHT_1 * self.weight
                + (((self.get_mean_speed() * self.KM_H_IN_M_S) ** 2)
                 / (self.height / self.SM_IN_M)) * self.COEF_WEIGHT_2
                * self.weight) * (self.duration * self.H_IN_M))


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    COEF_SPEED_1 = 1.1
    COEF_SPEED_2 = 2

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.COEF_SPEED_1)
                * self.COEF_SPEED_2 * self.weight * self.duration)

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    codes: dict() = {'SWM': Swimming,
                     'RUN': Running,
                     'WLK': SportsWalking}
    for key in codes.keys():
        if workout_type == key and key == 'SWM':
            return codes[workout_type](data[0], data[1], data[2], data[3],
                                       data[4])
        if workout_type == key and key == 'RUN':
            return codes[workout_type](data[0], data[1], data[2])
        if workout_type == key and key == 'WLK':
            return codes[workout_type](data[0], data[1], data[2], data[3])


def main(training: Training) -> None:
    """Главная функция."""

    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
