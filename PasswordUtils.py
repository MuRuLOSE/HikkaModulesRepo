from hikkatl.types import Message
from .. import loader, utils
import string, random


@loader.tds
class PasswordUtils(loader.Module):
    """Ваш помощник в безопасных паролях"""
    strings = {"name": "PasswordUtils"}

    @loader.command(
        ru_doc=" - [Пароль] - Проверить пароль на безопасность"
    )
    async def passwordchecker(self, message: Message):
        """ - [Password] - Check the password for security"""
        args = utils.get_args_raw(message)
        symbols = "!@#$%^&*-+"
        balls = 0

        has_lower = any(c in args for c in string.ascii_lowercase)
        has_upper = any(c in args for c in string.ascii_uppercase)
        has_digit = any(c in args for c in string.digits)
        has_symbol = any(c in args for c in symbols)

        if has_lower:
            balls += 1
        if has_upper:
            balls += 1
        if has_digit:
            balls += 1
        if has_symbol:
            balls += 1
    
        await utils.answer(message, f"Balls: {balls}/4")
    
    @loader.command(
        ru_doc=" - Генерация пароля"
    )
    async def passwordgen(self,message):
        ''' - Gen password'''
        symbols = ["!","@","#","$","%","^","&","*","-","+"]
        letters = string.ascii_lowercase+string.ascii_uppercase
        password = ''.join(
            random.choice(letters) + random.choice(symbols) for _ in range(8)
        )
        await utils.answer(message,password) 


        