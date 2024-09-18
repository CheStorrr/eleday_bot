import os 


class Config:

    def __init__(self) -> None:
        self.bot_token = os.getenv('BOT_TOKEN')

config = Config()