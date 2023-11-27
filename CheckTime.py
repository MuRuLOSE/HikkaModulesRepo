from hikkatl.types import Message
from .. import loader, utils
import aiohttp
from ..inline.types import InlineCall
import datetime

# meta developer: @BruhHikkaModules

# required: aiohttp

@loader.tds
class CheckTime(loader.Module):
    """Check time in your city"""

    strings = {
        "name": "CheckTime",
        "right_setcity": "<b>Is this correct?</b> City: {city}, If yes, press: <b>✅ Correct</b>",
        "button_right_setcity": "✅ Correct",
        "button_wrong_setcity": "❌ Wrong",
        "city_set": "🌆 <b>The default city is set!</b>",
        "time": "<b>Timezone:</b> {}\n<b>Time:</b> {}",
        "error": "🚫 <b>Something wrong!</b>\nYou may have entered the wrong time zone, if you can't resolve this, contact @BruhHikkaModules in the chat room"
    }

    strings_ru = {
        "right_setcity": "<b>Всё верно?</b> Город: {city}, Если да, то нажмите: <b>✅ Верно</b>",
        "button_right_setcity": "✅ Верно",
        "button_wrong_setcity": "❌ Неверно",
        "city_set": "🌆 <b>Город по-улмолчанию установлен!</b>",
        "time": "<b>Часовой пояс:</b> <i>{}</i>\n<b>Время:</b> <code>{}</code>",
        "error": "🚫 <b>Что-то пошло не так!</b>\nВозможно вы указали неверный часовой пояс, если вы не можете это решить, обратитесь в чат @BruhHikkaModules",
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

        await self.inline.form(
            text=self.strings["right_setcity"].format(
                city=args
            ),
            message=message,

            reply_markup=[
                [
                    {
                        "text": self.strings["button_right_setcity"],
                        "callback": self.right,
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
                    time = data['datetime']
                    date = datetime.datetime.fromisoformat(time)
                    
                    result = date.strftime("%H:%M")



        else:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'http://worldtimeapi.org/api/timezone/{args}') as response:

                    if response.status != 200:
                        return await utils.answer(message,self.strings["error"])
                    
                    data = await response.json()
                    time = data['datetime']
                    date = datetime.datetime.fromisoformat(time)
                    
        result = date.strftime("%H:%M")

        await utils.answer(
            message,
            self.strings["time"].format(
                default or args,
                result
            )
        )

    async def right(self, call: InlineCall, city: str):
        self.config["city"] = city

        await call.edit(self.strings["city_set"])