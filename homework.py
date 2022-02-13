from dataclasses import dataclass, field


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        message = (f'Тип тренировки: {self.training_type}; '
                   f'Длительность: {self.duration:.3f} ч.; '
                   f'Дистанция: {self.distance:.3f} км; '
                   f'Ср. скорость: {self.speed:.3f} км/ч; '
                   f'Потрачено ккал: {self.calories:.3f}.')
        return message


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float

    LEN_STEP: float = field(default=0.65, init=False)  # Шаг(0.65 метра)
    M_IN_KM: int = field(default=1000, init=False)  # для перевода в километры.
    RAT_MIN: int = field(default=60, init=False)  # для перевода времени.

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info_message = InfoMessage(self.__class__.__name__,
                                   self.duration,
                                   self.get_distance(),
                                   self.get_mean_speed(),
                                   self.get_spent_calories())
        return info_message


class Running(Training):
    """Тренировка: бег."""
    CAL_1: int = 18
    CAL_2: int = 20

    def get_spent_calories(self) -> float:
        """рассчитывает количество затраченных калорий."""
        minute = self.duration * self.RAT_MIN
        speed_cal = (self.CAL_1 * self.get_mean_speed() - self.CAL_2)
        run_calories = speed_cal * self.weight / self.M_IN_KM * minute
        return run_calories


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: any
    COF_1: float = field(default=0.035, init=False)
    COF_2: float = field(default=0.029, init=False)

    def get_spent_calories(self) -> float:
        minute = self.duration * self.RAT_MIN
        speed = (self.get_mean_speed() ** 2 // self.height)
        cof_weight = self.COF_1 * self.weight
        cal_walk = (cof_weight + speed * self.COF_2 * self.weight) * minute
        return cal_walk


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    length_pool: any
    count_pool: any

    LEN_STEP: float = field(default=1.38, init=False)
    CP_1: float = field(default=1.1, init=False)
    CP_2: int = field(default=2, init=False)

    def get_mean_speed(self) -> float:
        pool = self.length_pool * self.count_pool
        mean_speed_pool = pool / self.M_IN_KM / self.duration
        return mean_speed_pool

    def get_spent_calories(self) -> float:
        calorie = (self.get_mean_speed() + self.CP_1)
        calories_pool = calorie * self.CP_2 * self.weight
        return calories_pool


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    packages = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking}
    if workout_type in packages:
        return packages[workout_type](*data)
    else:
        print('Ошибка')


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
