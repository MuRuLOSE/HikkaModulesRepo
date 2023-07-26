# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# '''Если вы хотите взять какую то идею, то упомяните меня в коде, спасибо (но функцию пишите сами)'''

# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# Not licensed
# meta developer: @bruhHikkaModules 
version = (0,0,5)

from telethon.tl.types import Message
from telethon import functions
import asyncio
from .. import loader, utils
import re
@loader.tds
class PerevodLimitsX(loader.Module): 
    """Модуль для перевода лимитов по новой системе Читайте .faq"""

    strings = {
        "name": "PerevodLimitsX",
        "time_perevod": "Задержка перевода"
    }

    async def client_ready(self, client, db):
        self._db = db
    
    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "time_perevod",
                2.0,
                lambda: self.strings["time_perevod"],
                validator=loader.validators.Float()
            )
        )
    
        
    @loader.command()
    async def perevodx(self,message):
     ''' - [Ник перевода] [Сколько переводить] - Перевод лимитов'''
     args = utils.get_args_split_by(message, " ")
     async with self.client.conversation("@mine_evo_bot") as conv:
        await conv.send_message("б")
        res = await conv.get_response()
        pattern = "<b>Баланс:</b>  (.*?)\n"
        match = re.search(pattern, res.text,re.DOTALL)
        if match:
        	balance = match.group(1)
        balance = match.group(1)
        await conv.send_message(f"Перевести {args[0]} {balance}")
        res = await conv.get_response()
        pattern = "\n(.*?)$"
        match = re.search(pattern, res.message, re.DOTALL)
        if match:
        	sum = match.group(1)
        else:
        	хуй

        conv.cancel()
        ost = 0
        self._db.set(__name__,"full",args[1])
        for i in range(int(args[1])):
        	self._db.get(__name__,"ost",0)
        	await self.client.send_message("@mine_evo_bot",f"Перевести {args[0]} {sum}")
        	await asyncio.sleep(self.config["time_perevod"])
        	ost += 1
        	self._db.set(__name__,"ost",ost)
        self._db.set(__name__,"ost",0)
        self._db.set(__name__,"full",0)
       	
       	
  
    
    @loader.command()
    async def perevfaq(self,message):
      ''' - FAQ по этому модулю'''
      await utils.answer(message, "Этот модуль предназначен для новой системы перевода лимитов, обновлятся лимиты по мере обновления уровня не будет, потому что в этом и был смысл убирания лимитов.\nРекомендуется запускать не больше одного перевода. Иначе это поломает счетчик")
     
    @loader.command()
    async def limits(self,message):
    	''' - Посмотреть сколько осталось лимитов перевести'''
    	full = self._db.get("full",0)
    	ost = self._db.get("ost",0)
    	await utils.answer(message,f"Осталось: <code>{ost}/{full}</code>")