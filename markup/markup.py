from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

EMPTY = types.ReplyKeyboardRemove()


def get_reply_keyboard(lst_name_btn: list, kb_type):
    builder = ReplyKeyboardBuilder()

    if kb_type == "row3":
        for i in lst_name_btn:
            builder.add(types.KeyboardButton(text=str(i)))
        if len(lst_name_btn) > 3:
            builder.adjust(round(len(lst_name_btn) / 3))
        return builder.as_markup(resize_keyboard=True)


def get_inline_keyboard(lst_name_btn, lst_data, kb_type):
    builder = InlineKeyboardBuilder()

    if kb_type == "url" and len(lst_name_btn) == len(lst_data):
        for i in range(len(lst_name_btn)):
            builder.add(types.InlineKeyboardButton(text=str(lst_name_btn[i]),
                                                   url=str(lst_data[i])))
        builder.adjust(1)
        return builder.as_markup(resize_keyboard=True)
    elif kb_type == "callback_data":
        for i in range(len(lst_name_btn)):
            builder.add(types.InlineKeyboardButton(text=str(lst_name_btn[i]),
                                                   callback_data=str(lst_data[i])))
        builder.adjust(1)
        return builder.as_markup(resize_keyboard=True)
