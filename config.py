import os 

main_chat = -1002392779446
class Config:

    def __init__(self) -> None:
        self.bot_token = os.getenv('BOT_TOKEN')

config = Config()