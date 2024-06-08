import logging
import time
import keyboard
from pynput import keyboard
from web3 import Web3
from time import sleep
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



##############################################################################
###############################   БАТОН КЛИК   ###############################
##############################################################################

def click_button(driver, selector, selector_type=By.XPATH, input_value=None, max_attempts=2, wait_time=5, retry_interval=5, scroll = True):
    """
    Пытается кликнуть на элемент с заданным селектором и при необходимости ввести значение, повторяя попытки.
    :param driver: Инстанс драйвера Selenium.
    :param selector: Селектор элемента.
    :param selector_type: Тип селектора (By.XPATH, By.ID и т.д.).
    :param input_value: Значение для ввода (опционально).
    :param max_attempts: Максимальное количество попыток клика.
    :param wait_time: Время ожидания элемента.
    :param retry_interval: Интервал между попытками.
    :param scroll: Прокручивать до элемента или нет.
    """
    attempts = 0
    while attempts < max_attempts:
        try:
            # Ожидание появления элемента и убеждаемся, что он кликабельный
            element = WebDriverWait(driver, wait_time).until(
                EC.element_to_be_clickable((selector_type, selector))
            )
            # Прокрутка страницы до элемента
            if scroll == True:
                driver.execute_script("arguments[0].scrollIntoView(true);", element)
            else:
                pass
            # Имитация наведения курсора и клика
            actions = ActionChains(driver)
            actions.move_to_element(element).click().perform()
            # Ввод значения, если передан параметр input_value
            if input_value is not None:
                element.clear()
                element.send_keys(str(input_value))
            else:
                pass
            return True
        except (NoSuchElementException, TimeoutException, ElementClickInterceptedException):
            attempts += 1
            sleep(retry_interval)
    return False
