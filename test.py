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

# <--- ДОБАВЛЕНА НОВАЯ ФУНКЦИЯ (ВЕСЬ БЛОК НИЖЕ) --->
def wait_for_file(file_path, timeout=30):
    """Ожидает появления файла"""
    start_time = time.time()
    while not os.path.exists(file_path):
        time.sleep(0.5)
        if time.time() - start_time > timeout:
            raise FileNotFoundError(f"Файл {file_path} не найден за {timeout} секунд")
    return file_path
# <--- КОНЕЦ ДОБАВЛЕННОЙ ФУНКЦИИ --->

@pytest.fixture()
def driver():
    options = Options()
    options.add_argument('start-maximized')

    download_dir = os.path.abspath("./downloads") # Создаем папку для загрузок, если её нет
    os.makedirs(download_dir, exist_ok=True)

    prefs = {
            "download.default_directory": download_dir,  # Указываем нашу папку
            "download.prompt_for_download": False,      # Отключаем диалог "Сохранить как..."
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True                # Отключаем защиту от опасных файлов
        }
    options.add_experimental_option("prefs", prefs)

    driver: WebDriver = webdriver.Chrome(options=options)
    yield driver



def test_export(driver):
    driver.get('https://fix-online.sbis.ru/')

    login = driver.find_element(By.XPATH, '//*[@data-qa="controls-Render__field"]/input')
    login.send_keys('Карета')
    login.send_keys(Keys.ENTER)

    password = driver.find_element(By.XPATH, '//*[@data-qa="controls-Render__field"]/*[@type="password"]')
    password.send_keys('Карета123')

    btn_sign_in = driver.find_element(By.XPATH, '//*[@data-qa="auth-AdaptiveLoginForm__signInButton"]')
    btn_sign_in.click()


    wait = WebDriverWait(driver, 10)

    btn_skip = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@data-qa="auth-AddConfirmContact__skipButton"]')))
    btn_skip.click()

    wait.until(EC.url_to_be('https://fix-online.sbis.ru/'))

    driver.get('https://fix-online.sbis.ru/page/nomenclature-catalog')

    try:
        home = driver.find_element(By.XPATH, '//*[@data-qa="breadcrumbs_home"]')
        home.click()
        wait.until_not(EC.visibility_of_element_located((By.XPATH, '//*[@data-qa="breadcrumbs_home"]')))
    except NoSuchElementException:
        pass

    bread_crumbs = driver.find_elements(By.XPATH, '//*[@data-qa="path_breadcrumbs_backButton"]')
    if bread_crumbs:
        bread_crumbs[0].click()
        wait.until_not(EC.visibility_of_element_located((By.XPATH, '//*[@data-qa="path_breadcrumbs_backButton"]')))

    search = driver.find_element(By.XPATH, '//*[@data-qa="controls-Render__field"]/input')
    search.send_keys('ГС База')

    folder_in_result_search: WebElement = wait.until(EC.visibility_of_element_located(
        (By.XPATH, '//*[@data-qa="breadcrumbs_view"]')))
    folder_in_result_search.click()

    sleep(2)

    btn_pmo = driver.find_element(By.XPATH, '//*[@data-qa="toggleOperationsPanel"]')
    btn_pmo.click()

    pmo_export = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@data-qa="export"]')))
    pmo_export.click()


    export_xlsx = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@title="XLSX"]')))
    export_xlsx.click()

    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@title="Применить"]'))).click()
    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@data-qa="extControls-doubleButton__icon"]'))).click()
    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@title="Компьютер"]'))).click()

    # Формируем путь к файлу
    download_dir = os.path.abspath("./downloads")
    file_path = os.path.join(download_dir, "Каталог.xlsx")

    # Ждем, пока файл скачается (вызов добавленной функции)
    wait_for_file(file_path, timeout=30)

    # Небольшая пауза для завершения записи файла
    time.sleep(1)

    # Читаем файл
    file = pandas.read_excel(file_path)  # <--- ИЗМЕНЕНО: pandas -> pd (если импортировали как pd)
    print(file)

    if os.path.exists(download_dir):
        shutil.rmtree(download_dir, ignore_errors=True)

def test_import(driver):
    # driver.get('https://fix-online.sbis.ru/')
    #
    # login = driver.find_element(By.XPATH, '//*[@data-qa="controls-Render__field"]/input')
    # login.send_keys('Карета')
    # login.send_keys(Keys.ENTER)
    #
    # password = driver.find_element(By.XPATH, '//*[@data-qa="controls-Render__field"]/*[@type="password"]')
    # password.send_keys('Карета123')
    #
    # btn_sign_in = driver.find_element(By.XPATH, '//*[@data-qa="auth-AdaptiveLoginForm__signInButton"]')
    # btn_sign_in.click()
    #
    # wait = WebDriverWait(driver, 10)
    #
    # btn_skip = wait.until(
    #     EC.visibility_of_element_located((By.XPATH, '//*[@data-qa="auth-AddConfirmContact__skipButton"]')))
    # btn_skip.click()
    #
    # wait.until(EC.url_to_be('https://fix-online.sbis.ru/'))
    #
    # driver.get('https://fix-online.sbis.ru/page/nomenclature-catalog')
    #
    # try:
    #     home = driver.find_element(By.XPATH, '//*[@data-qa="breadcrumbs_home"]')
    #     home.click()
    #     wait.until_not(EC.visibility_of_element_located((By.XPATH, '//*[@data-qa="breadcrumbs_home"]')))
    # except NoSuchElementException:
    #     pass
    #
    # bread_crumbs = driver.find_elements(By.XPATH, '//*[@data-qa="path_breadcrumbs_backButton"]')
    # if bread_crumbs:
    #     bread_crumbs[0].click()
    #     wait.until_not(EC.visibility_of_element_located((By.XPATH, '//*[@data-qa="path_breadcrumbs_backButton"]')))

    