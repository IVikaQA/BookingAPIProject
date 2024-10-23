from datetime import datetime, timedelta
from core.clients.api_client import APIClient
import pytest
from faker import Faker
import random


# Фикстура создания объекта классе ApiClient
@pytest.fixture(scope='session')
def api_client():
    # Создаем объект класса APIClient
    client = APIClient()
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
    #Будут созданы клиенты на русском, английском, китайском
    list_locale = ['ru_RU', 'en_US', 'zh_CN']
    faker_ru = Faker(locale='ru_RU')
    faker_en = Faker(locale='en_US')
    faker_ch = Faker(locale='zh_CN')

    # Генерация данных для клиента 1 (русский)
    firstname_ru = faker_ru.first_name()
    lastname_ru = faker_ru.last_name()
    totalprice_ru = faker_ru.random_number(digits=3, fix_len=True)
    depositpaid_ru = faker_ru.boolean()
    additionalneeds_ru = faker_ru.sentence()

    # Генерация данных для клиента 2 (китайский)
    firstname_ch = faker_ch.first_name()
    lastname_ch = faker_ch.last_name()
    totalprice_ch = faker_ch.random_number(digits=3, fix_len=True)
    depositpaid_ch = faker_ch.boolean()
    additionalneeds_ch = faker_ch.sentence()

    # Генерация данных для клиента 3 (английский)
    firstname_en = faker_en.first_name()
    lastname_en = faker_en.last_name()
    totalprice_en = faker_en.random_number(digits=3, fix_len=True)
    depositpaid_en = faker_en.boolean()
    additionalneeds_en = faker_en.sentence()

    custom_words = ["cat", "dog", "bird", "fish", "mouse", "parrot"]
    sentence_length = random.randint(1, 3)
    additionalneeds = ' '.join(random.choices(custom_words, k=sentence_length)) + '.'

    # Кладем сгенерированные данные в словарь
    data = {
        "client_1": {
            "firstname": firstname_ru,
            "lastname": lastname_ru,
            "totalprice": totalprice_ru,
            "depositpaid": depositpaid_ru,
            "bookingdates": booking_dates,
            "additionalneeds": additionalneeds,
        },
        "client_2": {
            "firstname": firstname_ch,
            "lastname": lastname_ch,
            "totalprice": totalprice_ch,
            "depositpaid": depositpaid_ch,
            "bookingdates": booking_dates,
            "additionalneeds": additionalneeds
        },
        "client_3": {
            "firstname": firstname_en,
            "lastname": lastname_en,
            "totalprice": totalprice_en,
            "depositpaid": depositpaid_en,
            "bookingdates": booking_dates,
            "additionalneeds": additionalneeds
        }
    }

    # Возвращаем этот словарь
    return data
