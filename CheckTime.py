from hikkatl.types import Message
from .. import loader, utils
import aiohttp
from ..inline.types import InlineCall
import datetime
import logging

# meta developer: @BruhHikkaModules

# required: aiohttp

logger = logging.getLogger(__name__)

@loader.tds
class CheckTime(loader.Module):
    """Check time in your city"""

    strings = {
        "name": "CheckTime",
        "right_setcity": "<b>Is this correct?</b> Timezone: {city}, If yes, press: <b>✅ Correct</b>",
        "button_right_setcity": "✅ Correct",
        "button_wrong_setcity": "❌ Wrong",
        "city_set": "🌆 <b>The default city is set!</b>",
        "time": "<b>Timezone:</b> {}\n<b>Time:</b> {}",
        "error": "🚫 <b>Something wrong!</b>\nYou may have entered the wrong time zone, if you can't resolve this, contact @BruhHikkaModules in the chat room",
        "select_tz": "<b>Select the time zone:</b>",
        "select_info": "<b>Select the information in the buttons:</b>",
        "general_info": "🌐 <b>General information:\n\nTime: <i>{}</i>\nDate: <i>{}</i>\nDay: <i>{}</i>\nTimezone: <i>{}</i>\nDay of the week: <i>{}</i></b>",
        "day_week" : ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    }

    strings_ru = {
        "right_setcity": "<b>Всё верно?</b> Часовой пояс: {city}, Если да, то нажмите: <b>✅ Верно</b>",
        "button_right_setcity": "✅ Верно",
        "button_wrong_setcity": "❌ Неверно",
        "city_set": "🌆 <b>Город по-улмочанию установлен!</b>",
        "time": "<b>Часовой пояс:</b> <i>{}</i>\n<b>Время:</b> <code>{}</code>",
        "error": "🚫 <b>Что-то пошло не так!</b>\nВозможно вы указали неверный часовой пояс, если вы не можете это решить, обратитесь в чат @BruhHikkaModules",
        "select_tz": "<b>Выберите часовой пояс</b>",
        "select_info": "<b>Выберите информацию рассположеную в кнопках:</b>",
        "general_info": "🌐 <b>Общая информация:\n\nВремя: <i>{}</i>\nДата: <i>{}</i>\nДень: <i>{}</i>\nЧасовой пояс: <i>{}</i>\nДень недели: <i>{}</i></b>",
        "day_week" : ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"],
        "_cls_doc": "Проверьте время в вашем городе"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "city",
                "Europe/Moscow",
                lambda: "For default city",
                validator=loader.validators.String()
            )
        )

    
    
    
        
    
    @loader.command(
        ru_doc=" [Часовой пояс] - Поставь свой город по-улмолчанию\nПример: .set_city Europe/Moscow",
    )
    async def setcity(self, message: Message):
        """ [Timezone] - Set your city to default\nExample: .set_city Europe/Moscow"""

        args = utils.get_args_raw(message)

        if not args:
            await self.inline.form(
                text=self.strings["select_tz"],
                message=message,

                reply_markup=[
                    [
                        {
                            "text": "America/Los Angeles",
                            "callback": self._setcity,
                            "args": ("America/Los_Angeles", )
                        },

                        {
                            "text": "Europe/Moscow",
                            "callback": self._setcity,
                            "args": ("Europe/Moscow", )
                        },

                        {
                            "text": "Europe/Kiyv",
                            "callback": self._setcity,
                            "args": ("Europe/Kiyv", )
                        }
                    ]
                ]
            )
            
        else:
            await self.inline.form(
                text=self.strings["right_setcity"].format(
                    city=args
                ),
                message=message,

                reply_markup=[
                    [
                        {
                            "text": self.strings["button_right_setcity"],
                            "callback": self._setcity,
                            "args": (args, )
                        },
                        {
                            "text": self.strings["button_wrong_setcity"],
                            "action": "close"
                        }
                    ]
                ]
            )


    @loader.command(
        ru_doc=" [Часовой пояс] - Узнать время"
    )
    async def showtime(self, message: Message):
        ''' [TimeZone] - Find out the time\nExample: .show_time Europe/Moscow'''

        args = utils.get_args_raw(message)
        default = self.config["city"]

        if not args:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'http://worldtimeapi.org/api/timezone/{default}') as response:
                    
                    if response.status != 200:
                        return await utils.answer(message,self.strings["error"])
                    
                    data = await response.json()
                    
                    datetimecity = data["datetime"]
                    abbreviation = data["abbreviation"]
                    day_of_week = data["day_of_week"]
                    day_of_year = data["day_of_year"]
                    tz = data["timezone"]
                    week_number = data["week_number"]



        else:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'http://worldtimeapi.org/api/timezone/{args}') as response:

                    if response.status != 200:
                        return await utils.answer(message,self.strings["error"])
                    
                    data = await response.json()
                    
                    datetimecity = data["datetime"]
                    abbreviation = data["abbreviation"]
                    day_of_week = data["day_of_week"]
                    day_of_year = data["day_of_year"]
                    tz = data["timezone"]
                    week_number = data["week_number"]
                    
                    


        await self.inline.form(
            text=self.strings["select_info"],
            message=message,

            reply_markup=[
                [
                    {
                        "text": "🌐 General",
                        "callback": self._general,
                        "args": ([datetimecity,abbreviation,day_of_week,day_of_year,tz,week_number], )
                    },

                    {
                        "text": "🕓 Time",
                        "action": "close"
                    }
                ]
            ]
        )
    
    async def _setcity(self, call: InlineCall, city: str):
        self.config["city"] = city

        await call.edit(self.strings["city_set"])

    async def _nothing(self, call: InlineCall):
        await call.answer("It's nothing, have a nice day :)")

    async def _general(self, call: InlineCall, data: list):
        datem = datetime.datetime.fromisoformat(data[0])

        
        await call.edit(
            reply_markup=[
                [
                    {
                        "text": "⏪ Back",
                        "callback": self._showtime_menu,
                        "args": (data, )
                    }
                ]
            ],
            text=self.strings["general_info"].format(
                datem.strftime("%H:%M"),
                datem.strftime("%d.%m.%Y"),
                data[3],
                data[4],
                self.strings["day_week"][data[2]]
        )
        )
    
    async def _showtime_menu(self, call: InlineCall, data: list):
        await call.edit(
            text=self.strings["select_info"],
            reply_markup=[
                [
                    {
                        "text": "🌐 General",
                        "callback": self._general,
                        "args": (data, )
                    },

                    {
                        "text": "❌ Close",
                        "action": "close"
                    }
                ]
            ]
        )

        
