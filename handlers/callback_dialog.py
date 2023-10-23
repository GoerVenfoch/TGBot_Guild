from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from bitrix import bitrix_call_func
from markup import markup
from other import PrimaryState
from view import BitrixView

mes_about_user = """
{Name}, отличное начало! А вот и твой _первый подарок_: 

💯 _баллов на баланс!_ 

Мои поздравления!
"""

mes_about_user_2 = """
Как и куда ты их сможешь потратить я расскажу тебе чуть позже, не все сразу )
А прямо сейчас тебя ждет твоя новая миссия _“Знакомство”_.

Напиши в чате членов свое первое приветственное сообщение✍:
`- поприветствуй коллег,`
`- расскажи из какой ты компании,`
`- чем она занимается,`
`- в чем твоя экспертность,`
`- какие уже есть достижения?`

В общем, расскажи коллегам, каков он: *{Name}* - `новый член Гильдии Интеграторов!`

После прохождения этой миссии нажми _“Представился”_
"""

mes_request_foto = """
*{Name}*, я рада, что смогла узнать тебя получше! А чтобы стать к коллегам еще ближе, поделись со мной своей лучшей 💣

фотографией _(размером не менее 600х600)_. 

`Она нам будет нужна для сайта ассоциации.`
"""

mes_praise_connect_portal = """
Как говорил один известный в узких кругах философ: 
💬💬💬
“Вы великолепны! Ваша интеграция в Гильдию проходит успешно!” 
💬💬💬
Теперь тебе доступен новый квест “Сила в знании”.
"""

mes_introduction_guild = """
Все члены Гильдии Интеграторов схожи не только в профессиональных интересах. Мы едины в наших ценностях и убеждениях. 

*Наша миссия как сообщества* - усилить IT-интеграторов за счет _объединения_, _коллективных ресурсов_, _профессионального 
нетворкинга_ и _структуризации отрасли_.

*Открытость, самореализация, взаимоподдержка, доверие, командность* - всё это теперь часть тебя, члена _Гильдии_. 

Подробнее о *миссии Гильдии* можно прочитать [здесь](https://gildin.ru). Как ознакомишься, напиши в чат слово _“Миссия”_
"""

mes_praise_introduction_guild = """
Как говорил тот же известный в узких кругах философ: 
💬💬💬
“Как волнительно, уровень вашей интеграции повысился!” 
💬💬💬
И как здорово, что и твой уровень становится выше!

_Ознакомься с правилами ношения_ [шильдика](https://docs.google.com/document/d/1XXzQaJdl6PbwWif8ORPM5soj7wD9h1RDcmuOeWCl4-M/edit)
"""

mes_introduction_regulation = """
Для любой организации важен фундамент, который обеспечивает порядок и регламентирует взаимоотношения между коллегами. 

И этот фундамент - *устав*.

Правила упрощают рабочее общение, а их знание помогает избежать неприятных ситуаций. 
Игра становится  легче, когда знаешь как играть _верно_?

Пожалуйста, ознакомься с *уставом Гильдии*. Его можно прочитать по [ссылке](https://gildin.ru/docs/ustav-gildii/). 

После прочтения напиши в этот чат _“Ознакомлен”_.
"""

mes_praise_introduction_regulation = """
Ты успешно прошел квест *“Сила - в знании!”*. Теперь эта сила - _в тебе_. `Используй ее во благо.`
"""

mes_look_points = """
Наша задача развивать рынок интеграторов и мы начинаем с себя. Для развития отрасли и каждого мы осуществляем 
совместные проекты в которых мы объединяемся.

Важно, что участие в активностях не только помогает тебе развиваться, но и позволят получать от нас _подарки_ в 
виде _баллов_. Их можно потратить на *платные курсы Гильдии*.

Ознакомиться с *системой баллов* и, после ознакомления, напиши _“Я готов сделать шаг”_
"""

mes_introduction_project = """
`Я очень рада, что тебе не терпиться поучаствовать в наших проектах)` 

Держи список актуальных проектов. Ты можешь написать в чате их руководителям и включится в работу. 

_Не забудь написать мне какой проект заинтересовал тебя больше всего._
"""

mes_praise_introduction_project = """
*Поздравляю!* Ты теперь не новичок, а активный член _нашей Гильдии_. 

И в честь завершения твоей интеграции, предлагаю пройти [тест]() и небольшой подарок к нему.
"""

mes_finish_state = """
`Ты любишь награды?`

Мы тоже! Поэтому готовы подарить тебе наш шильдик. Прими активное участие в обсуждении проекта 
и он - твой) Размести его у себя на сайте и все увидят, ты - один из нас!

Спасибо за твое время и вот обещанный подарок - 1⃣0⃣0⃣0⃣  _баллов_ на курсы.  

*Молодец что дошел будь активнее*
"""

router = Router()


# Присоединился по ссылке, отправляем задание "Представиться"
@router.callback_query(F.data == "connect_chat")
async def callback_connect_chat_guild(callback: types.CallbackQuery):
    await bitrix_call_func('crm.deal.update',
                           BitrixView.user.id_deal,
                           {
                               'STAGE_ID': BitrixView.stages["EnterChat"]
                           })
    await callback.message.answer(
        text=mes_about_user.format(Name=BitrixView.user.name),
        parse_mode="Markdown"
    )
    await callback.message.answer_sticker(FSInputFile('data/stickers/thanks.png'))
    await callback.message.answer(
        text=mes_about_user_2.format(Name=BitrixView.user.name),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Представился",
                                                                                 callback_data="imagine")]]),
        parse_mode="Markdown"
    )


@router.callback_query(F.data == "imagine")
async def callback_request_foto(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text=mes_request_foto.format(Name=BitrixView.user.name),
        parse_mode="Markdown"
    )
    await bitrix_call_func('crm.deal.update',
                           BitrixView.user.id_deal,
                           {
                               'STAGE_ID': BitrixView.stages["WriteComment"],
                               'COMMENTS': BitrixView.user.comment
                           })
    await state.set_state(PrimaryState.getFoto)


@router.callback_query(F.data == "connect_obit")
async def callback_connect_portal(callback: types.CallbackQuery):
    await callback.message.answer(mes_praise_connect_portal, parse_mode="Markdown")
    await bitrix_call_func('crm.deal.update',
                           BitrixView.user.id_deal,
                           {
                               'STAGE_ID': BitrixView.stages["SignPortal"]
                           })
    await callback.message.answer(
        text=mes_introduction_guild,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Миссия",
                                                                                 callback_data="mission")]]),
        parse_mode="Markdown"
    )


@router.callback_query(F.data == "mission")
async def callback_introduction_guild(callback: types.CallbackQuery):
    await callback.message.answer(
        text=mes_introduction_regulation,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Ознакомлен",
                                                                                 callback_data="learn_mission")]]),
        parse_mode="Markdown"
    )
    await bitrix_call_func('crm.deal.update',
                           BitrixView.user.id_deal,
                           {
                               'STAGE_ID': BitrixView.stages["IntroductionGuild"]
                           })


@router.callback_query(F.data == "learn_mission")
async def callback_introduction_shildic(callback: types.CallbackQuery):
    await callback.message.answer(
        text=mes_praise_introduction_guild,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Ознакомлен",
                                                                                 callback_data="learn_shildic")]]),
        parse_mode="Markdown"
    )


@router.callback_query(F.data == "learn_shildic")
async def callback_look_points(callback: types.CallbackQuery):
    await callback.message.answer(
        text="`Ура! Теперь мы с уверенностью можем доверить тебе использование отличительного знака.`",
        parse_mode="Markdown")
    await callback.message.answer_sticker(FSInputFile('data/stickers/hearts.png'))
    await callback.message.answer(mes_praise_introduction_regulation, parse_mode="Markdown")
    await bitrix_call_func('crm.deal.update',
                           BitrixView.user.id_deal,
                           {'STAGE_ID': BitrixView.stages["IntroductionRegulation"]})
    await callback.message.answer(
        text=mes_look_points,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Я готов сделать шаг",
                                                                                 callback_data="ready_step")]]),
        parse_mode="Markdown"
    )


@router.callback_query(F.data == "ready_step")
async def callback_introduction_project(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text=mes_introduction_project,
        reply_markup=markup.get_inline_keyboard([group['NAME'] for group in BitrixView.groups],
                                                ["group_" + group['ID'] for group in BitrixView.groups],
                                                "callback_data"),
        parse_mode="Markdown"
    )
    await bitrix_call_func('crm.deal.update',
                           BitrixView.user.id_deal,
                           {'STAGE_ID': BitrixView.stages["PushShildik"]})
    await callback.message.answer_sticker(FSInputFile('data/stickers/cash.png'),
                                          reply_markup=ReplyKeyboardMarkup(
                                              keyboard=[[KeyboardButton(text="Продолжим")]]))
    await state.set_state(PrimaryState.finishState)


@router.callback_query(F.data == "continue_integra")
async def finish_handlers(callback: types.CallbackQuery):
    await bitrix_call_func('crm.deal.update',
                           BitrixView.user.id_deal,
                           {'STAGE_ID': BitrixView.stages["Win"]})
    await callback.message.answer(mes_praise_introduction_project,
                                  reply_markup=markup.EMPTY,
                                  parse_mode="Markdown")
    await callback.message.answer_document(FSInputFile('data/shildic/shildic_dark.jpg'))
    await callback.message.answer_document(FSInputFile('data/shildic/shildic_white.jpg'))
    await callback.message.answer(mes_finish_state,
                                  reply_markup=markup.EMPTY,
                                  parse_mode="Markdown")
    await callback.message.answer_sticker(FSInputFile('data/stickers/okay.png'))
    await bitrix_call_func('crm.deal.update',
                           BitrixView.user.id_deal,
                           {'STAGE_ID': BitrixView.stages["PushShildik"]})
