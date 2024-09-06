import asyncio
import logging
from aiogram.utils.token import TokenValidationError
from router import router, dp, bot
from bridge_docs import check_and_add_headers


async def main():
    check_and_add_headers()
    dp.include_router(router)
    try:
        await dp.start_polling(bot)
    except TokenValidationError as e:
        logging.error(f"Ошибка валидации токена: {e}")


if __name__ == "__main__":
    asyncio.run(main())
