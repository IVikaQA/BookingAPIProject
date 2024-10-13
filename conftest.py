from datetime import datetime, timedelta
from core.clients.api_client import APIClient
import pytest
from faker import Faker
import random


# Фикстура создания объекта классе ApiClient
@pytest.fixture(scope='session')
def api_client():
    # Создаем объект класса APIClient
    client = APIClient
    # Теперь нам доступны функции класса
    client.auth()
    return client


# Фикстура генерации случайных дат: Отчет дат идет от текущей
@pytest.fixture()
def booking_dates():
    # В today кладем дату ткущего дня
    today = datetime.today()
    # Добавляем к today 10 дней - дата начала бронирования
    checkin_date = today + timedelta(days=10)
    # Добавляем к today 5 дней - дата окончания брони
    checkout_date = checkin_date + timedelta(days=5)

    return {
        "checkin": checkin_date.strftime('%Y-%m-%d'),
        "checkout": checkout_date.strftime('%Y-%m-%d')
    }


# Фикстура генерации случайных данных клиента
@pytest.fixture()
def generate_random_booking_data(booking_dates):
    # Генерация ФИО на китайском
    faker = Faker('zh_CN')
    firstname = faker.first_name()
    lastname = faker.last_name()
    # Значение переменной totalprice - это три цифры,
    # fix_len=True - это значит,что число будет иметь фиксированную длину, равную `digits`
    totalprice = faker.random_number(digits=3, fix_len=True)
    depositpaid = faker.boolean()
    # Переменная additionalneeds будет содержать слова из списка
    additionalneeds = faker.sentence()
    custom_words = ["кот", "собака", "птица", "рыба", "мышь", "попугай"]
    # Генерируем случайное предложение из кастомных слов
    # Длина предложения от 1 до 3 слов
    sentence_length = random.randint(1, 3)
    additionalneeds = ' '.join(random.choices(custom_words, k=sentence_length)) + '.'

    # Кладем сгенерированные данные в словарь
    data = {
        "firstname": firstname,
        "lastname": lastname,
        "totalprice": totalprice,
        "depositpaid": depositpaid,
        "bookingdates": booking_dates,
        "additionalneeds": additionalneeds
    }
    # Возвращаем этот словарь
    return data
