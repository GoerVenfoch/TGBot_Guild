from aiogram import Router
from aiogram.types import Message, FSInputFile

from other import NoDealInBitrix
router = Router()


@router.message(NoDealInBitrix.whereDeal)
async def who_are_you(message: Message):
    await message.answer("Я не знаю тебя")
    await message.answer_sticker(FSInputFile('data/stickers/samurai.png'))
