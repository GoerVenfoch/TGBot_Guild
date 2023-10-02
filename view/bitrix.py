from view.user_bitrix import UserBitrix


class BitrixView:
    user = UserBitrix()
    groups = []
    stages = {"EnterChat": 'C11:PREPARATION',
              "WriteComment": 'C11:PREPAYMENT_INVOIC',
              "GetFoto": 'C11:EXECUTING',
              "GetLogo": 'C11:FINAL_INVOICE',
              "SignPortal": 'C11:UC_R7QTLR',
              "IntroductionGuild": 'C11:UC_8V4B8N',
              "IntroductionRegulation": 'C11:UC_EKVSP3',
              "Win": 'C11:WON',
              "Lose": 'C11:LOSE',
              "APOLOGY": 'C11:APOLOGY'}
