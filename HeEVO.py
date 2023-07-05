

# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# '''Если вы хотите взять какую то идею, то упомяните меня в коде, спасибо (но функцию пишите сами)'''

# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# Not licensed
# meta developer: @bruhHikkaModules 
__version__ = (0,0,1)

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
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "autouplvl",
                False,
                lambda: self.strings["upstat"],
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "autouplvl_interval",
                1800,
                lambda: self.strings["autouplvl_interval"],
                validator=loader.validators.Integer()
            ),
            loader.ConfigValue(
               "bursborauto",
                False,
                lambda: self.strings["bursborauto"],
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "interval_bursborauto",
                3600,
                lambda:  self.strings['interval_bursborauto'],
                validator=loader.validators.Integer()
           ),
           loader.ConfigValue(
                "burzapravauto",
                False,
                lambda: self.strings["burzapravauto"],
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "interval_burzapravauto",
                3600,
                lambda:  self.strings["interval_burzapravauto"],
                validator=loader.validators.Integer()
           )
        )

    @loader.command()
    async def autouplvl(self, message):
    	'''Включить автоповышение уровня'''
    	interval = self.config['autouplvl_interval']
    	autouplvl = self.config['autouplvl']
    	if autouplvl == True:
    		await utils.answer(message,"Запущено автоповышение уровня")
    	while autouplvl:
    		await asyncio.sleep(interval)
    		async with self.client.conversation("@mine_evo_bot") as conv:
    			await conv.send_message("ур") 
    			response = await conv.get_response()
    			find = response.text.count("✅")
    			if find == 2:
    				await response.click(0)
    	if autouplvl == False:
    		await utils.answer(message,"У вас выключена функция заправки, в конфиге она называется <b>autouplvl</b>\n\n<i>Скоро будет выключение/включение по команде.</i>")
    
    @loader.command()
    async def Bautosbor(self, message):
    	''' - Включить автосбор ресурсов с бура'''
    	interval = self.config['interval_bursborauto']
    	sbor = self.config['bursborauto']
    	if sbor == True:
    		await utils.answer(message,"Запущено автосбор с бура")
    	while sbor:
    		await asyncio.sleep(interval)
    		async with self.client.conversation("@mine_evo_bot") as conv:
    			await conv.send_message("Мой бур")
    			response = await conv.get_response()
    			await response.click(0)
    	if sbor == False:
    		await utils.answer(message,"У вас выключена функция заправки, в конфиге она называется <b>bursborauto</b>\n\n<i>Скоро будет выключение/включение по команде.</i>")
    		
    @loader.command()
    async def Baurozapr(self, message):
    	''' - Включить автозаправку бура'''
    	interval = self.config['interval_burzapravauto']
    	zapr = self.config['burzapravauto']
    	if zapr == True:
    		await utils.answer(message,"Запущен автозаправщик бура")
    	while zapr:
    		await asyncio.sleep(interval)
    		async with self.client.conversation("@mine_evo_bot") as conv:
    			await conv.send_message("Мой бур")
    			response = await conv.get_response()
    			await response.click(1)
    	if zapr == False:
    		await utils.answer(message,"У вас выключена функция заправки, в конфиге она называется <b>burzapravauto</b>\n\n<i>Скоро будет выключение/включение по команде.</i>")