from aiogram import Router
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from other import PrimaryState

router = Router()


start_message = """
Привет, рада новому знакомству! Я Гильдина, твой личный
помощник-компаньон при прохождении миссий
“Интеграции”. Я помогу тебе освоиться в Гильдии
Интеграторов и расскажу все, что необходимо знать.
Квест разделен на несколько простых миссий, которые
помогут разобраться в устройстве Гильдии, рассказать о
себе и познакомиться ближе с коллегами-интеграторами.
Кстати, можешь звать меня просто Галя )
А кто же тот воин, о котором скальды сложат песни?...
Как тебя зовут?
"""


@router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    await message.answer(start_message)
    await state.set_state(PrimaryState.getName)

