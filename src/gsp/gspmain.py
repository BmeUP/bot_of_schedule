import platform
import gspread
import datetime
import asyncio
from src.bot.tokens import Apikeys
from src.db.database import s
from src.db.models.schedule_model import ScheduleTable
from ..db.models.users_time import UserTime
from ..bot.bot import bot
from .months import months


if 'MANJARO' in platform.release():
    fn = Apikeys.gspmain_test
else:
    fn = Apikeys.gspmain_prod

gc = gspread.service_account(filename=fn)

sh = gc.open("4. График работы Тверская")

m = datetime.datetime.now().month
y = datetime.datetime.now().year

current_date = f'{months.get(m)} {str(y)[2:]}'

dates = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
         20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]

async def send_notif_to_me():
    await bot.send_message(Apikeys.me, 'База данных обновлена.')

def get_sheet():
    with s as ss:
        ss.query(ScheduleTable).delete()
        ss.query(UserTime).delete()
        ss.commit()
    for i in sh.worksheets():
        if i.title == current_date:
            for lst in i.get_all_values():
                if 'Сотрудники' in lst[0]:
                    break
                else:
                    if lst[0] != '' \
                    and 'ГРАФИК' not in lst[0] \
                    and 'ФИО' not in lst[0]:
                        with s as ses:
                            record = ScheduleTable(fullname=lst[0], position=lst[1])
                            ses.add(record)
                            ses.flush()
                            for t, d in zip(lst[2:], dates):
                                user_time = UserTime(user_id=record.id, time=t, date=d)
                                ses.add(user_time)
                            ses.commit()
            asyncio.run(send_notif_to_me())
