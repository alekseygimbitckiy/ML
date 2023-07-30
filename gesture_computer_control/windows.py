from selenium import webdriver
import requests
import subprocess
import time

class Window:

    def __init__(self, proc = None, path = None):
        self.proc = proc
        self.path = path

    def open(self):
        try:
            if self.proc is None:
                self.proc = subprocess.Popen(self.path)
               # print (proc.pid)
                #time.sleep(1)

        except:
            # time.sleep(1)
            print ('cant open ' + self.path)
            self.close()
            #self.proc = None


        return self.proc
#
    def close (self):
        try:
            if self.proc is not None:
                print (self.proc.pid)
                self.proc.send_signal(signal.SIGTERM)
                self.proc.terminate()
                #time.sleep(1)
                self.proc = None
        except:
            self.proc.kill()
            print ('cant close corectly ' + self.path)
            #time.sleep(1)
            self.proc = None


# class Browser(Windows):
#
#     def __init__ (self, driver, name = 'browser'):
#         self.driver  driver
#         self.name = name
#
#
#
# class Telegram(Windows):
#
#     def __init__ (self, driver, name = 'browser'):
#         self.driver  driver
#         self.name = name
#
#
#     def open():
#     try:
#         url = "https://www.google.com"
#         response = requests.get(url)
#
#         response.raise_for_status()
#         # создаем объект Firefox WebDriver
#         driver = webdriver.Firefox()
#
#         # открываем веб-страницу в Firefox
#         driver.get("https://www.google.com")
#
#     except (requests.exceptions.RequestException, webdriver.WebDriverException) as e:
#
#         driver = None
#
#         print ('cant open ' + name)

# import subprocess
# import time
#
# # запускаем процесс
# process = subprocess.Popen(["firefox"])
# time.sleep(1)
# # переключаемся на окно
# subprocess.call(["xdotool", "search", "--onlyvisible", "--class", "firefox", "windowactivate"])
# print ("done")


