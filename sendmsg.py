__version__ = (0,1,0)
# meta developer: @bruhHikkaModules
import telethon
import asyncio
from telethon import events,functions
from telethon.tl.types import Message, ChatAdminRights
from .. import loader, utils

@loader.tds
class SendMSGA(loader.Module):
	'''Модуль для отправки сообщений, куда угодно, кому угодно'''
	strings = {
	    "name": "SendMSGA",
	    "fast_username1": "Запишите тут первый важный юзернейм!\nОбозначается как I",
	    "fast_username2": "Запишите тут второй важный юзернейм!\nОбозначается как II",
	    "fast_username3": "Запишите тут третий важный юзернейм!\nОбозначается как III"
	}
	
	def __init__(self):
		self.config = loader.ModuleConfig(
		    loader.ConfigValue(
		        "fusername",
		        "me",
		        lambda: self.strings("fast_username1"),
		        validator=loader.validators.String()
		    ),
		    loader.ConfigValue(
		        "fusername2",
		        "me",
		        lambda: self.strings("fast_username2"),
		        validator=loader.validators.String()
		    ),
		    loader.ConfigValue(
		        "fusername3",
		        "me",
		        lambda: self.strings("fast_username3"),
		        validator=loader.validators.String()
		    ),
		)
	
	@loader.command()
	async def SendMSG(self,message):
		''' - Команда для отправки сообщений\nHапишите её если хотите посмотреть пример'''
		I = self.config["fusername"]
		II = self.config["fusername2"]
		III = self.config["fusername3"]
		error = False
		args = utils.get_args_raw(message)
		try:
			send_to = args.split()[0]
			if send_to.lower() == "i":
				send_to = I
			if send_to.lower() == "ii":
				send_to = II
			if send_to.lower() == "iii":
				send_to = III
		except IndexError as e:
			error = True
			await utils.answer(message,f"Пример команды:\n .sendmsg me 1234\n Вместо me юзернейм, вместо 1234 ваш текст")
		message.message = " ".join(args.split()[1:])
		try:
			if error == False:
				await message.client.send_message(send_to,message.message)
		except ValueError as e:
			error = True
			await utils.answer(message,f" | Ошибка ValueError:\n<code>{e}</code>\n\nЭта ошибка скорее всего вызвана тем что вы написали неверный юзернейм в первом аргументе, но разработчик не может учесть все ошибки, поэтому переведите ошибку.")
		except Exception as e:
			error = True
			await utils.answer(message,f" | Непредвиденная ошибка:\n<code>{e}</code>\n\nСообщите об этой ошибке разработчику модуля! @MuRuLOSE")
		if error == False:
			await utils.answer(message,"Сообщение успешно отправлено")
		
		