from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.chat_action import ChatActionSender

from other import NoDealInBitrix, bot
from view.bitrix import completion_bitrix

router = Router()

mes_connect_chat_guild = """
Очень приятно, *{Name}*!

И вот твоя первая миссия _“Вступление в чат”_.

Присоединись к закрытому чату Членов Гильдии по [ссылке](https://t.me/+LSBI6iI_SNdjOGNi) и нажми _“Присоединился”_
"""


@router.message(NoDealInBitrix.whereDeal)
async def who_are_you(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        user_data = await completion_bitrix(message, 2)
        await state.update_data(user=user_data)
        if user_data.id_deal == "":
            await message.answer("Мы снова не смогли найти вас. Попробуйте ещё раз!")
        else:
            await message.answer(
                text=mes_connect_chat_guild.format(Name=user_data.name),
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Присоединился",
                                                                                         callback_data="connect_chat")]]),
                parse_mode="Markdown"
            )
