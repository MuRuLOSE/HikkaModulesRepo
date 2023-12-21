from hikkatl.types import Message
from .. import loader, utils

'''
    ███    ███ ██    ██ ██████  ██    ██ ██       ██████  ███████ ███████
    ████  ████ ██    ██ ██   ██ ██    ██ ██      ██    ██ ██      ██  
    ██ ████ ██ ██    ██ ██████  ██    ██ ██      ██    ██ ███████ █████
    ██  ██  ██ ██    ██ ██   ██ ██    ██ ██      ██    ██      ██ ██  
    ██      ██  ██████  ██   ██  ██████  ███████  ██████  ███████ ███████ 


    K
    📜 Licensed under the GNU AGPLv3	
'''

# meta banner: https://0x0.st/HgME.jpg
# meta desc: K
# meta developer: @BruhHikkaModules


@loader.tds
class K(loader.Module):
    """K"""

    strings = {"name": "K", "K": "K"}

    @loader.command()
    async def k(self, message: Message):
        """K"""
        await utils.answer(message, self.strings["K"])
