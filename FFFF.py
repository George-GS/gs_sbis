import os
import shutil
import csv
import pytest

import pandas

from selenium import webdriver

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import NoSuchElementException

from time import sleep
import time

import pyautogui
import pyperclip
import pygetwindow as gw

options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

driver = webdriver.Chrome(options=options)

wait = WebDriverWait(driver, 10)

# btn_pmo = driver.find_element(By.XPATH, '//*[@data-qa="toggleOperationsPanel"]')
# btn_pmo.click()

# pmo_import: WebElement = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@data-qa="download"]')))
# pmo_import.click()

base_path = os.path.dirname(__file__)
file_path = os.path.join(base_path, 'gs_files', 'base_import.xlsx')
imp_file: WebElement = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@title="Из файла"]')))
imp_file.click()

time.sleep(2)

# Нажимаем Tab несколько раз, чтобы "дойти" до поля ввода
pyautogui.press('tab')
time.sleep(0.3)
pyautogui.press('tab')
time.sleep(0.3)

# Теперь вставляем
pyperclip.copy(file_path)
pyautogui.hotkey('ctrl', 'v')
pyautogui.press('enter')