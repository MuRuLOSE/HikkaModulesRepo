

# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# '''Если вы хотите взять какую то идею, то упомяните меня в коде, спасибо (но функцию пишите сами)'''

# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# Not licensed
# Идея @TbI_kosmoc
# meta developer: @bruhHikkaModules 

from hikkatl.types import Message
import asyncio
from .. import loader, utils


@loader.tds
class factorial(loader.Module):
    strings =  {
        "name": "factorial"
    }
    		
    @loader.command()
    async def factorial(self, message):
    	''' - [число] Вычисление факториала числа'''
    	try:
    		args = int(utils.get_args_raw(message))
    	except ValueError:
    		await utils.answer(message,"Введи просто число, и всё!")
    	b = args**args
    	await utils.answer(message,f"Факториал числа {args}: <code>{b}</code>")