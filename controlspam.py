from hikkatl.types import Message
from .. import loader, utils

# meta developer: @BruhHikkaModules

@loader.tds
class ControlSpam(loader.Module):
    """Не просто спамь, а контролируй"""
    strings = {"name": "ControlSpam", "hello": "Hello world!"}
    strings_ru = {"hello": "Привет мир!"}

    

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "status",
                True,
                lambda: "Просто статус спама",
                validator=loader.validators.Boolean()
            )
        ) 
    @loader.command()
    async def spam(self, message: Message):
        """ [текст] [количество спама] - Начать спам"""
        self.config["status"] = True
        args = utils.get_args_split_by(message," ")
        a = 0
        while self.config["status"]:
            a += 1
            await self.client.send_message(message.chat_id,args[0])
            if a > int(args[1]):
                break
    
    @loader.command()
    async def spam_stop(self, message: Message):
        ''' - Закончить весь спам'''
        self.config["status"] = False
        await utils.answer(message,"Я закончил спамить")

    