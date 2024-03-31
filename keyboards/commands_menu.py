from aiogram import Bot
from aiogram.types import BotCommand

COMMAND = {
      '/start': 'Запуск бота',
      '/help': 'Справка по работе с ботом'
}

# Функция для настройки кнопки Menu бота
async def set_commands_menu(bot: Bot, user_id = None):
      await bot.delete_my_commands()
      main_menu_commands = [BotCommand(
                              command=command,
                              description=description
                        ) for command,
                              description in COMMAND.items()]
      await bot.set_my_commands(main_menu_commands)