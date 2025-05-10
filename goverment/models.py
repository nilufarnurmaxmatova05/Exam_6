import random

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Ministry(models.Model):
    name = models.CharField(max_length=200, verbose_name="Vazirlik nomi")
    description = models.TextField(verbose_name="Tavsif")
    established_date = models.DateField(verbose_name="Tashkil etilgan sana")
    website = models.URLField(verbose_name="Rasmiy veb-sayt", blank=True, null=True)

    class Meta:
        verbose_name = "Vazirlik"
        verbose_name_plural = "Vazirliklar"

    def __str__(self):
        return self.name


class Minister(models.Model):
    GENDER_CHOICES = (
        ('M', 'Erkak'),
        ('F', 'Ayol'),
    )

    @property
    def full_name(self):
        if self.middle_name:
            return f"{self.last_name} {self.first_name} {self.middle_name}"
        return f"{self.last_name} {self.first_name}"

    first_name = models.CharField(max_length=100, verbose_name="Ism")
    last_name = models.CharField(max_length=100, verbose_name="Familiya")
    middle_name = models.CharField(max_length=100, verbose_name="Otasining ismi", blank=True, null=True)
    photo = models.ImageField(upload_to='ministers/', verbose_name="Rasm", blank=True, null=True)
    birth_date = models.DateField(verbose_name="Tug'ilgan sana",null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Jinsi")
    biography = models.TextField(verbose_name="Biografiya")
    ministry = models.ForeignKey(Ministry, on_delete=models.CASCADE, related_name='ministers', verbose_name="Vazirlik")
    position = models.CharField(max_length=200, verbose_name="Lavozim")
    appointment_date = models.DateField(verbose_name="Tayinlangan sana")
    email = models.EmailField(verbose_name="Email", blank=True, null=True)
    phone = models.CharField(max_length=20, verbose_name="Telefon raqami", blank=True, null=True)

    class Meta:
        verbose_name = "Vazir"
        verbose_name_plural = "Vazirlar"

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Department(models.Model):
    name = models.CharField(max_length=200, verbose_name="Bo'lim nomi")
    ministry = models.ForeignKey(Ministry, on_delete=models.CASCADE, related_name='departments',
                                 verbose_name="Vazirlik")
    description = models.TextField(verbose_name="Tavsif")
    head = models.CharField(max_length=200, verbose_name="Bo'lim boshlig'i", blank=True, null=True)

    class Meta:
        verbose_name = "Bo'lim"
        verbose_name_plural = "Bo'limlar"

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, verbose_name="Telefon raqami", blank=True, null=True)
    address = models.CharField(max_length=255, verbose_name="Manzil", blank=True, null=True)
    photo = models.ImageField(upload_to='profiles/', verbose_name="Rasm", blank=True, null=True)

    class Meta:
        verbose_name = "Foydalanuvchi profili"
        verbose_name_plural = "Foydalanuvchi profillari"

    def __str__(self):
        return self.user.username

class PasswordResetCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"Reset code for {self.user.username}"

    def is_valid(self):
        return not self.is_used and self.expires_at > timezone.now()

    @classmethod
    def generate_code(cls, user):
        # Avvalgi ishlatilmagan kodlarni o'chirish
        cls.objects.filter(user=user, is_used=False).delete()

        # 6 xonali raqamli kod yaratish
        code = ''.join(random.choices('0123456789', k=6))

        # 30 daqiqa amal qiladigan kod yaratish
        expires_at = timezone.now() + timezone.timedelta(minutes=30)

        # Yangi kod yaratish va saqlash
        reset_code = cls(user=user, code=code, expires_at=expires_at)
        reset_code.save()

        return reset_code