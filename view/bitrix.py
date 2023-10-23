from view.user_bitrix import UserBitrix
from aiogram.types import Message

from other import bitrix


class BitrixView:
    user = UserBitrix()
    groups = []
    deals = []
    contacts_deals = []
    contacts = []
    login = ""
    password = ""
    # stages = {"EnterChat": 'C21:PREPARATION',
    #           "WriteComment": 'C21:PREPAYMENT_INVOIC',
    #           "GetFoto": 'C21:EXECUTING',
    #           "GetLogo": 'C21:FINAL_INVOICE',
    #           "SignPortal": 'C21:UC_422MA3',
    #           "IntroductionGuild": 'C21:UC_ZQ580U',
    #           "IntroductionRegulation": 'C21:UC_OO1U7T',
    #           "PushShildik": 'C21:UC_C15C28',
    #           "Win": 'C21:WON'}
    stages = {"EnterChat": 'C2:PREPARATION',
              "WriteComment": 'C2:PREPAYMENT_INVOIC',
              "GetFoto": 'C2:EXECUTING',
              "GetLogo": 'C2:FINAL_INVOICE',
              "SignPortal": 'C2:UC_89NKDN',
              "IntroductionGuild": 'C2:UC_1GHBCY',
              "IntroductionRegulation": 'C2:UC_18R9AA',
              "PushShildik": 'C2:UC_UZUUQ9',
              "Win": 'C2:WON'}

    async def completion_bitrix(self, message: Message):
        group = await bitrix.get_all('sonet_group.get',
                                     params={
                                         'FILTER': {'%VISIBLE': 'Y'}
                                     })
        for g in group:
            self.groups.append({'ID': g['ID'], 'NAME': g['NAME']})

        # id всех сделок
        self.deals = await bitrix.get_all(
            'crm.deal.list',
            params={
                'select': ['ID'],
                'filter': {'?STAGE_ID': 'C2:'}
            })
        # id сделок и id контактов к ним
        self.contacts_deals = await bitrix.get_by_ID(
            'crm.deal.contact.items.get',
            [d['ID'] for d in self.deals])
        print(self.contacts_deals)
        print(self.deals)

        # id контактов
        try:
            for i in [c for c in self.contacts_deals]:
                buffer = ([i, c['CONTACT_ID']] for c in self.contacts_deals.get(i))
                self.contacts += buffer
        except AttributeError:
            self.contacts = [self.deals[0]['ID'], self.contacts_deals[0]['CONTACT_ID']]

        try:
            # данные пользователей по id
            users = await bitrix.get_by_ID(
                'crm.contact.get',
                [c[1] for c in self.contacts])

            # возвращаемся к id сделки через пользователя
            for i in self.contacts:
                if (users[str(i[1])]['NAME'] == message.from_user.first_name and
                        users[str(i[1])]['LAST_NAME'] == message.from_user.last_name):
                    self.user.name = message.from_user.first_name
                    self.user.last_name = message.from_user.last_name
                    for id_contact in self.contacts:
                        if str(id_contact[1]) == str(users[str(i[1])]['ID']):
                            self.user.id_deal = id_contact[0]
                            self.user.id_contact = users[str(i[1])]['ID']
                            print(users[str(i[1])]['ID'])
                            break
        except TypeError:
            # данные пользователей по id
            users = await bitrix.get_by_ID(
                'crm.contact.get',
                [self.contacts[1]])

            # возвращаемся к id сделки через пользователя
            if (users[str(self.contacts[1])]['NAME'] == message.from_user.first_name and
                    users[str(self.contacts[1])]['LAST_NAME'] == message.from_user.last_name):
                self.user.name = message.from_user.first_name
                self.user.last_name = message.from_user.last_name
                self.user.id_deal = self.contacts[0]
                self.user.id_contact = users[str(self.contacts[1])]['ID']

        deal = await bitrix.get_by_ID("crm.deal.get", self.user.id_deal)
        self.login = deal["UF_CRM_LOGIN"]
        self.password = deal["UF_CRM_PASS"]
        # пользователи
        users = await bitrix.get_all('user.get')

        try:
            for u in users:
                if (self.user.name == u['NAME'] and
                        self.user.last_name == u['LAST_NAME']):
                    self.user.id_user = u['ID']
                    break
        except KeyError:
            pass
