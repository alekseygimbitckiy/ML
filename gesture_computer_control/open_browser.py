from selenium import webdriver
import requests

import Xlib.display

def open():
    try:
        url = "https://www.google.com"
        response = requests.get(url)

        response.raise_for_status()
        # создаем объект Firefox WebDriver
        driver = webdriver.Firefox()

        # открываем веб-страницу в Firefox
        driver.get("https://www.google.com")

    except (requests.exceptions.RequestException, webdriver.WebDriverException) as e:

        driver = None

        print ('No Enternet conection open')


    return driver

def activate(s):
   # получаем объект дисплея (экрана)
    display = Xlib.display.Display()

    # получаем корневое окно (рабочий стол)
    root_window = display.screen().root

    # получаем список всех дочерних окон
    children = root_window.query_tree().children

    # ищем окно с нужным заголовком
    window_title = s
    for child in children:
        window = child.get_wm_class()
        print (window[1])
        if window is not None and window[1] == window_title:

            # нашли нужное окно, активируем его
            attributes = child.get_attributes()
            if attributes.map_state == Xlib.X.IsViewable:
                child.set_input_focus(Xlib.X.RevertToParent, Xlib.X.CurrentTime)
                print ('Done')
                display.sync()
            break

def close (driver):
    # закрываем браузер
    if driver is not None:
        driver.quit()
