from django.db import models


class Department(models.Model):
    """ Model Department
    """
    name = models.CharField(verbose_name="Назва відділення", max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Відділ"
        verbose_name_plural = "Відділи"


class Permissions(models.Model):
    """ Add permissions for users
    """
    name = models.CharField(verbose_name="Право доступу", max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Право доступу"
        verbose_name_plural = "Права доступу"


class Group(models.Model):
    """ Add group
    """
    name = models.CharField(verbose_name="Назва групи", max_length=15)

    educational_program = models.ForeignKey(
        'EducationalProgram',
        verbose_name="Освітня програма",
        on_delete=models.CASCADE,
        related_name='group_ed_prog'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Група"
        verbose_name_plural = "Групи"


class EducationalProgram(models.Model):
    """Освітні програми"""

    name = models.CharField(verbose_name="Назва освіт. програми", max_length=50)

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        verbose_name="Відділення",
        related_name='ed_prog_department'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Освітня програма"
        verbose_name_plural = "Освітні програми"
