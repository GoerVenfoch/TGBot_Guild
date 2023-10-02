import asyncio
import logging

from aiogram.fsm.storage.memory import MemoryStorage

import handlers
import other

from aiogram import Bot, Dispatcher


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=other.config_reader.config.bot_token.get_secret_value())
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_routers(handlers.dialog_handrers.router,
                       handlers.different_handlers.router)

    await other.command_menu.set_default_commands(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
