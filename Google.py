from hikkatl.types import Message
from .. import loader,utils

# meta developer: @BruhHikkaModules


@loader.tds
class GoogleQueryGen(loader.Module):
    """ - Create links for google query"""
    strings = {"name": "GoogleQueryGen"}
    strings_ru = {"_cls_doc": " - Создаёт ссылки для гугл запросов"}

    @loader.command(ru_doc=" - [Аргументы] - Генерирует ссылку для гугл запроса")
    async def GoogleQueryGen(self, message: Message):
        """ - [Args] - Gen link for google query"""
        args_raw = utils.get_args_split_by(message," ")
        args = "+".join(args_raw)
        await utils.answer(message,f"https://www.google.com/search?q={args}")
        