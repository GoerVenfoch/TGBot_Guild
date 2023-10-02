from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.fsm.context import FSMContext

from other import PrimaryState
from view.contact import ContactUser

mes_connect_chat_guild = """
Очень приятно, {Name}!
И вот твоя первая миссия “Вступление в чат”.
Присоединись к закрытому чату Членов Гильдии по ссылке и нажми “Присоединился”
"""
mes_about_user = """
{Name}, отличное начало! А вот и твой первый подарок: 100 баллов на балланс! Мои
поздравления!
Как и куда ты их сможешь потратить я расскажу тебе чуть позже, не все сразу )
А прямо сейчас тебя ждет твоя новая миссия “Знакомство”.
Напиши в чате членов свое первое приветственное сообщение:
- поприветствуй коллег,
- расскажи из какой ты компании,
- чем она занимается,
- в чем твоя экспертность,
- какие уже есть достижения?
В общем, расскажи коллегам, каков он: {Name} - новый член Гильдии Интеграторов!
После прохождения этой миссии нажми “Представился”
"""
mes_request_foto = """
{Name}, я рада, что смогла узнать тебя получше! А чтобы стать к коллегам еще ближе, поделись со мной своей лучшей 
фотографией (размером не менее 600х600). Она нам будет нужна для сайта ассоциации.
"""
mes_request_logo = """
Ты любишь выделиться и хочешь чтобы другие это узнали? Отправь нам лого компании и 
мы добавим его на наш сайт, чтобы все узнали о тебе.
"""
mes_connect_portal = """
Мы как и любая гильдия имеем свою обитель, в ней не только уютно, но также много волшебных знаний. 
Проекции наших встреч,шаблоны договоров и многое другое помогут тебе сохранить чудесное настроение 
даже в самый хмурый день. Вот держи ссылку  и присоединяйся!
"""
mes_praise_connect_portal = """
Как говорил один известный в узких кругах философ: “Вы великолепны! Ваша интеграция в Гильдию проходит успешно!” 
Теперь тебе доступен новый квест “Сила в знании”.
"""
mes_introduction_guild = """
Все члены Гильдии Интеграторов схожи не только в профессиональных интересах. Мы едины в наших ценностях и убеждениях. 
Наша миссия как сообщества - усилить IT-интеграторов за счет объединения, коллективных ресурсов, профессионального 
нетворкинга и структуризации отрасли.

Открытость, самореализация, взаимоподдержка, доверие, командность - всё это теперь часть тебя, члена Гильдии. 
Подробнее о миссии Гильдии можно прочитать здесь. Как ознакомишься, напиши в чат слово “Миссия”
"""
mes_praise_introduction_guild = """
Как говорил тот же известный в узких кругах философ: “Как волнительно, уровень вашей интеграции повысился!” 
И как здорово, что и твой уровень становится выше!
"""
mes_introduction_regulation = """
Для любой организации важен фундамент, который обеспечивает порядок и регламентирует взаимоотношения между коллегами. 
И этот фундамент - устав. Правила упрощают рабочее общение, а их знание помогает избежать неприятных ситуаций. 
Игра становится  легче, когда знаешь как играть верно?
Пожалуйста, ознакомься с уставом Гильдии. Его можно прочитать по ссылке. После прочтения напиши в этот чат “Ознакомлен”.
"""
mes_praise_introduction_regulation = """
Ты успешно прошел квест “Сила - в знании!” Теперь эта сила - в тебе. Используй ее во благо.
"""
mes_look_points = """
Наша задача развивать рынок интеграторов и мы начинаем с себя. Для развития отрасли и каждого мы осуществляем 
совместные проекты в которых мы объединяемся.
Важно, что участие в активностях не только помогает тебе развиваться, но и позволят получать от нас подарки в 
виде баллов. Их можно потратить на платные курсы Гильдии.
Ознакомиться с системой баллов и, после ознакомления, напиши “Я готов сделать шаг”
"""
mes_introduction_project = """
Я очень рада, что тебе не терпиться поучаствовать в наших проектах) 
Держи список актуальных проектов. Ты можешь написать в чате их руководителям и включится в работу. 
Не забудь написать мне какой проект заинтересовал тебя больше всего.
"""
mes_praise_introduction_project = """
Поздравляю! Ты теперь не новичок, а активный член нашей Гильдии. 
И в честь завершения твоей интеграции, предлагаю пройти тест и небольшой подарок к нему.
"""
mes_finish_state = """
Ты любишь награды? Мы тоже! Поэтому готовы подарить тебе наш шильдик. Прими активное участие в обсуждении проекта 
и он- твой) Размести его у себя на сайте и все увидят, ты - один из нас!
Спасибо за твое время и вот обещанный подарок - 1000 баллов на курсы.  Молодец что дошел будь активнее
"""

router = Router()


# Получаем имя и отправляем ссылку
@router.message(PrimaryState.getName)
async def get_name_handler(message: Message, state: FSMContext):
    ContactUser.name = message.text
    await message.answer(
        text=mes_connect_chat_guild.format(Name=ContactUser.name),
        reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Присоединился")]])
    )
    await state.set_state(PrimaryState.connectChatGuild)


# Присоединился по ссылке, отправляем задание "Представиться"
@router.message(PrimaryState.connectChatGuild, F.text == "Присоединился")
async def get_connect_chat_guild(message: Message, state: FSMContext):
    await message.answer(
        text=mes_about_user.format(Name=ContactUser.name),
        reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Представился")]])
    )
    await state.set_state(PrimaryState.acquaintance)


@router.message(PrimaryState.acquaintance, F.text == "Представился")
async def request_foto(message: Message, state: FSMContext):
    await message.answer(
        text=mes_request_foto.format(Name=ContactUser.name),
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(PrimaryState.getFoto)


# Принимаем представление
@router.message(PrimaryState.acquaintance)
async def get_about_user(message: Message):
    ContactUser.about_user += message.text


@router.message(PrimaryState.getFoto, F.photo)
async def get_foto(message: Message, state: FSMContext):
    ContactUser.foto = message.photo[-1].file_id
    await message.answer("Классное фото))")
    await message.answer(mes_request_logo)
    await state.set_state(PrimaryState.getLogo)


@router.message(PrimaryState.getLogo, F.photo)
async def get_logo(message: Message, state: FSMContext):
    ContactUser.logo = message.photo[-1].file_id
    await message.answer(
        text=mes_connect_portal,
        reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Присоединился")]])
    )
    await state.set_state(PrimaryState.connectPortal)


@router.message(PrimaryState.connectPortal, F.text == "Присоединился")
async def get_connect_portal(message: Message, state: FSMContext):
    await message.answer(mes_praise_connect_portal)
    await message.answer(
        text=mes_introduction_guild,
        reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Миссия")]])
    )
    await state.set_state(PrimaryState.introductionGuild)


@router.message(PrimaryState.introductionGuild, F.text == "Миссия")
async def get_introduction_guild(message: Message, state: FSMContext):
    await message.answer(mes_praise_introduction_guild)
    await message.answer(
        text=mes_introduction_regulation,
        reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Ознакомлен")]])
    )
    await state.set_state(PrimaryState.look_points)


@router.message(PrimaryState.look_points, F.text == "Ознакомлен")
async def get_look_points(message: Message, state: FSMContext):
    await message.answer("Ура! Теперь мы с уверенностью можем доверить тебе использование отличительного знака.")
    await message.answer(mes_praise_introduction_regulation)
    await message.answer(
        text=mes_look_points,
        reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Я готов сделать шаг")]])
    )
    await state.set_state(PrimaryState.introductionProject)


@router.message(PrimaryState.introductionProject, F.text == "Я готов сделать шаг")
async def get_introduction_project(message: Message, state: FSMContext):
    await message.answer(
        text=mes_introduction_project,
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(PrimaryState.finishState)


@router.message(PrimaryState.finishState)
async def finish_handlers(message: Message):
    await message.answer(mes_praise_introduction_project)
    await message.answer(mes_finish_state)
