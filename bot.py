import asyncio
import logging
from environs import Env

from aiogram import Bot, Dispatcher

from keyboards.commands_menu import set_commands_menu
from handlers import user_handlers, other_handlers

from services.parsing import get_offers

logger = logging.getLogger(__name__)
env: Env = Env()
env.read_env()

token = env('token')

async def main():
    logging.basicConfig(
        level=logging.INFO,
        filename = "botlog.log",
        filemode='a',
        format = "%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
        datefmt='%H:%M:%S',
        )
    logger.info('Starting bot')
    

    bot = Bot(token=token, parse_mode='HTML')
    dp = Dispatcher()

    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    await set_commands_menu(bot)
    

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error('Bot stopped')