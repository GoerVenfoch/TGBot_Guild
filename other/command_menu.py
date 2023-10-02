from aiogram import types


async def set_default_commands(bot):
    await bot.set_my_commands([
        types.BotCommand(command="start", description="Запустить бота"),
        types.BotCommand(command="get_data", description="111"),
        types.BotCommand(command="help", description="Помощь"),
    ])
