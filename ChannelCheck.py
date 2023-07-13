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
class ChannelCheck(loader.Module): 
    """Модуль для получении информации о нахождении человека в канале."""

    strings = {
        "name": "ChannelCheck",
        "not_channel": f" Not in the channel ",
        "in_channel": f" Located in the channel ",
    }
    strings_ru = {
        "not_channel": f" Не находится в канале ",
        "in_channel": f" Находится в канале "
    }
    
    

        
    @loader.command()
    async def checksub(self,message):
    	''' [айди или юзернейм канала] [юзернейм или айди человека]- Проверить, находится ли человек в указанном вами канале '''
    	status = None
    	args = utils.get_args_raw(message)
    	user_info = args.split()[1]
    	channel_info = args.split()[0]
    	
    	channel = await self.client.get_entity(channel_info)
    	user = await self.client.get_entity(user_info)
    	
    	check_user = await self.client.get_participants(channel)
    	check_member = any(participant.id == user.id for participant in check_user)
    	if check_member:
    		status = self.strings["in_channel"]
    		await utils.answer(message,f"🥳 <b>{user.username}</b>{status}<b>{channel.title}</b>")
    	else:
    		status = self.strings["not_channel"]
    		await utils.answer(message,f"😓 <b>{user.username}</b>{status}<b>{channel.title}</b>")
    	