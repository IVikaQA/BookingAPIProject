from pydantic import BaseModel
from typing import Optional
from datetime import date

#Класс 3
class BookingDates(BaseModel):
    checkin: date
    checkout: date

# Класс 2
#Важно:Класс Booking добавить выше класса 1,чтобы класс 2 был
#доступен в классе 1
class Booking(BaseModel):
    firstname: str
    lastname: str
    totalprice: int
    depositpaid: bool
    #В классе BookingDates будут хранится даты
    bookingdates: BookingDates
    #Слово Optional говорит,что параметр НЕобязательный
    additionalneeds: Optional[str] = None


# Класс 1:Наследуемся от класса BaseModel
class BookingResponse(BaseModel):
    bookingid: int
    booking: Booking
