from aiogram import types
from asgiref.sync import sync_to_async

from bot.main import dp
from methodist.models import Student


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    # import django
    # django.setup()
    # from methodist.models import Student
    try:
        student_id = message['text'].split()[1]
        await sync_to_async(Student.objects.filter(id=student_id).update)(telegram_id=message['from']['id'])
        await message.answer("Start used bot for success study")
    except IndexError:
        await message.answer("Команда виконується тільки із реферальним посилання /start")
