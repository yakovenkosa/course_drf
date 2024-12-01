from rest_framework.exceptions import ValidationError
import re


class ValidatorLinkToTheVideo:

    message = "Неверная ссылка! Доступ только с видеохостинга youtube.com!"

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        youtube_pattern = r"^(https?://)?(www\.)?youtube\.com/.+"
        tmp_field = dict(value).get(self.field)
        if not re.match(youtube_pattern, tmp_field):
            raise ValidationError(self.message)
