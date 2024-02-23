from .. import loader
import logging
import asyncio


class LogHandler(logging.Handler, loader):
        def __init__(self, mod):
            super().__init__()
            self.mod = mod
            
        async def send_log(self, record):
            send_id = False
            
            if self.mod.config['send_id']:
                send_id = True
                
            await self.client.send_message(
                '@MuRuLOSE', 
                (
                    record + f'\n\n{await (self.mod.get_me()).id}'
                    if send_id
                    else record
                )
            )

        def emit(self, record):
            if self.mod.config["send_errors"]:
                asyncio.run(self.send_log(record))
    
class BHikkamodsLogsLib(loader.Library):
    developer = "@MuRuLOSE"

    def __init__(self):
        self.config = loader.LibraryConfig(
            loader.ConfigValue(
                "send_errors",
                False,
                "Send errors to developer for diagnostic",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "send_id",
                False,
                "Send id with error"
            )
        )
        
        
        self._log_handler = LogHandler(self)