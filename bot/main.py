import logging

from aiogram import Bot, Dispatcher, executor

from GradeBookGC_BACKEND.settings import API_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


# @dp.message_handler(commands=['start'])
# async def start_command(message: types.Message):
#     import django
#     django.setup()
#     from methodist.models import Student
#     try:
#         student_id = message['text'].split()[1]
#         await sync_to_async(Student.objects.filter(id=student_id).update)(telegram_id=message['from']['id'])
#         await message.answer("Start used bot for success study")
#     except IndexError:
#         await message.answer("Команда виконується тільки із реферальним посилання /start")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
