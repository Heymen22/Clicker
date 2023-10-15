from typing import Optional, Sequence

from macros_service import _macros_list, MacrosModel
from utilities.types import MacrosType


class ControllerException(Exception):
    pass


class MacrosController:

    @staticmethod
    def get_macros(macros_id: int) -> MacrosType:
        """
        Возвращает макрос MacrosModel с идентификатором id
        :param macros_id: Идентификатор макроса
        :type macros_id: int
        :return: Макрос
        :rtype: MacrosModel
        """
        if macros_id < 0 or macros_id >= len(_macros_list):
            raise ControllerException(f'Неверный macros_id! {macros_id=}')
        macros = _macros_list[macros_id]
        return MacrosType(id=macros_id, name=macros.name, points=macros.points)

    @staticmethod
    def get_macros_list() -> Sequence[MacrosType]:

        return [MacrosType(id=macros_id, name=macros.name, points=macros.points)
                for macros_id, macros in enumerate(_macros_list)]

    @staticmethod
    def create_macros() -> None:
        _macros_list.append(MacrosModel())

    @staticmethod
    def run_macros(macros_id: int) -> None:
        """
        Запускает максрос с идентификатормо macros_id
        :param macros_id: Идентификатор макроса
        :type macros_id: int
        :return: None
        :rtype: None
        """
        if macros_id < 0 or macros_id >= len(_macros_list):
            return None
        _macros_list[macros_id].run()
