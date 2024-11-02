from http.client import responses
import allure
import pytest
from pydantic import ValidationError
from conftest import api_client
from core.models.boooking import BookingResponse
import time

@allure.feature('Test creating booking')
@allure.story('Positive:creating booking with custom data')
def test_creating_booking_with_custom_data(api_client):
    with allure.step('Gotovim dannye dlya zaprosa'):
        booking_data = {
        "firstname" : "Ivan",
        "lastname" : "Ivanovich",
        "totalprice" : 111,
        "depositpaid" : True,
        "bookingdates" : {
            "checkin" : "2025-02-01",
            "checkout" : "2025-02-10"
        },
        "additionalneeds" : "Dinner"
        }

    #Отправили запрос с подготовленными данными с помощью метода - create_booking из api_client
    with allure.step('Otpravlyaem zaprros s podgotovlennymi dannymi s pomoshchyu metoda - create_booking из api_client'):
        response = api_client.create_booking(booking_data)
        try:
            #Вызываем класс BookingResponse из файла booking.py и
            #передаем в него сформированный выше response (kwargs)
            BookingResponse(**response)
        except ValidationError as e:
            raise ValidationError(f"Response validation failed: {e}")

        assert response['booking']['firstname'] == booking_data['firstname']
        assert response['booking']['lastname'] == booking_data['lastname']
        assert response['booking']['totalprice'] == booking_data['totalprice']
        assert response['booking']['depositpaid'] == booking_data['depositpaid']
        assert response['booking']['bookingdates']['checkin'] == booking_data['bookingdates']['checkin']
        assert response['booking']['bookingdates']['checkout'] == booking_data['bookingdates']['checkout']
        assert response['booking']['additionalneeds'] == booking_data['additionalneeds']

@allure.feature('Test creating booking')
@allure.story('Positive: creating booking with dynamic dates')
def test_create_booking_with_dynamic_dates(api_client, booking_dates):
    with allure.step('Gotovim dannye dlya zaprosa'):
        booking_data = {
            "firstname": "Ivan",
            "lastname": "Ivanovich",
            "totalprice": 150,
            "depositpaid": True,
            "bookingdates": {
                "checkin": booking_dates['checkin'],
                "checkout": booking_dates['checkout']
            },
            "additionalneeds": "Dinner"
        }
    with allure.step('Otpravlyaem zaprros s podgotovlennymi dannymi s pomoshchyu metoda - create_booking из api_client'):
        created_booking_response = api_client.create_booking(booking_data)
        # Проверка-1: Соответствует ли ответ API ожидаемой структуре и типам данных
        # Вызываем класс BookingResponse из файла booking.py и
        # передаем в него сформированный выше response:
        # Две звезды - это значит,что передаем словарь и поэтому-kwargs
        try:
            BookingResponse(**created_booking_response)
        except ValidationError as e:
            raise ValidationError(f"Response validation failed: {e}")
        # Проверка:
        assert created_booking_response['booking']['firstname'] == booking_data['firstname']
        assert created_booking_response['booking']['lastname'] == booking_data['lastname']
        assert created_booking_response['booking']['totalprice'] == booking_data['totalprice']
        assert created_booking_response['booking']['depositpaid'] == booking_data['depositpaid']
        assert created_booking_response['booking']['bookingdates']['checkin'] == booking_data['bookingdates']['checkin']
        assert created_booking_response['booking']['bookingdates']['checkout'] == booking_data['bookingdates']['checkout']

        #Мои добавленные проверки
        # Проверка-3: Сколько времени выполняется запрос?
        #start_time = time.time()
        #created_booking_response = api_client.create_booking(booking_data)
        #elapsed_time = (time.time() - start_time) * 1000  # Переводим в миллисекунды

        #print(f"Ответ API при создании бронирования: {created_booking_response}")
        #print(f"Время ответа API: {elapsed_time:.2f} миллисекунд")

        # Проверка-4: Время ответа меньше 1000 миллисекунд?
        #assert elapsed_time < 1000, f"Ответ пришел слишком долго: {elapsed_time:.2f} миллисекунд"


#Мои тесты
@allure.feature('Test creating booking')
@allure.story('Negative:Creating booking s nepolnymi dannymi')
def test_sozdanie_bronirovaniya_s_nepolnymi_dannymi(api_client, booking_dates):
    # Не передаю firstname, lastname
    with allure.step('Gotovim dannye dlya zaprosa:Ne peredayu firstname, lastname'):
        booking_data = {
            "totalprice": 150,
            "depositpaid": True,
            "bookingdates": {
                "checkin": booking_dates['checkin'],
                "checkout": booking_dates['checkout']
            },
            "additionalneeds": "Dinner"
        }
    with allure.step('Otpravlyaem zaprros s podgotovlennymi dannymi s pomoshchyu metoda - create_booking из api_client'):
        response = api_client.create_booking(booking_data)

    # Cервер вернет 400 Bad Request для неполных данных
    assert response.status_code == 400
    # В ответе на недостоющее переданное поле вернет слово error
    assert "firstname" in response.json()["error"]
    assert "lastname" in response.json()["error"]

@allure.feature('Test creating booking')
@allure.story('Negative:Creating booking s pustym JSON')
def test_sozdanie_bronirovaniya_s_pustym_JSON(api_client,booking_dates):
    # Передаем пустой JSON
    with allure.step('Gotovim dannye dlya zaprosa:Peredaem pustoj zapros JSON'):
        booking_data = {
        }

    #Выполняем запрос
    with allure.step('Otpravlyaem zapros s pustym JSON s pomoshchyu metoda - create_booking из api_client'):
        response = api_client.create_booking(booking_data)
    #Какие то проверки

@allure.feature('Test creating booking')
@allure.story('Negative:Creating booking s nevernymi dannymi')
def test_sozdanie_bronirovaniya_s_nevernymi_dannymi(api_client,booking_dates):
    with allure.step('Gotovim dannye dlya zaprosa: V pole totalprice peredayu stroku vmesto chisla'):
        booking_data = {
            "totalprice": "150",
            "depositpaid": True,
            "bookingdates": {
                "checkin": booking_dates['checkin'],
                "checkout": booking_dates['checkout']
            },
            "additionalneeds": "Dinner"
        }
    with allure.step('Otpravlyaem zapros s nevernymi dannymi: '
                     'V pole totalprice kladem stroku vmesto chisla s pomoshchyu metoda '
                     '- create_booking iz api_client'):
        response = api_client.create_booking(booking_data)
        #Какие то проверки