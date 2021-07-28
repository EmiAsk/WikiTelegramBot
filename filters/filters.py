from aiogram.dispatcher.filters import BoundFilter, AdminFilter
from aiogram.types import Message
from config import ADMINS_ID


class IsAdmin(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, message: Message) -> bool:
        return message.from_user.id in ADMINS_ID


