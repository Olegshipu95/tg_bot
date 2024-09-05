from aiogram import Bot, types
from config_reader import config

from aiogram.types import LabeledPrice

PRICE = LabeledPrice(label="Подписка на 1 месяц", amount=10000)  # amount в копейках

async def initiate_payment(message: types.Message, bot : Bot):
    await bot.send_invoice(
        chat_id=message.chat.id,
        title="Подписка на спикинг клуб",
        description="Оплатите подписку на спикинг клуб на 1 месяц.",
        payload="subscription_payment",  # Payload для обработки платежа
        provider_token=config.payments_token.get_secret_value(),
        start_parameter="subscribe",
        currency="RUB",
        prices=[PRICE]
    )