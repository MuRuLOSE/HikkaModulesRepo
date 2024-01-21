from .. import loader
from telethon.types import Message


class CommonLib(loader.Library):
    '''Lib for modules with common items, like topic resolver.'''
    developer = "@MuRuLOSE"

    async def _topic_resolver(self, message: Message):
        if message.reply_to.forum_topic:
            topic_id = message.reply_to.reply_to_top_id
            return topic_id

