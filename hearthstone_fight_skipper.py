# -*- coding: utf-8 -*-
import sys
import os
import time
import ctypes
import logging
from config import Config


LOG_LEVEL = logging.DEBUG
logging.basicConfig(
    filename='hearthstone_fight_skip.log',
    filemode='a',
    format='[%(asctime)s] %(levelname)s: %(filename)s(%(lineno)d): %(funcName)s: %(message)s',
    level=LOG_LEVEL,
    encoding='utf-8',
)
logger = logging.getLogger(__name__)
logger.info(' Start '.center(100, '='))



def check_is_admin() -> bool:
    """
    Проверить, запущен ли скрипт с правами администратора

    :return: Есть права администратора
    :rtype:  bool
    """
    result = ctypes.windll.shell32.IsUserAnAdmin()
    result = bool(result)
    logger.debug(f'Is admin: {result}')

    return result



def disconnect_hs() -> None:
    """
    Создать правило на блок сети у hearthstone

    :return: None
    """
    print('Отключение ...')
    logger.info('Disconnecting ...')
    command = f'netsh advfirewall firewall add rule name="{Config.RULE_NAME}" ' \
              f'dir=out action=block program="{Config.HEARTHSTONE_PATH}"'
    os.system(command)
    logger.info('Disconnected')


def connect_hs() -> None:
    """
    Удалить правило на блок сети у hearthstone

    :return: None
    """
    print('Подключение ...')
    logger.info('Connecting ...')
    command = f'netsh advfirewall firewall delete rule name="{Config.RULE_NAME}"'
    os.system(command)
    logger.info('Connected')


def reconnect() -> None:
    """
    Переподключиться к бою

    :return: None
    """
    disconnect_hs()

    print(f'Ожидаю {Config.SLEEP_TIME} сек.')
    time.sleep(Config.SLEEP_TIME)

    connect_hs()


def clear_console() -> None:
    """
    Очистить консоль

    :return: None
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def main() -> None:
    is_admin = check_is_admin()
    if not is_admin:
        ctypes.windll.shell32.ShellExecuteW(None, 'runas', sys.executable, ' '.join(sys.argv), None, 1)  # noqa
        sys.exit(0)

    while True:
        clear_console()
        menu_text = ('Press enter to reconnect hearthstone\n'
                     'Type anything press CTRL+C to exit ...\n')
        print(menu_text)
        input_text = input('>>> ')

        if not input_text:
            reconnect()
        else:
            return


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info('Keyboard interrupt')
        sys.exit(-1)
    except Exception as exception:
        logger.exception(exception)
        raise
