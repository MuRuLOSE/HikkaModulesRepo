from hikkatl.types import Message
from .. import loader,utils

# meta developer: @BruhHikkaModules


@loader.tds
class GoogleQueryGen(loader.Module):
    """ - Create links for search engines query"""
    strings = {"name": "GoogleQueryGen"}
    strings_ru = {"_cls_doc": " - Создаёт ссылки для поисковых запросов"}

    @loader.command(ru_doc=" - [Аргументы] - Генерирует ссылку для гугл запроса")
    async def GoogleQueryGen(self, message: Message):
        """ - [Args] - Gen link for google query"""
        args_raw = utils.get_args_split_by(message," ")
        args = "+".join(args_raw)
        await utils.answer(message,f"https://google.com/search?q={args}")
    
    @loader.command(ru_doc=" - [Аргументы] - Генерирует ссылку для яндекс запроса")
    async def YandexQueryGen(self, message: Message):
        """ - [Args] - Gen link for yandex query"""
        args_raw = utils.get_args_split_by(message," ")
        args = "+".join(args_raw)
        await utils.answer(message,f"https://yandex.ru/search/?text={args}")

    @loader.command(ru_doc=" - [Аргументы] - Генерирует ссылку для бинг запроса")
    async def BingQueryGen(self, message: Message):
        """ - [Args] - Gen link for bing query"""
        args_raw = utils.get_args_split_by(message," ")
        args = "+".join(args_raw)
        await utils.answer(message,f"https://bing.com/search?q={args}")

    @loader.command(ru_doc=" - [Аргументы] - Генерирует ссылку для УткаУткаВперёд запроса")
    async def DDGQueryGen(self, message: Message):
        """ - [Args] - Gen link for DuckDuckGo query"""
        args_raw = utils.get_args_split_by(message," ")
        args = "+".join(args_raw)
        await utils.answer(message,f"https://duckduckgo.com/?q={args}")

    @loader.command(ru_doc=" - [Аргументы] - Генерирует ссылку для яху запроса")
    async def YahooQueryGen(self, message: Message):
        """ - [Args] - Gen link for yahoo query"""
        args_raw = utils.get_args_split_by(message," ")
        args = "+".join(args_raw)
        await utils.answer(message,f"https://search.yahoo.com/search?p={args}")

    
        