from django.db import models
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
    start_date = models.DateTimeField(verbose_name='Дата начала', blank=True, null=True)
    end_date = models.DateTimeField(verbose_name='Дата сдачи', blank=True, null=True)
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
    coexecutor = models.ForeignKey(
        AppUser,
        related_name='project_coexecutors',
        verbose_name='Соисполнитель',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    auditor = models.ForeignKey(
        AppUser,
        related_name='project_auditors',
        verbose_name='Наблюдатель',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    is_finished = models.BooleanField(default=False, verbose_name='Закончен')

    def __str__(self):
        return f'{self.number} - {self.name}'

    def get_absolute_url(self):
        return reverse('project', kwargs={'project_slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.number) + '-' + self.name)
        super(Project, self).save(*args, kwargs)


class Task(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=100, verbose_name='Задача')
    slug = models.SlugField(max_length=100, unique=True)
    project = models.ForeignKey(
        Project,
        related_name='projects',
        verbose_name='Проект',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    duration = models.PositiveIntegerField(default=0, verbose_name='Продолжительность')
    # start_date = models.DateTimeField(
    #     auto_now_add=True,
    #     verbose_name='Дата начала',
    #     blank=True,
    #     null=True
    # )
    # end_date = models.DateTimeField(
    #     verbose_name='Дата сдачи',
    #     blank=True,
    #     null=True
    # )
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
    coexecutor = models.ForeignKey(
        AppUser,
        related_name='task_coexecutors',
        verbose_name='Соисполнитель',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    auditor = models.ForeignKey(
        AppUser,
        related_name='task_auditors',
        verbose_name='Наблюдатель',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    def __str__(self):
        return f'{self.project.number} - {self.project.name} - {self.name}'

    def get_absolute_url(self):
        return reverse('tasks', kwargs={'task_slug': self.slug})
