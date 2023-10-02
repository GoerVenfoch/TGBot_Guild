from aiogram.types import Message

from other import bitrix
from view import BitrixView


async def completion_bitrix(message: Message):
    group = await bitrix.get_all('sonet_group.get',
                                 params={
                                     'FILTER': {'%VISIBLE': 'Y'}
                                 })
    for g in group:
        BitrixView.groups.append({'ID': g['ID'], 'NAME': g['NAME']})

    # id всех сделок
    deals = await bitrix.get_all(
        'crm.deal.list',
        params={
            'select': ['ID'],
            'filter': {'?STAGE_ID': 'C11:'}
        })
    # id сделок и id контактов к ним
    contacts = await bitrix.get_by_ID(
        'crm.deal.contact.items.get',
        [d['ID'] for d in deals])

    # id контактов
    contacts_num = []
    for i in [c for c in contacts]:
        buffer = ([c['CONTACT_ID'] for c in contacts.get(i)])
        contacts_num += buffer

    # данные пользователей по id
    users = await bitrix.get_by_ID(
        'crm.contact.get',
        contacts_num)

    # возвращаемся к id сделки через пользователя
    for i in contacts_num:
        if (users[str(i)]['NAME'] == message.from_user.first_name and
                users[str(i)]['LAST_NAME'] == message.from_user.last_name):
            BitrixView.user.name = message.from_user.first_name
            BitrixView.user.last_name = message.from_user.last_name
            for id_contact in [c for c in contacts]:
                if str(([c['CONTACT_ID'] for c in contacts.get(id_contact)])[0]) == users[str(i)]['ID']:
                    BitrixView.user.id_deal = id_contact
                    BitrixView.user.id_contact = users[str(i)]['ID']
                    break

    # пользователи
    users = await bitrix.get_all('user.get')

    try:
        for u in users:
            if (BitrixView.user.name == u['NAME'] and
                    BitrixView.user.last_name == u['LAST_NAME']):
                BitrixView.user.id_user = u['ID']
                break
    except KeyError:
        pass
