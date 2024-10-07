# Для работы с запросами
from http.client import responses
from threading import TIMEOUT_MAX

import requests
# Для работы с файлами
import os
# Строка from dotenv import load_dotenv используется
# для импорта функции load_dotenv из библиотеки python-dotenv.
# Эта библиотека позволяет загружать переменные окружения
# из файла .envlesson1 в среду выполнения Python.
from dotenv import load_dotenv
from core.settings.environments import Environment
import allure
from core.clients.endpoints import Endpoints
from core.settings.configgit  import Users, Timeouts

load_dotenv()

class APIClient:
    # Инициализация переменных для кода
    def __init__(self):
        # В переменную environment_str кладем значение переменной ENVIRONMENT
        # Значение переменной ENVIRONMENT берется из настроек:
        # Edit Configurations ->Edit Configurations Templates
        environment_str = os.getenv('ENVIRONMENT')
        try:
            # Из класса Environment по ключу, у нас ключ равен TEST
            # вытащить значение test
            environment = Environment[environment_str]
        except KeyError:
            # Если мы не нашли такого ключа, ТО пишем сообщение + название ключа
            raise ValueError(f"Unsupported environment value: {environment_str}")
        self.base_url = self.get_base_url(environment)
        # Чтобы сохранять сессию,пока выполняются запросы
        self.session = requests.Session()
        self.session.headers = {
            'Content-Type': 'application/json'
        }

    # В функции вытаскиваются значения из файла .envlesson1
    # С помощью записи: -> str говорим о том,что тип возращаемого значения - строка
    def get_base_url(self, environment: Environment) -> str:
        if environment == Environment.TEST:
            return os.getenv('TEST_BASE_URL')
        elif environment == Environment.PROD:
            return os.getenv('PROD_BASE_URL')
        else:
            raise ValueError(f"Unsupported environment: {environment}")

    # Метод GET - Не используется
    # Теперь вместо response будем обращаться к ApiClient
    def get(self, endpoint, params=None, status_code=200):
        # base_url берется из init,
        # endpoint мы передаем
        url = self.base_url + endpoint
        # Формируем запрос из url,headers,params
        response = requests.get(url, headers=self.headers, params=params)
        if status_code:
            assert response.status_code == status_code
        return response.json()

    # Метод POST - Не используется
    # Теперь вместо response будем обращаться к ApiClient
    def post(self, endpoint, data=None, status_code=200):
        # base_url берется из init,
        # endpoint мы передаем
        url = self.base_url + endpoint
        # Формируем запрос из url,headers,params
        response = requests.post(url, headers=self.headers, params=data)
        if status_code:
            assert response.status_code == status_code
        return response.json()

    # Метод на проверку работоспособности API - Health Check
    def ping(self):
        with allure.step('Ping api client'):
            # Собираем запрос
            url = f"{self.base_url}{Endpoints.PING_ENDPOINT}"
            # Отправляем собранный запрос в текущей сессии
            response = self.session.get(url)
            # Проверяем, что нет HTTP-ошибки
            response.raise_for_status()
        with allure.step('Assert status code'):
            assert response.status_code == 201, f'Expected status 201 but got {response.status_code}'
        return response.status_code

    # Метод аутентификации пользователя
    def auth(self):
        with allure.step('Getting autheticate'):
            # Собираем адрес url
            url = f"{self.base_url}{AUTH_ENDPOINT}"
            # Собираем тело для post-запроса
            payload = {"username": Users.USERNAME, "password": Users.PASSWORD}
            #Посылаем запрос с и ждем выполнения 5 сек
            response = self.session.post(url, json=payload, timeout=Timeouts.TIMEOUT)
            #Проверяем что в ответе нет HTTP-ошибки
            response.raise_for_status()
        with allure.step('Ckecking status code'):
            assert response.status_code == 200, f'Expected status 200 but got {response.status_code}'
        # Получить из ответа значение поля с названием - token
        #Можно пллучить значение и через квадратные скобки, как в проекте-1
        token = response.json().get('token')
        with allure.step('Updating header with authorization'):
            #Добавляем заголовок в сессию
            self.session.headers.update({"Authorization": f"Bearer {token}"})

    # Метод получения брони по ID пользователя
    def get_booking_by_id(self, booking_id):
        with allure.step(f'Getting booking by ID: {Users.BOOKING_ID}'):
            # Собираем адрес url
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT}/{booking_id}"
            # Посылаем GET-запрос и ждем выполнения 5 сек
            response = self.session.get(url, timeout=Timeouts.TIMEOUT)
            # Проверяем, что в ответе нет HTTP-ошибки
            response.raise_for_status()

        with allure.step('Checking status code'):
            assert response.status_code == 200, f'Expected status 200 but got {response.status_code}'

        # Возвращаем данные о бронировании
        return response.json()