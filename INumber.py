from telethon.types import Message
from .. import loader, utils

import aiohttp

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
# meta desc: Facts about numbers, dates, years, etc
# meta developer: @BruhHikkaModules

class NumberAPI:
    async def _request(self, number: str='24', numbertype: str='trivia', random: bool=False):
        """Request function for NUMBER API

        Arguments:
            number {str} -- Number or date for which the fact should be (why date too? because it should be specified in month/day format)

        Keyword Arguments:
            numbertype {str} -- Type of fact (math, trivia, or date) (default: {'trivia'})
            random {bool} -- Should be fact is random (default: {False})
        """
        url = 'numbersapi.com/'
        if random:
            url += 'random/'
            match numbertype:
                case 'trivia':
                    url += 'trivia'
                case 'math':
                    url += 'math'
                case 'date':
                    url += 'date'
                case 'year':
                    url += 'year'
        else:
            url += number
            match numbertype:
                case 'trivia':
                    url += 'trivia'
                case 'math':
                    url += 'math'
                case 'date':
                    url += 'date'

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return response.text()

    async def trivia_fact(self, number, random: bool=True):
        if random:
            return self._request(random=True)
        else:
            return self._request(number=number)

    async def date_fact(self, date, random: bool=True):
        if random:
            return self._request(random=True, numbertype='date')
        else:
            return self._request(numbertype='date', number=date) # 1/12

    async def math_fact(self, number, random: bool=True):
        if random:
            return self._request(random=True, numbertype='math')
        else:
            return self._request(numbertype='math', number=number)

    async def year_fact(self):
        """ONLY RANDOM!!!"""
        return self._request(numbertype='year', random=True)
        

@loader.tds
class INumber(loader.Module):
    """Facts about numbers, dates, years, etc"""

    strings = {
        "name": "INumber",
        "type_not_exist": "<emoji document_id=5364261552515979078>😞</emoji> Fact type does not exist :("
    }
    strings_ru = {
        "type_not_exist": "<emoji document_id=5364261552515979078>😞</emoji> Тип факта не существует :("
    }

    @loader.command()
    async def randomfact(self, message: Message):
        """ - [Type of random facts (year, trivia, math, date)] Random fact about something"""
        args = utils.get_args_raw(message)
        api = NumberAPI()
        fact = ""
        match args:
            case 'year':
                fact = await api.year_fact()
            case 'trivia':
                fact = await api.trivia_fact(random=True)
            case 'math':
                fact = await api.math_fact(random=True)
            case 'date':
                fact = await api.date_fact(random=True)
            case _:
                return await utils.answer(
                    message,
                    self.strings("type_not_exist")
                )

        await utils.answer(
            message,
            await self._client.translate(
                message.peer_id,
                message,
                to_lang=self._db.get("hikka.translations", "lang")[0:2],
                raw_text=fact,
                entities=message.entities,
            ),
        )
