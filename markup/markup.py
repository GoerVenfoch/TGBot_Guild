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


def get_inline_keyboard(lst_name_btn, kb_type):
    builder = InlineKeyboardBuilder()

    if kb_type == "url":
        for key in lst_name_btn:
            builder.add(types.InlineKeyboardButton(text=str(key),
                                                   url=str(lst_name_btn[key])))
        return builder.as_markup(resize_keyboard=True)
    elif kb_type == "callback_data":
        for key in lst_name_btn:
            builder.add(types.InlineKeyboardButton(text=str(key),
                                                   callback_data=str(lst_name_btn[key])))
        return builder.as_markup(resize_keyboard=True)
