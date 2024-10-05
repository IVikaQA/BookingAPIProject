# Для работы с запросами
import requests
# Для работы с файлами
import os
# Строка from dotenv import load_dotenv используется
# для импорта функции load_dotenv из библиотеки python-dotenv.
# Эта библиотека позволяет загружать переменные окружения
# из файла .envlesson1 в среду выполнения Python.
from dotenv import load_dotenv
from core.settings.environments_lesson1 import Environment

load_dotenv()

class APIClient:
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
        self.headers = {
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

    #Метод GET
    #Теперь вместо response будем обращаться к ApiClient
    def get(self, endpoint,params=None,status_code=200):
        #base_url берется из init,
        #endpoint мы передаем
        url = self.base_url+endpoint
        #Формируем запрос из url,headers,params
        response = requests.get(url,headers=self.headers,params=params)
        if status_code:
            assert response.status_code == status_code
        return response.json()

    # Метод POST
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