from aiogram import Bot
from aiogram.types import BotCommand

from tg_bot.config import settings

if settings.BOT_LANGUAGE == 'en':
    from tg_bot.lexicon.en import LEXICON_COMMANDS
elif settings.BOT_LANGUAGE == 'ru':
    from tg_bot.lexicon.ru import LEXICON_COMMANDS
else:
    raise ValueError(f"Unsupported language: {settings.BOT_LANGUAGE}")



# Функция для настройки кнопки Menu бота
async def set_main_menu(bot: Bot):
    main_menu_commands = [BotCommand(
        command=command,
        description=description
    ) for command,
        description in LEXICON_COMMANDS.items()]
    await bot.set_my_commands(main_menu_commands)