from time import sleep
from typing import Iterable

import mouse

from utilities.types import Point


class MacrosModel:
    """
    Макрос - набор точек с параметром задержки перехода и методом обхода этих точек
    """

    def __init__(self, *points: Point, name: str = "Новый макрос", point_delay: int = 1000, repetitions: int = 1):
        self.name = name
        self.points = []
        for point in points:
            self.points.append(point)
        self._is_running: bool = False
        self._point_delay = point_delay
        self._repetitions = repetitions

    @property
    def point_delay(self):
        return self._point_delay

    @point_delay.setter
    def point_delay(self, value: int):
        if value < 0:
            # TODO: сделать валидатор, чтобы не повторять код или юзать pydantic
            raise ValueError(
                "Длительность перемещения не может быть меньше 0")
        self._point_delay = value

    @property
    def repetitions(self):
        return self._repetitions

    @repetitions.setter
    def repetitions(self, value: int):
        if value < 1:
            # TODO: сделать валидатор, чтобы не повторять код или юзать pydantic
            raise ValueError("Количество повторений не может быть меньше 1")
        self._repetitions = value

    def run(self) -> None:
        """
        Запускает макрос.
        :return: None
        :rtype: None
        """
        self._is_running = True

        for point in self._get_point_sequence():
            if not self._is_running:
                break
            self._move_mouse_to_point_and_click(point=point)
            sleep(self._point_delay / 1000)

    def stop(self):
        """
        Останавливает макрос
        :return: None
        :rtype: None
        """
        self._is_running = False

    def _get_point_sequence(self) -> Iterable:
        """
        Возвращает последовательность точек
        :return: Generator
        :rtype: Iterable
        """
        for _ in range(0, self._repetitions):
            for point in self.points:
                yield point

    @staticmethod
    def _move_mouse_to_point_and_click(point: Point) -> None:
        """
        Передвигает указатель мыши в точку point и кликает ЛКМ
        :param point: точка на экране
        :type point: Point
        :return: None
        :rtype: None
        """
        mouse.move(point.x, point.y, absolute=True)
        print(f'moved {point=}')  # TODO: Заменить на логгер, если это вообще нужно...
        mouse.click()


_macros_list: list[MacrosModel] = []

if __name__ == "__main__":
    my_points = [
        Point(x=100, y=200),
        Point(x=100, y=300),
        Point(x=100, y=400),
    ]
    MacrosModel(
        *my_points,
        point_delay=2000,
        repetitions=5
    ).run()
