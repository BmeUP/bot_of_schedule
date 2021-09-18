import logging
import datetime
import platform
from aiogram import types, Dispatcher
from aiogram.bot.bot import Bot
from ..db.database import s
from ..db.models.users_time import UserTime
from .tokens import Apikeys

if 'MANJARO' in platform.release():
    API_TOKEN = Apikeys.test
else:
    API_TOKEN = Apikeys.prod

# Configure logging
logging.basicConfig(encoding='utf-8', level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_using(message: types.Message):
    msg = 'Привет, Я твоя Булочка с Корицей!\n' + \
        'Буду помогать тебе с графиком. \n' + \
        'Нужно просто отправить мне цифру, к примеру 5, ' + \
        'и Я тебе скину актуальный график смен на этот день текущего месяца. \n' + \
        'Все просто, попробуй😘'

    await message.answer(msg)

@dp.message_handler(commands=['whoiam'])
async def get_myself(message: types.Message):
    me = message.from_user
    print(me)
    user_name = me.username if me.username else "Ника нет(\nНик можно установить в настройка в поле `username`"
    await message.answer(
        f"Ты {me.first_name}\nТвой ник - {user_name}\nТвой id - {me.id}"
        )

async def send_message_to_me(msg):
    await bot.send_message(
        Apikeys.me, f'{msg.from_user.first_name} - {msg.from_user.username} -' +\
                    f'{msg.text} - {datetime.datetime.now()}')

@dp.message_handler()
async def echo(message: types.Message):
    schedule_string = ''
    await send_message_to_me.__call__(message)
    if not message.text.isdigit():
        await message.answer('Необходимо ввести цифру')
    elif int(message.text) > 31:
        await message.answer('В месяце не может быть больше 31 дня.')
    else:
        usr_tim = s.query(UserTime).filter_by(date=message.text).all()
        for i in usr_tim:
            if i.time != '':
                schedule_string += f'{i.parent.fullname} {i.parent.position} {i.time} \n'
        await message.answer(schedule_string)
