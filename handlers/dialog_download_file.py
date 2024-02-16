import pathlib
import random

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile

import base64

from aiogram.utils.chat_action import ChatActionSender

from other import PrimaryState, bot, bitrix
from view import BitrixView

router = Router()

mes_request_logo = """
`Ты любишь выделиться и хочешь чтобы другие это узнали?` 

Отправь нам _лого компании_ и мы добавим его на наш сайт, чтобы все узнали о тебе.

Формат файла: .png
Размер логотипа: не менее 448 × 348 px
"""

random_sticker = [
    'data/stickers/bull.png',
    'data/stickers/cat.png',
    'data/stickers/down.png',
    'data/stickers/gorilla.png',
    'data/stickers/red.png',
    'data/stickers/question.png'
]


@router.message(PrimaryState.getFoto, F.photo)
async def get_foto(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        context_data = await state.get_data()
        user_data = context_data.get('user')
        photo = await bot.get_file(message.photo[-1].file_id)
        await bot.download(photo, f'photo{photo.file_id}.png')
        image_read = open(f'photo{photo.file_id}.png', 'rb').read()
        image_64_encode = base64.b64encode(image_read).decode('utf-8')
        await bitrix.call('crm.contact.update',
                          [{
                              'ID': user_data.id_contact,
                              'fields': {
                                  'PHOTO': {
                                      "fileData": [f'{message.from_user.last_name}_foto.png',
                                                   str(image_64_encode)]}
                              }
                          }])
        await bitrix.call('crm.deal.update',
                          [{
                              'ID': user_data.id_deal,
                              'fields': {
                                  'STAGE_ID': BitrixView.stages["GetFoto"]}
                          }])
        file = pathlib.Path(f'photo{photo.file_id}.png')
        file.unlink()
    await message.answer("Классное фото))")
    await message.answer_sticker(FSInputFile('data/stickers/sticker.png'))
    await message.answer(mes_request_logo,
                         parse_mode="Markdown",
                         input_field_placeholder="Жду логотип")
    await state.set_state(PrimaryState.getLogo)


@router.message(PrimaryState.getFoto)
async def default_get_foto(message: Message):
    await message.answer("Мне нужно фото!")
    await message.answer_sticker(FSInputFile(random.choice(random_sticker)))


@router.message(PrimaryState.getLogo, F.photo)
async def get_logo(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        context_data = await state.get_data()
        user_data = context_data.get('user')
        logo = await bot.get_file(message.photo[-1].file_id)
        await bot.download(logo, f'logo{logo.file_id}.png')
        image_read = open(f'logo{logo.file_id}.png', 'rb').read()
        image_64_encode = base64.b64encode(image_read).decode('utf-8')
        await bitrix.call('disk.folder.uploadfile',
                          [{
                              'id': 2570,
                              'data': {'NAME': f'{message.from_user.last_name}_logo_1.png'},
                              "fileContent": [f'{message.from_user.last_name}_logo.png',
                                              str(image_64_encode)]
                          }])
        await bitrix.call('crm.deal.update',
                          [{
                              'ID': user_data.id_deal,
                              'fields': {
                                  'STAGE_ID': BitrixView.stages["GetLogo"]
                              }
                          }])
        file = pathlib.Path(f'logo{logo.file_id}.png')
        file.unlink()
    await message.answer(
        text="Отлично) Отправь ссылку на свой сайт, чтобы при нажатии на логотип все желающие могли с тобой познакомиться поближе",
    )
    await state.set_state(PrimaryState.getLink)


@router.message(PrimaryState.getLogo)
async def default_get_logo(message: Message):
    await message.answer("Я жду логотип!")
    await message.answer_sticker(FSInputFile(random.choice(random_sticker)))
