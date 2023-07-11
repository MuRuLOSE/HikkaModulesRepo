# meta developer: @MuRuLOSE

from hikkatl.types import Message
from .. import loader, utils 
import asyncio

@loader.tds
class ShowRules(loader.Module):
    """Модуль для показывания правил"""

    strings = {
        "name": "ShowRules",
        "id_group": "Specify your group id for rules",
        "change_it_text": "Change rules text in config",
        "rules_text": "Specify your rules",
        "rules_changed": "Rules changed"
    }
                                                          
    strings_ru = {
        "id_group": "Укажите айди группы для правил",
        "change_it_text": "Поменяйте текст правил в конфиге",
        "rules_text": "Укажите ваши правила",
        "rules_changed": "Правила изменены"
    }
    
    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
               "ID_GROUP",
                12345678,
                lambda: self.strings["id_group"],
                validator=loader.validators.TelegramID()
            ),
            loader.ConfigValue(
               "RULES_TEXT",
               "|_/|_|\_|",
               lambda: self.strings["rules_text"],
               validator=loader.validators.String()
           )
       )
            
    @loader.watcher()
    async def watcher(self,message):
    	strings = self.strings
    	cfg = self.config
    	if message.chat_id == cfg["ID_GROUP"] and message.text == "/rules".lower():
    		await self.client.send_message(entity=message.chat.id,message=cfg["RULES_TEXT"],reply_to=message.id)
    @loader.command(alias="ыуекгдуы", ru_doc="Написать правила")
    async def setrules(self, msg: Message):
        """Write rules""" 
        strings = self.strings
        args = utils.get_args_raw(msg)
        self.config["RULES_TEXT"] = args
        await utils.answer(msg,strings["rules_changed"])
        