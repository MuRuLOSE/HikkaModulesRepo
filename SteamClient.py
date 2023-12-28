from hikkatl.types import Message
from .. import loader, utils
from steam import Steam
from datetime import datetime

"""
    ███    ███ ██    ██ ██████  ██    ██ ██       ██████  ███████ ███████
    ████  ████ ██    ██ ██   ██ ██    ██ ██      ██    ██ ██      ██  
    ██ ████ ██ ██    ██ ██████  ██    ██ ██      ██    ██ ███████ █████
    ██  ██  ██ ██    ██ ██   ██ ██    ██ ██      ██    ██      ██ ██  
    ██      ██  ██████  ██   ██  ██████  ███████  ██████  ███████ ███████ 


    Module name
    📜 Licensed under the GNU AGPLv3	
"""

# meta banner: link
# meta desc: desc
# meta developer: @BruhHikkaModules
# requires: python-steam-api beautifulsoup4


@loader.tds
class SteamClient(loader.Module):
    """Module for manage steam"""

    strings = {
        "name": "SteamClient",
        "profile_data": "<emoji document_id=5936017305585586269>🪪</emoji> <b>Steam ID:</b> <code>{id}</code>"
        "\n<emoji document_id=5870994129244131212>👤</emoji> <b>Username:</b> <code>{username}</code>"
        "\n<emoji document_id=5879770735999717115>👤</emoji> <b>Profile URL:</b> <code>{profileurl}</code>"
        "\n<emoji document_id=5967412305338568701>📅</emoji> <b>Registration date:</b> <code>{registration_date}</code>",
        "api_key_updated": "<emoji document_id=5292226786229236118>🔄</emoji> <b>API key has been updated</b>",
    }

    strings_ru = {
        "profile_data": "<emoji document_id=5936017305585586269>🪪</emoji> <b>Steam ID:</b> <code>{id}</code>"
        "\n<emoji document_id=5870994129244131212>👤</emoji> <b>Юзернейм:</b> <code>{username}</code>"
        "\n<emoji document_id=5879770735999717115>👤</emoji> <b>Профиль:</b> <code>{profileurl}</code>"
        "\n<emoji document_id=5967412305338568701>📅</emoji> <b>Дата регистрации:</b> <code>{registration_date}</code>",
        "api_key_updated": "<emoji document_id=5292226786229236118>🔄</emoji> <b>API ключ был обновлён</b>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "apikey",
                "Here's your api key",
                "About API key: https://steamcommunity.com/dev/apikey",
                validator=loader.validators.Hidden(),
            )
        )

        self.steam = Steam(self.config["apikey"])

    def resolve_id(self, username):
        data = self.steam.users.search_user(username)
        data["player"]["steamid"]

    @loader.command(
        ru_doc=" [Юзернейм] (--raw если ты хочешь сырой ответ) - Найти пользователя"
    )
    async def searchuser(self, message: Message):
        """ [Username] (--raw if you want just raw json answer) - Search user"""
        args = utils.get_args_raw(message).split()

        user = args[0]
        userdata = self.steam.users.search_user(user)["player"]
        if "--raw" in args:
            return await utils.answer(
                message, f"<pre><code class='language-json'>{userdata}</code></pre>"
            )
        else:
            account_created_date = datetime.fromtimestamp(userdata["timecreated"])
            account_created_formatted = account_created_date.strftime("%d.%m.%Y")
            await utils.answer_file(
                message,
                userdata["avatarfull"],
                caption=self.strings["profile_data"].format(
                    id=userdata["steamid"],
                    username=userdata["personaname"],
                    profileurl=userdata["profileurl"],
                    avatar=userdata["avatar"],
                    registration_date=account_created_formatted,
                ),
            )

    @loader.command(
        ru_doc=" - Обновить API ключ"
    )
    async def updateapikey(self, message: Message):
        """ - Update API key"""
        self.steam = Steam(self.config["apikey"])
        await utils.answer(message, self.strings["api_key_updated"])
