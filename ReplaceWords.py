from hikkatl.types import Message
from .. import loader, utils
import logging

from ..pointers import PointerDict

logger = logging.getLogger()

# meta developer: @BruhHikkaModules
@loader.tds
class ReplaceWords(loader.Module):
    """Replaces words"""

    async def client_ready(self,client,db):
        self.db = db
        self._words = PointerDict(self.db, module="ReplaceWordsNew", key="words",default={})

    strings = {
        "name": "ReplaceWords",
        "status": "Switch to True if you need to enable the module",
        "aleardy_exist": "The word already exists",
        "word_first": "The word {} will be replaced by the {}",
        "word_edit": "{} word edit to {}",
        "word_edit_err": "That word doesn't exist",
        "word_remove": "Word removed"
    }

    strings_ru = {
        "_cls_doc": "Заменяет слова",
        "status": "Переключите на True если вам нужно включить модуль",
        "aleardy_exist": "Слово уже существует",
        "word_first": "Слово {} Будет заменяться на {}",
        "word_edit": "Слово {} изменено на {}",
        "word_edit_err": "Этого слова нету",
        "word_remove": "Слово удалено"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "status",
                False,
                lambda: self.strings("status"),
                validator=loader.validators.Boolean()
            )
        )

    def check_word_in_dict(self,word):
        words = self._words

        if word in words.keys():
            return True
        else:
            return False
        
    @loader.watcher()
    async def watcher(self,message):
        words = self._words
        me = await self.client.get_me(id)
        user_id = me.user_id

        if (
            ''.join(list((words.keys()))) in message.text
            and self.config["status"] 
            and message.from_id == user_id
        ):

            wordslist = message.raw_text.split()

            keywordslist = list(filter(self.check_word_in_dict, wordslist))
                
            for raw_word in keywordslist:
                word = self._words.get(raw_word)
                new_text = message.raw_text.replace(raw_word,word)
            
            try:
                await utils.answer(message,new_text)
            except UnboundLocalError:
                pass

    @loader.command(
        ru_doc=" - Включить / Выключить замену слов"
    )
    async def enable_rw(self, message: Message):
        """ - Enable / Disable replace words"""
        status = self.config["status"]
        status = not status
        status_str = (
            "Авто замена слов включена"
            if status
            else "Авто замена слов выключена"
        ) 
        await utils.answer(message,status_str)

    @loader.command(
        ru_doc = " - [Слово] [Чем заменить] - Добавить слово"
    )
    async def add_word(self,message):
        ''' - [Word] [What to replace it with] - Add word'''
        args = utils.get_args_split_by(message," ")
        words = self._words
        if args[0] in words.keys():
            await utils.answer(message,self.strings("aleardy_exist"))
            return
        words.update({args[0]: args[1]})
        await utils.answer(
            message, 
            self.strings('word_first').format(
                args[0],args[1]
            )
        )

    @loader.command(
        ru_doc = " - [Слово] [На что изменить] - Изменить заменяемое слово"
    )
    async def edit_word(self,message):
        ''' - [Word] [What to edit it with] - Edit word'''
        args = utils.get_args_split_by(message," ")
        words = self._words.keys()

        if args[0] in words:
            self._words.update({args[0]:args[1]})
            word_edit = self.strings("word_edit")
            await utils.answer(
                message,
                self.strings("word_edit").format(
                    args[0],args[1]
                )
            )
        else:
            await utils.answer(message,self.strings("word_edit_err")) 
    
    @loader.command(
        ru_doc = " - [Слово] - Удалить слово"
    )
    async def remove_word(self,message):
        ''' - [word] - Remove word'''
        args = utils.get_args_raw(message)
        words = self._words
        if args.lower() in words.keys():
            self._words.pop(args.lower())
            await utils.answer(message,self.strings("word_remove"))
        else:
            await utils.answer(message,self.strings("word_edit_err"))

    @loader.command(
        ru_doc = " - Посмотреть все замены слов"
    )
    
    async def list_words(self,message):
        ''' - Watch all replaced words'''

        words = self._words
        words_str = ""
        for key, value in words.items():
            words_str += f"{key}: {value}\n"

        await utils.answer(message,words_str)

