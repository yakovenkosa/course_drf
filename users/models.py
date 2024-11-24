from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None

    email = models.EmailField(
        unique=True, verbose_name="Email", help_text="Введите ваш Email"
    )
    phone = models.CharField(
        max_length=35,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Введите ваш телефон",
    )
    country = models.TextField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Страна",
        help_text="Введите вашу страну",
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Загрузите свой аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payments(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ("наличные", "наличные"),
        ("перевод на счет", "перевод на счет"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Пользователь",
    )
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата оплаты")
    course_paid = models.ForeignKey(
        "materials.Course",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Курс оплачен",
    )
    lesson_paid = models.ForeignKey(
        "materials.Lesson",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Урок оплачен",
    )
    payment_amount = models.DecimalField(
        max_digits=9, decimal_places=2, verbose_name="Сумма оплаты"
    )
    payment_method = models.CharField(
        max_length=50, choices=PAYMENT_METHOD_CHOICES, verbose_name="Cпособ оплаты"
    )

    def __str__(self):
        return f"{self.user} - {self.payment_amount} - {self.payment_date}"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ["-payment_date"]
