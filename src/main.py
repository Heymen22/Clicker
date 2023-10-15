__author__ = 'Randy Marsh'


import logging

from packaging.version import Version

import config
from ui.mainwindow import Window
from utilities.update import is_new_version_available


def main() -> None:
    app = Window()
    app.mainloop()



if __name__ == "__main__":
    logging.basicConfig(filename=config.LOG_PATH / 'main.log', encoding='UTF-8', level=logging.DEBUG)

    print("Доступна новая версия" if is_new_version_available(Version(version=config.VERSION)) else "Версия актуальна")
    main()
