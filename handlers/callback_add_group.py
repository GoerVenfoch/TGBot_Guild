from aiogram import Router, F, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from other import bitrix

router = Router()


@router.callback_query(F.data.startswith("group_"))
async def callback_group(callback: types.CallbackQuery, state: FSMContext):
    context_data = await state.get_data()
    user_data = context_data.get('user')
    id_group = callback.data.split("_")[1]
    try:
        await bitrix.call('sonet_group.user.add', {
            'GROUP_ID': int(id_group),
            'USER_ID': user_data.id_user
        })
        for group in user_data.groups:
            if id_group == group['ID']:
                await callback.message.answer("Вы добавлены в группу " + '"' + group['NAME'] + '"')
    except IndexError:
        for group in user_data.groups:
            if id_group == group['ID']:
                await callback.message.answer("Мы не можем добавить вас в группу " + '"' + group['NAME'] + '".\n' +
                                              "_Проверьте свой список групп или свяжитесь с администратором портала._",
                                              reply_markup=InlineKeyboardMarkup(
                                                  inline_keyboard=[[InlineKeyboardButton(
                                                      text="Продолжить интеграцию в Гильдию",
                                                      callback_data="continue_integra"
                                                  )]]),
                                              parse_mode="Markdown")
