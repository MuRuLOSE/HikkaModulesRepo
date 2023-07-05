

# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# '''Если вы хотите взять какую то идею, то упомяните меня в коде, спасибо (но функцию пишите сами)'''

# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# Not licensed
# meta developer: @bruhHikkaModules 
__version__ = (0,2,0)

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
        "interval_burzapravauto": "Укажите интервал заправки бура\nВ секундах",
        "hi": "Показывать приветственное сообщение?"
    }
    
    
    def __init__(self):
        
        self.autouplvl1 = False
        self.bursborauto1 = False
        self.burzaprauto1 = False
        self.config = loader.ModuleConfig(
            
            loader.ConfigValue(
                "autouplvl_interval",
                1800,
                lambda: self.strings["autouplvl_interval"],
                validator=loader.validators.Integer()
            ),
            loader.ConfigValue(
                "hi",
                True,
                lambda: self.strings["hi"],
                validator=loader.validators.Boolean()
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
        
    async def client_ready(self):
        	if self.config["hi"] == True:
        		self.message2 = await self.client.send_message("me","<b><emoji document_id=5278312084327636289>❤️\u200d🔥</emoji> Приветик! Спасибо за установку модуля HeEVO</b>\n\nЯ сейчас рад что вы видите это сообщение, потому что вы установили мой модуль <b>HeEVO</b>\n\nЭто сообщение будет отправлено всего один раз, и только в избранное.\n\n<emoji document_id=5362088337718909649>\U0001fae2</emoji> <b>Ладно, не буду засорять избранное, можешь удалять) Пока 🥰")
        		self.message1 = await self.client.send_message("me","<emoji document_id=5271531301629866501>🔶</emoji><emoji document_id=5273719407078552078>🔶</emoji><emoji document_id=5273786202409938995>🔶</emoji><emoji document_id=5271531301629866501>🔶</emoji><emoji document_id=5271508486763589107>🔶</emoji><emoji document_id=5271981431382355955>🔶</emoji><emoji document_id=5271871458744741066>‼️</emoji><emoji document_id=5274110571225034474>🔶</emoji>\n<emoji document_id=5271508486763589107>🔶</emoji><emoji document_id=5273924616320987261>🔶</emoji><emoji document_id=5273913397866410397>🔶</emoji><emoji document_id=5271871458744741066>🔶</emoji><emoji document_id=5273860183221612720>🔶</emoji><emoji document_id=5271871458744741066>🔶</emoji><emoji document_id=5271567770197175320>🔶</emoji><emoji document_id=5271694871164368298>🔶</emoji><emoji document_id=5274063219210596376>🔶</emoji><emoji document_id=5271871458744741066>🔶</emoji><emoji document_id=5273924616320987261>🔶</emoji><emoji document_id=5271851551571326099>🔶</emoji><emoji document_id=5273730853166396176>🔶</emoji><emoji document_id=5271972682533974848>🔶</emoji><emoji document_id=5274030044883201235>🔶</emoji>")
        		self.config["hi"] = False

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