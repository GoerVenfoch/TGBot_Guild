from other import bitrix
from view.user_bitrix import UserBitrix
from aiogram.types import Message


async def completion_bitrix(message: Message):
    user_data = UserBitrix()
    group = await bitrix.get_all('sonet_group.get',
                                 params={
                                     'FILTER': {'%VISIBLE': 'Y'}
                                 })
    for g in group:
        user_data.groups.append({'ID': g['ID'], 'NAME': g['NAME']})

    # id всех сделок
    user_data.deals = await bitrix.get_all(
        'crm.deal.list',
        params={
            'select': ['ID'],
            'filter': {'?STAGE_ID': 'C21:'}
        })
    # id сделок и id контактов к ним
    user_data.contacts_deals = await bitrix.get_by_ID(
        'crm.deal.contact.items.get',
        [d['ID'] for d in user_data.deals])

    # id контактов
    try:
        for i in [c for c in user_data.contacts_deals]:
            buffer = ([i, c['CONTACT_ID']] for c in user_data.contacts_deals.get(i))
            user_data.contacts += buffer
    except AttributeError:
        user_data.contacts = [user_data.deals[0]['ID'], user_data.contacts_deals[0]['CONTACT_ID']]
    print(user_data.name)
    print(user_data.id_user)
    print(user_data.last_name)
    print(user_data.id_deal)
    try:
        # данные пользователей по id
        users = await bitrix.get_by_ID(
            'crm.contact.get',
            [c[1] for c in user_data.contacts])

        # возвращаемся к id сделки через пользователя
        for i in user_data.contacts:
            if (users[str(i[1])]['NAME'] == message.from_user.first_name and
                    users[str(i[1])]['LAST_NAME'] == message.from_user.last_name):
                user_data.name = message.from_user.first_name
                user_data.last_name = message.from_user.last_name
                for id_contact in user_data.contacts:
                    if str(id_contact[1]) == str(users[str(i[1])]['ID']):
                        user_data.id_deal = id_contact[0]
                        user_data.id_contact = users[str(i[1])]['ID']
                        UserBitrix.login = str(users[str(i[1])]['UF_CRM_LOGIN'])
                        UserBitrix.password = str(users[str(i[1])]['UF_CRM_PASS'])
                        user_data.id_company = str(users[str(i[1])]['COMPANY_ID'])
                        break
    except TypeError:
        # данные пользователей по id
        users = await bitrix.get_by_ID(
            'crm.contact.get',
            [user_data.contacts[1]])

        # возвращаемся к id сделки через пользователя
        if (users[str(user_data.contacts[1])]['NAME'] == message.from_user.first_name and
                users[str(user_data.contacts[1])]['LAST_NAME'] == message.from_user.last_name):
            user_data.name = message.from_user.first_name
            user_data.last_name = message.from_user.last_name
            user_data.id_deal = user_data.contacts[0]
            user_data.id_contact = users[str(user_data.contacts[1])]['ID']
            user_data.login = str(users[str(user_data.contacts[1])]['UF_CRM_LOGIN'])
            user_data.password = str(users[str(user_data.contacts[1])]['UF_CRM_PASS'])
            user_data.id_company = str(users[str(user_data.contacts[1])]['COMPANY_ID'])

    # пользователи
    users = await bitrix.get_all('crm.contact.list')
    try:
        for u in users:
            if (user_data.name == u['NAME'] and
                    user_data.last_name == u['LAST_NAME']):
                user_data.id_user = u['ID']
                break
    except KeyError:
        pass

    return user_data


class BitrixView:
    stages = {"EnterChat": 'C21:PREPARATION',
              "WriteComment": 'C21:PREPAYMENT_INVOIC',
              "GetFoto": 'C21:EXECUTING',
              "GetLogo": 'C21:FINAL_INVOICE',
              "SignPortal": 'C21:UC_422MA3',
              "IntroductionGuild": 'C21:UC_ZQ580U',
              "IntroductionRegulation": 'C21:UC_OO1U7T',
              "PushShildik": 'C21:UC_C15C28',
              "Win": 'C21:WON'}
    # stages = {"EnterChat": 'C2:PREPARATION',
    #           "WriteComment": 'C2:PREPAYMENT_INVOIC',
    #           "GetFoto": 'C2:EXECUTING',
    #           "GetLogo": 'C2:FINAL_INVOICE',
    #           "SignPortal": 'C2:UC_89NKDN',
    #           "IntroductionGuild": 'C2:UC_1GHBCY',
    #           "IntroductionRegulation": 'C2:UC_18R9AA',
    #           "PushShildik": 'C2:UC_UZUUQ9',
    #           "Win": 'C2:WON'}




