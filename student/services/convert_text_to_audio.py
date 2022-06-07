from gtts import gTTS

from student.models import StudentSource


class ConvertTextToAudioService:

    def __init__(
            self,
            student,
            text: str,
            lang: str = 'uk',
            slow: bool = False
    ):
        self.student = student
        self.text = text
        self.lang = lang
        self.slow = slow

    def __call__(self):
        return StudentSource().save_file(file=self.generate_audio(), student=self.student)

    def generate_audio(self):
        return gTTS(text=self.text, lang=self.lang, slow=self.slow)
