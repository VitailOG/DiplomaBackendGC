from celery import shared_task

from methodist.services.send_student_info_about_set_rating import SendInfoRatingService


@shared_task(
    ignore_result=True
)
def send_message_to_telegram_about_set_rating(user: int, rating_5: int, teacher: int, subject: int):
    SendInfoRatingService(
        user_id=user,
        rating=rating_5,
        teacher_id=teacher,
        subject_id=subject,
    )()
