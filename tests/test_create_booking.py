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
@allure.story('Negative: creating booking with dynamic dates')
def test_create_booking_with_dynamic_dates(api_client, booking_dates):
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

    created_booking_response = api_client.create_booking(booking_data)
    # Проверка-1: Соответствует ли ответ API ожидаемой структуре и типам данных
    # Вызываем класс BookingResponse из файла booking.py и
    # передаем в него сформированный выше response:
    # Две звезды - это значит,что передаем словарь и поэтому-kwargs
    try:
        BookingResponse(**created_booking_response)
    except ValidationError as e:
        raise ValidationError(f"Response validation failed: {e}")
    # Проверка-2:
    assert created_booking_response['booking']['firstname'] == booking_data['firstname']
    assert created_booking_response['booking']['lastname'] == booking_data['lastname']
    assert created_booking_response['booking']['totalprice'] == booking_data['totalprice']
    assert created_booking_response['booking']['depositpaid'] == booking_data['depositpaid']
    assert created_booking_response['booking']['bookingdates']['checkin'] == booking_data['bookingdates']['checkin']
    assert created_booking_response['booking']['bookingdates']['checkout'] == booking_data['bookingdates']['checkout']

    #Мои добавленные проверки
    # Проверка-3: Сколько времени выполняется запрос?
    start_time = time.time()
    created_booking_response = api_client.create_booking(booking_data)
    elapsed_time = (time.time() - start_time) * 1000  # Переводим в миллисекунды

    print(f"Ответ API при создании бронирования: {created_booking_response}")
    print(f"Время ответа API: {elapsed_time:.2f} миллисекунд")

    # Проверка-4: Время ответа меньше 1000 миллисекунд?
    assert elapsed_time < 1000, f"Ответ пришел слишком долго: {elapsed_time:.2f} миллисекунд"

    # Проверка-3: Статус-код ответа 200?
    status_code = api_client.get_response_status_code(created_booking_response)
    # Возврращается None
    #print(status_code)

#Мои тесты
@allure.feature('Test creating booking')
@allure.story('Positive:Sozdanie bronirovaniya s nepolnymi dannymi')
def test_sozdanie_bronirovaniya_s_nepolnymi_dannymi(api_client, booking_dates):
    # Не передаю firstname, lastname
    booking_data = {
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            "checkin": booking_dates['checkin'],
            "checkout": booking_dates['checkout']
        },
        "additionalneeds": "Dinner"
    }

    response = api_client.create_booking(booking_data)

    # Cервер вернет 400 Bad Request для неполных данных
    assert response.status_code == 400  # Предполагаем, что сервер вернет 400 Bad Request для неполных данных
    # В ответе на недостоющее переданное поле вернет слово error
    assert "firstname" in response.json()["error"]
    assert "lastname" in response.json()["error"]

def test_sozdanie_bronirovaniya_s_pustym_JSON(api_client,booking_dates):
    # Передаем пустой JSON
    booking_data = {
    }

    #Выполняем запрос
    response = api_client.create_booking(booking_data)

def test_sozdanie_bronirovaniya_s_nevernymi_dannymi(api_client,booking_dates):
    # Не передаю firstname, lastname
    booking_data = {
        "totalprice": "150",
        "depositpaid": True,
        "bookingdates": {
            "checkin": booking_dates['checkin'],
            "checkout": booking_dates['checkout']
        },
        "additionalneeds": "Dinner"
    }

    response = api_client.create_booking(booking_data)
