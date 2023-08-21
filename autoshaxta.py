
# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# '''Если вы хотите взять какую то идею, то упомяните меня в коде, спасибо (но функцию пишите сами)'''

# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# Not licensed
# meta developer: @bruhHikkaModules 
__version__ = (0,0,5)

from telethon.tl.types import Message, ChatAdminRights
from telethon import functions
import asyncio
from .. import loader, utils
import re

@loader.tds
class AutoShaxta(loader.Module): 
    """Модуль для авто выбора шахты"""

    strings = {
        "name": "AutoShaxta"
    }
    
    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "status_shaxta",
                False,
                lambda: None,
                validator=loader.validators.Boolean()
            )
        )
        
        
    @loader.watcher()
    async def watcher(self,message):
    	if message.chat_id == 5522271758 and "🔓 Открыта новая шахта:" in message.raw_text:
    		pattern =  "Открыта новая шахта: <code>(.*?)</code>"
    		match = re.search(pattern, message.text, re.DOTALL)
    		if match:
    			mine = match.group(1)
    		if self.config["status_shaxta"]:
    			self.client.send_message("@mine_evo_bot",mine)
    @loader.command()
    async def auto_shaxt(self,message):
    	''' - Включить выключить авто переключение шахты'''
    	self.config["status_shaxta"] = not self.config["status_shaxta"]
    	status = (
    	"<b>Включено авто переключение шахт</b>"
    	if self.config["status_shaxta"]
    	else "<b>Выключено авто переключение шахт</b>"
    	)
    	await utils.answer(message,status)
    
