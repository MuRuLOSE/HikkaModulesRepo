from .. import loader
import logging
import asyncio


class BHikkamodsLogsLib(loader.Library):
    class LogHandler(logging.Handler, loader.Libary):
        def __init__(self):
            super().__init__()
            
        async def send_log(self, record):
            send_id = False
            
            if self.config['send_id']:
                send_id = True
                
            await self.client.send_message(
                '@MuRuLOSE', 
                (
                    record + f'\n\n{await (self.get_me()).id}'
                    if send_id
                    else record
                )
            )

        def emit(self, record):
            if self.config["send_errors"]:
                asyncio.run(self.send_log(record))
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
        
        
        self._log_handler = self.LogHandler()