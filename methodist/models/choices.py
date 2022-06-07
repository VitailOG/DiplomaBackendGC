from django.db import models


class SemesterChoice(models.IntegerChoices):
    FIRST = 1, "Перший"
    SECOND = 2, "Другий"
    THIRD = 3, "Третій"
    FOURTH = 4, "Четвертий"
    FIFTH = 5, "П'ятий"
    SIXTH = 6, "Шостий"
    SEVENTH = 7, "Сьомий"
    EIGHTH = 8, "Восьмий"


class ControlChoice(models.TextChoices):
    EXAM = 'Екзамен', 'Екзамен'
    TEST = 'Залік', 'Залік'
    TERM_PAPER = 'Курсова', 'Курсова'
    PRACTICE = 'Практика', 'Практика'


class FormEducationChoice(models.TextChoices):
    STATE = 'Державна', 'Державна'
    CONTRACT = 'Контрактна', 'Контрактна'
