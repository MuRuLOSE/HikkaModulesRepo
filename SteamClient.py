from hikkatl.types import Message
from .. import loader, utils
from steam_web_api import Steam
from datetime import datetime
import logging

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

logger = logging.getLogger(__name__)


@loader.tds
class SteamClient(loader.Module):
    """Module for manage steam"""

    strings = {
        "name": "SteamClient",
        "profile_data": "<emoji document_id=5936017305585586269>🪪</emoji> <b>Steam ID:</b> <code>{id}</code>"
        "\n<emoji document_id=5870994129244131212>👤</emoji> <b>Username:</b> <code>{username}</code>"
        "\n<emoji document_id=5933613451044720529>🙂</emoji> <b>Steam level:</b> <code>{level}</code>"
        "\n<emoji document_id=5879770735999717115>👤</emoji> <b>Profile URL:</b> <code>{profileurl}</code>"
        "\n<emoji document_id=5872829476143894491>🚫</emoji> <b>VAC-BAN INFO:</b> {vacinfo}"
        "\n<emoji document_id=5967412305338568701>📅</emoji> <b>Registration date:</b> <code>{registration_date}</code>",
        "api_key_updated": "<emoji document_id=5292226786229236118>🔄</emoji> <b>API key has been updated</b>",
        "vac_ban":
            "\n    <b>VACBanned</b>: <code>{vacbanned}</code>"
            "\n    <b>Number of VAC-BANs</b>: <code>{numberofvacbans}</code>"
            "\n    <b>Days since last VAC-BAN</b>: <code>{dayslastvac}</code>"
            "\n    <b>Number of game bans</b>: <code>{numberofgamebans}</code>",
        "vac_ban_title": "<b>Information about bans of</b> <code>{}</code>:",
        "game_info_title": "<b>Information about games of</b> <code>{}</code>",
        "game_info_template": 
            "\n    <b>Name:</b> <code>{name}</code>"
            "\n    <b>Total playtime:</b> <code>{playtime_forever}</code>minutes"
            "\n    <b>Played in the last two weeks:</b> <code>{playtime_2weeks}</code>minutes"
            "\n    <b>Last launch:</b> <code>{lastplay}</code>",
    }

    strings_ru = {
        "profile_data": "<emoji document_id=5936017305585586269>🪪</emoji> <b>Steam ID:</b> <code>{id}</code>"
        "\n<emoji document_id=5870994129244131212>👤</emoji> <b>Юзернейм:</b> <code>{username}</code>"
        "\n<emoji document_id=5933613451044720529>🙂</emoji> <b>Уроверь Steam:</b> <code>{level}</code>"
        "\n<emoji document_id=5879770735999717115>👤</emoji> <b>Профиль:</b> <code>{profileurl}</code>"
        "\n<emoji document_id=5872829476143894491>🚫</emoji> <b>VAC-BAN INFO:</b> {vacinfo}"
        "\n<emoji document_id=5967412305338568701>📅</emoji> <b>Дата регистрации:</b> <code>{registration_date}</code>",
        "api_key_updated": "<emoji document_id=5292226786229236118>🔄</emoji> <b>API ключ был обновлён</b>",
        "vac_ban":
            "\n    <b>VACBanned</b>: <code>{vacbanned}</code>"
            "\n    <b>Число VAC-BANов</b>: <code>{numberofvacbans}</code>"
            "\n    <b>Дни с последнего VAC-BANа</b>: <code>{dayslastvac}</code>"
            "\n    <b>Число игровых банов</b>: <code>{numberofgamebans}</code>",
        "vac_ban_title": "<b>Информация о банах</b> <code>{}</code>:",
        "game_info_title": "<b>Информация о играх</b> <code>{}</code>",
        "game_info_template": 
            "\n    <b>Название:</b> <code>{name}</code>"
            "\n    <b>Наиграно всего:</b> <code>{playtime_forever}</code>мин"
            "\n    <b>Наиграно за последние 2 недели:</b> <code>{playtime_2weeks}</code>мин"
            "\n    <b>Последний запуск:</b> <code>{lastplay}</code>",
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
        self.debug = False

    async def client_ready(self, db, client):
        self.steam = Steam(self.config["apikey"])

    def resolve_id(self, username):
        data = self.steam.users.search_user(username)
        return data["player"]["steamid"]

    @loader.command(
        ru_doc=" [Юзернейм] Найти пользователя (--id поиск по id)"
    )
    async def searchuser(self, message: Message):
        """ [Username] (--raw  raw json answer) (--id search by id) - Search user"""
        args = utils.get_args_raw(message).split()

        user = args[0]

        userdata = None
        if "--id" in args:
            userdata = self.steam.users.get_user_details(int(user))["player"]
            level = self.steam.users.get_user_steam_level(int(user))["player_level"]
            vacdata = self.steam.users.get_player_bans(int(user))["players"][0]

        else:
            userdata = self.steam.users.search_user(user)["player"]
            uid = self.resolve_id(user)
            level = self.steam.users.get_user_steam_level(uid)["player_level"]
            vacdata = self.steam.users.get_player_bans(uid)["players"][0]

        
        vacinfo = self.strings["vac_ban"].format(
            vacbanned=vacdata["VACBanned"],
            numberofvacbans=vacdata["NumberOfVACBans"],
            dayslastvac=vacdata["DaysSinceLastBan"],
            numberofgamebans=vacdata["NumberOfGameBans"]
        )

        account_created_date = datetime.fromtimestamp(userdata["timecreated"])
        account_created_formatted = account_created_date.strftime("%d.%m.%Y")
        await utils.answer_file(
            message,
            userdata["avatarfull"],
            caption=self.strings["profile_data"].format(
                id=userdata["steamid"],
                username=userdata["personaname"],
                level=level,
                profileurl=userdata["profileurl"],
                vacinfo=vacinfo,
                avatar=userdata["avatar"],
                registration_date=account_created_formatted,
            ),
        )

    @loader.command(
        ru_doc=" [Юзернейм] Информация о VAC-BANах пользователя (--id поиск по id)"
    )
    async def vacbaninfo(self, message: Message):
        ''' [Username] Informbation about user VAC-BANs (--id search by id)'''

        args = utils.get_args_raw(message).split()

        user = args[0]
        
        if "--id" in args:
            userdata = self.steam.users.get_user_details(int(user))["player"]
            vacdata = self.steam.users.get_player_bans(int(user))["players"][0]

        else:
            userdata = self.steam.users.search_user(user)["player"]
            uid = self.resolve_id(user)
            vacdata = self.steam.users.get_player_bans(uid)["players"][0]
        
        vacinfo = self.strings["vac_ban"].format(
            vacbanned=vacdata["VACBanned"],
            numberofvacbans=vacdata["NumberOfVACBans"],
            dayslastvac=vacdata["DaysSinceLastBan"],
            numberofgamebans=vacdata["NumberOfGameBans"]
        )
        vactitle = self.strings["vac_ban_title"]
        await utils.answer(
            message, 
            response=vactitle.format(userdata["personaname"]) + vacinfo
        )

    @loader.command(
        ru_doc=" - [Юзернейм] Информация о играх пользователя (--id поиск по id)"
    )
    async def gameownedlist(self, message: Message):
        ''' - [Username] Informbation about user games (--id search by id)'''

        args = utils.get_args_raw(message).split()

        user = args[0]
        
        if "--id" in args:
            userdata = self.steam.users.get_user_details(int(user))["player"]
            gamedata = self.steam.users.get_owned_games(user)['games']

        else:
            userdata = self.steam.users.search_user(user)["player"]
            uid = self.resolve_id(user)
            gamedata = self.steam.users.get_owned_games(uid)['games']
        
        # инфо о играх vacinfo = self.strings["vac_ban"].format(
            #vacbanned=vacdata["VACBanned"],
            #numberofvacbans=vacdata["NumberOfVACBans"],
            #dayslastvac=vacdata["DaysSinceLastBan"],
            #numberofgamebans=vacdata["NumberOfGameBans"]
        #)

        gameinfo_templates = [] 
        for info in gamedata:
            gameinfo = self.strings["game_info_template"].format(
                name=info['name'],
                playtime_forever=info['playtime_forever'],
                playtime_2weeks=info.get('playtime_2weeks') or 0,
                lastplay=info['rtime_last_played']
            )

            gameinfo_templates.append(gameinfo)

        print(gameinfo)
        logger.info(gameinfo.join('\n'))
    
        await utils.answer(
            message, 
            response=self.strings['game_info_title'].format(userdata["personaname"]) 
            + '\n\n'.join(gameinfo_templates)
        )

    @loader.command()
    async def execsteamcode(self, message: Message):
        ''' DO NOT USE THIS COMMAND! IT ONLY WORKS WHEN DEBUGGING IS ENABLED! THIS COMMAND IS FOR DEVELOPER'''
        if not self.debug:
            await utils.answer(
            message, 
            "this command does nothing if debug-mode is not enabled."
            "don't try to use it." 
            "even if you get into the code and enable debug-mode, all responsibility for actions with this command is yours."
            )
        else:
            environment = {
                'client': self.steam
            }
            args = utils.get_args_raw(message)

            await utils.answer(message, str(eval(args, environment)))

    @loader.command(
        ru_doc=" - Обновить API ключ"
    )
    async def updateapikey(self, message: Message):
        """ - Update API key"""
        self.steam = Steam(self.config["apikey"])
        await utils.answer(message, self.strings["api_key_updated"])
