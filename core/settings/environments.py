import os
from enum import Enum

class Environment(Enum):
    #Эти переменные нужны для переключения между средами
    TEST = "test"
    PROD = "production"