from hikkatl.types import Message
from collections import Counter
import logging
from .. import loader, utils

logger = logging.getLogger(__name__)


'''
    ███    ███ ██    ██ ██████  ██    ██ ██       ██████  ███████ ███████
    ████  ████ ██    ██ ██   ██ ██    ██ ██      ██    ██ ██      ██  
    ██ ████ ██ ██    ██ ██████  ██    ██ ██      ██    ██ ███████ █████
    ██  ██  ██ ██    ██ ██   ██ ██    ██ ██      ██    ██      ██ ██  
    ██      ██  ██████  ██   ██  ██████  ███████  ██████  ███████ ███████ 


    Module name
    📜 Licensed under the GNU AGPLv3	
'''

# meta banner: link
# meta desc: desc
# meta developer: @BruhHikkaModules


@loader.tds
class MindGameCheat(loader.Module):
    """Module for cheat in MindGame"""

    strings = {
        "name": "MindGameCheat",
        "wait": "<emoji document_id=5188311512791393083>🔎</emoji> <b>Searching for emoji...</b>",
        "finded": "<emoji document_id=5206607081334906820>✔️</emoji> <b>The emoji has been found!</b>"
    }
    strings_ru = {
        "wait": "<emoji document_id=5188311512791393083>🔎</emoji> <b>Поиск эмоджи...</b>",
        "finded": "<emoji document_id=5206607081334906820>✔️</emoji> <b>Эмоджи найден!</b>"
    }

    @loader.command()
    async def mcheat(self, message: Message):
        """ - [reply to MindGame] - Find emoji"""
        await utils.answer(message, self.strings["wait"])

        reply = await message.get_reply_message()
        
        emojis = [
            button.text
            for row in reply.reply_markup.rows
            for button in row.buttons
        ]

        counter = Counter(emojis)
        different_emoji = ''.join([emoji for emoji, count in counter.items() if count == 1])

        emoji_index = emojis.index(different_emoji)

        await reply.click(emoji_index)

        await utils.answer(message, self.strings['finded'])


