class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Возвращает строку сообщения."""
        return (
            f'Тип тренировки: {self.training_type};'
            f' Длительность: {round(self.duration, 3)} ч.;'
            f' Дистанция: {round(self.distance, 3)} км;'
            f' Ср. скорость: {round(self.speed, 3)} км/ч;'
            f' Потрачено ккал: {round(self.calories,3)}.'
        )


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

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
        if type(self).__name__ is Running:
            return InfoMessage(
                'Running', self.duration, self.get_distance(),
                self.get_mean_speed(), self.get_spent_calories()
            )
        elif type(self).__name__ is SportsWalking:
            return InfoMessage(
                'SportsWalking', self.duration, self.get_distance(),
                self.get_mean_speed(), self.get_spent_calories()
            )
        elif type(self).__name__ is Swimming:
            return InfoMessage(
                'Swimming', self.duration, self.get_distance(),
                self.get_mean_speed(), self.get_spent_calories()
            )


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calor_1 = 18
        coeff_calor_2 = 20
        coeff_m_in_hr = 60

        return (
            (coeff_calor_1
             * self.get_mean_speed()
             - coeff_calor_2)
            * self.weight
            / self.M_IN_KM
            * self.duration
            * coeff_m_in_hr
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_cal_1 = 0.035
        coeff_cal_2 = 0.029
        coeff_m_in_hr = 60

        return (
            (coeff_cal_1
             * self.weight
             + (self.get_mean_speed()**2
                // self.height)
             * coeff_cal_2
             * self.weight)
            * self.duration
            * coeff_m_in_hr
        )


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return (
            self.length_pool
            * self.count_pool
            / self.M_IN_KM
            / self.duration
        )

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_cal_1 = 1.1
        coeff_cal_2 = 2

        return (
            (self.get_mean_speed()
             + coeff_cal_1)
            * coeff_cal_2
            * self.weight
        )


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    trainings = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    if workout_type == trainings.get('SWM'):
        return trainings['SWM'](*data)

    elif workout_type == trainings.get('RUN'):
        return trainings['RUN'](*data)

    elif workout_type == trainings.get('WLK'):
        return trainings['WLK'](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = Training.show_training_info(training)
    return info.get_message()


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
