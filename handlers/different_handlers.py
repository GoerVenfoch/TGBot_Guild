from aiogram import Router, F
from aiogram.filters.command import Command
from aiogram.types import Message, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.utils.chat_action import ChatActionSender

from markup import markup
from other import PrimaryState, bot, NoDealInBitrix
from view.bitrix import completion_bitrix

router = Router()

start_message = f"""
`Привет, рада новому знакомству!`

Я `Гильдина`👩, твой личный помощник-компаньон при прохождении миссий _“Интеграции”_. 
Я помогу тебе освоиться в Гильдии Интеграторов🏯 и расскажу все, что необходимо знать.

Квест разделен на несколько простых миссий, которые помогут разобраться в устройстве Гильдии🏯, рассказать о себе и познакомиться ближе с _коллегами-интеграторами_.

Кстати, можешь звать меня просто `Галя`👩
"""

who = """
`А кто же тот воин, о котором скальды сложат песни?...`

_Как тебя зовут?_
"""

mes_connect_chat_guild = """
Очень приятно, *{Name}*!

И вот твоя первая миссия _“Вступление в чат”_.

Присоединись к закрытому чату Членов Гильдии по [ссылке](https://t.me/+LSBI6iI_SNdjOGNi) и нажми _“Присоединился”_
"""


@router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):

        try:
            user_data = await completion_bitrix(message)
            print(user_data.name)
            print(user_data.id_user)
            print(user_data.last_name)
            print(user_data.id_deal)
            await state.update_data(user=user_data)
            await message.answer(start_message, parse_mode="Markdown")
            await message.answer_sticker(FSInputFile('data/stickers/hello.png'))
            await message.answer(who,
                                 parse_mode="Markdown",
                                 reply_markup=markup.EMPTY,
                                 input_field_placeholder="Имя")
            await state.set_state(PrimaryState.getName)
        except:
            await message.answer("У меня проблемы! Попробуйте попозже:)")


# Получаем имя и отправляем ссылку
@router.message(PrimaryState.getName, F.text)
async def get_name_handler(message: Message, state: FSMContext):
    context_data = await state.get_data()
    user_data = context_data.get('user')
    user_data.name = message.text
    if user_data.id_deal == "":
        await message.answer("Мы не смогли найти вас. Напишите вашу фамилию!")
        await state.set_state(NoDealInBitrix.whereDeal)
    else:
        await message.answer(
            text=mes_connect_chat_guild.format(Name=user_data.name),
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Присоединился",
                                                                                     callback_data="connect_chat")]]),
            parse_mode="Markdown"
        )
        await state.update_data(user_data)
