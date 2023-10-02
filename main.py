import asyncio
import logging

from aiogram.fsm.storage.memory import MemoryStorage

import handlers
import other

from aiogram import Dispatcher


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = other.bot
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_routers(handlers.dialog_handrers.router,
                       handlers.different_handlers.router,
                       handlers.search_deal_on_contact_handlers.router,
                       handlers.dialog_download_file.router,
                       handlers.callback_function.router)

    await other.command_menu.set_default_commands(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
