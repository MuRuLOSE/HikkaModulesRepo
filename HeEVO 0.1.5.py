

# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# '''Если вы хотите взять какую то идею, то упомяните меня в коде, спасибо (но функцию пишите сами)'''

# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# Not licensed
# meta developer: @bruhHikkaModules 
__version__ = (0,1,5)

from hikkatl.types import Message
import asyncio
from .. import loader, utils


@loader.tds
class HeEVO(loader.Module): # думал назвать HuEVO - типо хуево
    """Модуль для облегчения игрового процесса в боте: @mine_evo_bot"""

    strings = {
        "name": "HeEVO", 
        "upstat": "Включить авто повышение уровня?",
        "autouplvl_interval": "Интервал авто повышения уровня\nВ секундах",
        "bursborauto": "Собирать автоматически ресурсы (плазма, руда) с бура?",
        "interval_bursborauto": "Укажите интервал сбора ресурсов в буре\nВ секундах",
        "burzapravauto": "Заправлять автоматически бур нефтью?",
        "interval_burzapravauto": "Укажите интервал заправки бура\nВ секундах"
    }
    
    
    def __init__(self):
        self.autouplvl1 = False
        self.bursborauto1 = False
        self.burzaprauto1 = False
        self.hi = False
        self.config = loader.ModuleConfig(
            
            loader.ConfigValue(
                "autouplvl_interval",
                1800,
                lambda: self.strings["autouplvl_interval"],
                validator=loader.validators.Integer()
            ),
            loader.ConfigValue(
                "interval_bursborauto",
                3600,
                lambda:  self.strings['interval_bursborauto'],
                validator=loader.validators.Integer()
           ),
            loader.ConfigValue(
                "interval_burzapravauto",
                3600,
                lambda:  self.strings["interval_burzapravauto"],
                validator=loader.validators.Integer()
           )
        )
        
        async def client_ready(self,message):
        	if self.autouplvl1 == True:
        		while self.autouplvl1:
        			await asyncio.sleep(interval)
        			async with self.client.conversation("@mine_evo_bot") as conv:
        				await conv.send_message("ур") 
        				response = await conv.get_response()
        				find = response.text.count("✅")
        				if find == 2:
        					await response.click(0)

    @loader.command()
    async def autouplvl(self, message):
    	'''Включить автоповышение уровня'''
    	interval = self.config['autouplvl_interval']
    	self.autouplvl1 = not self.autouplvl1
    	status = (
    	    "| <b>Запущено автоповышение уровня</b>"
    	    if self.autouplvl1
    	    else "| <b>Выключено автоповышение уровня...</b>"
    	)
    	await utils.answer(message,f"<emoji document_id=5827738598778080268>ℹ️</emoji> {status}")
    	while self.autouplvl1:
    		await asyncio.sleep(interval)
    		async with self.client.conversation("@mine_evo_bot") as conv:
    			await conv.send_message("ур") 
    			response = await conv.get_response()
    			find = response.text.count("✅")
    			if find == 2:
    				await response.click(0)
    @loader.command()
    async def Bautosbor(self, message):
    	''' - Включить автосбор ресурсов с бура'''
    	interval = self.config['interval_bursborauto']
    	self.bursborauto1 = not self.bursborauto1
    	status = (
    	    "| <b>Запущен автосбор ресурсов</b>"
    	    if self.bursborauto1
    	    else "| <b>Выключен автосбор ресурсов...</b>"
    	)
    	await utils.answer(message,f"<emoji document_id=5827738598778080268>ℹ️</emoji> {status}")
    	while self.bursborauto1:
    		await asyncio.sleep(interval)
    		async with self.client.conversation("@mine_evo_bot") as conv:
    			await conv.send_message("Мой бур")
    			response = await conv.get_response()
    			await response.click(0)
    		
    @loader.command()
    async def Bautozapr(self, message):
    	''' - Включить автозаправку бура'''
    	interval = self.config['interval_burzapravauto']
    	self.burzaprauto1 = not self.burzaprauto1
    	status = (
    	    "| <b>Запущен автосбор ресурсов</b>"
    	    if self.burzaprauto1
    	    else "| <b>Выключен автосбор ресурсов...</b>"
    	)
    	await utils.answer(message,f"<emoji document_id=5827738598778080268>ℹ️</emoji> {status}")
    	while self.burzaprauto1:
    		await asyncio.sleep(interval)
    		async with self.client.conversation("@mine_evo_bot") as conv:
    			await conv.send_message("Мой бур")
    			response = await conv.get_response()
    			await response.click(1)