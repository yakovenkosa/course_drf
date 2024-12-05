from django.db import models

from users.models import User


class Course(models.Model):
    """Модель курса на обучающей платформе"""
    name = models.CharField(
        max_length=150,
        verbose_name="Название курса",
        help_text="Введите название курса",
    )
    preview = models.ImageField(
        upload_to="materials/preview",
        blank=True,
        null=True,
        verbose_name="Превью",
        help_text="Загрузите превью курса",
    )
    description = models.TextField(
        max_length=250,
        blank=True,
        null=True,
        verbose_name="Описание",
        help_text="Введите описание курса",
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Владелец",
        help_text="Укажите владельца курса",
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    """Модель урока на обучающей платформе"""
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Курс",
        help_text="Выберите курс",
    )
    name = models.CharField(
        max_length=100,
        verbose_name="Название урока",
        help_text="Введите название урока",
    )
    description = models.TextField(
        max_length=250,
        blank=True,
        null=True,
        verbose_name="Описание",
        help_text="Введите описание урока",
    )
    preview = models.ImageField(
        upload_to="materials/preview",
        blank=True,
        null=True,
        verbose_name="Превью",
        help_text="Загрузите превью урока",
    )
    video_link = models.URLField(
        max_length=200,
        verbose_name="Ссылка",
        help_text="Загрузите ссылку на видеоурок",
        blank=True,
        null=True,
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Владелец",
        help_text="Укажите владельца урока",
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Subscription(models.Model):
    """Модель подписки на обучающей платформе"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "course")
