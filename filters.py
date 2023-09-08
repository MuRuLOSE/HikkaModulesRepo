from hikkatl.types import Message
from .. import loader, utils

# meta developer: @BruhHikkaModules

@loader.tds
class TextFilters(loader.Module):
    """ - Module for filter text """

    async def client_ready(self,db,client):
        self.db = db
        self.set("filter","Dont care")
    strings = {
        "name": "TextFilters", 
        "wrong": "Wrong Argument. \n\nupper - Capitalize\ncapitalize - Starts with a capital letter and the rest are small.\nlower - Reduces all letters",
        "correct": "Filter changed to {}"
    }
    strings_ru = {
        "wrong": "Неверный аргумент. \n\nupper - Большие буквы\ncapitalize - Начинает с большой буквы, а остальные маленькие\nlower - Уменьшает все буквы",
        "correct": "Фильтр сменён на {}"
    }

    @loader.watcher()
    async def watcher(self,message):
        me = await self.client.get_me(id)
        if message.from_id == me.user_id and message.text:
            filter_txt = self.get("filter","Dont care")

            if filter_txt == "lower":
                await message.edit(message.text.lower())

            elif filter_txt == "upper":
                await message.edit(message.text.upper())
            
            elif filter_txt == "capitalize":
                await message.edit(message.text.capitalize())

    @loader.command(ru_doc=" - [lower / capitalize / upper] - Выбрать фильтр")
    async def filter_ch(self, message: Message):
        """ - [lower / capitalize / upper] - Chose filter"""
        args = utils.get_args_raw(message)
        if args.lower() not in [lower,capitalize,upper]:
            await utils.answer(message,self.strings("wrong"))
        else:
            await utils.answer(message,self.strings("correct"))
            self.set("filter",args.lower())
