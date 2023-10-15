from tkinter import *
from tkinter.messagebox import showerror
from typing import Callable, Optional

import config
from contorllers import MacrosController, ControllerException
from utilities.types import MacrosType


class Window(Tk):
    """
    Главное окно приложения
    """

    def __init__(self):
        """
        Добавляет основную верстку окна
        """
        super().__init__()
        self.title(f"{config.APP_NAME} {config.VERSION}")
        self.geometry("500x500")

        self._tools_frame = ToolsFrame(self, borderwidth=3, relief=RIDGE, padx=5, pady=5,
                                       add_macros_callback=self._update_macros_listbox)
        self._tools_frame.pack(fill=X, padx=5, pady=5)

        self._macros_listbox = MacrosListbox(self, selectmode=MULTIPLE)
        self._macros_listbox.pack(expand=True, fill=BOTH, side=LEFT, padx=1)

        self._macros_settings_frame = MacrosSettingsFrame(self, borderwidth=3, relief=RIDGE, padx=5, pady=5)
        self._macros_settings_frame.pack(expand=True, fill=BOTH, side=RIGHT, padx=1)

        self._macros_listbox.bind("<<ListboxSelect>>", self._update_macros_settings_frame)

    def _update_macros_listbox(self) -> None:
        """
        Обновляет список макросов
        :return:
        :rtype:
        """
        self._macros_listbox.update_content()

    def _update_macros_settings_frame(self, *args, **kwargs):
        macros = self._macros_listbox.get_selected_macros()
        self._macros_settings_frame.update_content(macros)


class ToolsFrame(Frame):
    """
    Панель кнопок с инструментами
    """

    def __init__(self, *args, add_macros_callback: Callable[[], None], **kwargs):
        super().__init__(*args, **kwargs)
        self._add_macros_callback = add_macros_callback
        self._create_macros_btn = Button(self, text="Создать макрос", command=self._add_default_macros)
        self._create_macros_btn.pack(side=LEFT)

    def _add_default_macros(self) -> None:
        """
        Показывает окно создания макроса
        :return: None
        :rtype: None
        """
        MacrosController.create_macros()
        self._add_macros_callback()


class MacrosSettingsFrame(Frame):
    """
    Окно настроек выбранного макроса
    """

    # TODO: Сдлеать редактирование параметров по дополнительной кнопке, чтобы лейблы превращались в энтри, а включение и отключение макроса сделать чекбоксами и на каждое изменение вешать хендлер который дергает контроллер или как то еще реагирует на выключение макроса + нужно продумать и поебатсья с тем как будет работать горячие клавиши


    # self._start_stop_btn = Button(self, text="Старт/стоп", command=self._run_macros)
    # self._start_stop_btn.pack()

    def __init__(self, *args, macros: Optional[MacrosType] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self._macros = macros
        self._points_listbox = Listbox()

        self._name_frame = Frame(self, padx=5, pady=5)
        self._name_frame.pack(fill=X, side=LEFT)

        self._name_label = Label(self._name_frame, text='Название макроса: ')
        self._name_label.pack(side=LEFT)
        self._name_entry_stringvar = StringVar()
        self._name_entry = Entry(self._name_frame, textvariable=self._name_entry_stringvar)
        self._name_entry.pack(side=RIGHT)

        self._name_label = Label(self._name_frame, text='Название макроса: ')
        self._name_label.pack(side=LEFT)
        self._name_entry_stringvar = StringVar()
        self._name_entry = Entry(self._name_frame, textvariable=self._name_entry_stringvar)
        self._name_entry.pack(side=RIGHT)

    def _run_macros(self) -> None:
        """
        Запускает макрос
        :return:
        :rtype:
        """
        if self._macros is None:
            showerror('Ошибка', 'Не выбран ни один макрос')
            return
        MacrosController.run_macros(self._macros.id)

    def update_content(self, macros: Optional[MacrosType]):
        if macros is None:
            showerror('Ошибка', 'Не выбран ни один макрос')
            return
        self._macros = macros
        self._name_entry_stringvar.set(self._macros.name)
        print('ЕНТРАЙ ДОЛЖЕН МЕНЯТСЯ!')


class MacrosListbox(Listbox):
    """
    Список макросов
    """

    def __init__(self, *args, **kwargs):
        self._listvariable = Variable()
        super().__init__(*args, listvariable=self._listvariable, **kwargs)

    def update_content(self) -> None:
        self._listvariable.set([f"{macros.id}. {macros.name}" for macros in MacrosController.get_macros_list()])

    def get_selected_macros(self) -> Optional[MacrosType]:
        selected_range: tuple = self.curselection()
        if len(selected_range) < 1:
            return None
        macros_list_string: str = self._listvariable.get()[selected_range[0]]
        macros_id: int = int(macros_list_string.split(".")[0])
        try:
            return MacrosController.get_macros(macros_id=macros_id)
        except ControllerException as e:
            print(e)
            return None

if __name__ == "__main__":
    myWindow = Window()
    myWindow.mainloop()
