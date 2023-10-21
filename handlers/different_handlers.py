from aiogram import Router
from aiogram.filters.command import Command
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.utils.chat_action import ChatActionSender

from markup import markup
from other import PrimaryState, bot
from view import BitrixView

router = Router()

start_message = f"""
`Привет, рада новому знакомству!`

Я `Гильдина`👩, твой личный
помощник-компаньон при прохождении миссий
_“Интеграции”_. Я помогу тебе освоиться в Гильдии
Интеграторов🏯 и расскажу все, что необходимо знать.

Квест разделен на несколько простых миссий, которые
помогут разобраться в устройстве Гильдии🏯, рассказать о
себе и познакомиться ближе с _коллегами-интеграторами_.

Кстати, можешь звать меня просто `Галя`👩
"""

who = """
`А кто же тот воин, о котором скальды сложат песни?...`

_Как тебя зовут?_
"""


@router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        try:
            await BitrixView().completion_bitrix(message)
            await message.answer(start_message, parse_mode="Markdown")
            await message.answer_sticker(FSInputFile('data/stickers/hello.png'))
            await message.answer(who,
                                 parse_mode="Markdown",
                                 reply_markup=markup.EMPTY,
                                 input_field_placeholder="Имя")
            await state.set_state(PrimaryState.getName)
        except:
            await message.answer("У меня проблемы! Попробуйте попозже:)")
