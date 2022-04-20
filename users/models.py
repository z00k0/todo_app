import os.path

from django.db import models
from django.contrib.auth.models import BaseUserManager, PermissionsMixin, AbstractBaseUser

from phonenumber_field.modelfields import PhoneNumberField


def user_avatar_path(user, filename):

    return os.path.join('avatars', str(user.email).replace('@', '_'), filename)


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **other_fields): # , first_name, last_name

        if not email:
            raise ValueError('You must provide email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)  # first_name=first_name, last_name=last_name,
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, **other_fields):  # first_name, last_name, password,

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True')

        return self.create_user(email, **other_fields)  # first_name, last_name, password,


class AppUser(AbstractBaseUser, PermissionsMixin):
    # id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True, verbose_name='Email')
    first_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Имя')
    last_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=100, blank=True, null=True, verbose_name='Отчество')
    man = 'М'
    woman = 'Ж'
    sex_choices = [
        (man, 'Мужской'),
        (woman, 'Женский'),
    ]
    sex = models.CharField(
        max_length=2,
        choices=sex_choices,
        blank=True,
        null=True,
        verbose_name='Пол'
    )
    position = models.CharField(max_length=200, blank=True, null=True, verbose_name='Должность')
    department = models.CharField(max_length=100, blank=True, null=True, verbose_name='Отдел')
    birthday = models.DateField(blank=True, null=True, verbose_name='День рождения')
    mobile = PhoneNumberField(blank=True, null=True, verbose_name='Телефон')
    avatar = models.ImageField(
        upload_to=user_avatar_path,
        blank=True,
        null=True,
        verbose_name='Аватар'
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        displayed_name = ' '.join(name for name in [self.first_name, self.last_name] if name)
        return displayed_name or self.email





