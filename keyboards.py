from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from enums import EnglishLevel, Confirmation

contact_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Поделиться контактом", request_contact=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

confirmation_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=Confirmation.YES)],
        [KeyboardButton(text=Confirmation.NO)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/start")],
        [KeyboardButton(text="/myself")],
        [KeyboardButton(text="/register")],
        [KeyboardButton(text="/pay")],
        [KeyboardButton(text="/callback")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие"
)

en_levels_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=EnglishLevel.Beginner)],
        [KeyboardButton(text=EnglishLevel.Elementary)],
        [KeyboardButton(text=EnglishLevel.Pre_Intermediate)],
        [KeyboardButton(text=EnglishLevel.Intermediate)],
        [KeyboardButton(text=EnglishLevel.Upper_Intermediate)],
        [KeyboardButton(text=EnglishLevel.Advanced)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
