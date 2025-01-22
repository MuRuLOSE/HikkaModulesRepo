from telethon.types import Message
from .. import loader, utils

import logging
import aiohttp
import os

"""
    ███    ███ ██    ██ ██████  ██    ██ ██       ██████  ███████ ███████
    ████  ████ ██    ██ ██   ██ ██    ██ ██      ██    ██ ██      ██  
    ██ ████ ██ ██    ██ ██████  ██    ██ ██      ██    ██ ███████ █████
    ██  ██  ██ ██    ██ ██   ██ ██    ██ ██      ██    ██      ██ ██  
    ██      ██  ██████  ██   ██  ██████  ███████  ██████  ███████ ███████ 

                                   
    Module Name
"""

# scopes:

# 🔒      Licensed under the GNU AGPLv3

# meta banner: link
# meta desc: desc
# meta developer: @BruhHikkaModules

logger = logging.getLogger(__name__)

class TothostAPI:
    def __init__(self, token):
        self._token = token

    async def logs(self, ub_id):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.tothost.live/api/v1/userbot/get_logs?userbotID={ub_id}&token={self._token}") as response:
                return bytes(await response.text(), encoding='utf-8')
            
    async def userbotstatus(self, ub_id):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.tothost.live/api/v1/userbot/status?userbotID={ub_id}&token={self._token}") as response:
                if dict(await response.json())['status'] == "active":
                    return True
                else:
                    return False
            
    async def userbotinfo(self, ub_id):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.tothost.live/api/v1/userbot/userbot_info?userbotID={ub_id}&token={self._token}") as response:
                data = await response.json()
                ubstatus = await self.userbotstatus(ub_id)
                enddate = data['endDate']
                
                info = {
                    "userbot": data['name'],
                    "emojistatus": "🟢" if ubstatus else "🔴",
                    "status": "Включен" if ubstatus else "Выключен",
                    "serveremoji": data['server']['emoji'],
                    "server": data['server']['text'],
                    "time": f"{enddate['year']}-{enddate['month']}-{enddate['day']} {enddate['hour']}:{enddate['minute']}:{enddate['second']}"
                }
                return info



@loader.tds
class ToTHosting(loader.Module):
    """Module for interaction with ToTHosting API (obviously) """

    strings = {
        "name": "ToTHosting",
        "userbot_info": (
            "<blockquote><b>🌟Информация о юзерботе🌟</b></blockquote>"
            "\n"
            "\n<blockquote><b>🤖 Юзербот: {}</b></blockquote>"
            "\n"
            "\n<blockquote><b>{} Статус: {}</b></blockquote>"
            "\n"
            "\n<blockquote><b>{} Сервер: {}</b></blockquote>"
            "\n"
            "\n<blockquote><b>⏰ Подписка истекает: <code>{}</code></b></blockquote>"
        )
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "token",
                "None",
                lambda: "Получите ваш токен в: https://t.me/ToThosTing_bot (/get_token)",
                validator=loader.validators.Hidden()
            )
        )

    @loader.loop(interval=5, autostart=True)
    async def autoupdatetoken(self):
        self.api = TothostAPI(token=self.config['token'])
    
    # async def client_ready(self, client, db):
        # self.get("token_ready", False) soon
        
        

    @loader.command()
    async def tinfo(self, message: Message):
        """ [id] - Get info about your userbot"""
        args = utils.get_args_raw(message)

        data = await self.api.userbotinfo(ub_id=args)

        await utils.answer(
            message,
            self.strings['userbot_info'].format(
                data['userbot'],
                data['emojistatus'],
                data['status'],
                data['serveremoji'],
                data['server'],
                data['time']
            )
        )

    @loader.command()
    async def tlogs(self, message: Message):
        ''' [id] - Get logs of your userbot'''
        args = utils.get_args_raw(message)

        logs = await self.api.logs(ub_id=args)

        with open("logs.html", "wb") as f:
            f.write(logs)
            await utils.answer_file(message, "logs.html" ,"<emoji document_id=5226512880362332956>📖</emoji> Here you go!")
            filename = f.name

        os.remove(filename)


        
