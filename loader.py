from aiogram import Bot, Dispatcher
from config import config

bot = Bot(token=config.bot_token, parse_mode='html')
dp = Dispatcher()