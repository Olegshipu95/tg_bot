import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, LabeledPrice
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram import Router
from aiogram.fsm.storage.memory import MemoryStorage
from datetime import datetime

from aiohttp.web_fileresponse import content_type

from bridge_docs import *
from keyboards import *
from payment import initiate_payment
from config_reader import config
from enums import *


logging.basicConfig(level=logging.INFO)


bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher(storage=MemoryStorage())


class Form(StatesGroup):
    name = State()
    phone = State()
    english_level = State()
    confirmation = State()
    payment = State()


router = Router()


@router.message(Command('start'))
async def router_cmd_start(message: types.Message):
    await message.answer("Привет! Запишите себя на спикинг клуб, отправив команду /register.",
                         reply_markup=start_keyboard)


@router.message(Command('register'))
async def router_register_user(message: types.Message, state: FSMContext):
    await message.answer("Привет! Я помогу тебе записаться на спикинг клуб.\nНапиши, как тебя зовут?")
    await state.set_state(Form.name)


@router.message(Command('pay'))
async def router_initiate_payment_process(message: types.Message):
    username = message.from_user.username
    user_data = check_user_data(username)
    if user_data is None:
        await message.answer("Вы не зарегистрированы на спикинг клуб. Пожалуйста, используйте команду /register.")
        return

    if user_data['Payment'] == 'TRUE':
        await message.answer("Вы уже оплатили подписку.")
    else:
        await message.answer("Вам необходимо оплатить подписку для участия в спикинг клубе.")
        await initiate_payment(message, bot)


@router.message(Form.name)
async def router_get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text, username=message.from_user.username)
    await message.answer(f"Отлично, {message.text}, теперь поделись своим номером телефона, нажав кнопку 'поделиться'.",
                         reply_markup=contact_keyboard)
    await state.set_state(Form.phone)


@router.message(Form.phone, F.contact)
async def router_get_contact(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    await message.answer(f"Отлично! Выбери, какой у тебя уровень английского?",
                         reply_markup=en_levels_keyboard)
    await state.set_state(Form.english_level)


@router.message(Form.english_level, F.text.in_(EnglishLevel))
async def router_get_english_level(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    user_data['english_level'] = message.text
    user_data['registration_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if check_user_exists(user_data['username']):
        await message.answer(
            "Данные для пользователя с таким же username уже существуют. Вы хотите перезаписать их?",
            reply_markup=confirmation_keyboard
        )
        await state.update_data(user_data=user_data)
        await state.set_state(Form.confirmation)
    else:
        save_user_data_to_sheet(user_data)
        await message.answer("Ты успешно зарегистрировался на спикинг клуб! Теперь можно перейти к оплате. (/pay)",
                             reply_markup=start_keyboard)


@router.message(Form.confirmation, F.text.in_(Confirmation))
async def router_handle_confirmation(message: types.Message, state: FSMContext):
    user_data = (await state.get_data()).get('user_data', {})
    if message.text == Confirmation.YES:
        delete_old_record_and_add_new(user_data)
        await message.answer("Данные успешно перезаписаны.", reply_markup=start_keyboard)
    elif message.text == Confirmation.NO:
        await message.answer("Ваши данные остались неизменными.", reply_markup=start_keyboard)
    await state.clear()


@router.pre_checkout_query()
async def router_process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@router.message(F.successful_payment)
async def router_handle_payment(message: types.Message):
    user_data = check_user_data(message.from_user.username)
    if user_data:
        # Обновляем данные пользователя, что зон оплатил подписку
        update_payment_status(message.from_user.username)
        await message.answer("Платеж успешно обработан! Спасибо за подписку.")
    else:
        await message.answer("Не удалось найти ваши данные. Пожалуйста, зарегистрируйтесь заново.")