from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.db.models import JSONField
from django.urls import reverse
from slugify import slugify

from users.models import AppUser


class Project(models.Model):
    number = models.PositiveIntegerField(primary_key=True, verbose_name='Номер')
    name = models.CharField(max_length=100, verbose_name='Название')
    address = models.CharField(max_length=100, verbose_name='Адрес')
    slug = models.SlugField(max_length=100, unique=True)
    project_link = models.CharField(
        max_length=150,
        verbose_name='Ссылка на проект',
        blank=True,
        null=True
    )
    project_start_date = models.DateField(verbose_name='Дата начала', blank=True, null=True)
    project_end_date = models.DateField(verbose_name='Дата окончания', blank=True, null=True)
    last_update = models.DateTimeField(verbose_name='Последнее обновление', auto_now_add=True)
    originator = models.ForeignKey(
        AppUser,
        related_name='project_originators',
        verbose_name='Постановщик',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    executor = models.ForeignKey(
        AppUser,
        related_name='project_executors',
        verbose_name='Исполнитель',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    calendar_chart = JSONField(blank=True, null=True, encoder=DjangoJSONEncoder)

    is_finished = models.BooleanField(default=False, verbose_name='Закончен')

    def __str__(self):
        return f'{self.number} - {self.name}'

    def get_absolute_url(self):
        return reverse('projects:project', kwargs={'project_slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.number) + '-' + self.name)
        super(Project, self).save(*args, kwargs)


class Task(models.Model):
    number = models.IntegerField(verbose_name='Номер')
    name = models.CharField(max_length=100, verbose_name='Задача')
    # slug = models.SlugField(max_length=100, unique=True)
    project = models.ForeignKey(
        Project,
        related_name='tasks',
        verbose_name='Проект',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    duration = models.PositiveIntegerField(default=0, verbose_name='Продолжительность')
    task_start_date = models.DateField(
        auto_now_add=True,
        verbose_name='Дата начала',
        blank=True,
        null=True
    )
    task_end_date = models.DateField(
        verbose_name='Дата сдачи',
        blank=True,
        null=True
    )
    last_update = models.DateTimeField(verbose_name='Последнее обновление', auto_now_add=True)
    originator = models.ForeignKey(
        AppUser,
        related_name='task_originators',
        verbose_name='Постановщик',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    executor = models.ForeignKey(
        AppUser,
        related_name='task_executors',
        verbose_name='Исполнитель',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    field_color = models.CharField(max_length=15, blank=True, null=True, verbose_name='Цвет')

    is_finished = models.BooleanField(default=False, verbose_name='Закончен')

    def __str__(self):
        return f'{self.project_id} - {self.name}'

    def get_absolute_url(self):
        return reverse('tasks', kwargs={'id': self.id})

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(str(self.project.number) + '-' + str(self.project.name) + '-' + str(self.name))
    #     super(Task, self).save(*args, kwargs)

    class Meta:
        ordering = ('-project_id', 'number',)
