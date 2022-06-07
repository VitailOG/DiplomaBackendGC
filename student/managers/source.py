from django.db.models import Manager

from methodist.models import Student


class StudentSourceManager(Manager):

    def save_files(self, semester: int, files: list, student: Student):
        sources = [self.model(semester=semester, file=_, student=student) for _ in files]
        return self.bulk_create(sources)
