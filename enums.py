from enum import StrEnum


class EnglishLevel(StrEnum):
    Beginner = "Beginner",
    Elementary = "Elementary",
    Pre_Intermediate = "Pre-Intermediate",
    Intermediate = "Intermediate",
    Upper_Intermediate = "Upper Intermediate",
    Advanced = "Advanced"


class Confirmation(StrEnum):
    YES = "Да, перезаписать",
    NO = "Нет, оставить старые данные"
