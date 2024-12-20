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

