from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from filters.filters import IsAdmin

from config import TOKEN


bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())
dp.filters_factory.bind(IsAdmin)